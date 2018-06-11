from raster_base.models import *
from hyper_resource.serializers import *
from rest_framework_gis.serializers import GeoFeatureModelSerializer

from rest_framework.serializers import HyperlinkedRelatedField

class ImagemExemplo1Serializer(GeoBusinessSerializer):
    class Meta:
        model = ImagemExemplo1
        fields = ['rid','rast']
        identifier = 'rid'
        identifiers = ['pk', 'rid']

class ImagemExemplo2Serializer(BusinessSerializer):
    class Meta:
        model = ImagemExemplo2
        fields = ['rid','rast']
        identifier = 'rid'
        identifiers = ['pk', 'rid']

class ImagemExemploTile1Serializer(BusinessSerializer):
    class Meta:
        model = ImagemExemploTile1
        fields = ['rid','rast']
        identifier = 'rid'
        identifiers = ['pk', 'rid']

class ImagemExemploTile2Serializer(BusinessSerializer):
    class Meta:
        model = ImagemExemploTile2
        fields = ['rid','rast']
        identifier = 'rid'
        identifiers = ['pk', 'rid']



serializers_dict = {}