from django.shortcuts import render
from django.views.generic import (TemplateView,ListView,
                                  DetailView,CreateView,
                                  UpdateView,DeleteView,
                                  FormView)
from django.contrib.auth.mixins import LoginRequiredMixin



# Create your views here.
class Dash(LoginRequiredMixin, TemplateView):
	template_name='xenos_admin/index.html'
	login_url='/account/login'