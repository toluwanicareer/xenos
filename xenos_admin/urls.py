from django.conf.urls import url
from . import views

app_name='office'

urlpatterns = [
    
    url(r'^$', views.Invest.as_view(), name='invest'),
    url(r'^pay/$', views.pay.as_view(), name='pay'),
    url(r'^withdraw/$', views.Withdraw.as_view(), name='withdraw'),
     url(r'^coinbase_notify/$', views.notif_handler.as_view(), name='withdraw'),
     url(r'^profile/$', views.ProfileUpdateView.as_view(), name='profile'),
    
    ]