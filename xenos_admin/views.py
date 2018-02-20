from django.shortcuts import render
from django.views.generic import (TemplateView,ListView,
                                  DetailView,CreateView,
                                  UpdateView,DeleteView,
                                  FormView)
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from .models import Plan, Investment, Percentage, Transaction, test_model
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
from .forms import UserForm, ProfileForm, PostForm



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
		if self.request.GET.get('plan'):
			plan=self.request.GET.get('plan')
			plan=Plan.objects.get(name__icontains=plan)
			context['plan']=plan
		return render(self.request,'xenos_admin/invest.html', context)



class pay(LoginRequiredMixin, View):
	bitcoin_addresses=['15E6G39yb3proGjF6xbZK8BUmwErXMYweA','1FCCRDHhs4xdJSrNLNSx6WVNw3BvJFmhoK','1BhSCT8cAqmXa74YAQBvV7BLvxwqED6UY']
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

class Withdraw(LoginRequiredMixin, View):

	def post(self, *args, **kwargs):
		amount=self.request.POST.get('amount')
		wallet=self.request.user.profile.wallet
		if int(amount) < wallet:
			messages.warning(self.request, 'Cant withdraw more than your wallet amount')
			return HttpResponseRedirect(reverse('office:invest'))
		else:
			Transaction.objects.create(trans_type='Withdrawal', status='Pending', amount=amount, user=self.request.user, info='Withdrawal request')
			messages.success(self.request, 'Withdrawal Request Made. We will get back to you')
			return HttpResponseRedirect(reverse('office:invest'))	

'''

class notif_handler(View):

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
    	pdb.set_trace()
        return super(notif_handler, self).dispatch(request, *args, **kwargs)

	def post(self,request,*args, **kwargs):
		notif_type=self.request.POST.get('type')
		test_model.objects.create(justin='yeah',data='ok yeah')
		return HttpResponse(status=200)


		
		if notif_type=='wallet:addresses:new-payment':
			data=self.request.POST.get('data')
			address=data.address
			investment=Investment.objects.get(bitaddress=address)
			investment.status='Active'
			investment.save()

			return HttpResponse(status=200)
		'''
@csrf_exempt
def notify_handler(request):
	if request.method=='POST':
		test_model.objects.create(justin='yeah',data='ok yeah')
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



def id_generator(size=12, chars=string.ascii_uppercase + string.digits):
	return ''.join(random.choice(chars) for _ in range(size))
