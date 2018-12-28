from collections import OrderedDict

from rest_framework.reverse import reverse
from rest_framework.views import APIView

from hyper_resource.resources.TiffCollectionResource import TiffCollectionResource
from hyper_resource.resources.TiffResource import TiffResource
from hyper_resource.views import * # depraced
from raster_base.contexts import *
from raster_base.serializers import *
from hyper_resource.resources.EntryPointResource import RasterEntryPointResource

class APIRoot(RasterEntryPointResource):
    serializer_class = EntryPointSerializer

    def get_root_response(self, request, format=None, *args, **kwargs):
        root_links = {
          'imagem-exemplo1-list': reverse('raster_base:ImagemExemplo1_list' , request=request, format=format),
          'imagem-exemplo2-list': reverse('raster_base:ImagemExemplo2_list' , request=request, format=format),
          'imagem-exemplo-tile1-list': reverse('raster_base:ImagemExemploTile1_list' , request=request, format=format),
          'imagem-exemplo4-tile2-list': reverse('raster_base:ImagemExemploTile2_list' , request=request, format=format),
        }

        ordered_dict_of_link = OrderedDict(sorted(root_links.items(), key=lambda t: t[0]))
        return ordered_dict_of_link

class ImagemExemplo1List(TiffCollectionResource):
    queryset = ImagemExemplo1.objects.all()
    serializer_class = ImagemExemplo1Serializer
    contextclassname = 'imagem-exemplo1-list'
    def initialize_context(self):
        self.context_resource = ImagemExemplo1ListContext()
        self.context_resource.resource = self

class ImagemExemplo1Detail(TiffResource):
    serializer_class = ImagemExemplo1Serializer
    contextclassname = 'imagem-exemplo1-list'
    def initialize_context(self):
        self.context_resource = ImagemExemplo1DetailContext()
        self.context_resource.resource = self

class ImagemExemplo2List(TiffCollectionResource):
    queryset = ImagemExemplo2.objects.all()
    serializer_class = ImagemExemplo2Serializer
    contextclassname = 'imagem-exemplo2-list'
    def initialize_context(self):
        self.context_resource = ImagemExemplo2ListContext()
        self.context_resource.resource = self

class ImagemExemplo2Detail(TiffResource):
    serializer_class = ImagemExemplo2Serializer
    contextclassname = 'imagem-exemplo2-list'
    def initialize_context(self):
        self.context_resource = ImagemExemplo2DetailContext()
        self.context_resource.resource = self

class ImagemExemploTile1List(TiffCollectionResource):
    queryset = ImagemExemploTile1.objects.all()
    serializer_class = ImagemExemploTile1Serializer
    contextclassname = 'imagem-exemplo-tile1-list'
    def initialize_context(self):
        self.context_resource = ImagemExemploTile1ListContext()
        self.context_resource.resource = self

class ImagemExemploTile1Detail(TiffResource):
    serializer_class = ImagemExemploTile1Serializer
    contextclassname = 'imagem-exemplo-tile1-list'
    def initialize_context(self):
        self.context_resource = ImagemExemploTile1DetailContext()
        self.context_resource.resource = self

class ImagemExemploTile2List(TiffCollectionResource):
    queryset = ImagemExemploTile2.objects.all()
    serializer_class = ImagemExemploTile2Serializer
    contextclassname = 'imagem-exemplo-tile2-list'
    def initialize_context(self):
        self.context_resource = ImagemExemploTile2ListContext()
        self.context_resource.resource = self

class ImagemExemploTile2Detail(TiffResource):
    serializer_class = ImagemExemploTile2Serializer
    contextclassname = 'imagem-exemplo-tile2-list'
    def initialize_context(self):
        self.context_resource = ImagemExemploTile2DetailContext()
        self.context_resource.resource = self