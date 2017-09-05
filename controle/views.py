from collections import OrderedDict
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.views import APIView
from rest_framework import permissions
from rest_framework import generics
from rest_framework import status
from hyper_resource.views import *
from controle.models import *
from controle.serializers import *
from controle.contexts import *

def get_root_response(request):
    format = None
    root_links = {

      'gasto-list': reverse('controle_v1:Gasto_list' , request=request, format=format),
      'tipo-gasto-list': reverse('controle_v1:TipoGasto_list' , request=request, format=format),
      'usuario-list': reverse('controle_v1:Usuario_list' , request=request, format=format),
    }

    ordered_dict_of_link = OrderedDict(sorted(root_links.items(), key=lambda t: t[0]))
    return ordered_dict_of_link

class APIRoot(APIView):

    def __init__(self):
        super(APIRoot, self).__init__()
        self.base_context = BaseContext('api-root')

    def options(self, request, *args, **kwargs):
        context = self.base_context.getContextData(request)
        root_links = get_root_response(request)
        context.update(root_links)
        response = Response(context, status=status.HTTP_200_OK, content_type="application/ld+json")
        response = self.base_context.addContext(request, response)
        return response

    def get(self, request, *args, **kwargs):
        root_links = get_root_response(request)
        response = Response(root_links)
        return self.base_context.addContext(request, response)

class GastoList(CollectionResource):
    queryset = Gasto.objects.all()
    serializer_class = GastoSerializer
    contextclassname = 'gasto-list'
    def initialize_context(self):
        self.context_resource = GastoContext()
        self.context_resource.resource = self

class GastoDetail(NonSpatialResource):
    serializer_class = GastoSerializer
    contextclassname = 'gasto-list'
    def initialize_context(self):
        self.context_resource = GastoContext()
        self.context_resource.resource = self

class TipoGastoList(CollectionResource):
    queryset = TipoGasto.objects.all()
    serializer_class = TipoGastoSerializer
    contextclassname = 'tipo-gasto-list'
    def initialize_context(self):
        self.context_resource = TipoGastoContext()
        self.context_resource.resource = self

class TipoGastoDetail(NonSpatialResource):
    serializer_class = TipoGastoSerializer
    contextclassname = 'tipo-gasto-list'
    def initialize_context(self):
        self.context_resource = TipoGastoContext()
        self.context_resource.resource = self

class UsuarioList(CollectionResource):
    queryset = Usuario.objects.all()
    serializer_class = UsuarioSerializer
    contextclassname = 'usuario-list'
    def initialize_context(self):
        self.context_resource = UsuarioContext()
        self.context_resource.resource = self

class UsuarioDetail(NonSpatialResource):
    serializer_class = UsuarioSerializer
    contextclassname = 'usuario-list'
    def initialize_context(self):
        self.context_resource = UsuarioContext()
        self.context_resource.resource = self

