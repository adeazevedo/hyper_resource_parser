from collections import OrderedDict
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.views import APIView
from rest_framework import permissions
from rest_framework import generics
from rest_framework import status
from hyper_resource.contexts import EntryPointResourceContext
from hyper_resource.resources.EntryPointResource import NonSpatialEntryPointResource
from controle.models import *
from controle.serializers import *
from controle.contexts import *

from hyper_resource.resources.CollectionResource import CollectionResource
from hyper_resource.resources.NonSpatialResource import NonSpatialResource



class APIRoot(NonSpatialEntryPointResource):
    serializer_class = EntryPointSerializer

    def get_root_response(self, request, format=None, *args, **kwargs):
        root_links = {
          'gasto-list': reverse('controle_v1:Gasto_list' , request=request, format=format),
          'tipo-gasto-list': reverse('controle_v1:TipoGasto_list' , request=request, format=format),
          'usuario-list': reverse('controle_v1:Usuario_list' , request=request, format=format),
        }

        ordered_dict_of_link = OrderedDict(sorted(root_links.items(), key=lambda t: t[0]))
        return ordered_dict_of_link

class GastoList(CollectionResource):
    queryset = Gasto.objects.all()
    serializer_class = GastoSerializer
    contextclassname = 'gasto-list'
    def initialize_context(self):
        self.context_resource = GastoCollectionContext()
        self.context_resource.resource = self


class UsuarioRegister(CollectionResource):
    queryset = Usuario.objects.all()
    serializer_class = UsuarioSerializer
    contextclassname = 'usuario-list'
    def initialize_context(self):
        self.context_resource = UsuarioContext()
        self.context_resource.resource = self

    def post(self, request, *args, **kwargs):
        print(request)
        resp = super(UsuarioRegister, self).post(request, *args, **kwargs)
        resp['x-access-token'] = self.object_model.getToken()
        return resp

class UsuarioLogin(CollectionResource):
    queryset = Usuario.objects.all()
    serializer_class = UsuarioSerializer
    contextclassname = 'usuario-list'
    def initialize_context(self):
        self.context_resource = UsuarioContext()
        self.context_resource.resource = self

    def post(self, request, *args, **kwargs):
        res = Usuario.getOneOrNone(request.data['nome_usuario'], request.data['senha'])
        if res is None:
            res = Response(status=status.HTTP_401_UNAUTHORIZED, content_type='application/json')
            res['WWW-Authenticate'] = 'Bearer'
            return res
        response = Response(status=status.HTTP_201_CREATED, content_type='application/json')
        response['Content-Location'] = request.path + str(res.id)
        response['x-access-token'] = res.getToken()
        return response


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
        self.context_resource = UsuarioCollectionContext()
        self.context_resource.resource = self

class UsuarioDetail(NonSpatialResource):
    serializer_class = UsuarioSerializer
    contextclassname = 'usuario-list'
    def initialize_context(self):
        self.context_resource = UsuarioContext()
        self.context_resource.resource = self

