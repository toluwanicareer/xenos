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
from django.core.mail import EmailMessage
from django.http import  HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.views import View
from django.contrib import messages

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

class DeveloperView(View):
	template_name='main/developer.html'

	def get(self,request, *args, **kwargs):
		return render(request, self.template_name, {})
	def post(self, request, *args, **kwargs):
		firstname=request.POST.get('firstname')
		lastname=request.POST.get('lastname')
		email=request.POST.get('email')
		cv=request.FILES['cv']
		subject='Developer Job Application on Xenos'
		message=' A user with email ' + email + ' just applied as a developer on xenos. Attached is his/her CV'
		email2=EmailMessage(subject, message,'contact@xenos.com', to=['abiodun.toluwanii@gmail.com'], reply_to=['no-reply@avetiz.com'],)
		email2.attach(cv.name, cv.read(), cv.content_type)
		try:
			email2.send()
			messages.success(request, 'Successful Job Application, We will get back to you. Thank you')
		except:
			messages.warning(request, 'Network Error please try again later')

		return HttpResponseRedirect(reverse('main:developer'))


class TechView(View):
	template_name='main/tech.html'

	def get(self,request, *args, **kwargs):
		return render(request, self.template_name, {})

	def post(self, request, *args, **kwargs):
		firstname=request.POST.get('firstname')
		lastname=request.POST.get('lastname')
		email=request.POST.get('email')
		cv=request.FILES['cv']
		subject='Tech Support Job Application on Xenos'
		message=' A user with email ' + email + ' just applied as a tech_support on xenos. Attached is his/her CV'
		email2=EmailMessage(subject, message,'contact@xenos.com', to=['abiodun.toluwanii@gmail.com'], reply_to=['no-reply@avetiz.com'],)
		email2.attach(cv.name, cv.read(), cv.content_type)
		try:
			email2.send()
			messages.success(request, 'Successful Job Application, We will get back to you. Thank you')
		except:
			messages.warning(request, 'Network Error please try again later')

		return HttpResponseRedirect(reverse('main:tech'))

class TraderView(TemplateView):
	template_name='main/trader.html'

class UpdateView(ListView):
	model=Post
	template_name='main/update.html'
	queryset=Post.objects.all().order_by('-created_date')
	context_object_name = 'posts'



