from django.conf.urls import include, url
from rest_framework.urlpatterns import format_suffix_patterns
from controle_adesao import views 

urlpatterns = format_suffix_patterns([
    url(r'^$', views.APIRoot.as_view(), name='api_root'),

    url(r'^ator-list/(?P<pk>[0-9]+)/$', views.AtorDetail.as_view(), name='Ator_detail'),
    url(r'^ator-list/(?P<pk>[0-9]+)/(?P<attributes_functions>.*)/$', views.AtorDetail.as_view(), name='Ator_detail_af'),
    url(r'^ator-list/$', views.AtorList.as_view(), name='Ator_list'),
    url(r'^ator-list/(?P<attributes_functions>.*)/?$', views.AtorList.as_view(), name='Ator_list_af'),

    url(r'^publicacaoinformacaogeoespacial-list/(?P<pk>[0-9]+)/$', views.PublicacaoinformacaogeoespacialDetail.as_view(), name='Publicacaoinformacaogeoespacial_detail'),
    url(r'^publicacaoinformacaogeoespacial-list/(?P<pk>[0-9]+)/(?P<attributes_functions>.*)/$', views.PublicacaoinformacaogeoespacialDetail.as_view(), name='Publicacaoinformacaogeoespacial_detail_af'),
    url(r'^publicacaoinformacaogeoespacial-list/$', views.PublicacaoinformacaogeoespacialList.as_view(), name='Publicacaoinformacaogeoespacial_list'),
    url(r'^publicacaoinformacaogeoespacial-list/(?P<attributes_functions>.*)/?$', views.PublicacaoinformacaogeoespacialList.as_view(), name='Publicacaoinformacaogeoespacial_list_af'),

    url(r'^representante-list/(?P<pk>[0-9]+)/$', views.RepresentanteDetail.as_view(), name='Representante_detail'),
    url(r'^representante-list/(?P<pk>[0-9]+)/(?P<attributes_functions>.*)/$', views.RepresentanteDetail.as_view(), name='Representante_detail_af'),
    url(r'^representante-list/$', views.RepresentanteList.as_view(), name='Representante_list'),
    url(r'^representante-list/(?P<attributes_functions>.*)/?$', views.RepresentanteList.as_view(), name='Representante_list_af'),


])
