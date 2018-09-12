
import sys

from django.conf.urls import url

from parser_test.views import HyperView


basic_path = 'ibge/bcim/'
host_name = sys.argv[-1]
protocol = 'http'
app_name = "hyper_resource_py"
urlpatterns = (
    url(r'^(.+)$', HyperView.as_view()),
    # url(r'^'+ 'api/bcim/', include('bcim.urls', namespace='bcim_v1')),
    # url(r'^controle_adesao-list/',include('controle_adesao.urls',namespace='controle_adesao')),
    # url(r'^controle-list/',include('controle.urls',namespace='controle_v1')),
    # url(r'^user_management-list/',include('user_management.urls',namespace='user_management')),
    # url(r'^expression/',include('expression_interface.urls',namespace='expression_interface')),
    # url(r'^raster/',include('raster_base.urls',namespace='raster')),
)