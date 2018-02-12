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

	def get(self, *args, **kwargs):
		payment_method=self.request.GET.get('method')
		amount=self.request.GET.get('amount')
		plan=self.request.GET.get('plan')
		plan=Plan.objects.get(name__icontains=plan)
		order_id=id_generator()
		Investment.objects.create(user=self.request.user,amount=int(amount), plan=plan).save()
		messages.success(self.request, 'Payment successful. Investment Created')
		return HttpResponseRedirect(reverse('office:invest'))
        

def id_generator(size=12, chars=string.ascii_uppercase + string.digits):
	return ''.join(random.choice(chars) for _ in range(size))