from django.shortcuts import render
from django.views.generic import (TemplateView,ListView,
                                  DetailView,CreateView,
                                  UpdateView,DeleteView,
                                  FormView)
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from .models import Plan, Investment, Percentage, Transaction, test_model, xenos_payment
from django.http import HttpResponse

import random, string
import pdb
from django.contrib.auth.models import User
from django.contrib import messages
from django.http import  HttpResponseRedirect
from django.core.urlresolvers import reverse
from acc.models import Profile
from forex_python.bitcoin import BtcConverter
from django.db.models import Sum
import random
from coinbase.wallet.client import Client
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.clickjacking import xframe_options_exempt
from django.utils.decorators import method_decorator
from .forms import UserForm, ProfileForm, PostForm, XenosForm
from django.core.mail import EmailMessage
from django.core.mail import EmailMessage

# Create your views here.
class Dash(LoginRequiredMixin, TemplateView):
	template_name='xenos_admin/index.html'
	login_url='/account/login'

class Invest(LoginRequiredMixin, View):
	login_url='/account/login/'
	def get(self, *args, **kwargs):
		context={}
		investment=Investment.objects.filter(user=self.request.user)
		context['percentage']=Percentage.objects.all()
		context['investment']=investment
		context['total_earned']=Investment.objects.filter(user=self.request.user).aggregate(Sum('profit'))
		context['total_investment']=Investment.objects.filter(user=self.request.user).filter(status='Active').aggregate(Sum('amount'))
		context['pending_transactions']=Transaction.objects.filter(user=self.request.user).order_by('-created_date')[:10]
		context['amt_available_for_withdrwal']=self.request.user.profile.wallet
		context['form']=XenosForm()
		
		
			#link='https://blockchain.info/payment_request?address='+pending_investment.bitaddress+'&amount='+str(btc_value)+'&message=Plan: '+pending_investment.plan.name+' source : Xenos'

		if self.request.GET.get('plan'):
			plan=self.request.GET.get('plan')
			plan=Plan.objects.get(name__icontains=plan)
			context['plan']=plan
		return render(self.request,'xenos_admin/invest.html', context)



class pay(LoginRequiredMixin,View):

	def post(self, request, *args, **kwargs):
		
		address=get_address()
		if address:
			Transaction.objects.create(trans_type='Credit', status='Pending',user=self.request.user,info='Deposit for Investment', bitaddress=address)
			return redirect_to_invest(request,True,'Transaction created successfully, please complete the transaction by paying to the bitcoin address')
		else:
			return redirect_to_invest(request,False, 'Network error please try again later' )
			


class pay_for_investment(LoginRequiredMixin, View):
	def post(self, request, *args, **kwargs):
		amount=request.POST.get('amount')
		plan=request.POST.get('plan')
		plan=get_plan(plan)
		profile=get_profile(request)
		balance=get_balance(profile)
		if int(amount) > balance:
			return redirect_to_invest(request,False, 'Insufficient balance in wallet' )
	
		else:
			
			i=Investment.objects.create(amount=amount, reinvest=True, user=self.request.user,plan=plan,  status='Active')	
			i.pay_referee()
			round_up_purchase(profile, balance, amount)
	
			return redirect_to_invest(request,True,'Investment Active')
			
			
class bot_pay(LoginRequiredMixin, View):

	def post(self,request,*args, **kwargs):
	
		form=XenosForm(request.POST)
		if form.is_valid():
			xenos_trans=form.save(commit=False)
			xenos_trans.bought_user=request.user
			amount=xenos_trans.bot.price
			profile=get_profile(request)
			balance=get_balance(profile)

			if int(amount) > balance:
				return redirect_to_invest(request,False, 'Insufficient balance in wallet' )
			else:
				xenos_trans.status='Active'
				xenos_trans.save()
				round_up_purchase(profile, balance, amount)

				return redirect_to_invest(request,True,'Successful Prchase of Bot')

