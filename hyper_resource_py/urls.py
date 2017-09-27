from django.conf.urls import include, url
urlpatterns = [

    url(r'^controle_adesao-list/',include('controle_adesao.urls',namespace='controle_adesao_v1')),


]
urlpatterns += [

    url(r'^api-auth/', include('rest_framework.urls',namespace='rest_framework')),

]


