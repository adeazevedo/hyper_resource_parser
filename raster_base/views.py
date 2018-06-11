from collections import OrderedDict
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.views import APIView
from rest_framework import permissions
from rest_framework import generics
from rest_framework import status
from hyper_resource.views import *
from raster_base.models import *
from raster_base.serializers import *
from raster_base.contexts import *

def get_root_response(request):
    format = None
    root_links = {

      'imagem-exemplo1-list': reverse('raster_base:ImagemExemplo1_list' , request=request, format=format),
      'imagem-exemplo2-list': reverse('raster_base:ImagemExemplo2_list' , request=request, format=format),
      'imagem-exemplo-tile1-list': reverse('raster_base:ImagemExemploTile1_list' , request=request, format=format),
      'imagem-exemplo4-tile2-list': reverse('raster_base:ImagemExemploTile2_list' , request=request, format=format),
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

class ImagemExemplo1List(SpatialCollectionResource):
    queryset = ImagemExemplo1.objects.all()
    serializer_class = ImagemExemplo1Serializer
    contextclassname = 'imagem-exemplo1-list'
    def initialize_context(self):
        self.context_resource = ImagemExemplo1ListContext()
        self.context_resource.resource = self

class ImagemExemplo1Detail(RasterResource):
    serializer_class = ImagemExemplo1Serializer
    contextclassname = 'imagem-exemplo1-list'
    def initialize_context(self):
        self.context_resource = ImagemExemplo1DetailContext()
        self.context_resource.resource = self

class ImagemExemplo2List(SpatialCollectionResource):
    queryset = ImagemExemplo2.objects.all()
    serializer_class = ImagemExemplo2Serializer
    contextclassname = 'imagem-exemplo2-list'
    def initialize_context(self):
        self.context_resource = ImagemExemplo2ListContext()
        self.context_resource.resource = self

class ImagemExemplo2Detail(RasterResource):
    serializer_class = ImagemExemplo2Serializer
    contextclassname = 'imagem-exemplo2-list'
    def initialize_context(self):
        self.context_resource = ImagemExemplo2DetailContext()
        self.context_resource.resource = self

class ImagemExemploTile1List(SpatialCollectionResource):
    queryset = ImagemExemploTile1.objects.all()
    serializer_class = ImagemExemploTile1Serializer
    contextclassname = 'imagem-exemplo-tile1-list'
    def initialize_context(self):
        self.context_resource = ImagemExemploTile1ListContext()
        self.context_resource.resource = self

class ImagemExemploTile1Detail(RasterResource):
    serializer_class = ImagemExemploTile1Serializer
    contextclassname = 'imagem-exemplo-tile1-list'
    def initialize_context(self):
        self.context_resource = ImagemExemploTile1DetailContext()
        self.context_resource.resource = self

class ImagemExemploTile2List(SpatialCollectionResource):
    queryset = ImagemExemploTile2.objects.all()
    serializer_class = ImagemExemploTile2Serializer
    contextclassname = 'imagem-exemplo-tile2-list'
    def initialize_context(self):
        self.context_resource = ImagemExemploTile2ListContext()
        self.context_resource.resource = self

class ImagemExemploTile2Detail(RasterResource):
    serializer_class = ImagemExemploTile2Serializer
    contextclassname = 'imagem-exemplo-tile2-list'
    def initialize_context(self):
        self.context_resource = ImagemExemploTile2DetailContext()
        self.context_resource.resource = self