class Withdraw(LoginRequiredMixin, View):

	def post(self, *args, **kwargs):
		
		client = get_coinbase_client
		if client:
			primary_account = client.get_primary_account()
		else:
			return redirect_to_invest(request,False, 'Network error please try again later')
		amount=self.request.POST.get('amount')
		balance=get_balance(get_profile(self.request))
		address=self.request.POST.get('bitaddress')
		
		btc_value=convert_to_btc(amount)
		if int(amount) > balance:
			return redirect_to_invest(request,False, 'Cant withdraw more than your wallet amount')
		else:
			try:
			
				tx = primary_account.send_money(to=address,
	                                amount=format(btc_value, '.8f'),
	                                currency='BTC')

				messages.success(self.request, 'Transfer Complete. ')
				self.request.user.profile.wallet=balance-amount
				self.request.user.profile.save()
				message='A withdrawal was just made on xenos for a total of ' + str(btc_value) + ' to address ' + address + ' by '+ self.request.user.email
				subject="Withdrawal Completed"
				mail=EmailMessage(subject, message,'contact@xenos.com', to=['xeotrading@gmail.com'], reply_to=['no-reply@xenos.com'],)
				
			
			except:
				Transaction.objects.create(trans_type='Withdrawal', status='Pending', amount=amount, user=self.request.user, info='Withdrawal request')
				
				message='A withdrawal request was just made on xenos for a total of ' + str(btc_value) + ' to address ' + address + ' by '+ self.request.user.email
				subject="Withdrwal request on Xenos"
				mail=EmailMessage(subject, message,'contact@xenos.com', to=['xeotrading@gmail.com'], reply_to=['no-reply@xenos.com'],)

			return redirect_to_invest(request,False, 'Couldnt transefer now, Admin has been contacted to complete transaction manually')



@csrf_exempt
def notify_handler(request):
	if request.method=='POST':
		notification_data=request.body
		address=notification_data.data.address
		amount=notification_data.additional_data.amount.amount
		try:
			tx=Transaction.objects.get(bitaddress=address)
			amount=tx.complete(amount)
			profile=get_profile(request)
			balance=get_balance(profile)
			credit_account(profile, balance, amount)
		except:
			pass










class ProfileUpdateView(LoginRequiredMixin, View):
	login_url='account/login'
	def get(self, request, *args, **kwargs):
		userform=UserForm(instance=self.request.user)
		profile=Profile.objects.get(user=self.request.user)
		profileform=ProfileForm(instance=profile)
		context={'user':request.user, 'userform':userform, 'profileform':profileform}
		return render(self.request, 'xenos_admin/profile.html',context)

	def post(self, request, *args, **kwargs):
		try:
			userform=UserForm(data=self.request.POST, instance=self.request.user)
			profile=Profile.objects.get(user=self.request.user)
			profileform=ProfileForm(data=self.request.POST, instance=profile, files=request.FILES)
			userform.save()
			profileform.save()
		except:
			messages.warning(request,'Invalid form input, please try again or send email to hello@dailynaija.com')
		messages.success(request, 'Profile Updated Successfully')
		return HttpResponseRedirect(reverse('office:invest'))


class xenos_bot(View):
	def get(self,request, *args, **kwargs):
		render(self.request, 'xenos_admin/xenos_bot.html',{})



def id_generator(size=12, chars=string.ascii_uppercase + string.digits):
	return ''.join(random.choice(chars) for _ in range(size))


def get_address():
	try:
		
		client=get_coinbase_client()
	
		primary_account = client.get_primary_account()
		address_data = primary_account.create_address()
		return address_data.address
	except:
		#messages.warning(self.request, 'Network Error please try again later')
		return False

def redirect_to_invest(request, status_of_message,message=''):
	if status_of_message:
		messages.success(request,message)
	else:	
		messages.warning(request, message)
	return HttpResponseRedirect(reverse('office:invest'))

def get_balance(profile):
	balance = int(profile.wallet)
	return balance

def get_profile(request):
	profile=request.user.profile
	return profile

def get_plan(plan_name):
	try:
		plan=Plan.objects.get(name__icontains=plan_name)
		return plan
	except:
		return False

def get_coinbase_client():
	try:

		return  Client('qLfg5C9hhnEWL9tt',
		            'qMwSqeIiDqeLCitIFnUjitX5EcGVgghF') 
	except:
		return False

def convert_to_btc(amount):
	rate=dollar_bitcoin_rate()
	return float(amount)*float(rate)

#from xeno_admin.views import convert_to_btc
def dollar_bitcoin_rate():
	client=get_coinbase_client()
	rates = client.get_exchange_rates(currency='USD')
	return  rates.rates.BTC




def round_up_purchase(profile, balance, amount):
	profile.wallet=balance-int(amount)
	profile.save()

def credit_account(profile, balance, amount):
	profile.wallet=balance+int(amount)
	profile.save()


