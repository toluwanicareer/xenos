from django.conf.urls import url
from . import views

app_name='main'

urlpatterns = [
    url(r'^$',views.Home.as_view(), name='home'),
    url(r'^about/$',views.AboutView.as_view(), name='about'),
    url(r'^bot/$',views.XenosView.as_view(), name='bot'),
    url(r'^faq/$',views.FAQView.as_view(), name='faq'),
    url(r'^contact/$',views.ContactView.as_view(), name='contact'),
    url(r'^developer/$',views.DeveloperView.as_view(), name='developer'),
    url(r'^technical-assistant/$',views.TechView.as_view(), name='tech'),
    url(r'^apply-trader/$',views.TraderView.as_view(), name='trader'),
    ]