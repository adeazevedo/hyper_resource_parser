from django.conf.urls import include, url
from rest_framework.urlpatterns import format_suffix_patterns
from controle import views

app_name = "controle"
urlpatterns = format_suffix_patterns((
    url(r'^(?P<attributes_functions>count-resource.*$|projection.*$|filter.*$|collect.*$|offset-limit.*$)/?$', views.APIRoot.as_view(), name='api_root_af'), # HARCODED
    url(r'^$', views.APIRoot.as_view(), name='api_root'),

    url(r'^gasto-list/(?P<pk>[0-9]+)/?$', views.GastoDetail.as_view(), name='Gasto_detail'),
    url(r'^gasto-list/(?P<pk>[0-9]+)/(?P<attributes_functions>.*)/?$', views.GastoDetail.as_view(), name='Gasto_detail_af'),
    url(r'^gasto-list/?$', views.GastoList.as_view(), name='Gasto_list'),
    url(r'^gasto-list/(?P<attributes_functions>.*)/?$', views.GastoList.as_view(), name='Gasto_list_af'),

    url(r'^tipo-gasto-list/(?P<pk>[0-9]+)/?$', views.TipoGastoDetail.as_view(), name='TipoGasto_detail'),
    url(r'^tipo-gasto-list/(?P<pk>[0-9]+)/(?P<attributes_functions>.*)/?$', views.TipoGastoDetail.as_view(), name='TipoGasto_detail_af'),
    url(r'^tipo-gasto-list/?$', views.TipoGastoList.as_view(), name='TipoGasto_list'),
    url(r'^tipo-gasto-list/(?P<attributes_functions>.*)/?$', views.TipoGastoList.as_view(), name='TipoGasto_list_af'),

    url(r'^usuario-list/(?P<pk>[0-9]+)/?$', views.UsuarioDetail.as_view(), name='Usuario_detail'),
    url(r'^usuario-list/(?P<pk>[0-9]+)/(?P<attributes_functions>.*)/?$', views.UsuarioDetail.as_view(), name='Usuario_detail_af'),
    url(r'^usuario-list/registro/?$', views.UsuarioRegister.as_view(), name='Usuario_register'),
    url(r'^usuario-list/login/?$', views.UsuarioLogin.as_view(), name='Usuario_login'),
    url(r'^usuario-list/registro/?$', views.UsuarioRegister.as_view(), name='Usuario_registro'),
    url(r'^usuario-list/?$', views.UsuarioList.as_view(), name='Usuario_list'),
    url(r'^usuario-list/(?P<attributes_functions>.*)/?$', views.UsuarioList.as_view(), name='Usuario_list_af'),


))
