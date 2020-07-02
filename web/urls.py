"""GSM URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf.urls import url
from .views import account
from .views import home
urlpatterns = [
    path('admin/', admin.site.urls),
    url(r'^login.html/$',account.login,name='login'),
    url(r'^check_code.html$',account.check_code),
    url(r'^logout.html/$',account.logout,name='logout'),
    url(r'^register/$',account.register,name='register'),
    url(r'^all/(?P<article_type_id>\d+).html$',home.index,name='index'),
    url(r'^(?P<site>\w+).html$',home.home),
    url(r'^(?P<site>\w+)/(?P<condition>((tag)|(date)|(category)))/(?P<val>\w+-*\w*).html$', home.filter),
    url(r'^(?P<site>\w+)/(?P<nid>\d+).html',home.detail),
]
