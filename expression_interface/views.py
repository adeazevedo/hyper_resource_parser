
from collections import OrderedDict

from rest_framework import status
from rest_framework.reverse import reverse

# Create your views here.
from rest_framework.views import APIView

from hyper_resource.models import boolean_operator
from hyper_resource.views import AbstractResource, BaseContext
from rest_framework.response import Response

HTTP_IF_NONE_MATCH = 'HTTP_IF_NONE_MATCH'
HTTP_IF_MATCH = 'HTTP_IF_MATCH'
HTTP_IF_UNMODIFIED_SINCE = 'HTTP_IF_UNMODIFIED_SINCE'
HTTP_IF_MODIFIED_SINCE = 'HTTP_IF_MODIFIED_SINCE'
HTTP_ACCEPT = 'HTTP_ACCEPT'
CONTENT_TYPE = 'CONTENT_TYPE'
ETAG = 'Etag'
CONTENT_TYPE_GEOJSON = "application/vnd.geo+json"
CONTENT_TYPE_JSON = "application/json"
CONTENT_TYPE_LD_JSON = "application/ld+json"
CONTENT_TYPE_OCTET_STREAM = "application/octet-stream"
CONTENT_TYPE_IMAGE_PNG = "image/png"
SUPPORTED_CONTENT_TYPES = (CONTENT_TYPE_GEOJSON, CONTENT_TYPE_JSON,CONTENT_TYPE_LD_JSON, CONTENT_TYPE_OCTET_STREAM, CONTENT_TYPE_IMAGE_PNG)
ACCESS_CONTROL_ALLOW_METHODS = ['GET', 'OPTIONS', 'HEAD']

CORS_ALLOW_HEADERS = (
    'accept',
    'accept-encoding',
    'authorization',
    'content-type',
    'content-location',
    'dnt',
    'origin',
    'user-agent',
    'x-csrftoken',
    'x-requested-with',
    'link',
)

CORS_EXPOSE_HEADERS = [
    'accept',
    'accept-encoding',
    'authorization',
    'content-type',
    'content-location',
    'dnt',
    'origin',
    'user-agent',
    'x-csrftoken',
    'x-requested-with',
    'x-access-token',
    'access-control-allow-origin',
    'link',
]

ENABLE_COMPLEX_REQUESTS = True

GEOSGEOMETRY_SUBCLASSES = ['POINT', 'MULTIPOINT', 'LINESTRING', 'MULTILINESTRING', 'POLYGON', 'MULTIPOLYGON', 'GEOMETRYCOLLECTION']


def get_root_response(request):
    format = None
    root_links = {
        'boolean-operators': reverse('expression_interface:sub_boolean_operator', request=request, format=format),
    }
    ordered_dict_of_link = OrderedDict(sorted(root_links.items(), key=lambda t: t[0]))
    return ordered_dict_of_link


class APIRoot(APIView):

    def __init__(self):
        super(APIRoot, self).__init__()
        self.base_context = BaseContext('api-root')

    def add_url_in_header(self, url, response, rel):
        link = ' <'+url+'>; rel=\"'+rel+'\" '
        if "Link" not in response:
            response['Link'] = link
        else:
            response['Link'] += "," + link
        return response

    def add_cors_headers_in_header(self, response):
        response["access-control-allow-origin"] = "*"
        access_control_allow_headers_str = ''
        for value in CORS_ALLOW_HEADERS:
            access_control_allow_headers_str += ', ' + value

        access_control_expose_headers_str = ''
        for value in CORS_EXPOSE_HEADERS:
            access_control_expose_headers_str += ', ' + value

        access_control_allow_methods_str = ''
        for value in ACCESS_CONTROL_ALLOW_METHODS:
            access_control_allow_methods_str += ', ' + value
        response['access-control-allow-headers'] = access_control_allow_headers_str
        response['access-control-expose-headers'] = access_control_expose_headers_str
        response['access-control-allow-methods'] = access_control_allow_methods_str

    def options(self, request, *args, **kwargs):
        context = self.base_context.getContextData(request)
        root_links = get_root_response(request)
        context.update(root_links)
        response = Response(context, status=status.HTTP_200_OK, content_type="application/ld+json")
        entry_pointURL = reverse('bcim_v1:api_root', request=request)
        response = self.add_url_in_header(entry_pointURL, response, 'http://schema.org/EntryPoint')
        response = self.base_context.addContext(request, response)
        return response

    def get(self, request, *args, **kwargs):
        root_links = get_root_response(request)
        response = Response(root_links)
        self.add_cors_headers_in_header(response)
        entry_pointURL = reverse('bcim_v1:api_root', request=request)
        response = self.add_url_in_header(entry_pointURL, response, 'http://schema.org/EntryPoint')
        return self.base_context.addContext(request, response)

class SubBooleanOperatorResource(AbstractResource):
    contextclassname = 'boolean-operators'
    def get(self, request, *args, **kwargs):
        dici = {}
        for oper_name in boolean_operator():
            dici[oper_name] = oper_name
        return Response(data=dici, content_type='application/json')


