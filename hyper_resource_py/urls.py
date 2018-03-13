from django.conf.urls import include, url
import sys

basic_path = 'ibge/bcim/'
host_name = sys.argv[-1]
protocol = 'http'
app_name = "hyper_resource_py"
urlpatterns = (
    url(r'^'+ 'ibge/bcim/', include('bcim.urls', namespace='bcim_v1')),
    url(r'^controle_adesao-list/',include('controle_adesao.urls',namespace='controle_adesao')),
    url(r'^controle-list/',include('controle.urls',namespace='controle_v1')),
     url(r'^user_management-list/',include('user_management.urls',namespace='user_management')),
)

