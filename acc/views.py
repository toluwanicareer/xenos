from django.shortcuts import render
import account.views
import account.forms
from django.contrib import messages
from django.contrib import auth, messages
from django.http import  HttpResponseRedirect
from django.core.urlresolvers import reverse
from account.compat import reverse, is_authenticated
import pdb
# Create your views here.

class LoginView(account.views.LoginView):

	def form_invalid(self, form):
		messages.warning(self.request, 'Wrong username or password')
		return super(LoginView,self).form_invalid(form)

	def form_valid(self,form):
		return super(LoginView,self).form_valid(form)	

class LogoutView(account.views.LogoutView):

	def  get(self, *args, **kwargs):
		if is_authenticated(self.request.user):
			auth.logout(self.request)
			return render(self.request, self.template_name, {})
		if not is_authenticated(self.request.user):
			return HttpResponseRedirect(reverse('login'))


class SignupView(account.views.SignupView):
	def form_invalid(self,form):
		messages.warning(self.request, 'Username or email already exist')
		return super(SignupView,self).form_invalid(form)

	def form_valid(self, form):
		a=super(SignupView, self).form_valid(form)
		messages.success(self.request, 'Account Created. Please wait, until your account is Verified. You will be verified via email . Thank you ')
		self.created_user.is_active = False
		self.created_user.save()
		return HttpResponseRedirect(reverse('signup'))

		

			


