from django.shortcuts import render
from django.views.generic import (TemplateView,ListView,
                                  DetailView,CreateView,
                                  UpdateView,DeleteView,
                                  FormView)
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from .models import Plan, Investment, Percentage


import random, string
import pdb
from django.contrib.auth.models import User
from django.contrib import messages
from django.http import  HttpResponseRedirect
from django.core.urlresolvers import reverse
from acc.models import Profile
from forex_python.bitcoin import BtcConverter
import random


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
		if self.request.GET.get('plan'):
			plan=self.request.GET.get('plan')
			plan=Plan.objects.get(name__icontains=plan)
			context['plan']=plan
		return render(self.request,'xenos_admin/invest.html', context)



class pay(LoginRequiredMixin, View):
	bitcoin_addresses=['15E6G39yb3proGjF6xbZK8BUmwErXMYweA','1FCCRDHhs4xdJSrNLNSx6WVNw3BvJFmhoK','1BhSCT8cAqmXa74YAQBvV7BLvxwqED6UY']
	link='https://blockchain.info/payment_request?address=1FCCRDHhs4xdJSrNLNSx6WVNw3BvJFmhoK&amount=100&message=for%20greatness'
	def get(self, *args, **kwargs):
		
		payment_method=self.request.GET.get('method')
		amount=self.request.GET.get('amount')
		plan=self.request.GET.get('plan')
		address=random.choice(self.bitcoin_addresses)
		b = BtcConverter() 
		btc_value=b.convert_to_btc(int(amount), 'USD')
		self.request.session['btc_value']=btc_value
		link='https://blockchain.info/payment_request?address='+address+'&amount='+str(btc_value)+'&message=Plan: '+plan+' source : Xenos'
		plan=Plan.objects.get(name__icontains=plan)

		Investment.objects.create(amount=amount, reinvest=True, user=self.request.user,plan=plan, bitaddress=address,link=link, status='Pending')
		self.request.session['address']=address
		self.request.session['link']=link
		
		self.request.session['amount']=amount
		messages.success(self.request, 'Please click on link to make payment.')
		return HttpResponseRedirect(reverse('office:invest'))
		
		

def id_generator(size=12, chars=string.ascii_uppercase + string.digits):
	return ''.join(random.choice(chars) for _ in range(size))