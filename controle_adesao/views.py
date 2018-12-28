from collections import OrderedDict
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.views import APIView
from rest_framework import permissions
from rest_framework import generics
from rest_framework import status
from hyper_resource.contexts import EntryPointResourceContext
from hyper_resource.resources.EntryPointResource import NonSpatialEntryPointResource
from controle_adesao.models import *
from controle_adesao.serializers import *
from controle_adesao.contexts import *

from hyper_resource.resources.CollectionResource import CollectionResource
from hyper_resource.resources.NonSpatialResource import NonSpatialResource

class APIRoot(NonSpatialEntryPointResource):

    def get_root_response(self, request, format=None, *args, **kwargs):
        root_links = {

          'ator-list': reverse('controle_adesao:Ator_list' , request=request, format=format),
          'publicacaoinformacaogeoespacial-list': reverse('controle_adesao:Publicacaoinformacaogeoespacial_list' , request=request, format=format),
          'representante-list': reverse('controle_adesao:Representante_list' , request=request, format=format),
        }

        ordered_dict_of_link = OrderedDict(sorted(root_links.items(), key=lambda t: t[0]))
        return ordered_dict_of_link

    '''
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

    def get(self, request, format=None, *args, **kwargs):
        root_links = get_root_response(request)
        response = Response(root_links)
        return self.base_context.addContext(request, response)
    '''

class AtorList(CollectionResource):
    queryset = Ator.objects.all()
    serializer_class = AtorSerializer
    contextclassname = 'ator-list'
    def initialize_context(self):
        self.context_resource = AtorContext()
        self.context_resource.resource = self

class AtorDetail(NonSpatialResource):
    serializer_class = AtorSerializer
    contextclassname = 'ator-list'
    def initialize_context(self):
        self.context_resource = AtorContext()
        self.context_resource.resource = self

class PublicacaoinformacaogeoespacialList(CollectionResource):
    queryset = Publicacaoinformacaogeoespacial.objects.all()
    serializer_class = PublicacaoinformacaogeoespacialSerializer
    contextclassname = 'publicacaoinformacaogeoespacial-list'
    def initialize_context(self):
        self.context_resource = PublicacaoinformacaogeoespacialContext()
        self.context_resource.resource = self

class PublicacaoinformacaogeoespacialDetail(NonSpatialResource):
    serializer_class = PublicacaoinformacaogeoespacialSerializer
    contextclassname = 'publicacaoinformacaogeoespacial-list'
    def initialize_context(self):
        self.context_resource = PublicacaoinformacaogeoespacialContext()
        self.context_resource.resource = self

class RepresentanteList(CollectionResource):
    queryset = Representante.objects.all()
    serializer_class = RepresentanteSerializer
    contextclassname = 'representante-list'
    def initialize_context(self):
        self.context_resource = RepresentanteContext()
        self.context_resource.resource = self

class RepresentanteDetail(NonSpatialResource):
    serializer_class = RepresentanteSerializer
    contextclassname = 'representante-list'
    def initialize_context(self):
        self.context_resource = RepresentanteContext()
        self.context_resource.resource = self

