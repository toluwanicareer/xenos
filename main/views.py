from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
# Create your views here.
from django.views.generic import (TemplateView,ListView,
                                  DetailView,CreateView,
                                  UpdateView,DeleteView,
                                  FormView)

from xenos_admin.models import Post
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse


class Home(TemplateView):
	template_name='main/index.html'

class AboutView(TemplateView):
	template_name='main/about.html'

class XenosView(TemplateView):
	template_name='main/bot.html'

class FAQView(TemplateView):
	template_name='main/faq.html'

class ContactView(TemplateView):
	template_name='main/contact.html'

class DeveloperView(TemplateView):
	template_name='main/developer.html'

class TechView(TemplateView):
	template_name='main/tech.html'

class TraderView(TemplateView):
	template_name='main/trader.html'

class UpdateView(ListView):
	model=Post
	template_name='main/update.html'
	queryset=Post.objects.all().order_by('-created_date')
	context_object_name = 'posts'



