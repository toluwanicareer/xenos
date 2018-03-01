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

	def get(self, *args, **kwargs):
		context={}
		investment=Investment.objects.filter(user=self.request.user)
		context['percentage']=Percentage.objects.all()
		context['investment']=investment
		context['total_earned']=Investment.objects.filter(user=self.request.user).aggregate(Sum('profit'))
		context['total_investment']=Investment.objects.filter(user=self.request.user).filter(status='Active').aggregate(Sum('amount'))
		context['pending_transactions']=Transaction.objects.filter(user=self.request.user)
		context['amt_available_for_withdrwal']=self.request.user.profile.wallet
		context['form']=XenosForm()
		try:
			pending_investment=Investment.objects.get(status='Pending')
			b = BtcConverter() 
			btc_value=b.convert_to_btc(int(pending_investment.amount), 'USD')
			link='https://blockchain.info/payment_request?address='+pending_investment.bitaddress+'&amount='+str(btc_value)+'&message=Plan: '+pending_investment.plan.name+' source : Xenos'
			context['link']=link
			context['btc_address']=pending_investment.bitaddress
			context['btc_value']=btc_value
			context['amount']=pending_investment.amount
		except:
			pass

		try:
			pending_xenos_bot_purchase=xenos_payment.objects.get(status='Pending')
			b = BtcConverter() 
			btc_value=b.convert_to_btc(int(pending_xenos_bot_purchase.bot.price), 'USD')
			link='https://blockchain.info/payment_request?address='+pending_xenos_bot_purchase.address+'&amount='+str(btc_value)+'&message=Xenos Purchase '+pending_xenos_bot_purchase.bot.plan_name+' source : Xenos'
			context['xenos_link']=link
			context['xenos_btc_address']=pending_investment.bitaddress
			context['xenos_btc_value']=btc_value

		except:
			pass

		if self.request.GET.get('plan'):
			plan=self.request.GET.get('plan')
			plan=Plan.objects.get(name__icontains=plan)
			context['plan']=plan
		return render(self.request,'xenos_admin/invest.html', context)



class pay(LoginRequiredMixin, View):
	
	def get(self, *args, **kwargs):
		investments=Investment.objects.filter(status='Pending')
		amount=self.request.GET.get('amount')
		plan=self.request.GET.get('plan')
		payment_method=self.request.GET.get('method')
		plan=Plan.objects.get(name__icontains=plan)
		if investments.exists():
			messages.warning(self.request, 'Please complete the payment of the pending investment')
			return HttpResponseRedirect(reverse('office:invest'))
		if payment_method=='coinbase':
			client = Client('qLfg5C9hhnEWL9tt',
                'qMwSqeIiDqeLCitIFnUjitX5EcGVgghF')

			primary_account = client.get_primary_account()
			address_data = primary_account.create_address()
			address=address_data.address
			Investment.objects.create(amount=amount, reinvest=True, user=self.request.user,plan=plan, bitaddress=address, status='Pending')
			messages.success(self.request, 'Please click on link to make payment through blockchain or use the bitcoin address ')
			
			return HttpResponseRedirect(reverse('office:invest'))	
			
		if payment_method=='wallet':
			profile=self.request.user.profile
			balance = int(profile.wallet)
			if int(amount) > balance:
				
				messages.warning(self.request, 'Insufficient balance in wallet')
				return HttpResponseRedirect(reverse('office:invest'))
			else:
				i=Investment.objects.create(amount=amount, reinvest=True, user=self.request.user,plan=plan,  status='Active')	
				i.pay_referee()
				profile.wallet=balance-int(amount)
				profile.save()
				messages.success(self.request, 'Investment Active')
				return HttpResponseRedirect(reverse('office:invest'))

class bot_pay(LoginRequiredMixin, View):

	def post(self,request,*args, **kwargs):
		client = Client('qLfg5C9hhnEWL9tt',
	                'qMwSqeIiDqeLCitIFnUjitX5EcGVgghF')
		primary_account = client.get_primary_account()
		address_data = primary_account.create_address()
		address=address_data.address
		form=XenosForm(request.POST)
		if form.is_valid():
			xenos_trans=form.save()
			xenos_trans.bought_user=request.user
			xenos_trans.address=address
			xenos_trans.status='Pending'
			xenos_trans.save()
		return HttpResponseRedirect(reverse('office:invest'))




class Withdraw(LoginRequiredMixin, View):

	def post(self, *args, **kwargs):
		client = Client('qLfg5C9hhnEWL9tt',
                'qMwSqeIiDqeLCitIFnUjitX5EcGVgghF')
		primary_account = client.primary_account
		amount=self.request.POST.get('amount')
		wallet=self.request.user.profile.wallet
		address=self.request.POST.get('bitaddress')
		b = BtcConverter() 
		btc_value=b.convert_to_btc(int(pending_investment.amount), 'USD')
		if int(amount) < wallet:
			messages.warning(self.request, 'Cant withdraw more than your wallet amount')
			return HttpResponseRedirect(reverse('office:invest'))
		else:
			try:
				tx = primary_account.send_money(to=address,
	                                amount=str(btc_value),
	                                currency='BTC')
				messages.success(self.request, 'Transfer Complete. ')
				Transaction.objects.create(trans_type='Withdrawal', status='Success', amount=amount, user=self.request.user, info='Withdrawal request')
			except:
				Transaction.objects.create(trans_type='Withdrawal', status='Pending', amount=amount, user=self.request.user, info='Withdrawal request')
				messages.warning(self.request, 'Couldnt transefer now, Admin has been contacted to complete transaction manually')
				message='A withdrawal request was just made on xenos for a total of ' + str(btc_value) + ' to address ' + address + ' by '+ self.request.user.email
				subject="Withdrwal request on Xenos"
				mail=EmailMessage(subject, message,'contact@xenos.com', to=['xeotrading@gmail.com'], reply_to=['no-reply@xenos.com'],)
			return HttpResponseRedirect(reverse('office:invest'))	


@csrf_exempt
def notify_handler(request):
	if request.method=='POST':
		test_model.objects.create(justin='yeah',data=request.POST)
		return HttpResponse(status=200)





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
		render(self.request, 'xenos_admin/xenos_bot',{})



def id_generator(size=12, chars=string.ascii_uppercase + string.digits):
	return ''.join(random.choice(chars) for _ in range(size))
