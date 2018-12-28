from raster_base.models import *
from hyper_resource.serializers import *
from rest_framework_gis.serializers import GeoFeatureModelSerializer

from rest_framework.serializers import HyperlinkedRelatedField

class EntryPointSerializer(BusinessSerializer):
    class Meta:
        model = EntryPoint
        fields = ["imagem-exemplo-tile1-list", "imagem-exemplo1-list", "imagem-exemplo2-list", "imagem-exemplo4-tile2-list"]
        identifier = None
        identifiers = []

class ImagemExemplo1Serializer(GeoBusinessSerializer):
    class Meta:
        model = ImagemExemplo1
        fields = ['rid','rast']
        identifier = 'rid'
        identifiers = ['pk', 'rid']
        geo_field = 'rast'

class ImagemExemplo2Serializer(BusinessSerializer):
    class Meta:
        model = ImagemExemplo2
        fields = ['rid','rast']
        identifier = 'rid'
        identifiers = ['pk', 'rid']
        geo_field = 'rast'

class ImagemExemploTile1Serializer(BusinessSerializer):
    class Meta:
        model = ImagemExemploTile1
        fields = ['rid','rast']
        identifier = 'rid'
        identifiers = ['pk', 'rid']
        geo_field = 'rast'

class ImagemExemploTile2Serializer(BusinessSerializer):
    class Meta:
        model = ImagemExemploTile2
        fields = ['rid','rast']
        identifier = 'rid'
        identifiers = ['pk', 'rid']
        geo_field = 'rast'



serializers_dict = {}