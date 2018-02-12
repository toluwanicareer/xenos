from django.conf.urls import url
from . import views

app_name='office'

urlpatterns = [
    
    url(r'^$', views.Invest.as_view(), name='invest'),
    url(r'^pay/$', views.pay.as_view(), name='pay'),
    
    ]