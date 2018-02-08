"""xenos URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from acc import views
from django.views.static import serve
from django.conf import settings
 

app_name='xenos'
urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'', include('main.urls')),
    url(r"^account/login/$", views.LoginView.as_view(), name="login"),
    url(r"^account/", include("account.urls")),
    url(r'^media/(?P<path>.*)', serve, {'document_root': settings.MEDIA_ROOT}),
]
