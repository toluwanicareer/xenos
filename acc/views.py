from django.shortcuts import render
import account.views
import account.forms
from django.contrib import messages

# Create your views here.

class LoginView(account.views.LoginView):

	def form_invalid(self, form):
		messages.warning(self.request, 'Wrong username or password')
		return super(LoginView,self).form_invalid(form)

