
from django.conf.urls import include,  url
from rest_framework.urlpatterns import format_suffix_patterns
from expression_interface import views

urlpatterns = (
    url(r'^$', views.APIRoot.as_view(), name='api_root'),
    url(r'^boolean-operators/?$', views.SubBooleanOperatorResource.as_view(), name='sub_boolean_operator' )

)

urlpatterns = format_suffix_patterns(urlpatterns, allowed=['json', 'png', 'jsonld'])

