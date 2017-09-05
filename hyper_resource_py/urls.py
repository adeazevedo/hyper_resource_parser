"""hyper_resource_py URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
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
from django.conf.urls import include, url
import sys

#from django.contrib import admin
basic_path = 'ibge/bcim/'
basic_path_context = 'ibge/contexts/'
basic_path_hydra = 'ibge/hydra/'

host_name = sys.argv[-1]
protocol = 'http'

urlpatterns = [

     url(r'^controle/',include('controle.urls',namespace='controle_v1')),
     url(r'^'+ basic_path, include('bcim.urls', namespace='bcim_v1')),

]

urlpatterns += [

    url(r'^api-auth/', include('rest_framework.urls',namespace='rest_framework')),

]

