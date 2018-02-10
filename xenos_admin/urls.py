from django.conf.urls import url
from . import views

app_name='office'

urlpatterns = [
    url(r'^$',views.Dash.as_view(), name='home'),
    ]