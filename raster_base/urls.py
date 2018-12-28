from django.conf.urls import include, url
from rest_framework.urlpatterns import format_suffix_patterns
from raster_base import views 

# maybe the operations below doesn't make sense for entry point
#'distinct'
#'group-by-count'
#'join'
#"group-by-sum"

app_name="raster_base"

urlpatterns = format_suffix_patterns((
    url(r'^(?P<attributes_functions>count-resource.*$|projection.*$|filter.*$|collect.*$|offset-limit.*$)/?$', views.APIRoot.as_view(), name='api_root_af'), # HARCODED
    url(r'^$', views.APIRoot.as_view(), name='api_root'),

    url(r'^imagem-exemplo1-list/(?P<pk>[0-9]+)/?$', views.ImagemExemplo1Detail.as_view(), name='ImagemExemplo1_detail'),
    url(r'^imagem-exemplo1-list/(?P<pk>[0-9]+)/(?P<attributes_functions>.*)/?$', views.ImagemExemplo1Detail.as_view(), name='ImagemExemplo1_detail_af'),
    url(r'^imagem-exemplo1-list/?$', views.ImagemExemplo1List.as_view(), name='ImagemExemplo1_list'),
    url(r'^imagem-exemplo1-list/(?P<attributes_functions>.*)/?$', views.ImagemExemplo1List.as_view(), name='ImagemExemplo1_list_af'),

    url(r'^imagem-exemplo2-list/(?P<pk>[0-9]+)/?$', views.ImagemExemplo2Detail.as_view(), name='ImagemExemplo2_detail'),
    url(r'^imagem-exemplo2-list/(?P<pk>[0-9]+)/(?P<attributes_functions>.*)/?$', views.ImagemExemplo2Detail.as_view(), name='ImagemExemplo2_detail_af'),
    url(r'^imagem-exemplo2-list/?$', views.ImagemExemplo2List.as_view(), name='ImagemExemplo2_list'),
    url(r'^imagem-exemplo2-list/(?P<attributes_functions>.*)/?$', views.ImagemExemplo2List.as_view(), name='ImagemExemplo2_list_af'),

    url(r'^imagem-exemplo-tile1-list/(?P<pk>[0-9]+)/?$', views.ImagemExemploTile1Detail.as_view(), name='ImagemExemploTile1_detail'),
    url(r'^imagem-exemplo-tile1-list/(?P<pk>[0-9]+)/(?P<attributes_functions>.*)/?$', views.ImagemExemploTile1Detail.as_view(), name='ImagemExemploTile1_detail_af'),
    url(r'^imagem-exemplo-tile1-list/?$', views.ImagemExemploTile1List.as_view(), name='ImagemExemploTile1_list'),
    url(r'^imagem-exemplo-tile1-list/(?P<attributes_functions>.*)/?$', views.ImagemExemploTile1List.as_view(), name='ImagemExemploTile_list_af'),

    url(r'^imagem-exemplo-tile2-list/(?P<pk>[0-9]+)/?$', views.ImagemExemploTile2Detail.as_view(), name='ImagemExemploTile2_detail'),
    url(r'^imagem-exemplo-tile2-list/(?P<pk>[0-9]+)/(?P<attributes_functions>.*)/?$', views.ImagemExemploTile2Detail.as_view(), name='ImagemExemploTile2_detail_af'),
    url(r'^imagem-exemplo-tile2-list/?$', views.ImagemExemploTile2List.as_view(), name='ImagemExemploTile2_list'),
    url(r'^imagem-exemplo-tile2-list/(?P<attributes_functions>.*)/?$', views.ImagemExemploTile2List.as_view(), name='ImagemExemplo4_list_af'),


))
