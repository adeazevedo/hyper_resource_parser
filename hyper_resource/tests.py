import django
import rest_framework
#from rest_framework import generics
#from rest_framework.response import Response
#from rest_framework.views import APIView
#from rest_framework import permissions
#from rest_framework import permissions

from django.contrib.gis.geos import Point
from django.test import TestCase
# Create your tests here.
from django.contrib.gis.db import models

from hyper_resource.models import FeatureModel, FactoryComplexQuery
from hyper_resource.contexts import *
from hyper_resource.resources.AbstractResource import AbstractResource
from hyper_resource.resources.FeatureCollectionResource import FeatureCollectionResource
from hyper_resource.resources.AbstractCollectionResource import AbstractCollectionResource
from django.contrib.gis.geos import GEOSGeometry
from django.test import SimpleTestCase

import json
import requests
from django.http import HttpResponse
from django.shortcuts import get_object_or_404


from django.test.runner import DiscoverRunner
#import os
#os.environ['DJANGO_SETTINGS_MODULE'] = 'bc_edgv.settings'
#django.setup()
#python manage.py test bcim.test_utils  --testrunner=bcim.test_utils.NoDbTestRunner
#python manage.py test hyper_resource.tests --testrunner=hyper_resource.tests.NoDbTestRunner
from django.contrib.gis.db.models import Q

HOST = 'LUC00557196:8000/'

class NoDbTestRunner(DiscoverRunner):
   """ A test runner to test without database creation/deletion """

   def setup_databases(self, **kwargs):
     pass

   def teardown_databases(self, old_config, **kwargs):
     pass

class Ponto(FeatureModel):
    id_objeto = models.IntegerField(primary_key=True)
    geom = models.PointField(blank=True, null=True)
class Linha(FeatureModel):
    id_objeto = models.IntegerField(primary_key=True)
    geom = models.LineStringField(blank=True, null=True)
class Poligono(FeatureModel):
    id_objeto = models.IntegerField(primary_key=True)
    geom = models.PolygonField(blank=True, null=True)
class Geometria(FeatureModel):
    id_objeto = models.IntegerField(primary_key=True)
    geom = models.GeometryField(blank=True, null=True)

## ativando virtual environment em: source ~/desenv/env/env_bc_edgv/bin/activate
## Testando
# python manage.py test hyper_resource.tests  --testrunner=hyper_resource.tests.NoDbTestRunner
##
#python manage.py test bcim.test_utils  --testrunner=bcim.test_utils.NoDbTestRunner
#python manage.py test hyper_resource.tests --testrunner=hyper_resource.tests.NoDbTestRunner
from django.test import SimpleTestCase
#from bcim.utils import APIViewHypermedia
#python manage.py test app --testrunner=app.filename.NoDbTestRunner
#python manage.py test bcim.tests  --testrunner=bcim.tests.NoDbTestRunner
#python manage.py test hyper_resource.tests --testrunner=hyper_resource.tests.NoDbTestRunner
from bcim.models import ModeloTeste

class ModelTest(models.Model):
    id_objeto = models.IntegerField(primary_key=True)
    nome = models.CharField(max_length=100, blank=True, null=True)
    nomeabrev = models.CharField(max_length=50, blank=True, null=True)
    geometriaaproximada = models.CharField(max_length=3, blank=True, null=True)
    operacional = models.CharField(max_length=12, blank=True, null=True)
    situacaofisica = models.TextField(blank=True, null=True)
    tipopostofisc = models.CharField(max_length=22, blank=True, null=True)
    geometry = models.GeometryField(blank=True, null=True)
    polygon = models.PolygonField(blank=True, null=True)
    lineString = models.LineStringField(blank=True, null=True)
    point = models.PointField(blank=True, null=True)
    multipolygon = models.MultiPolygonField(blank=True, null=True)

class TesteResource(AbstractResource):
    def __init__(self, a_name, params, answer):
        self.name = a_name
        self.parameters = params
        self.return_type = answer

class FeatureModelTestCase(SimpleTestCase):
    def setUp(self):
        self.ponto = Ponto()
        self.linha = Linha()
        self.poligono = Poligono()
        self.geometria = Geometria()

    def url_feature(self):
        return ''

    def test_get_geometry_type(self):
        self.assertEquals(self.ponto.get_geometry_type(), Point)

    def test_fields(self):
        self.assertEquals(self.ponto.fields()[0].name, 'id_objeto')

class AbstractResourceTestCase(SimpleTestCase):

    def setUp(self):
        self.tr = TesteResource('name', 'parameters', 'answer')
        self.ar = AbstractCollectionResource()

    def test_attributes(self):
        pass
    def test_operations(self):
        pass
    def test_remove_last_slash(self):

        self.assertEquals(self.ar.remove_last_slash('within/__tokenurl__1/collect/geom/buffer/0.2/'), 'within/__tokenurl__1/collect/geom/buffer/0.2')
        self.assertEquals(self.ar.remove_last_slash('within/__tokenurl__1/collect/geom/buffer/0.2'), 'within/__tokenurl__1/collect/geom/buffer/0.2')
        self.assertEquals(self.ar.remove_last_slash('within/__tokenurl__1/collect/geom/buffer/0.2 '), 'within/__tokenurl__1/collect/geom/buffer/0.2')

    def test_attribute_functions_str_splitted_by_slash(self):
        res = self.ar.attribute_functions_str_splitted_by_slash('within/http://172.30.10.86:8000/ibge/bcim/municipios/3159407/*collect/geom/buffer/0.2/intersects/https://172.30.10.86:8000/instituicoes/bcim/estado/rj/*')
        self.assertEquals(res[0], 'within')
        self.assertEquals(res[1], 'http://172.30.10.86:8000/ibge/bcim/municipios/3159407/')
        self.assertEquals(res[2], '*collect')
        self.assertEquals(res[3], 'geom')
        self.assertEquals(res[4], 'buffer')
        self.assertEquals(res[5], '0.2')
        self.assertEquals(res[6], 'intersects')
        self.assertEquals(res[7], 'https://172.30.10.86:8000/instituicoes/bcim/estado/rj/')

class SpatialResourceTest(SimpleTestCase):

    def test_attributeContextualized(self):
        pass

class FeatureResourceTest(SimpleTestCase):

    def test_basic_get(self):
        pass
    def test_options_url_without_parameters(self):
        pass
    def test_options_url_with_only_attributes(self):
        pass
    def test_options_url_with_only_one_attribute(self):
        pass
    def test_options_url_with_spatia_functions(self):
        pass

class FactoryComplexQueryTest(SimpleTestCase):
    def setUp(self):
        self.fcq = FactoryComplexQuery()
    def test_q_object_for_in(self):

        q = self.fcq.q_object_for_in(str,'sigla', ['ES,RJ'])
        self.assertEquals(Q(sigla__in=['ES,RJ']).__repr__(), q.__repr__())

    def test_q_object_for_eq(self):

        q = self.fcq.q_object_for_eq(str,'sigla', 'ES')
        self.assertEquals(Q(sigla='ES').__repr__(), q.__repr__())

    def test_q_object_for_neq(self):

        q = self.fcq.q_object_for_neq(str, 'sigla', 'ES')
        self.assertEquals((~Q(sigla='ES')).__repr__(), q.__repr__())

    def test_q_object_by_filter_operation(self):
        attribute_operation_str ='filter/sigla/in/rj,es,go/and/data/between/2017-02-01,2017-06-30/'
        import datetime
        start_date = datetime.date(2017, 2, 1)
        end_date = datetime.date(2017, 6, 30)
        q = Q(sigla__in=['rj','es','go']) & Q(data__range=(start_date, end_date))
        model_class = ModeloTeste
        self.fcq.q_object_serialized_by_filter_operation(attribute_operation_str, model_class)

class AbstractCollectionResourceTestCase(SimpleTestCase):
    def setUp(self):
        self.attributes_functions = ['filter/sigla/in/rj,es,go/', 'filter/sigla/uppercase/in/rj,es,go/and/data/between/2017-02-01,2017-06-30/', 'filter/sigla/in/rj,es,go/and/geom/within/{"type":"Polygon","coordinates":[[[-41.881710164667396,-21.297482165015307],[-28.840495695785098,-21.297482165015307],[-28.840495695785098,-17.886950999070834],[-41.881710164667396,-17.886950999070834],[-41.881710164667396,-21.297482165015307]]]}']
        self.acr = AbstractCollectionResource()

    def test_get_operation_name_from_path(self):
        self.assertEquals(self.acr.get_operation_name_from_path('collect/geom/buffer/0.2'), 'collect')
        self.assertEquals(self.acr.get_operation_name_from_path('filter/geom/buffer/0.2'), 'filter')
        self.assertEquals(self.acr.get_operation_name_from_path('filter/geom/containing/http://host/aldeias-indigenas/821/*collect/nome.geom/buffer/0.2'), 'filter_collect')
        self.assertEquals(self.acr.get_operation_name_from_path('collect/nome&geom/buffer/0.2/containing/http://host/aldeias-indigenas/821/*filter/nome/startswith/rio'), 'collect_filter')
        self.assertEquals(self.acr.get_operation_name_from_path('count_resource'), 'count_resource')
        self.assertEquals(self.acr.get_operation_name_from_path('group_by/nome'), 'group_by')
        self.assertEquals(self.acr.get_operation_name_from_path('group_by_count/nome'), 'group_by_count')
        self.assertEquals(self.acr.get_operation_name_from_path('distinct'), 'distinct')
        self.assertEquals(self.acr.get_operation_name_from_path('offset_limit/1&10'), 'offset_limit')
        self.assertEquals(self.acr.get_operation_name_from_path('nadahaver'), None)
    def test_attributes_functions_str_is_filter_with_spatial_operation(self):
        pass
        """
        self.assertTrue(self.acr.attributes_functions_str_is_filter_with_spatial_operation('filter/sigla/in/rj,es,go/and/geom/within/Point(1,2)'))
        self.assertFalse(self.acr.attributes_functions_str_is_filter_with_spatial_operation('/filter'))
        self.assertFalse(self.acr.attributes_functions_str_is_filter_with_spatial_operation('/filter/filter'))
        self.assertFalse(self.acr.attributes_functions_str_is_filter_with_spatial_operation('/filter/ast/eq/ass/geom/within/asd'))
        self.assertFalse(self.acr.attributes_functions_str_is_filter_with_spatial_operation('/filter/within/eq/asd'))
        self.assertTrue(self.acr.attributes_functions_str_is_filter_with_spatial_operation('/filter/within/eq/geom/and/geom/within/asd'))
        self.assertFalse(self.acr.attributes_functions_str_is_filter_with_spatial_operation('/filter/operacao/eq/within'))
        self.assertTrue(self.acr.attributes_functions_str_is_filter_with_spatial_operation('/filter/eq/within/abxgeom'))
        self.assertFalse(self.acr.attributes_functions_str_is_filter_with_spatial_operation('/filter/within/eq/abxx'))
        self.assertFalse(self.acr.attributes_functions_str_is_filter_with_spatial_operation('/within/geom'))
        self.assertFalse(self.acr.attributes_functions_str_is_filter_with_spatial_operation('/within/filter'))
        """
    def test_attributes_functions_str_splitted_by_slash(self):
        self.acr.attribute_functions_str_splitted_by_slash('collect/geom/buffer/0.2') == ['collect','geom', 'buffer', '0.2']
        self.acr.attribute_functions_str_splitted_by_slash('collect/geom/buffer/0.2/') == ['collect','geom', 'buffer', '0.2']
        self.assertEquals(self.acr.attribute_functions_str_splitted_by_slash('collect/geom/buffer/0.2'), ['collect','geom', 'buffer', '0.2'])
        self.assertEquals(self.acr.attribute_functions_str_splitted_by_slash('collect/geom/buffer/0.2/transform/3005&True/area'), ['collect', 'geom', 'buffer', '0.2', 'transform', '3005&True', 'area'])
        self.assertEquals(self.acr.attribute_functions_str_splitted_by_slash('offsetLimit/1&10/collect/geom/buffer/0.2'), ['offsetLimit', '1&10', 'collect', 'geom', 'buffer', '0.2'])
        self.assertEquals(self.acr.attribute_functions_str_splitted_by_slash('within/{"type":"Polygon","coordinates":[[[-48.759514611370854,-28.3426735036349],[-48.631647133384185,-28.3426735036349],[-48.631647133384185,-28.082673631081306],[-48.759514611370854,-28.082673631081306],[-48.759514611370854,-28.3426735036349]]]}/collect/geom/buffer/0.2'), ['within', '{"type":"Polygon","coordinates":[[[-48.759514611370854,-28.3426735036349],[-48.631647133384185,-28.3426735036349],[-48.631647133384185,-28.082673631081306],[-48.759514611370854,-28.082673631081306],[-48.759514611370854,-28.3426735036349]]]}', 'collect', 'geom', 'buffer', '0.2'])
        self.assertEquals(self.acr.attribute_functions_str_splitted_by_slash('within/http://172.30.10.86:8000/instituicoes/ibge/bcim/municipios/3159407/*collect/geom/buffer/0.2/'), ['within', 'http://172.30.10.86:8000/instituicoes/ibge/bcim/municipios/3159407/', '*collect', 'geom', 'buffer', '0.2'])
        self.assertEquals(self.acr.attribute_functions_str_splitted_by_slash('within/https://172.30.10.86:8000/instituicoes/ibge/bcim/municipios/3159407/*collect/geom/buffer/0.2'), ['within', 'https://172.30.10.86:8000/instituicoes/ibge/bcim/municipios/3159407/', '*collect', 'geom', 'buffer', '0.2'])
        self.assertEquals(self.acr.attribute_functions_str_splitted_by_slash('within/http://www.ibge.gov.br:8080/instituicoes/ibge/bcim/municipios/3159407/*collect/geom/buffer/0.2/within/http://ibge/unidades-federativas/RJ/*'), ['within', 'http://www.ibge.gov.br:8080/instituicoes/ibge/bcim/municipios/3159407/', '*collect', 'geom', 'buffer', '0.2', 'within','http://ibge/unidades-federativas/RJ/'])
        self.assertEquals(self.acr.attribute_functions_str_splitted_by_slash('filter/geom/within/http://www.ibge.gov.br:8080/instituicoes/ibge/bcim/municipios/3159407/*'), ['filter', 'geom', 'within', 'http://www.ibge.gov.br:8080/instituicoes/ibge/bcim/municipios/3159407/'])
        self.assertEquals(self.acr.attribute_functions_str_splitted_by_slash('filter/geom/within/http://www.ibge.gov.br:8080/instituicoes/ibge/bcim/municipios/3159407/geom/*and/sigla/eq/http://www.ibge.gov.br:8080/instituicoes/ibge/bcim/municipios/3159407/geocodigo/*'), ['filter', 'geom', 'within', 'http://www.ibge.gov.br:8080/instituicoes/ibge/bcim/municipios/3159407/geom/', '*and', 'sigla', 'eq', 'http://www.ibge.gov.br:8080/instituicoes/ibge/bcim/municipios/3159407/geocodigo/'])
        self.assertEquals(self.acr.attribute_functions_str_splitted_by_slash('filter/geom/within/http://www.ibge.gov.br:8080/instituicoes/ibge/bcim/municipios/3159407/geom/*collect/collect/eq/http://www.ibge.gov.br:8080/instituicoes/ibge/bcim/municipios/3159407/geocodigo/*'), ['filter', 'geom', 'within', 'http://www.ibge.gov.br:8080/instituicoes/ibge/bcim/municipios/3159407/geom/', '*collect', 'collect', 'eq', 'http://www.ibge.gov.br:8080/instituicoes/ibge/bcim/municipios/3159407/geocodigo/'])
 #       self.assertEquals(self.acr.attribute_functions_str_splitted_by_slash('filter/geom/within/http://www.ibge.gov.br:8080/instituicoes/ibge/bcim/municipios/3159407/geom*/and/geocodigo/eq/http://www.ibge.gov.br:8080/instituicoes/ibge/bcim/municipios/3159407/geocodigo/*/collect/collect/eq/http://www.ibge.gov.br:8080/instituicoes/ibge/bcim/municipios/3159407/geocodigo*'),
#['filter', 'geom', 'within', 'http://www.ibge.gov.br:8080/instituicoes/ibge/bcim/municipios/3159407/geom','and','geocodigo','eq','http://www.ibge.gov.br:8080/instituicoes/ibge/bcim/municipios/3159407/geom/and/geocodigo', 'collect', 'collect', 'eq', 'http://www.ibge.gov.br:8080/instituicoes/ibge/bcim/municipios/3159407/geocodigo'])
        #self.assertEquals(self.acr.attribute_functions_str_splitted_by_slash('within/WWw.ibge.gov.br:8080/instituicoes/ibge/bcim/municipios/3159407*/collect/geom/buffer/0.2'), ['filter', 'geom', 'within', 'http://www.ibge.gov.br:8080/instituicoes/ibge/bcim/municipios/3159407/geom', 'and', 'sigla', 'eq', 'http://www.ibge.gov.br:8080/instituicoes/ibge/bcim/municipios/3159407/geocodigo'])
        self.assertEquals(self.acr.attribute_functions_str_splitted_by_slash('filter/collect/within/http://www.ibge.gov.br:8080/instituicoes/ibge/bcim/municipios/3159407/*collect/collect/transform/3005&True/area'),[
            'filter','collect','within','http://www.ibge.gov.br:8080/instituicoes/ibge/bcim/municipios/3159407/','*collect','collect','transform', '3005&True','area'] )

    def test_get_generic_operation_name(self):

        prefix = 'get_objects_from_'
        suffix = '_operation'

        operation_name = self.acr.get_generic_operation_name('filter/geom/within/http://luc00557347.ibge.gov.br/ibge/bcim/unidades-federativas/ES/geom/buffer/0.2*/and/fclass/eq/school/*collect/geom/buffer/0.2')
        self.assertEquals(operation_name, prefix + 'filter_and_collect' + suffix)

        operation_name = self.acr.get_generic_operation_name('filter/sigla/in/RJ,ES/*collect/geom/transform/3005&True/area')
        self.assertEquals(operation_name, prefix + 'filter_and_collect' + suffix)

        operation_name = self.acr.get_generic_operation_name('collect/geom/buffer/0.2/*filter/geom/within/http://luc00557347.ibge.gov.br/ibge/bcim/unidades-federativas/ES/geom/buffer/0.2/and/fclass/eq/school*/')
        self.assertEquals(operation_name, prefix + 'collect_and_filter' + suffix)

        operation_name = self.acr.get_generic_operation_name('filter/geom/within/http://luc00557347.ibge.gov.br/ibge/bcim/unidades-federativas/ES/geom/buffer/0.2')
        self.assertEquals(operation_name, prefix + 'filter' + suffix)

        operation_name = self.acr.get_generic_operation_name('collect/geom/buffer/0.2')
        self.assertEquals(operation_name, prefix + 'collect' + suffix)

        operation_name = self.acr.get_generic_operation_name('groupby/geom/')
        self.assertEquals(operation_name, prefix + 'groupby' + suffix)

        operation_name = self.acr.get_generic_operation_name('groupbycount/geom/')
        self.assertEquals(operation_name, prefix + 'groupbycount' + suffix)

        operation_name = self.acr.get_generic_operation_name('offsetlimit/1:10/')
        self.assertEquals(operation_name, prefix + 'offsetlimit' + suffix)

        operation_name = self.acr.get_generic_operation_name('distinct')
        self.assertEquals(operation_name, prefix + 'distinct' + suffix)

        operation_name = self.acr.get_generic_operation_name('countresource')
        self.assertEquals(operation_name, prefix + 'countresource' + suffix)

        operation_name = self.acr.get_generic_operation_name('annotate/')
        self.assertEquals(operation_name, prefix + 'annotate' + suffix)

#python manage.py test hyper_resource.tests.FeatureCollectionResourceTest --testrunner=hyper_resource.tests.NoDbTestRunner
class FeatureCollectionResourceTest(SimpleTestCase):
    def setUp(self):
        self.attributes_functions = [
            'filter/sigla/in/rj,es,go/',
            'filter/sigla/uppercase/in/rj,es,go/and/data/between/2017-02-01,2017-06-30/',
            'filter/sigla/in/rj,es,go/and/geom/within/{"type":"Polygon","coordinates":[[[-41.881710164667396,-21.297482165015307],[-28.840495695785098,-21.297482165015307],[-28.840495695785098,-17.886950999070834],[-41.881710164667396,-17.886950999070834],[-41.881710164667396,-21.297482165015307]]]}',
        ]
        self.fc = FeatureCollectionResource()

    def test_is_filter_operation(self):
        self.assertTrue(self.fc.path_has_filter_operation('filter/sigla/in/rj,es,go/and/geom'))
        self.assertFalse( self.fc.path_has_filter_operation('/filter'))
        self.assertTrue('filter/sigla/uppercase/in/rj,es,go/and/data/between/2017-02-01,2017-06-30/')

    """
    def test_q_objects_from_filter_operation(self):
        result = self.fc.q_object_for_filter_expression('filter/sigla/eq/ES')
        self.assertEquals(result.__repr__(), Q(sigla='ES').__repr__())
        result = self.fc.q_object_for_filter_expression('filter/sigla/eq/ES/')[0]
        self.assertEquals(result.__repr__(), Q(sigla='ES').__repr__())
        result = self.fc.q_object_for_filter_expression('filter/sigla/in/ES,RJ')[0]
        self.assertEquals(result.__repr__(), Q(sigla__in=['ES,RJ']).__repr__())
        result = self.fc.q_object_for_filter_expression('filter/sigla/in/ES,RJ/')[0]
        self.assertEquals(result, Q(sigla__in=['ES,RJ']))
        result1 = self.fc.q_object_for_filter_expression('filter/sigla/in/ES,RJ/and/data/between/2017-02-01,2017-06-30')[0]
        result2 = self.fc.q_object_for_filter_expression('filter/sigla/in/ES,RJ/and/data/between/2017-02-01,2017-06-30')[1]
        self.assertEquals(result1, Q(sigla__in=['ES,RJ']))
        self.assertEquals(result2, Q(data='ES,RJ'))
    """

    def test_transform_path_with_spatial_operation_str_and_url_as_array(self):
        self.maxDiff = None
        s = 'geom/contains/http://172.30.10.86:8000/instituicoes/ibge/bcim/municipios/3159407/*or/geom/contains/http://172.30.10.86:8000/instituicoes/ibge/bcim/municipios/3159406'
        arr = ['geom', 'contains', 'http:','172.30.10.86:8000','instituicoes','ibge','bcim','municipios','3159407', '*or', 'geom', 'contains', 'http:','172.30.10.86:8000','instituicoes','ibge','bcim','municipios','3159406']
        arr1 = ['geom', 'contains', 'http://172.30.10.86:8000/instituicoes/ibge/bcim/municipios/3159407/', '*or', 'geom', 'contains', 'http://172.30.10.86:8000/instituicoes/ibge/bcim/municipios/3159406/']

        self.assertEquals(len(self.fc.transform_path_with_url_as_array(arr)), len(arr1))

class CollectionResourceTest(SimpleTestCase):
    def setUp(self):
        self.host = 'luc00557196.ibge.gov.br:8000/'
        self.base_uri = "http://" + self.host + "controle-list/"

    def test_simple_collection_request(self):
        # requests.get(uri, headers={key: value, key: value})
        res = requests.get(self.base_uri + "gasto-list/")
        self.assertEquals(res.status_code, 200)
        self.assertEquals(res.headers['content-type'], 'application/json')

    def test_collection_request_by_attributes(self):
        res = requests.get(self.base_uri + "gasto-list/id,data,valor")
        self.assertEquals(res.status_code, 200)
        self.assertEquals(res.headers['content-type'], 'application/json')

    def test_distinct_operation_for_collection_resource(self):
        res = requests.get(self.base_uri + "gasto-list/distinct/data")
        self.assertEquals(res.status_code, 200)
        self.assertEquals(res.headers['content-type'], 'application/json')

    def test_offset_limit_operation_for_collection_resource(self):
        res = requests.get(self.base_uri + "gasto-list/offsetLimit/2&3")
        self.assertEquals(res.status_code, 200)
        self.assertEquals(res.headers['content-type'], 'application/json')
    """
    def test_groupBy_operation_for_collection_resource(self):
        res = requests.get(self.base_uri + "gasto-list/groupBy/data,valor")
        self.assertEquals(res.status_code, 200)
        self.assertEquals(res.headers['content-type'], 'application/json')
    """

class AbstractRequestTest(SimpleTestCase):
    def setUp(self):
        self.bcim_base_uri = "http://" + HOST + "api/bcim/"
        self.controle_base_uri = "http://" + HOST + "controle-list/"
        self.raster_base_uri = "http://" + HOST + "raster/"
        self.simple_path_options_dict_keys = ['@context', '@id', '@type', 'hydra:iriTemplate', 'hydra:representationName', 'hydra:supportedOperations', 'hydra:supportedProperties']
        self.keys_from_attrs_context = ["@id", "@type", "hydra:supportedOperations"]
        self.keys_from_oper_context = ["@id", "@type"]
        self.spatial_operation_names = ['area', 'boundary', 'buffer', 'centroid', 'contains', 'convex_hull', 'coord_seq', 'coords', 'count', 'crosses',
                                        'crs', 'difference', 'dims', 'disjoint', 'distance', 'empty', 'envelope', 'equals', 'equals_exact', 'ewkb',
                                        'ewkt', 'extend', 'extent', 'geojson', 'geom_type', 'geom_typeid', 'get_coords', 'get_srid', 'get_x', 'get_y',
                                        'get_z', 'has_cs', 'hasz', 'hex', 'hexewkb', 'index', 'interpolate', 'intersection', 'intersects', 'join', 'json', 'kml',
                                        'length', 'normalize', 'num_coords', 'num_geom', 'num_points', 'ogr', 'overlaps', 'point_on_surface', 'relate',
                                        'relate_pattern', 'ring', 'simple', 'simplify', 'srid',
                                        'srs', 'sym_difference', 'touches', 'transform', 'union', 'valid', 'valid_reason', 'within', 'wkb', 'wkt', 'x', 'y', 'z']
         #'set_coords', 'set_srid', 'set_x', 'set_y', 'set_z',
        self.string_operations_names = ['capitalize', 'center', 'count', 'endswith', 'find', 'isalnum', 'isalpha', 'isdigit', 'islower', 'isupper',
                                        'join', 'lower', 'split', 'startswith', 'upper']
        self.basic_operations_names = ['join']
        self.spatial_collection_operation_names = ['bbcontains', 'bboverlaps', 'collect', 'contained', 'contains', 'contains_properly', 'count_resource',
                                                    'covers', 'covers_by', 'crosses', 'disjoint', 'distance_gt', 'distance_gte', 'distance_lt', 'distance_lte',
                                                    'distinct', 'dwithin', 'extent', 'filter', 'group_by', 'group_by_count', 'group_by_sum', 'intersects', 'isvalid', 'join', 'left',
                                                    'make_line', 'offset_limit', 'overlaps', 'overlaps_above', 'overlaps_below', 'overlaps_left', 'overlaps_right', 'projection',
                                                   'relate', 'right', 'strictly_above', 'strictly_below', 'touches', 'union', 'within']
        self.collection_operation_names = ['collect', 'count_resource', 'distinct', 'filter', 'group_by', 'group_by_count', 'group_by_sum', 'offset_limit', 'projection']
        self.non_simple_path_dict_keys = ["@context", '@id', '@type', 'hydra:supportedOperations']

    def aux_get_dict_from_response(self, response):
        return dict( json.loads(response.text) )

    def aux_get_keys_from_response(self, response):
        response_dict = self.aux_get_dict_from_response(response)
        return sorted( list(response_dict.keys()) )

    # todo: this methods below must be moved for "AbstractOptionsRequestTest" class
    def aux_get_keys_from_response_context(self, response):
        response_dict = self.aux_get_dict_from_response(response)
        return sorted( list(response_dict["@context"].keys()) )

    def aux_get_keys_from_acontext_attrs(self, response, attr_name):
        response_dict = self.aux_get_dict_from_response(response)
        context_dict = response_dict["@context"]
        return sorted( list( context_dict[attr_name].keys() ) )

    def aux_get_supported_operations_names(self, response):
        response_dict = self.aux_get_dict_from_response(response)
        operations_names = [operation_dict['hydra:operation'] for operation_dict in response_dict['hydra:supportedOperations']]
        return sorted(operations_names)

class AbstractGetRequestTest(AbstractRequestTest):
    def setUp(self):
        super(AbstractGetRequestTest, self).setUp()
        self.feature_collection_keys = ["features", "type"]
        self.geometry_collection_keys = ["geometries", "type"]
        self.feature_keys = ["geometry", "properties", "type"]
        self.geometry_keys = ["coordinates", "type"]

    def aux_get_list_from_response(self, response):
        return list( json.loads(response.text) )

    def aux_get_first_feature(self, response):
        response_dict = self.aux_get_dict_from_response(response)

        if "features" not in response_dict.keys():
            return response_dict
        return response_dict["features"][0]

    def aux_get_first_feature_keys(self, response):
        first_feature = self.aux_get_first_feature(response)
        return sorted( list(first_feature.keys()) )

    def aux_get_first_feature_properties_keys(self, response):
        first_feature = self.aux_get_first_feature(response)
        return sorted( list(first_feature['properties'].keys()) )

    def aux_get_first_element_keys_from_response_list(self, response):
        response_list = self.aux_get_list_from_response(response)
        return sorted( list(response_list[0].keys()) )

    def aux_get_first_geometry_keys_from_response_list(self, response):
        response_dict = self.aux_get_dict_from_response(response)
        first_geometry = response_dict["geometries"][0]
        return sorted( list(first_geometry.keys()) )

    def aux_get_single_feature_properties_keys_from_response(self, response):
        response_dict = self.aux_get_dict_from_response(response)
        return sorted( list(response_dict['properties'].keys()) )

#python manage.py test hyper_resource.tests.CollectOperationTest --testrunner=hyper_resource.tests.NoDbTestRunner
class CollectOperationTest(AbstractGetRequestTest):

    # --------------- TESTS FOR FEATURE COLLECTION ---------------------------------
    # FeatureCollection return
    def test_collect_operation_with_feature_collection_return(self):
        response = requests.get(self.bcim_base_uri + "aldeias-indigenas/collect/nome&geom/buffer/0.2/")
        self.assertEquals(response.status_code, 200)
        self.assertEquals(response.headers['content-type'], 'application/vnd.geo+json')

        response_dict_keys = self.aux_get_keys_from_response(response)
        self.assertEquals(response_dict_keys, self.feature_collection_keys)

        first_feature_keys = self.aux_get_first_feature_keys(response)
        self.assertEquals(first_feature_keys, self.feature_keys)

        first_feature_properties_keys = self.aux_get_first_feature_properties_keys(response)
        self.assertEquals(first_feature_properties_keys, ['nome'])

    def test_collect_operation_with_feature_collection_return_accept_header(self):
        response = requests.get(self.bcim_base_uri + "aldeias-indigenas/collect/nome&geom/buffer/0.2/",
                                headers={'Accept': 'application/octet-stream'})
        self.assertEquals(response.status_code, 200)
        self.assertEquals(response.headers['content-type'], 'application/octet-stream')

    def test_collect_operation_with_non_spatial_operation_and_feature_collection_return(self):
        response = requests.get(self.bcim_base_uri + "aldeias-indigenas/collect/geom&nome/upper")
        self.assertEquals(response.status_code, 200)
        self.assertEquals(response.headers['content-type'], 'application/vnd.geo+json')

        response_dict_keys = self.aux_get_keys_from_response(response)
        self.assertEquals(response_dict_keys, self.feature_collection_keys)

        first_feature_keys = self.aux_get_first_feature_keys(response)
        self.assertEquals(first_feature_keys, self.feature_keys)

        first_feature_properties_keys = self.aux_get_first_feature_properties_keys(response)
        self.assertEquals(first_feature_properties_keys, ['upper']) # possible conceitual error

        #response_dict = self.aux_get_dict_from_response(response)
        #self.assertEquals(list(response_dict["features"][0]["properties"].keys()), ["upper"])

    def test_collect_operation_with_non_spatial_operation_and_feature_collection_return_accept_header(self):
        response = requests.get(self.bcim_base_uri + "aldeias-indigenas/collect/geom&nome/upper",
                                headers={'Accept': 'application/octet-stream'})
        self.assertEquals(response.status_code, 200)
        self.assertEquals(response.headers['content-type'], 'application/octet-stream')

    # GeometryCollection return
    def test_collect_operation_with_geometry_collection_return(self):
        response = requests.get(self.bcim_base_uri + "aldeias-indigenas/collect/geom/buffer/0.2/")
        self.assertEquals(response.status_code, 200)
        self.assertEquals(response.headers['content-type'], 'application/vnd.geo+json')

        response_dict_keys = self.aux_get_keys_from_response(response)
        self.assertEquals(response_dict_keys, self.geometry_collection_keys)

        first_geometry_keys = self.aux_get_first_geometry_keys_from_response_list(response)
        self.assertEquals(first_geometry_keys, self.geometry_keys)

    def test_collect_operation_with_geometry_collection_return_accept_header(self):
        response = requests.get(self.bcim_base_uri + "aldeias-indigenas/collect/geom/buffer/0.2/",
                                headers={'Accept': 'application/octet-stream'})
        self.assertEquals(response.status_code, 200)
        self.assertEquals(response.headers['content-type'], 'application/octet-stream')

    # list return
    def test_collect_operation_with_spatial_operation_and_float_return(self):
        response = requests.get(self.bcim_base_uri + "aldeias-indigenas/collect/nome&geom/area")
        self.assertEquals(response.status_code, 200)
        self.assertEquals(response.headers['content-type'], 'application/json')

        first_element_keys = self.aux_get_first_element_keys_from_response_list(response)
        self.assertEquals(first_element_keys, ["area", "nome"])

    def test_collect_operation_with_spatial_operation_and_float_return_accept_header(self):
        response = requests.get(self.bcim_base_uri + "aldeias-indigenas/collect/nome&geom/area",
                                headers={'Accept': 'application/octet-stream'})
        self.assertEquals(response.status_code, 200)
        self.assertEquals(response.headers['content-type'], 'application/octet-stream')

    def test_collect_operation_with_alphanumeric_operation(self):
        response = requests.get(self.bcim_base_uri + "aldeias-indigenas/collect/nome/upper")
        self.assertEquals(response.status_code, 200)

        first_element_keys = self.aux_get_first_element_keys_from_response_list(response)
        self.assertEquals(first_element_keys, ["upper"])

    def test_collect_operation_with_alphanumeric_operation_accept_header(self):
        response = requests.get(self.bcim_base_uri + "aldeias-indigenas/collect/nome/upper",
                                headers={'Accept': 'application/octet-stream'})
        self.assertEquals(response.status_code, 200)
        self.assertEquals(response.headers['content-type'], 'application/octet-stream')

    # with projection
    def test_collect_operation_with_projection(self):
        response = requests.get(self.bcim_base_uri + "aldeias-indigenas/projection/nome,geom/collect/nome&geom/buffer/0.5")
        self.assertEquals(response.status_code, 200)
        self.assertEquals(response.headers['content-type'], 'application/vnd.geo+json')

        response_keys = self.aux_get_keys_from_response(response)
        self.assertListEqual(response_keys, self.feature_collection_keys)

        first_feature_keys = self.aux_get_first_feature_keys(response)
        self.assertListEqual(first_feature_keys, self.feature_keys)

        first_feature_properties_keys = self.aux_get_first_feature_properties_keys(response)
        self.assertEquals(list(first_feature_properties_keys), ["nome"])

    def test_collect_operation_with_projection_accept_header(self):
        response = requests.get(self.bcim_base_uri + "aldeias-indigenas/collect/nome/upper",
                                headers={'Accept': 'application/octet-stream'})
        self.assertEquals(response.status_code, 200)
        self.assertEquals(response.headers['content-type'], 'application/octet-stream')

    def test_collect_operation_with_projection_different_from_collect_attrs(self):
        response = requests.get(self.bcim_base_uri + "aldeias-indigenas/projection/geom/collect/nome&geom/buffer/0.5")
        self.assertEquals(response.status_code, 400)
        self.assertEquals(response.headers['content-type'], 'application/json')


    # ------------------- TESTS FOR COLLECTION -------------------------------------
    # list return
    def test_collect_operation_with_collection_return(self):
        response = requests.get(self.controle_base_uri + "usuario-list/collect/email&nome/upper/")
        self.assertEquals(response.status_code, 200)
        self.assertEquals(response.headers['content-type'], 'application/json')

        first_element_keys = self.aux_get_first_element_keys_from_response_list(response)
        self.assertEquals(first_element_keys, ["email", "upper"])

    def test_collect_operation_with_collection_return_with_accept_header(self):
        response = requests.get(self.controle_base_uri + "usuario-list/collect/email&nome/upper/",
                                headers={'Accept': 'application/octet-stream'})
        self.assertEquals(response.status_code, 200)
        self.assertEquals(response.headers['content-type'], 'application/octet-stream')

    def test_collect_operation_with_collection_return_only_one_attribute(self):
        response = requests.get(self.controle_base_uri + "usuario-list/collect/nome/upper/")
        self.assertEquals(response.status_code, 200)
        self.assertEquals(response.headers['content-type'], 'application/json')

        first_element_keys = self.aux_get_first_element_keys_from_response_list(response)
        self.assertEquals(first_element_keys, ["upper"])

    def test_collect_operation_with_collection_return_only_one_attribute_with_accept_header(self):
        response = requests.get(self.controle_base_uri + "usuario-list/collect/nome/upper/",
                                headers={'Accept': 'application/octet-stream'})
        self.assertEquals(response.status_code, 200)
        self.assertEquals(response.headers['content-type'], 'application/octet-stream')

    # with projection
    def test_collect_operation_with_projection_and_collection_return(self):
        response = requests.get(self.controle_base_uri + "usuario-list/projection/nome,email/collect/email&nome/upper/")
        self.assertEquals(response.status_code, 200)
        self.assertEquals(response.headers['content-type'], 'application/json')

        first_element_keys = self.aux_get_first_element_keys_from_response_list(response)
        self.assertEquals(first_element_keys, ["email", "upper"])

    def test_collect_operation_with_projection_collection_return_and_accept_header(self):
        response = requests.get(self.controle_base_uri + "usuario-list/projection/nome,email/collect/email&nome/upper/",
                                headers={'Accept': 'application/octet-stream'})
        self.assertEquals(response.status_code, 200)
        self.assertEquals(response.headers['content-type'], 'application/octet-stream')

    def test_collect_operation_for_collection_with_projection_diferent_from_collect_attrs(self):
        response = requests.get(self.controle_base_uri + "usuario-list/projection/email/collect/email&nome/upper/")
        self.assertEquals(response.status_code, 400)
        self.assertEquals(response.headers['content-type'], 'application/json')

#python manage.py test hyper_resource.tests.OptionsForCollectOperationTest --testrunner=hyper_resource.tests.NoDbTestRunner
class OptionsForCollectOperationTest(AbstractRequestTest):
    # --------------- TESTS FOR FEATURE COLLECTION ---------------------------------
    # FeatureCollection return
    def test_options_collect_operation_for_feature_collection_buffer_operation(self):
        response = requests.options(self.bcim_base_uri + "unidades-federativas/collect/sigla&geom/buffer/0.2")
        self.assertEquals(response.status_code, 200)

        response_keys = self.aux_get_keys_from_response(response)
        self.assertEquals(response_keys, self.non_simple_path_dict_keys)

        acontext_keys = self.aux_get_keys_from_response_context(response)
        self.assertEquals(acontext_keys, ["buffer", "collect", "geom", "sigla"])

        geom_context_keys = self.aux_get_keys_from_acontext_attrs(response, "geom")
        self.assertEquals(geom_context_keys, self.keys_from_attrs_context)
        collect_context_keys = self.aux_get_keys_from_acontext_attrs(response, "collect")
        self.assertEquals(collect_context_keys, self.keys_from_oper_context)
        buffer_context_keys = self.aux_get_keys_from_acontext_attrs(response, "buffer")
        self.assertEquals(buffer_context_keys, self.keys_from_oper_context)
        sigla_context_keys = self.aux_get_keys_from_acontext_attrs(response, "sigla")
        self.assertEquals(sigla_context_keys, self.keys_from_attrs_context)

        operations_names = self.aux_get_supported_operations_names(response)
        self.assertEquals(operations_names, self.spatial_collection_operation_names)

        response_dict = self.aux_get_dict_from_response(response)
        self.assertEquals(response_dict["@type"], "FeatureCollection")

    def test_options_collect_operation_for_feature_collection_buffer_operation_accept_octet_stream(self):
        response = requests.options(self.bcim_base_uri + "unidades-federativas/collect/sigla&geom/buffer/0.2",
                                    headers={"accept": "application/octet-stream"})
        self.assertEquals(response.status_code, 200)

        response_keys = self.aux_get_keys_from_response(response)
        self.assertEquals(response_keys, self.non_simple_path_dict_keys)

        acontext_keys = self.aux_get_keys_from_response_context(response)
        self.assertEquals(acontext_keys, ["buffer", "collect", "geom", "sigla"])

        geom_context_keys = self.aux_get_keys_from_acontext_attrs(response, "geom")
        self.assertEquals(geom_context_keys, self.keys_from_attrs_context)
        collect_context_keys = self.aux_get_keys_from_acontext_attrs(response, "collect")
        self.assertEquals(collect_context_keys, self.keys_from_oper_context)
        buffer_context_keys = self.aux_get_keys_from_acontext_attrs(response, "buffer")
        self.assertEquals(buffer_context_keys, self.keys_from_oper_context)
        sigla_context_keys = self.aux_get_keys_from_acontext_attrs(response, "sigla")
        self.assertEquals(sigla_context_keys, self.keys_from_attrs_context)

        operations_names = self.aux_get_supported_operations_names(response)
        self.assertEquals(operations_names, self.spatial_collection_operation_names)

        response_dict = self.aux_get_dict_from_response(response)
        self.assertEquals(response_dict["@type"], "GeobufCollection")

    def test_options_collect_operation_for_feature_collection_lower_operation(self):
        response = requests.options(self.bcim_base_uri + "unidades-federativas/collect/geom&sigla/lower/")
        self.assertEquals(response.status_code, 200)

        response_keys = self.aux_get_keys_from_response(response)
        self.assertEquals(response_keys, self.non_simple_path_dict_keys)

        acontext_keys = self.aux_get_keys_from_response_context(response)
        self.assertEquals(acontext_keys, ["collect", "geom", "lower", "sigla"])

        geom_context_keys = self.aux_get_keys_from_acontext_attrs(response, "geom")
        self.assertEquals(geom_context_keys, self.keys_from_attrs_context)
        collect_context_keys = self.aux_get_keys_from_acontext_attrs(response, "collect")
        self.assertEquals(collect_context_keys, self.keys_from_oper_context)
        lower_context_keys = self.aux_get_keys_from_acontext_attrs(response, "lower")
        self.assertEquals(lower_context_keys, self.keys_from_oper_context)
        sigla_context_keys = self.aux_get_keys_from_acontext_attrs(response, "sigla")
        self.assertEquals(sigla_context_keys, self.keys_from_attrs_context)

        operations_names = self.aux_get_supported_operations_names(response)
        self.assertEquals(operations_names, self.spatial_collection_operation_names)

        response_dict = self.aux_get_dict_from_response(response)
        self.assertEquals(response_dict["@type"], "FeatureCollection")

    def test_options_collect_operation_for_feature_collection_lower_operation_accept_octet_stream(self):
        response = requests.options(self.bcim_base_uri + "unidades-federativas/collect/geom&sigla/lower",
                                    headers={"accept": "application/octet-stream"})
        self.assertEquals(response.status_code, 200)

        response_keys = self.aux_get_keys_from_response(response)
        self.assertEquals(response_keys, self.non_simple_path_dict_keys)

        acontext_keys = self.aux_get_keys_from_response_context(response)
        self.assertEquals(acontext_keys, ["collect", "geom", "lower", "sigla"])

        geom_context_keys = self.aux_get_keys_from_acontext_attrs(response, "geom")
        self.assertEquals(geom_context_keys, self.keys_from_attrs_context)
        collect_context_keys = self.aux_get_keys_from_acontext_attrs(response, "collect")
        self.assertEquals(collect_context_keys, self.keys_from_oper_context)
        lower_context_keys = self.aux_get_keys_from_acontext_attrs(response, "lower")
        self.assertEquals(lower_context_keys, self.keys_from_oper_context)
        sigla_context_keys = self.aux_get_keys_from_acontext_attrs(response, "sigla")
        self.assertEquals(sigla_context_keys, self.keys_from_attrs_context)

        operations_names = self.aux_get_supported_operations_names(response)
        self.assertEquals(operations_names, self.spatial_collection_operation_names)

        response_dict = self.aux_get_dict_from_response(response)
        self.assertEquals(response_dict["@type"], "GeobufCollection")

    # GeometryCollection return
    def test_options_collect_operation_for_feature_collection_only_geometry_attribute_and_buffer_operation(self):
        response = requests.options(self.bcim_base_uri + "unidades-federativas/collect/geom/buffer/0.2")
        self.assertEquals(response.status_code, 200)

        response_keys = self.aux_get_keys_from_response(response)
        self.assertEquals(response_keys, self.non_simple_path_dict_keys)

        acontext_keys = self.aux_get_keys_from_response_context(response)
        self.assertEquals(acontext_keys, ["buffer", "collect", "geom"])

        geom_context_keys = self.aux_get_keys_from_acontext_attrs(response, "geom")
        self.assertEquals(geom_context_keys, self.keys_from_attrs_context)
        collect_context_keys = self.aux_get_keys_from_acontext_attrs(response, "collect")
        self.assertEquals(collect_context_keys, self.keys_from_oper_context)
        buffer_context_keys = self.aux_get_keys_from_acontext_attrs(response, "buffer")
        self.assertEquals(buffer_context_keys, self.keys_from_oper_context)

        operations_names = self.aux_get_supported_operations_names(response)
        self.assertEquals(operations_names, self.spatial_collection_operation_names)

        response_dict = self.aux_get_dict_from_response(response)
        self.assertEquals(response_dict["@type"], "GeometryCollection")

    def test_options_collect_operation_for_feature_collection_only_geometry_attribute_and_buffer_operation_accept_octet_stream(self):
        response = requests.options(self.bcim_base_uri + "unidades-federativas/collect/geom/buffer/0.2",
                                    headers={"accept": "application/octet-stream"})
        self.assertEquals(response.status_code, 200)

        response_keys = self.aux_get_keys_from_response(response)
        self.assertEquals(response_keys, self.non_simple_path_dict_keys)

        acontext_keys = self.aux_get_keys_from_response_context(response)
        self.assertEquals(acontext_keys, ["buffer", "collect", "geom"])

        geom_context_keys = self.aux_get_keys_from_acontext_attrs(response, "geom")
        self.assertEquals(geom_context_keys, self.keys_from_attrs_context)
        collect_context_keys = self.aux_get_keys_from_acontext_attrs(response, "collect")
        self.assertEquals(collect_context_keys, self.keys_from_oper_context)
        buffer_context_keys = self.aux_get_keys_from_acontext_attrs(response, "buffer")
        self.assertEquals(buffer_context_keys, self.keys_from_oper_context)

        operations_names = self.aux_get_supported_operations_names(response)
        self.assertEquals(operations_names, self.spatial_collection_operation_names)

        response_dict = self.aux_get_dict_from_response(response)
        self.assertEquals(response_dict["@type"], "GeobufCollection")

    # Collection return
    def test_options_collect_operation_for_feature_collection_area_operation(self):
        response = requests.options(self.bcim_base_uri + "unidades-federativas/collect/geom/area")
        self.assertEquals(response.status_code, 200)

        response_keys = self.aux_get_keys_from_response(response)
        self.assertEquals(response_keys, self.non_simple_path_dict_keys)

        acontext_keys = self.aux_get_keys_from_response_context(response)
        self.assertEquals(acontext_keys, ["area", "collect", "geom"])

        geom_context_keys = self.aux_get_keys_from_acontext_attrs(response, "geom")
        self.assertEquals(geom_context_keys, self.keys_from_attrs_context)
        collect_context_keys = self.aux_get_keys_from_acontext_attrs(response, "collect")
        self.assertEquals(collect_context_keys, self.keys_from_oper_context)
        area_context_keys = self.aux_get_keys_from_acontext_attrs(response, "area")
        self.assertEquals(area_context_keys, self.keys_from_oper_context)

        operations_names = self.aux_get_supported_operations_names(response)
        self.assertEquals(operations_names, self.collection_operation_names)

        response_dict = self.aux_get_dict_from_response(response)
        self.assertEquals(response_dict["@type"], "Collection")

    def test_options_collect_operation_for_feature_collection_area_operation_accept_octet_stream(self):
        response = requests.options(self.bcim_base_uri + "unidades-federativas/collect/geom/area",
                                    headers={"accept": "application/octet-stream"})
        self.assertEquals(response.status_code, 200)

        response_keys = self.aux_get_keys_from_response(response)
        self.assertEquals(response_keys, self.non_simple_path_dict_keys)

        acontext_keys = self.aux_get_keys_from_response_context(response)
        self.assertEquals(acontext_keys, ["area", "collect", "geom"])

        geom_context_keys = self.aux_get_keys_from_acontext_attrs(response, "geom")
        self.assertEquals(geom_context_keys, self.keys_from_attrs_context)
        collect_context_keys = self.aux_get_keys_from_acontext_attrs(response, "collect")
        self.assertEquals(collect_context_keys, self.keys_from_oper_context)
        area_context_keys = self.aux_get_keys_from_acontext_attrs(response, "area")
        self.assertEquals(area_context_keys, self.keys_from_oper_context)

        operations_names = self.aux_get_supported_operations_names(response)
        self.assertEquals(operations_names, [])

        response_dict = self.aux_get_dict_from_response(response)
        self.assertEquals(response_dict["@type"], "bytes")

    def test_options_collect_operation_for_feature_collection_only_alphanumeric_attribute_and_lower_operation(self):
        response = requests.options(self.bcim_base_uri + "unidades-federativas/collect/sigla/lower")
        self.assertEquals(response.status_code, 200)

        response_keys = self.aux_get_keys_from_response(response)
        self.assertEquals(response_keys, self.non_simple_path_dict_keys)

        acontext_keys = self.aux_get_keys_from_response_context(response)
        self.assertEquals(acontext_keys, ["collect", "lower", "sigla"])

        lower_context_keys = self.aux_get_keys_from_acontext_attrs(response, "lower")
        self.assertEquals(lower_context_keys, self.keys_from_oper_context)
        collect_context_keys = self.aux_get_keys_from_acontext_attrs(response, "collect")
        self.assertEquals(collect_context_keys, self.keys_from_oper_context)
        sigla_context_keys = self.aux_get_keys_from_acontext_attrs(response, "sigla")
        self.assertEquals(sigla_context_keys, self.keys_from_attrs_context)

        operations_names = self.aux_get_supported_operations_names(response)
        self.assertEquals(operations_names, self.collection_operation_names)

        response_dict = self.aux_get_dict_from_response(response)
        self.assertEquals(response_dict["@type"], "Collection")

    def test_options_collect_operation_for_feature_collection_only_alphanumeric_attribute_and_lower_operation_accept_octet_stream(self):
        response = requests.options(self.bcim_base_uri + "unidades-federativas/collect/sigla/lower",
                                    headers={"accept": "application/octet-stream"})
        self.assertEquals(response.status_code, 200)

        response_keys = self.aux_get_keys_from_response(response)
        self.assertEquals(response_keys, self.non_simple_path_dict_keys)

        acontext_keys = self.aux_get_keys_from_response_context(response)
        self.assertEquals(acontext_keys, ["collect", "lower", "sigla"])

        sigla_context_keys = self.aux_get_keys_from_acontext_attrs(response, "sigla")
        self.assertEquals(sigla_context_keys, self.keys_from_attrs_context)
        collect_context_keys = self.aux_get_keys_from_acontext_attrs(response, "collect")
        self.assertEquals(collect_context_keys, self.keys_from_oper_context)
        lower_context_keys = self.aux_get_keys_from_acontext_attrs(response, "lower")
        self.assertEquals(lower_context_keys, self.keys_from_oper_context)

        operations_names = self.aux_get_supported_operations_names(response)
        self.assertEquals(operations_names, [])

        response_dict = self.aux_get_dict_from_response(response)
        self.assertEquals(response_dict["@type"], "bytes")

    # with projection
    def test_options_collect_operation_for_feature_collection_with_projection(self):
        response = requests.options(self.bcim_base_uri + "unidades-federativas/projection/sigla,geom/collect/sigla&geom/buffer/0.2")
        self.assertEquals(response.status_code, 200)

        response_keys = self.aux_get_keys_from_response(response)
        self.assertEquals(response_keys, self.non_simple_path_dict_keys)

        acontext_keys = self.aux_get_keys_from_response_context(response)
        self.assertEquals(acontext_keys, ["buffer", "collect", "geom", "sigla"])

        geom_context_keys = self.aux_get_keys_from_acontext_attrs(response, "geom")
        self.assertEquals(geom_context_keys, self.keys_from_attrs_context)
        collect_context_keys = self.aux_get_keys_from_acontext_attrs(response, "collect")
        self.assertEquals(collect_context_keys, self.keys_from_oper_context)
        buffer_context_keys = self.aux_get_keys_from_acontext_attrs(response, "buffer")
        self.assertEquals(buffer_context_keys, self.keys_from_oper_context)
        sigla_context_keys = self.aux_get_keys_from_acontext_attrs(response, "sigla")
        self.assertEquals(sigla_context_keys, self.keys_from_attrs_context)

        operations_names = self.aux_get_supported_operations_names(response)
        self.assertEquals(operations_names, self.spatial_collection_operation_names)

        response_dict = self.aux_get_dict_from_response(response)
        self.assertEquals(response_dict["@type"], "FeatureCollection")

    def test_options_collect_operation_for_feature_collection_with_projection_accept_octet_stream(self):
        response = requests.options(self.bcim_base_uri + "unidades-federativas/projection/sigla,geom/collect/sigla&geom/buffer/0.2",
                                    headers={"accept": "application/octet-stream"})
        self.assertEquals(response.status_code, 200)

        response_keys = self.aux_get_keys_from_response(response)
        self.assertEquals(response_keys, self.non_simple_path_dict_keys)

        acontext_keys = self.aux_get_keys_from_response_context(response)
        self.assertEquals(acontext_keys, ["buffer", "collect", "geom", "sigla"])

        geom_context_keys = self.aux_get_keys_from_acontext_attrs(response, "geom")
        self.assertEquals(geom_context_keys, self.keys_from_attrs_context)
        collect_context_keys = self.aux_get_keys_from_acontext_attrs(response, "collect")
        self.assertEquals(collect_context_keys, self.keys_from_oper_context)
        buffer_context_keys = self.aux_get_keys_from_acontext_attrs(response, "buffer")
        self.assertEquals(buffer_context_keys, self.keys_from_oper_context)
        sigla_context_keys = self.aux_get_keys_from_acontext_attrs(response, "sigla")
        self.assertEquals(sigla_context_keys, self.keys_from_attrs_context)

        operations_names = self.aux_get_supported_operations_names(response)
        self.assertEquals(operations_names, self.spatial_collection_operation_names)

        response_dict = self.aux_get_dict_from_response(response)
        self.assertEquals(response_dict["@type"], "GeobufCollection")

    def test_options_collect_operation_for_feature_collection_with_projection_attributes_different_from_collect_attributes(self):
        response = requests.options(self.bcim_base_uri + "unidades-federativas/projection/geom/collect/sigla&geom/buffer/0.2")
        self.assertEquals(response.status_code, 400)

    # ------------------- TESTS FOR COLLECTION -------------------------------------
    # list return
    # tests for collection collect operation
    def test_options_collect_for_collection_with_lower_operation(self):
        response = requests.options(self.controle_base_uri + 'usuario-list/collect/nome/upper')
        self.assertEquals(response.status_code, 200)

        response_dict_keys = self.aux_get_keys_from_response(response)
        self.assertEquals(response_dict_keys, self.non_simple_path_dict_keys)

        acontext_keys = self.aux_get_keys_from_response_context(response)
        self.assertEquals(acontext_keys, ['collect', 'nome', 'upper'])

        nome_context_keys = self.aux_get_keys_from_acontext_attrs(response, 'nome')
        self.assertEquals(nome_context_keys, self.keys_from_attrs_context)
        upper_context_keys = self.aux_get_keys_from_acontext_attrs(response, 'upper')
        self.assertEquals(upper_context_keys, self.keys_from_oper_context)
        collect_context_keys = self.aux_get_keys_from_acontext_attrs(response, 'collect')
        self.assertEquals(collect_context_keys, self.keys_from_oper_context)

        supported_operations_names = self.aux_get_supported_operations_names(response)
        self.assertEquals(supported_operations_names, self.collection_operation_names)

        response_dict = self.aux_get_dict_from_response(response)
        self.assertEquals(response_dict['@type'], "Collection")

    def test_options_collect_for_collection_with_lower_operation_accept_octet_stream(self):
        response = requests.options(self.controle_base_uri + 'usuario-list/collect/nome/upper',
                                    headers={"Accept": "application/octet-stream"})
        self.assertEquals(response.status_code, 200)

        response_dict_keys = self.aux_get_keys_from_response(response)
        self.assertEquals(response_dict_keys, self.non_simple_path_dict_keys)

        acontext_keys = self.aux_get_keys_from_response_context(response)
        self.assertEquals(acontext_keys, ['collect', 'nome', 'upper'])

        nome_context_keys = self.aux_get_keys_from_acontext_attrs(response, 'nome')
        self.assertEquals(nome_context_keys, self.keys_from_attrs_context)
        upper_context_keys = self.aux_get_keys_from_acontext_attrs(response, 'upper')
        self.assertEquals(upper_context_keys, self.keys_from_oper_context)
        collect_context_keys = self.aux_get_keys_from_acontext_attrs(response, 'collect')
        self.assertEquals(collect_context_keys, self.keys_from_oper_context)

        supported_operations_names = self.aux_get_supported_operations_names(response)
        self.assertEquals(supported_operations_names, [])

        response_dict = self.aux_get_dict_from_response(response)
        self.assertEquals(response_dict['@type'], "bytes")

    def test_options_collect_for_collection_with_lower_operation_two_attributes(self):
        response = requests.options(self.controle_base_uri + 'usuario-list/collect/nome&email/upper')
        self.assertEquals(response.status_code, 200)

        response_dict_keys = self.aux_get_keys_from_response(response)
        self.assertEquals(response_dict_keys, self.non_simple_path_dict_keys)

        acontext_keys = self.aux_get_keys_from_response_context(response)
        self.assertEquals(acontext_keys, ['collect', 'email', 'nome', 'upper'])

        nome_context_keys = self.aux_get_keys_from_acontext_attrs(response, 'nome')
        self.assertEquals(nome_context_keys, self.keys_from_attrs_context)
        email_context_keys = self.aux_get_keys_from_acontext_attrs(response, 'email')
        self.assertEquals(email_context_keys, self.keys_from_attrs_context)
        upper_context_keys = self.aux_get_keys_from_acontext_attrs(response, 'upper')
        self.assertEquals(upper_context_keys, self.keys_from_oper_context)
        collect_context_keys = self.aux_get_keys_from_acontext_attrs(response, 'collect')
        self.assertEquals(collect_context_keys, self.keys_from_oper_context)

        supported_operations_names = self.aux_get_supported_operations_names(response)
        self.assertEquals(supported_operations_names, self.collection_operation_names)

        response_dict = self.aux_get_dict_from_response(response)
        self.assertEquals(response_dict['@type'], "Collection")

    def test_options_collect_for_collection_with_lower_operation_two_attributes_accept_octet_stream(self):
        response = requests.options(self.controle_base_uri + 'usuario-list/collect/nome&email/upper',
                                    headers={"Accept": "application/octet-stream"})
        self.assertEquals(response.status_code, 200)

        response_dict_keys = self.aux_get_keys_from_response(response)
        self.assertEquals(response_dict_keys, self.non_simple_path_dict_keys)

        acontext_keys = self.aux_get_keys_from_response_context(response)
        self.assertEquals(acontext_keys, ['collect', 'email', 'nome', 'upper'])

        nome_context_keys = self.aux_get_keys_from_acontext_attrs(response, 'nome')
        self.assertEquals(nome_context_keys, self.keys_from_attrs_context)
        email_context_keys = self.aux_get_keys_from_acontext_attrs(response, 'email')
        self.assertEquals(email_context_keys, self.keys_from_attrs_context)
        upper_context_keys = self.aux_get_keys_from_acontext_attrs(response, 'upper')
        self.assertEquals(upper_context_keys, self.keys_from_oper_context)
        collect_context_keys = self.aux_get_keys_from_acontext_attrs(response, 'collect')
        self.assertEquals(collect_context_keys, self.keys_from_oper_context)

        supported_operations_names = self.aux_get_supported_operations_names(response)
        self.assertEquals(supported_operations_names, [])

        response_dict = self.aux_get_dict_from_response(response)
        self.assertEquals(response_dict['@type'], "bytes")

    # with projection
    def test_options_collect_for_collection_with_lower_operation_two_attributes_and_projection(self):
        response = requests.options(self.controle_base_uri + 'usuario-list/projection/nome,email/collect/nome&email/upper')
        self.assertEquals(response.status_code, 200)

        response_dict_keys = self.aux_get_keys_from_response(response)
        self.assertEquals(response_dict_keys, self.non_simple_path_dict_keys)

        acontext_keys = self.aux_get_keys_from_response_context(response)
        self.assertEquals(acontext_keys, ['collect', 'email', 'nome', 'upper'])

        email_context_keys = self.aux_get_keys_from_acontext_attrs(response, 'email')
        self.assertEquals(email_context_keys, self.keys_from_attrs_context)
        nome_upper_context_keys = self.aux_get_keys_from_acontext_attrs(response, 'nome')
        self.assertEquals(nome_upper_context_keys, self.keys_from_attrs_context)
        upper_context_keys = self.aux_get_keys_from_acontext_attrs(response, 'upper')
        self.assertEquals(upper_context_keys, self.keys_from_oper_context)
        collect_context_keys = self.aux_get_keys_from_acontext_attrs(response, 'collect')
        self.assertEquals(collect_context_keys, self.keys_from_oper_context)

        supported_operations_names = self.aux_get_supported_operations_names(response)
        self.assertEquals(supported_operations_names, self.collection_operation_names)

        response_dict = self.aux_get_dict_from_response(response)
        self.assertEquals(response_dict['@type'], "Collection")

    def test_options_collect_for_collection_with_lower_operation_two_attributes_and_projection_accept_octet_stream(self):
        response = requests.options(self.controle_base_uri + 'usuario-list/projection/nome,email/collect/nome&email/upper',
                                    headers={"Accept": "application/octet-stream"})
        self.assertEquals(response.status_code, 200)

        response_dict_keys = self.aux_get_keys_from_response(response)
        self.assertEquals(response_dict_keys, self.non_simple_path_dict_keys)

        acontext_keys = self.aux_get_keys_from_response_context(response)
        self.assertEquals(acontext_keys, ['collect', 'email', 'nome', 'upper'])

        email_context_keys = self.aux_get_keys_from_acontext_attrs(response, 'email')
        self.assertEquals(email_context_keys, self.keys_from_attrs_context)
        nome_upper_context_keys = self.aux_get_keys_from_acontext_attrs(response, 'nome')
        self.assertEquals(nome_upper_context_keys, self.keys_from_attrs_context)
        upper_context_keys = self.aux_get_keys_from_acontext_attrs(response, 'upper')
        self.assertEquals(upper_context_keys, self.keys_from_oper_context)
        collect_context_keys = self.aux_get_keys_from_acontext_attrs(response, 'collect')
        self.assertEquals(collect_context_keys, self.keys_from_oper_context)

        supported_operations_names = self.aux_get_supported_operations_names(response)
        self.assertEquals(supported_operations_names, [])

        response_dict = self.aux_get_dict_from_response(response)
        self.assertEquals(response_dict['@type'], "bytes")

    def test_options_collect_for_collection_with_projection_diferent_from_collect_attrs(self):
        response = requests.get(self.controle_base_uri + "usuario-list/projection/email/collect/email&nome/upper/")
        self.assertEquals(response.status_code, 400)

#python manage.py test hyper_resource.tests.GroupBySumOperationTest --testrunner=hyper_resource.tests.NoDbTestRunner
class GroupBySumOperationTest(AbstractRequestTest):
    def setUp(self):
        super(GroupBySumOperationTest, self).setUp()

    def test_group_by_sum_operation(self):
        response = requests.get(self.controle_base_uri + "gasto-list/group_by_sum/data/valor")
        self.assertEquals(response.status_code, 200)
        self.assertEquals(response.headers['content-type'], 'application/json')

#python manage.py test hyper_resource.tests.ProjectionOperationTest --testrunner=hyper_resource.tests.NoDbTestRunner
class ProjectionOperationTest(AbstractGetRequestTest):

    # --------------- TESTS FOR NONSPATIAL RESOURCE ---------------------------------
    def test_projection_for_non_spatial_resource(self):
        implicit_projection_resp = requests.get(self.controle_base_uri + "usuario-list/1/nome,email") # implicit projection
        self.assertEquals(implicit_projection_resp.status_code, 200)
        self.assertEquals(implicit_projection_resp.headers['content-type'], 'application/json')

        f_response_keys = self.aux_get_keys_from_response(implicit_projection_resp)
        self.assertEquals(f_response_keys, ["email", "nome"])

        explicit_projection_resp = requests.get(self.controle_base_uri + "usuario-list/1/projection/nome,email") # explicit projection
        self.assertEquals(explicit_projection_resp.status_code, 200)
        self.assertEquals(explicit_projection_resp.headers['content-type'], 'application/json')

        s_response_keys = self.aux_get_keys_from_response(explicit_projection_resp)
        self.assertEquals(s_response_keys, ["email", "nome"])

    def test_projection_for_non_spatial_resource_accept_octet_stream(self):
        implicit_projection_resp = requests.get(self.controle_base_uri + "usuario-list/1/nome,email", headers={"Accept": "application/octet-stream"}) # implicit projection
        self.assertEquals(implicit_projection_resp.status_code, 200)
        self.assertEquals(implicit_projection_resp.headers['content-type'], 'application/octet-stream')

        explicit_projection_resp = requests.get(self.controle_base_uri + "usuario-list/1/projection/nome,email", headers={"Accept": "application/octet-stream"}) # explicit projection
        self.assertEquals(explicit_projection_resp.status_code, 200)
        self.assertEquals(explicit_projection_resp.headers['content-type'], 'application/octet-stream')


    # --------------- TESTS FOR FEATURE RESOURCE ---------------------------------
    def test_projection_for_feature_resource(self):
        # implicit projection
        implicit_projection_resp = requests.get(self.bcim_base_uri + "unidades-federativas/ES/nome,geom")
        self.assertEquals(implicit_projection_resp.status_code, 200)
        self.assertEquals(implicit_projection_resp.headers['content-type'], 'application/vnd.geo+json')

        f_response_keys = self.aux_get_keys_from_response(implicit_projection_resp)
        self.assertEquals(f_response_keys, self.feature_keys)

        f_feature_properties_keys = self.aux_get_single_feature_properties_keys_from_response(implicit_projection_resp)
        self.assertEquals(f_feature_properties_keys, ["nome"])

        # explicit projection
        explicit_projection_resp = requests.get(self.bcim_base_uri + "unidades-federativas/ES/projection/nome,geom")
        self.assertEquals(explicit_projection_resp.status_code, 200)
        self.assertEquals(explicit_projection_resp.headers['content-type'], 'application/vnd.geo+json')

        s_response_keys = self.aux_get_keys_from_response(explicit_projection_resp)
        self.assertEquals(s_response_keys, self.feature_keys)

        s_feature_properties_keys = self.aux_get_single_feature_properties_keys_from_response(explicit_projection_resp)
        self.assertEquals(s_feature_properties_keys, ["nome"])

    def test_projection_for_feature_resource_without_geometric_attribute(self):
        # implicit projection
        implicit_projection_resp = requests.get(self.bcim_base_uri + "unidades-federativas/ES/nome,sigla")
        self.assertEquals(implicit_projection_resp.status_code, 200)
        self.assertEquals(implicit_projection_resp.headers['content-type'], 'application/json')

        f_feature_properties_keys = self.aux_get_keys_from_response(implicit_projection_resp)
        self.assertEquals(f_feature_properties_keys, ["nome", "sigla"])

        # explicit projection
        explicit_projection_resp = requests.get(self.bcim_base_uri + "unidades-federativas/ES/projection/nome,sigla")
        self.assertEquals(explicit_projection_resp.status_code, 200)
        self.assertEquals(explicit_projection_resp.headers['content-type'], 'application/json')

        s_feature_properties_keys = self.aux_get_keys_from_response(explicit_projection_resp)
        self.assertEquals(s_feature_properties_keys, ["nome", "sigla"])

    def test_projection_for_feature_resource_only_geometric_attribute(self):
        # implicit projection
        implicit_projection_resp = requests.get(self.bcim_base_uri + "unidades-federativas/ES/geom")
        self.assertEquals(implicit_projection_resp.status_code, 200)
        self.assertEquals(implicit_projection_resp.headers['content-type'], 'application/vnd.geo+json')

        f_response_keys = self.aux_get_keys_from_response(implicit_projection_resp)
        self.assertEquals(f_response_keys, self.geometry_keys)

        # explicit projection
        explicit_projection_resp = requests.get(self.bcim_base_uri + "unidades-federativas/ES/projection/geom")
        self.assertEquals(explicit_projection_resp.status_code, 200)
        self.assertEquals(explicit_projection_resp.headers['content-type'], 'application/vnd.geo+json')

        s_response_keys = self.aux_get_keys_from_response(explicit_projection_resp)
        self.assertEquals(s_response_keys, self.geometry_keys)

    def test_projection_for_feature_resource_accept_octet_stream(self):
        # implicit projection
        implicit_projection_resp = requests.get(self.bcim_base_uri + "unidades-federativas/ES/nome,geom", headers={"Accept": "application/octet-stream"})
        self.assertEquals(implicit_projection_resp.status_code, 200)
        self.assertEquals(implicit_projection_resp.headers['content-type'], 'application/octet-stream')

        explicit_projection_resp = requests.get(self.bcim_base_uri + "unidades-federativas/ES/projection/nome,geom", headers={"Accept": "application/octet-stream"})
        self.assertEquals(explicit_projection_resp.status_code, 200)
        self.assertEquals(explicit_projection_resp.headers['content-type'], 'application/octet-stream')

    def test_projection_for_feature_resource_without_geometric_attribute_accept_octet_stream(self):
        # implicit projection
        implicit_projection_resp = requests.get(self.bcim_base_uri + "unidades-federativas/ES/nome,sigla", headers={"Accept": "application/octet-stream"})
        self.assertEquals(implicit_projection_resp.status_code, 200)
        self.assertEquals(implicit_projection_resp.headers['content-type'], 'application/octet-stream')

        explicit_projection_resp = requests.get(self.bcim_base_uri + "unidades-federativas/ES/projection/nome,sigla", headers={"Accept": "application/octet-stream"})
        self.assertEquals(explicit_projection_resp.status_code, 200)
        self.assertEquals(explicit_projection_resp.headers['content-type'], 'application/octet-stream')

    def test_projection_for_feature_resource_only_geometric_attribute_accept_octet_stream(self):
        # implicit projection
        implicit_projection_resp = requests.get(self.bcim_base_uri + "unidades-federativas/ES/geom", headers={"Accept": "application/octet-stream"})
        self.assertEquals(implicit_projection_resp.status_code, 200)
        self.assertEquals(implicit_projection_resp.headers['content-type'], 'application/octet-stream')

        # explicit projection
        explicit_projection_resp = requests.get(self.bcim_base_uri + "unidades-federativas/ES/projection/geom", headers={"Accept": "application/octet-stream"})
        self.assertEquals(explicit_projection_resp.status_code, 200)
        self.assertEquals(explicit_projection_resp.headers['content-type'], 'application/octet-stream')

    # --------------- TESTS FOR COLLECTION ---------------------------------
    def test_projection_for_collection_resource(self):
        implicit_projection_resp = requests.get(self.controle_base_uri + "usuario-list/nome,email/")
        self.assertEquals(implicit_projection_resp.status_code, 200)
        self.assertEquals(implicit_projection_resp.headers['content-type'], 'application/json')

        f_keys_from_first_element = self.aux_get_first_element_keys_from_response_list(implicit_projection_resp)
        self.assertEquals(f_keys_from_first_element, ['email', 'nome'])

        explicit_projection_resp = requests.get(self.controle_base_uri + "usuario-list/projection/nome,email/")
        self.assertEquals(explicit_projection_resp.status_code, 200)
        self.assertEquals(explicit_projection_resp.headers['content-type'], 'application/json')

        s_keys_from_first_element = self.aux_get_first_element_keys_from_response_list(explicit_projection_resp)
        self.assertEquals(s_keys_from_first_element, ['email', 'nome'])

    def test_projection_for_collection_resource_with_collect_operation(self):
        response = requests.get(self.controle_base_uri + "usuario-list/projection/nome,email/collect/email&nome/upper")
        self.assertEquals(response.status_code, 200)
        self.assertEquals(response.headers['content-type'], 'application/json')

        keys_from_frist_element = self.aux_get_first_element_keys_from_response_list(response)
        self.assertEquals(keys_from_frist_element, ['email', 'upper'])

    def test_projection_for_collection_resource_with_collect_operation_projection_list_different_from_collect_list(self):
        response = requests.get(self.controle_base_uri + "usuario-list/projection/nome,email/collect/nome/upper")
        self.assertEquals(response.status_code, 400)

    def test_projection_for_collection_resource_accept_octet_stream(self):
        response = requests.get(self.controle_base_uri + "usuario-list/nome,email/", headers={"Accept": "application/octet-stream"})
        self.assertEquals(response.status_code, 200)
        self.assertEquals(response.headers['content-type'], 'application/octet-stream')

    def test_projection_for_collection_resource_with_collect_operation_accept_octet_stream(self):
        response = requests.get(self.controle_base_uri + "usuario-list/projection/nome,email/collect/email&nome/upper", headers={"Accept": "application/octet-stream"})
        self.assertEquals(response.status_code, 200)
        self.assertEquals(response.headers['content-type'], 'application/octet-stream')

    # --------------- TESTS FOR FEATURE COLLECTION ---------------------------------
    def test_projection_for_feature_collection(self):
        implicit_projection_resp = requests.get(self.bcim_base_uri + "unidades-federativas/nome,geom")
        self.assertEquals(implicit_projection_resp.status_code, 200)
        self.assertEquals(implicit_projection_resp.headers['content-type'], 'application/vnd.geo+json')

        f_first_feature_keys = self.aux_get_first_feature_keys(implicit_projection_resp)
        self.assertEquals(f_first_feature_keys, self.feature_keys)
        f_first_feature_properties_keys = self.aux_get_first_feature_properties_keys(implicit_projection_resp)
        self.assertEquals(f_first_feature_properties_keys, ['nome'])

        explicit_projection_resp = requests.get(self.bcim_base_uri + "unidades-federativas/projection/nome,geom")
        self.assertEquals(explicit_projection_resp.status_code, 200)
        self.assertEquals(explicit_projection_resp.headers['content-type'], 'application/vnd.geo+json')

        s_first_feature_keys = self.aux_get_first_feature_keys(explicit_projection_resp)
        self.assertEquals(s_first_feature_keys, self.feature_keys)
        s_first_feature_properties_keys = self.aux_get_first_feature_properties_keys(explicit_projection_resp)
        self.assertEquals(s_first_feature_properties_keys, ['nome'])

    def test_projection_for_feature_collection_without_geometric_attribute(self):
        implicit_projection_resp = requests.get(self.bcim_base_uri + "unidades-federativas/nome")
        self.assertEquals(implicit_projection_resp.status_code, 200)
        self.assertEquals(implicit_projection_resp.headers['content-type'], 'application/json')

        f_first_element_keys = self.aux_get_first_element_keys_from_response_list(implicit_projection_resp)
        self.assertEquals(f_first_element_keys, ['nome'])

        explicit_projection_resp = requests.get(self.bcim_base_uri + "unidades-federativas/projection/nome")
        self.assertEquals(explicit_projection_resp.status_code, 200)
        self.assertEquals(explicit_projection_resp.headers['content-type'], 'application/json')

        s_first_element_keys = self.aux_get_first_element_keys_from_response_list(explicit_projection_resp)
        self.assertEquals(s_first_element_keys, ['nome'])

    def test_projection_for_feature_collection_only_geometric_attribute(self):
        implicit_projection_resp = requests.get(self.bcim_base_uri + "unidades-federativas/geom")
        self.assertEquals(implicit_projection_resp.status_code, 200)
        self.assertEquals(implicit_projection_resp.headers['content-type'], 'application/vnd.geo+json')

        f_first_geometry_keys = self.aux_get_first_geometry_keys_from_response_list(implicit_projection_resp)
        self.assertEquals(f_first_geometry_keys, self.geometry_keys)

        explicit_projection_resp = requests.get(self.bcim_base_uri + "unidades-federativas/projection/geom")
        self.assertEquals(explicit_projection_resp.status_code, 200)
        self.assertEquals(explicit_projection_resp.headers['content-type'], 'application/vnd.geo+json')

        s_first_geometry_keys = self.aux_get_first_geometry_keys_from_response_list(explicit_projection_resp)
        self.assertEquals(s_first_geometry_keys, self.geometry_keys)

    # tests just to know if projection works with collect operation (tests for collect operation must be in his specific test class)
    def test_projection_for_feature_collection_with_collect_operation(self):
        response = requests.get(self.bcim_base_uri + "aldeias-indigenas/projection/nome,geom/collect/nome&geom/buffer/0.2")
        self.assertEquals(response.status_code, 200)
        self.assertEquals(response.headers['content-type'], 'application/vnd.geo+json')

        first_feature_keys = self.aux_get_first_feature_keys(response)
        self.assertEquals(first_feature_keys, self.feature_keys)
        first_feature_properties_keys = self.aux_get_first_feature_properties_keys(response)
        self.assertEquals(first_feature_properties_keys, ['nome'])

    def test_projection_for_feature_collection_with_collect_operation_projection_attributes_different_from_collect_attibutes(self):
        response = requests.get(self.bcim_base_uri + "aldeias-indigenas/projection/nome,geom/collect/geom/buffer/0.2")
        self.assertEquals(response.status_code, 400)
        self.assertEquals(response.headers['content-type'], 'application/json')

    # binary response
    def test_projection_for_feature_collection_accept_octet_stream(self):
        implicit_projection_resp = requests.get(self.bcim_base_uri + "unidades-federativas/nome,geom", headers={"Accept": "application/octet-stream"})
        self.assertEquals(implicit_projection_resp.status_code, 200)
        self.assertEquals(implicit_projection_resp.headers['content-type'], 'application/octet-stream')

        explicit_projection_resp = requests.get(self.bcim_base_uri + "unidades-federativas/projection/nome,geom", headers={"Accept": "application/octet-stream"})
        self.assertEquals(explicit_projection_resp.status_code, 200)
        self.assertEquals(explicit_projection_resp.headers['content-type'], 'application/octet-stream')

    def test_projection_for_feature_collection_without_geometric_attribute_accept_octet_stream(self):
        implicit_projection_resp = requests.get(self.bcim_base_uri + "unidades-federativas/nome", headers={"Accept": "application/octet-stream"})
        self.assertEquals(implicit_projection_resp.status_code, 200)
        self.assertEquals(implicit_projection_resp.headers['content-type'], 'application/octet-stream')

        explicit_projection_resp = requests.get(self.bcim_base_uri + "unidades-federativas/projection/nome", headers={"Accept": "application/octet-stream"})
        self.assertEquals(explicit_projection_resp.status_code, 200)
        self.assertEquals(explicit_projection_resp.headers['content-type'], 'application/octet-stream')

    def test_projection_for_feature_collection_only_geometric_attribute_accept_octet_stream(self):
        implicit_projection_resp = requests.get(self.bcim_base_uri + "unidades-federativas/geom", headers={"Accept": "application/octet-stream"})
        self.assertEquals(implicit_projection_resp.status_code, 200)
        self.assertEquals(implicit_projection_resp.headers['content-type'], 'application/octet-stream')

        explicit_projection_resp = requests.get(self.bcim_base_uri + "unidades-federativas/projection/geom", headers={"Accept": "application/octet-stream"})
        self.assertEquals(explicit_projection_resp.status_code, 200)
        self.assertEquals(explicit_projection_resp.headers['content-type'], 'application/octet-stream')

    def test_projection_for_feature_collection_with_collect_operation_accept_octet_stream(self):
        response = requests.get(self.bcim_base_uri + "aldeias-indigenas/projection/nome,geom/collect/nome&geom/buffer/0.2",
                                headers={"Accept": "application/octet-stream"})
        self.assertEquals(response.status_code, 200)
        self.assertEquals(response.headers['content-type'], 'application/octet-stream')

#python manage.py test hyper_resource.tests.OptionsForProjectionOperation --testrunner=hyper_resource.tests.NoDbTestRunner
class OptionsForProjectionOperation(AbstractRequestTest):

    # --------------- TESTS FOR NONSPATIAL RESOURCE ---------------------------------
    def test_options_for_non_spatial_resource_projection_operation(self):
        # implicit projection
        implicit_projection_resp = requests.options(self.controle_base_uri + "usuario-list/1/nome,email")
        self.assertEquals(implicit_projection_resp.status_code, 200)

        implicit_projection_resp_keys = self.aux_get_keys_from_response(implicit_projection_resp)
        self.assertEquals(implicit_projection_resp_keys, self.non_simple_path_dict_keys)

        f_supported_operations_names = self.aux_get_supported_operations_names(implicit_projection_resp)
        self.assertEquals(f_supported_operations_names, self.basic_operations_names)

        f_acontext_keys = self.aux_get_keys_from_response_context(implicit_projection_resp)
        self.assertEquals(f_acontext_keys, ['email', 'nome'])

        f_email_context_keys = self.aux_get_keys_from_acontext_attrs(implicit_projection_resp, 'email')
        self.assertEquals(f_email_context_keys, self.keys_from_attrs_context)
        f_nome_context_keys = self.aux_get_keys_from_acontext_attrs(implicit_projection_resp, 'nome')
        self.assertEquals(f_nome_context_keys, self.keys_from_attrs_context)

        f_resp_dict = self.aux_get_dict_from_response(implicit_projection_resp)
        self.assertEqual(f_resp_dict['@type'], 'Thing')

        # explicit projection
        explicit_projection_resp = requests.options(self.controle_base_uri + "usuario-list/1/projection/nome,email")
        self.assertEquals(explicit_projection_resp.status_code, 200)

        explicit_projection_resp_keys = self.aux_get_keys_from_response(explicit_projection_resp)
        self.assertEquals(explicit_projection_resp_keys, self.non_simple_path_dict_keys)

        s_supported_operations_names = self.aux_get_supported_operations_names(explicit_projection_resp)
        self.assertEquals(s_supported_operations_names, self.basic_operations_names)

        s_acontext_keys = self.aux_get_keys_from_response_context(explicit_projection_resp)
        self.assertEquals(s_acontext_keys, ['email', 'nome', 'projection'])

        s_email_context_keys = self.aux_get_keys_from_acontext_attrs(explicit_projection_resp, 'email')
        self.assertEquals(s_email_context_keys, self.keys_from_attrs_context)
        s_nome_context_keys = self.aux_get_keys_from_acontext_attrs(explicit_projection_resp, 'nome')
        self.assertEquals(s_nome_context_keys, self.keys_from_attrs_context)
        s_projection_context_keys = self.aux_get_keys_from_acontext_attrs(explicit_projection_resp, 'projection')
        self.assertEquals(s_projection_context_keys, self.keys_from_oper_context)

        s_resp_dict = self.aux_get_dict_from_response(explicit_projection_resp)
        self.assertEqual(s_resp_dict['@type'], 'Thing')

    def test_options_for_non_spatial_resource_projection_operation_accept_octet_stream(self):
        # implicit projection
        implicit_projection_resp = requests.options(self.controle_base_uri + "usuario-list/1/nome,email",
                                                    headers={"Accept": "application/octet-stream"})
        self.assertEquals(implicit_projection_resp.status_code, 200)

        implicit_projection_resp_keys = self.aux_get_keys_from_response(implicit_projection_resp)
        self.assertEquals(implicit_projection_resp_keys, self.non_simple_path_dict_keys)

        f_supported_operations_names = self.aux_get_supported_operations_names(implicit_projection_resp)
        self.assertEquals(f_supported_operations_names, [])

        f_acontext_keys = self.aux_get_keys_from_response_context(implicit_projection_resp)
        self.assertEquals(f_acontext_keys, ['email', 'nome'])

        f_email_context_keys = self.aux_get_keys_from_acontext_attrs(implicit_projection_resp, 'email')
        self.assertEquals(f_email_context_keys, self.keys_from_attrs_context)
        f_nome_context_keys = self.aux_get_keys_from_acontext_attrs(implicit_projection_resp, 'nome')
        self.assertEquals(f_nome_context_keys, self.keys_from_attrs_context)

        f_resp_dict = self.aux_get_dict_from_response(implicit_projection_resp)
        self.assertEqual(f_resp_dict['@type'], 'bytes')

        # explicit projection
        explicit_projection_resp = requests.options(self.controle_base_uri + "usuario-list/1/projection/nome,email",
                                                    headers={"Accept": "application/octet-stream"})
        self.assertEquals(explicit_projection_resp.status_code, 200)

        explicit_projection_resp_keys = self.aux_get_keys_from_response(explicit_projection_resp)
        self.assertEquals(explicit_projection_resp_keys, self.non_simple_path_dict_keys)

        s_supported_operations_names = self.aux_get_supported_operations_names(explicit_projection_resp)
        self.assertEquals(s_supported_operations_names, [])

        s_acontext_keys = self.aux_get_keys_from_response_context(explicit_projection_resp)
        self.assertEquals(s_acontext_keys, ['email', 'nome', 'projection'])

        s_email_context_keys = self.aux_get_keys_from_acontext_attrs(explicit_projection_resp, 'email')
        self.assertEquals(s_email_context_keys, self.keys_from_attrs_context)
        s_nome_context_keys = self.aux_get_keys_from_acontext_attrs(explicit_projection_resp, 'nome')
        self.assertEquals(s_nome_context_keys, self.keys_from_attrs_context)
        s_projection_context_keys = self.aux_get_keys_from_acontext_attrs(explicit_projection_resp, 'projection')
        self.assertEquals(s_projection_context_keys, self.keys_from_oper_context)

        s_resp_dict = self.aux_get_dict_from_response(explicit_projection_resp)
        self.assertEqual(s_resp_dict['@type'], 'bytes')

    # --------------- TESTS FOR FEATURE RESOURCE ---------------------------------
    def test_options_for_feature_resource_projection_operation(self):
        # implicit project
        implicit_projection_resp = requests.options(self.bcim_base_uri + "unidades-federativas/ES/nome,geom/")
        self.assertEquals(implicit_projection_resp.status_code, 200)

        implicit_projection_resp_keys = self.aux_get_keys_from_response(implicit_projection_resp)
        self.assertEquals(implicit_projection_resp_keys, self.non_simple_path_dict_keys)

        f_supported_operations_names = self.aux_get_supported_operations_names(implicit_projection_resp)
        self.assertEquals(f_supported_operations_names, self.spatial_operation_names)

        f_acontext_keys = self.aux_get_keys_from_response_context(implicit_projection_resp)
        self.assertEquals(f_acontext_keys, ['geom', 'nome'])

        f_geom_context_keys = self.aux_get_keys_from_acontext_attrs(implicit_projection_resp, 'geom')
        self.assertEquals(f_geom_context_keys, self.keys_from_attrs_context)
        f_nome_context_keys = self.aux_get_keys_from_acontext_attrs(implicit_projection_resp, 'nome')
        self.assertEquals(f_nome_context_keys, self.keys_from_attrs_context)

        f_resp_dict = self.aux_get_dict_from_response(implicit_projection_resp)
        self.assertEqual(f_resp_dict['@type'], 'Feature')

        # explicit projection
        explicit_projection_resp = requests.options(self.bcim_base_uri + "unidades-federativas/ES/projection/nome,geom/")
        self.assertEquals(explicit_projection_resp.status_code, 200)

        explicit_projection_resp_keys = self.aux_get_keys_from_response(explicit_projection_resp)
        self.assertEquals(explicit_projection_resp_keys, self.non_simple_path_dict_keys)

        s_supported_operations_names = self.aux_get_supported_operations_names(explicit_projection_resp)
        self.assertEquals(s_supported_operations_names, self.spatial_operation_names)

        s_acontext_keys = self.aux_get_keys_from_response_context(explicit_projection_resp)
        self.assertEquals(s_acontext_keys, ['geom', 'nome', 'projection'])

        s_geom_context_keys = self.aux_get_keys_from_acontext_attrs(explicit_projection_resp, 'geom')
        self.assertEquals(s_geom_context_keys, self.keys_from_attrs_context)
        s_nome_context_keys = self.aux_get_keys_from_acontext_attrs(explicit_projection_resp, 'nome')
        self.assertEquals(s_nome_context_keys, self.keys_from_attrs_context)
        s_projection_context_keys = self.aux_get_keys_from_acontext_attrs(explicit_projection_resp, 'projection')
        self.assertEquals(s_projection_context_keys, self.keys_from_oper_context)

        s_resp_dict = self.aux_get_dict_from_response(explicit_projection_resp)
        self.assertEqual(s_resp_dict['@type'], 'Feature')

    def test_options_for_feature_resource_projection_operation_only_geometric_attribute(self):
        # implicit project
        implicit_projection_resp = requests.options(self.bcim_base_uri + "unidades-federativas/ES/geom/")
        self.assertEquals(implicit_projection_resp.status_code, 200)

        implicit_projection_resp_keys = self.aux_get_keys_from_response(implicit_projection_resp)
        self.assertEquals(implicit_projection_resp_keys, self.non_simple_path_dict_keys)

        f_supported_operations_names = self.aux_get_supported_operations_names(implicit_projection_resp)
        self.assertEquals(f_supported_operations_names, self.spatial_operation_names)

        f_acontext_keys = self.aux_get_keys_from_response_context(implicit_projection_resp)
        self.assertEquals(f_acontext_keys, ['geom'])

        f_geom_context_keys = self.aux_get_keys_from_acontext_attrs(implicit_projection_resp, 'geom')
        self.assertEquals(f_geom_context_keys, self.keys_from_attrs_context)

        f_resp_dict = self.aux_get_dict_from_response(implicit_projection_resp)
        self.assertEqual(f_resp_dict['@type'], 'GeometryField')

        # explicit projection
        explicit_projection_resp = requests.options(self.bcim_base_uri + "unidades-federativas/ES/projection/geom/")
        self.assertEquals(explicit_projection_resp.status_code, 200)

        explicit_projection_resp_keys = self.aux_get_keys_from_response(explicit_projection_resp)
        self.assertEquals(explicit_projection_resp_keys, self.non_simple_path_dict_keys)

        s_supported_operations_names = self.aux_get_supported_operations_names(explicit_projection_resp)
        self.assertEquals(s_supported_operations_names, self.spatial_operation_names)

        s_acontext_keys = self.aux_get_keys_from_response_context(explicit_projection_resp)
        self.assertEquals(s_acontext_keys, ['geom', 'projection'])

        s_geom_context_keys = self.aux_get_keys_from_acontext_attrs(explicit_projection_resp, 'geom')
        self.assertEquals(s_geom_context_keys, self.keys_from_attrs_context)
        s_projection_context_keys = self.aux_get_keys_from_acontext_attrs(explicit_projection_resp, 'projection')
        self.assertEquals(s_projection_context_keys, self.keys_from_oper_context)

        s_resp_dict = self.aux_get_dict_from_response(explicit_projection_resp)
        self.assertEqual(s_resp_dict['@type'], 'GeometryField')

    def test_options_for_feature_resource_projection_operation_only_alphanumeric_attribute(self):
        # implicit project
        implicit_projection_resp = requests.options(self.bcim_base_uri + "unidades-federativas/ES/nome/")
        self.assertEquals(implicit_projection_resp.status_code, 200)

        implicit_projection_resp_keys = self.aux_get_keys_from_response(implicit_projection_resp)
        self.assertEquals(implicit_projection_resp_keys, self.non_simple_path_dict_keys)

        f_supported_operations_names = self.aux_get_supported_operations_names(implicit_projection_resp)
        self.assertEquals(f_supported_operations_names, self.string_operations_names)

        f_acontext_keys = self.aux_get_keys_from_response_context(implicit_projection_resp)
        self.assertEquals(f_acontext_keys, ['nome'])

        f_nome_context_keys = self.aux_get_keys_from_acontext_attrs(implicit_projection_resp, 'nome')
        self.assertEquals(f_nome_context_keys, self.keys_from_attrs_context)

        f_resp_dict = self.aux_get_dict_from_response(implicit_projection_resp)
        self.assertEqual(f_resp_dict['@type'], 'CharField')

        # explicit projection
        explicit_projection_resp = requests.options(self.bcim_base_uri + "unidades-federativas/ES/projection/nome/")
        self.assertEquals(explicit_projection_resp.status_code, 200)

        explicit_projection_resp_keys = self.aux_get_keys_from_response(explicit_projection_resp)
        self.assertEquals(explicit_projection_resp_keys, self.non_simple_path_dict_keys)

        s_supported_operations_names = self.aux_get_supported_operations_names(explicit_projection_resp)
        self.assertEquals(s_supported_operations_names, self.string_operations_names)

        s_acontext_keys = self.aux_get_keys_from_response_context(explicit_projection_resp)
        self.assertEquals(s_acontext_keys, ['nome', 'projection'])

        s_nome_context_keys = self.aux_get_keys_from_acontext_attrs(explicit_projection_resp, 'nome')
        self.assertEquals(s_nome_context_keys, self.keys_from_attrs_context)
        s_projection_context_keys = self.aux_get_keys_from_acontext_attrs(explicit_projection_resp, 'projection')
        self.assertEquals(s_projection_context_keys, self.keys_from_oper_context)

        s_resp_dict = self.aux_get_dict_from_response(explicit_projection_resp)
        self.assertEqual(s_resp_dict['@type'], 'CharField')

    # --------------- TESTS FOR COLLECTION ---------------------------------
    def test_options_for_collection_resource_projection_operation(self):
        implicit_projection_resp = requests.options(self.controle_base_uri + "usuario-list/nome,email")
        self.assertEquals(implicit_projection_resp.status_code, 200)

        implicit_projection_resp_keys = self.aux_get_keys_from_response(implicit_projection_resp)
        self.assertEquals(implicit_projection_resp_keys, self.non_simple_path_dict_keys)

        f_supported_operations_names = self.aux_get_supported_operations_names(implicit_projection_resp)
        self.assertEquals(f_supported_operations_names, self.collection_operation_names)

        f_acontext_keys = self.aux_get_keys_from_response_context(implicit_projection_resp)
        self.assertEquals(f_acontext_keys, ['email', 'nome'])

        f_email_context_keys = self.aux_get_keys_from_acontext_attrs(implicit_projection_resp, 'email')
        self.assertEquals(f_email_context_keys, self.keys_from_attrs_context)
        f_nome_context_keys = self.aux_get_keys_from_acontext_attrs(implicit_projection_resp, 'nome')
        self.assertEquals(f_nome_context_keys, self.keys_from_attrs_context)

        f_resp_dict = self.aux_get_dict_from_response(implicit_projection_resp)
        self.assertEqual(f_resp_dict['@type'], 'Collection')

        # explicit projection
        explicit_projection_resp = requests.options(self.controle_base_uri + "usuario-list/projection/nome,email")
        self.assertEquals(explicit_projection_resp.status_code, 200)

        explicit_projection_resp_keys = self.aux_get_keys_from_response(explicit_projection_resp)
        self.assertEquals(explicit_projection_resp_keys, self.non_simple_path_dict_keys)

        s_supported_operations_names = self.aux_get_supported_operations_names(explicit_projection_resp)
        self.assertEquals(s_supported_operations_names, self.collection_operation_names)

        s_acontext_keys = self.aux_get_keys_from_response_context(explicit_projection_resp)
        self.assertEquals(s_acontext_keys, ['email', 'nome', 'projection'])

        s_email_context_keys = self.aux_get_keys_from_acontext_attrs(explicit_projection_resp, 'email')
        self.assertEquals(s_email_context_keys, self.keys_from_attrs_context)
        s_nome_context_keys = self.aux_get_keys_from_acontext_attrs(explicit_projection_resp, 'nome')
        self.assertEquals(s_nome_context_keys, self.keys_from_attrs_context)
        s_projection_context_keys = self.aux_get_keys_from_acontext_attrs(explicit_projection_resp, 'projection')
        self.assertEquals(s_projection_context_keys, self.keys_from_oper_context)

        s_resp_dict = self.aux_get_dict_from_response(explicit_projection_resp)
        self.assertEqual(s_resp_dict['@type'], 'Collection')

    def test_options_for_collection_resource_projection_operation_with_collect_operation(self):
        response = requests.options(self.controle_base_uri + "usuario-list/projection/nome,email/collect/nome&email/upper")
        self.assertEquals(response.status_code, 200)

        response_keys = self.aux_get_keys_from_response(response)
        self.assertEquals(response_keys, self.non_simple_path_dict_keys)

        supported_operations_names = self.aux_get_supported_operations_names(response)
        self.assertEquals(supported_operations_names, self.collection_operation_names)

        acontext_keys = self.aux_get_keys_from_response_context(response)
        self.assertEquals(acontext_keys, ['collect', 'email', 'nome', 'upper'])

        email_context_keys = self.aux_get_keys_from_acontext_attrs(response, 'email')
        self.assertEquals(email_context_keys, self.keys_from_attrs_context)
        nome_context_keys = self.aux_get_keys_from_acontext_attrs(response, 'nome')
        self.assertEquals(nome_context_keys, self.keys_from_attrs_context)
        collect_context_keys = self.aux_get_keys_from_acontext_attrs(response, 'collect')
        self.assertEquals(collect_context_keys, self.keys_from_oper_context)
        upper_context_keys = self.aux_get_keys_from_acontext_attrs(response, 'upper')
        self.assertEquals(upper_context_keys, self.keys_from_oper_context)

        response_dict = self.aux_get_dict_from_response(response)
        self.assertEquals(response_dict['@type'], "Collection")

    def test_options_for_collection_resource_projection_operation_with_collect_operation_projection_list_different_from_collect_list(self):
        response = requests.options(self.controle_base_uri + "usuario-list/projection/nome/collect/nome&email/upper")
        self.assertEquals(response.status_code, 400)

    def test_options_for_collection_resource_projection_operation_accept_octet_stream(self):
        implicit_projection_resp = requests.options(self.controle_base_uri + "usuario-list/nome,email",
                                                    headers={"Accept": "application/octet-stream"})
        self.assertEquals(implicit_projection_resp.status_code, 200)

        implicit_projection_resp_keys = self.aux_get_keys_from_response(implicit_projection_resp)
        self.assertEquals(implicit_projection_resp_keys, self.non_simple_path_dict_keys)

        f_supported_operations_names = self.aux_get_supported_operations_names(implicit_projection_resp)
        self.assertEquals(f_supported_operations_names, [])

        f_acontext_keys = self.aux_get_keys_from_response_context(implicit_projection_resp)
        self.assertEquals(f_acontext_keys, ['email', 'nome'])

        f_email_context_keys = self.aux_get_keys_from_acontext_attrs(implicit_projection_resp, 'email')
        self.assertEquals(f_email_context_keys, self.keys_from_attrs_context)
        f_nome_context_keys = self.aux_get_keys_from_acontext_attrs(implicit_projection_resp, 'nome')
        self.assertEquals(f_nome_context_keys, self.keys_from_attrs_context)

        f_resp_dict = self.aux_get_dict_from_response(implicit_projection_resp)
        self.assertEqual(f_resp_dict['@type'], 'bytes')

        # explicit projection
        explicit_projection_resp = requests.options(self.controle_base_uri + "usuario-list/projection/nome,email",
                                                    headers={"Accept": "application/octet-stream"})
        self.assertEquals(explicit_projection_resp.status_code, 200)

        explicit_projection_resp_keys = self.aux_get_keys_from_response(explicit_projection_resp)
        self.assertEquals(explicit_projection_resp_keys, self.non_simple_path_dict_keys)

        s_supported_operations_names = self.aux_get_supported_operations_names(explicit_projection_resp)
        self.assertEquals(s_supported_operations_names, [])

        s_acontext_keys = self.aux_get_keys_from_response_context(explicit_projection_resp)
        self.assertEquals(s_acontext_keys, ['email', 'nome', 'projection'])

        s_email_context_keys = self.aux_get_keys_from_acontext_attrs(explicit_projection_resp, 'email')
        self.assertEquals(s_email_context_keys, self.keys_from_attrs_context)
        s_nome_context_keys = self.aux_get_keys_from_acontext_attrs(explicit_projection_resp, 'nome')
        self.assertEquals(s_nome_context_keys, self.keys_from_attrs_context)
        s_projection_context_keys = self.aux_get_keys_from_acontext_attrs(explicit_projection_resp, 'projection')
        self.assertEquals(s_projection_context_keys, self.keys_from_oper_context)

        s_resp_dict = self.aux_get_dict_from_response(explicit_projection_resp)
        self.assertEqual(s_resp_dict['@type'], 'bytes')

    def test_options_for_collection_resource_projection_operation_with_collect_operation_accept_octet_stream(self):
        response = requests.options(self.controle_base_uri + "usuario-list/projection/nome,email/collect/nome&email/upper",
                                    headers={"Accept": "application/octet-stream"})
        self.assertEquals(response.status_code, 200)

        response_keys = self.aux_get_keys_from_response(response)
        self.assertEquals(response_keys, self.non_simple_path_dict_keys)

        supported_operations_names = self.aux_get_supported_operations_names(response)
        self.assertEquals(supported_operations_names, [])

        acontext_keys = self.aux_get_keys_from_response_context(response)
        self.assertEquals(acontext_keys, ['collect', 'email', 'nome', 'upper'])

        email_context_keys = self.aux_get_keys_from_acontext_attrs(response, 'email')
        self.assertEquals(email_context_keys, self.keys_from_attrs_context)
        nome_context_keys = self.aux_get_keys_from_acontext_attrs(response, 'nome')
        self.assertEquals(nome_context_keys, self.keys_from_attrs_context)
        collect_context_keys = self.aux_get_keys_from_acontext_attrs(response, 'collect')
        self.assertEquals(collect_context_keys, self.keys_from_oper_context)
        upper_context_keys = self.aux_get_keys_from_acontext_attrs(response, 'upper')
        self.assertEquals(upper_context_keys, self.keys_from_oper_context)

        response_dict = self.aux_get_dict_from_response(response)
        self.assertEquals(response_dict['@type'], "bytes")

    # --------------- TESTS FOR FEATURE COLLECTION ---------------------------------
    def test_options_for_feature_collection_projection_operation(self):
        implicit_projection_resp = requests.options(self.bcim_base_uri + "unidades-federativas/nome,geom")
        self.assertEquals(implicit_projection_resp.status_code, 200)

        implicit_projection_resp_keys = self.aux_get_keys_from_response(implicit_projection_resp)
        self.assertEquals(implicit_projection_resp_keys, self.non_simple_path_dict_keys)

        f_supported_operations_names = self.aux_get_supported_operations_names(implicit_projection_resp)
        self.assertEquals(f_supported_operations_names, self.spatial_collection_operation_names)

        f_acontext_keys = self.aux_get_keys_from_response_context(implicit_projection_resp)
        self.assertEquals(f_acontext_keys, ['geom', 'nome'])

        f_geom_context_keys = self.aux_get_keys_from_acontext_attrs(implicit_projection_resp, "geom")
        self.assertEquals(f_geom_context_keys, self.keys_from_attrs_context)
        nome_context_keys = self.aux_get_keys_from_acontext_attrs(implicit_projection_resp, "nome")
        self.assertEquals(nome_context_keys, self.keys_from_attrs_context)

        f_response_dict = self.aux_get_dict_from_response(implicit_projection_resp)
        self.assertEquals(f_response_dict['@type'], "FeatureCollection")

        # explicit projection
        explicit_projection_resp = requests.options(self.bcim_base_uri + "unidades-federativas/projection/nome,geom")
        self.assertEquals(explicit_projection_resp.status_code, 200)

        explicit_projection_resp_keys = self.aux_get_keys_from_response(explicit_projection_resp)
        self.assertEquals(explicit_projection_resp_keys, self.non_simple_path_dict_keys)

        s_supported_operations_names = self.aux_get_supported_operations_names(explicit_projection_resp)
        self.assertEquals(s_supported_operations_names, self.spatial_collection_operation_names)

        s_acontext_keys = self.aux_get_keys_from_response_context(explicit_projection_resp)
        self.assertEquals(s_acontext_keys, ['geom', 'nome', 'projection'])

        s_geom_context_keys = self.aux_get_keys_from_acontext_attrs(explicit_projection_resp, "geom")
        self.assertEquals(s_geom_context_keys, self.keys_from_attrs_context)
        s_nome_context_keys = self.aux_get_keys_from_acontext_attrs(explicit_projection_resp, "nome")
        self.assertEquals(s_nome_context_keys, self.keys_from_attrs_context)
        s_projection_context_keys = self.aux_get_keys_from_acontext_attrs(explicit_projection_resp, "projection")
        self.assertEquals(s_projection_context_keys, self.keys_from_oper_context)

        s_response_dict = self.aux_get_dict_from_response(explicit_projection_resp)
        self.assertEquals(s_response_dict['@type'], "FeatureCollection")

    def test_options_for_feature_collection_projection_operation_only_geometric_attribute(self):
        implicit_projection_resp = requests.options(self.bcim_base_uri + "unidades-federativas/geom")
        self.assertEquals(implicit_projection_resp.status_code, 200)

        implicit_projection_resp_keys = self.aux_get_keys_from_response(implicit_projection_resp)
        self.assertEquals(implicit_projection_resp_keys, self.non_simple_path_dict_keys)

        f_supported_operations_names = self.aux_get_supported_operations_names(implicit_projection_resp)
        self.assertEquals(f_supported_operations_names, self.spatial_collection_operation_names)

        f_acontext_keys = self.aux_get_keys_from_response_context(implicit_projection_resp)
        self.assertEquals(f_acontext_keys, ['geom'])

        f_geom_context_keys = self.aux_get_keys_from_acontext_attrs(implicit_projection_resp, "geom")
        self.assertEquals(f_geom_context_keys, self.keys_from_attrs_context)

        f_response_dict = self.aux_get_dict_from_response(implicit_projection_resp)
        self.assertEquals(f_response_dict['@type'], "GeometryCollection")

        # explicit projection
        explicit_projection_resp = requests.options(self.bcim_base_uri + "unidades-federativas/projection/geom")
        self.assertEquals(explicit_projection_resp.status_code, 200)

        explicit_projection_resp_keys = self.aux_get_keys_from_response(explicit_projection_resp)
        self.assertEquals(explicit_projection_resp_keys, self.non_simple_path_dict_keys)

        s_supported_operations_names = self.aux_get_supported_operations_names(explicit_projection_resp)
        self.assertEquals(s_supported_operations_names, self.spatial_collection_operation_names)

        s_acontext_keys = self.aux_get_keys_from_response_context(explicit_projection_resp)
        self.assertEquals(s_acontext_keys, ['geom', 'projection'])

        s_geom_context_keys = self.aux_get_keys_from_acontext_attrs(explicit_projection_resp, "geom")
        self.assertEquals(s_geom_context_keys, self.keys_from_attrs_context)
        s_projection_context_keys = self.aux_get_keys_from_acontext_attrs(explicit_projection_resp, "projection")
        self.assertEquals(s_projection_context_keys, self.keys_from_oper_context)

        s_response_dict = self.aux_get_dict_from_response(explicit_projection_resp)
        self.assertEquals(s_response_dict['@type'], "GeometryCollection")

    def test_options_for_feature_collection_projection_operation_only_alphanumeric_attributes(self):
        implicit_projection_resp = requests.options(self.bcim_base_uri + "unidades-federativas/nome")
        self.assertEquals(implicit_projection_resp.status_code, 200)

        implicit_projection_resp_keys = self.aux_get_keys_from_response(implicit_projection_resp)
        self.assertEquals(implicit_projection_resp_keys, self.non_simple_path_dict_keys)

        f_supported_operations_names = self.aux_get_supported_operations_names(implicit_projection_resp)
        self.assertEquals(f_supported_operations_names, self.collection_operation_names)

        f_acontext_keys = self.aux_get_keys_from_response_context(implicit_projection_resp)
        self.assertEquals(f_acontext_keys, ['nome'])

        nome_context_keys = self.aux_get_keys_from_acontext_attrs(implicit_projection_resp, "nome")
        self.assertEquals(nome_context_keys, self.keys_from_attrs_context)

        f_response_dict = self.aux_get_dict_from_response(implicit_projection_resp)
        self.assertEquals(f_response_dict['@type'], "Collection")

        # explicit projection
        explicit_projection_resp = requests.options(self.bcim_base_uri + "unidades-federativas/projection/nome")
        self.assertEquals(explicit_projection_resp.status_code, 200)

        explicit_projection_resp_keys = self.aux_get_keys_from_response(explicit_projection_resp)
        self.assertEquals(explicit_projection_resp_keys, self.non_simple_path_dict_keys)

        s_supported_operations_names = self.aux_get_supported_operations_names(explicit_projection_resp)
        self.assertEquals(s_supported_operations_names, self.collection_operation_names)

        s_acontext_keys = self.aux_get_keys_from_response_context(explicit_projection_resp)
        self.assertEquals(s_acontext_keys, ['nome', 'projection'])

        s_nome_context_keys = self.aux_get_keys_from_acontext_attrs(explicit_projection_resp, "nome")
        self.assertEquals(s_nome_context_keys, self.keys_from_attrs_context)
        s_projection_context_keys = self.aux_get_keys_from_acontext_attrs(explicit_projection_resp, "projection")
        self.assertEquals(s_projection_context_keys, self.keys_from_oper_context)

        s_response_dict = self.aux_get_dict_from_response(explicit_projection_resp)
        self.assertEquals(s_response_dict['@type'], "Collection")

    def test_options_for_feature_collection_projection_operation_with_collect_operation(self):
        response = requests.options(self.bcim_base_uri + "unidades-federativas/projection/nome,geom/collect/nome&geom/buffer/0.2")
        self.assertEquals(response.status_code, 200)

        response_keys = self.aux_get_keys_from_response(response)
        self.assertEquals(response_keys, self.non_simple_path_dict_keys)

        supported_operations_names = self.aux_get_supported_operations_names(response)
        self.assertEquals(supported_operations_names, self.spatial_collection_operation_names)

        acontext_keys = self.aux_get_keys_from_response_context(response)
        self.assertEquals(acontext_keys, ['buffer', 'collect', 'geom', 'nome'])

        nome_context_keys = self.aux_get_keys_from_acontext_attrs(response, "nome")
        self.assertEquals(nome_context_keys, self.keys_from_attrs_context)
        geom_context_keys = self.aux_get_keys_from_acontext_attrs(response, "geom")
        self.assertEquals(geom_context_keys, self.keys_from_attrs_context)
        collect_context_keys = self.aux_get_keys_from_acontext_attrs(response, "collect")
        self.assertEquals(collect_context_keys, self.keys_from_oper_context)
        buffer_context_keys = self.aux_get_keys_from_acontext_attrs(response, "buffer")
        self.assertEquals(buffer_context_keys, self.keys_from_oper_context)

        response_dict = self.aux_get_dict_from_response(response)
        self.assertEquals(response_dict['@type'], "FeatureCollection")

    def test_options_for_feature_collection_projection_operation_with_collect_operation_projection_list_different_from_collect_list(self):
        response = requests.options(self.bcim_base_uri + "unidades-federativas/projection/nome,geom/collect/geom/buffer/0.2")
        self.assertEquals(response.status_code, 400)

    # Accept: application/octet-stream
    def test_options_for_feature_collection_projection_operation_accept_octet_stream(self):
        implicit_projection_resp = requests.options(self.bcim_base_uri + "unidades-federativas/nome,geom",
                                                    headers={"Accept": "application/octet-stream"})
        self.assertEquals(implicit_projection_resp.status_code, 200)

        implicit_projection_resp_keys = self.aux_get_keys_from_response(implicit_projection_resp)
        self.assertEquals(implicit_projection_resp_keys, self.non_simple_path_dict_keys)

        f_supported_operations_names = self.aux_get_supported_operations_names(implicit_projection_resp)
        self.assertEquals(f_supported_operations_names, self.spatial_collection_operation_names)

        f_acontext_keys = self.aux_get_keys_from_response_context(implicit_projection_resp)
        self.assertEquals(f_acontext_keys, ['geom', 'nome'])

        f_geom_context_keys = self.aux_get_keys_from_acontext_attrs(implicit_projection_resp, "geom")
        self.assertEquals(f_geom_context_keys, self.keys_from_attrs_context)
        nome_context_keys = self.aux_get_keys_from_acontext_attrs(implicit_projection_resp, "nome")
        self.assertEquals(nome_context_keys, self.keys_from_attrs_context)

        f_response_dict = self.aux_get_dict_from_response(implicit_projection_resp)
        self.assertEquals(f_response_dict['@type'], "GeobufCollection")

        #explicit projection
        explicit_projection_resp = requests.options(self.bcim_base_uri + "unidades-federativas/projection/nome,geom",
                                                    headers={"Accept": "application/octet-stream"})
        self.assertEquals(explicit_projection_resp.status_code, 200)

        explicit_projection_resp_keys = self.aux_get_keys_from_response(explicit_projection_resp)
        self.assertEquals(explicit_projection_resp_keys, self.non_simple_path_dict_keys)

        s_supported_operations_names = self.aux_get_supported_operations_names(explicit_projection_resp)
        self.assertEquals(s_supported_operations_names, self.spatial_collection_operation_names)

        s_acontext_keys = self.aux_get_keys_from_response_context(explicit_projection_resp)
        self.assertEquals(s_acontext_keys, ['geom', 'nome', 'projection'])

        s_geom_context_keys = self.aux_get_keys_from_acontext_attrs(explicit_projection_resp, "geom")
        self.assertEquals(s_geom_context_keys, self.keys_from_attrs_context)
        s_nome_context_keys = self.aux_get_keys_from_acontext_attrs(explicit_projection_resp, "nome")
        self.assertEquals(s_nome_context_keys, self.keys_from_attrs_context)
        s_projection_context_keys = self.aux_get_keys_from_acontext_attrs(explicit_projection_resp, "projection")
        self.assertEquals(s_projection_context_keys, self.keys_from_oper_context)

        s_response_dict = self.aux_get_dict_from_response(explicit_projection_resp)
        self.assertEquals(s_response_dict['@type'], "GeobufCollection")

    def test_options_for_feature_collection_projection_operation_only_geometric_attribute_accept_octet_stream(self):
        implicit_projection_resp = requests.options(self.bcim_base_uri + "unidades-federativas/geom",
                                                    headers={"Accept": "application/octet-stream"})
        self.assertEquals(implicit_projection_resp.status_code, 200)

        implicit_projection_resp_keys = self.aux_get_keys_from_response(implicit_projection_resp)
        self.assertEquals(implicit_projection_resp_keys, self.non_simple_path_dict_keys)

        f_supported_operations_names = self.aux_get_supported_operations_names(implicit_projection_resp)
        self.assertEquals(f_supported_operations_names, self.spatial_collection_operation_names)

        f_acontext_keys = self.aux_get_keys_from_response_context(implicit_projection_resp)
        self.assertEquals(f_acontext_keys, ['geom'])

        f_geom_context_keys = self.aux_get_keys_from_acontext_attrs(implicit_projection_resp, "geom")
        self.assertEquals(f_geom_context_keys, self.keys_from_attrs_context)

        f_response_dict = self.aux_get_dict_from_response(implicit_projection_resp)
        self.assertEquals(f_response_dict['@type'], "GeobufCollection")

        # explicit projection
        explicit_projection_resp = requests.options(self.bcim_base_uri + "unidades-federativas/projection/geom",
                                                    headers={"Accept": "application/octet-stream"})
        self.assertEquals(explicit_projection_resp.status_code, 200)

        explicit_projection_resp_keys = self.aux_get_keys_from_response(explicit_projection_resp)
        self.assertEquals(explicit_projection_resp_keys, self.non_simple_path_dict_keys)

        s_supported_operations_names = self.aux_get_supported_operations_names(explicit_projection_resp)
        self.assertEquals(s_supported_operations_names, self.spatial_collection_operation_names)

        s_acontext_keys = self.aux_get_keys_from_response_context(explicit_projection_resp)
        self.assertEquals(s_acontext_keys, ['geom', 'projection'])

        s_geom_context_keys = self.aux_get_keys_from_acontext_attrs(explicit_projection_resp, "geom")
        self.assertEquals(s_geom_context_keys, self.keys_from_attrs_context)
        s_projection_context_keys = self.aux_get_keys_from_acontext_attrs(explicit_projection_resp, "projection")
        self.assertEquals(s_projection_context_keys, self.keys_from_oper_context)

        s_response_dict = self.aux_get_dict_from_response(explicit_projection_resp)
        self.assertEquals(s_response_dict['@type'], "GeobufCollection")

    def test_options_for_feature_collection_projection_operation_only_alphanumeric_attributes_accept_octet_stream(self):
        implicit_projection_resp = requests.options(self.bcim_base_uri + "unidades-federativas/nome",
                                                    headers={"Accept": "application/octet-stream"})
        self.assertEquals(implicit_projection_resp.status_code, 200)

        implicit_projection_resp_keys = self.aux_get_keys_from_response(implicit_projection_resp)
        self.assertEquals(implicit_projection_resp_keys, self.non_simple_path_dict_keys)

        f_supported_operations_names = self.aux_get_supported_operations_names(implicit_projection_resp)
        self.assertEquals(f_supported_operations_names, [])

        f_acontext_keys = self.aux_get_keys_from_response_context(implicit_projection_resp)
        self.assertEquals(f_acontext_keys, ['nome'])

        f_nome_context_keys = self.aux_get_keys_from_acontext_attrs(implicit_projection_resp, "nome")
        self.assertEquals(f_nome_context_keys, self.keys_from_attrs_context)

        f_response_dict = self.aux_get_dict_from_response(implicit_projection_resp)
        self.assertEquals(f_response_dict['@type'], "bytes")

        # explicit projection
        explicit_projection_resp = requests.options(self.bcim_base_uri + "unidades-federativas/projection/nome",
                                                    headers={"Accept": "application/octet-stream"})
        self.assertEquals(explicit_projection_resp.status_code, 200)

        explicit_projection_resp_keys = self.aux_get_keys_from_response(explicit_projection_resp)
        self.assertEquals(explicit_projection_resp_keys, self.non_simple_path_dict_keys)

        s_supported_operations_names = self.aux_get_supported_operations_names(explicit_projection_resp)
        self.assertEquals(s_supported_operations_names, [])

        s_acontext_keys = self.aux_get_keys_from_response_context(explicit_projection_resp)
        self.assertEquals(s_acontext_keys, ['nome', 'projection'])

        s_nome_context_keys = self.aux_get_keys_from_acontext_attrs(explicit_projection_resp, "nome")
        self.assertEquals(s_nome_context_keys, self.keys_from_attrs_context)
        s_projection_context_keys = self.aux_get_keys_from_acontext_attrs(explicit_projection_resp, "projection")
        self.assertEquals(s_projection_context_keys, self.keys_from_oper_context)

        s_response_dict = self.aux_get_dict_from_response(explicit_projection_resp)
        self.assertEquals(s_response_dict['@type'], "bytes")

    def test_options_for_feature_collection_projection_operation_with_collect_operation_accept_octet_stream(self):
        response = requests.options(self.bcim_base_uri + "unidades-federativas/projection/nome,geom/collect/nome&geom/buffer/0.2",
                                    headers={"Accept": "application/octet-stream"})
        self.assertEquals(response.status_code, 200)

        response_keys = self.aux_get_keys_from_response(response)
        self.assertEquals(response_keys, self.non_simple_path_dict_keys)

        supported_operations_names = self.aux_get_supported_operations_names(response)
        self.assertEquals(supported_operations_names, self.spatial_collection_operation_names)

        acontext_keys = self.aux_get_keys_from_response_context(response)
        self.assertEquals(acontext_keys, ['buffer', 'collect', 'geom', 'nome'])

        nome_context_keys = self.aux_get_keys_from_acontext_attrs(response, "nome")
        self.assertEquals(nome_context_keys, self.keys_from_attrs_context)
        geom_context_keys = self.aux_get_keys_from_acontext_attrs(response, "geom")
        self.assertEquals(geom_context_keys, self.keys_from_attrs_context)
        collect_context_keys = self.aux_get_keys_from_acontext_attrs(response, "collect")
        self.assertEquals(collect_context_keys, self.keys_from_oper_context)
        buffer_context_keys = self.aux_get_keys_from_acontext_attrs(response, "buffer")
        self.assertEquals(buffer_context_keys, self.keys_from_oper_context)

        response_dict = self.aux_get_dict_from_response(response)
        self.assertEquals(response_dict['@type'], "GeobufCollection")

#python manage.py test hyper_resource.tests.FilterOperationTest --testrunner=hyper_resource.tests.NoDbTestRunner
class FilterOperationTest(AbstractRequestTest):

    def aux_get_attributes_from_features(self, response, attribute_name):
        response_dict = self.aux_get_dict_from_response(response)
        attrs_arr = [feature['properties'][attribute_name] for feature in response_dict['features'] ]
        return sorted(attrs_arr)

    def test_simple_filter(self):
        response = requests.get(self.bcim_base_uri + "unidades-federativas/filter/geocodigo/eq/22/")
        self.assertEquals(response.status_code, 200)

        names_list = self.aux_get_attributes_from_features(response, "nome")
        self.assertEquals(names_list, ["Piauí"])

    def test_filter_with_or_operator(self):
        # Maranhão = 21
        # Piauí = 22
        response = requests.get(self.bcim_base_uri + "unidades-federativas/filter/geocodigo/eq/22/or/nome/eq/Maranhão/")
        self.assertEquals(response.status_code, 200)

        names_list = self.aux_get_attributes_from_features(response, "nome")
        self.assertEquals(names_list, ["Maranhão", "Piauí"])

    def test_filter_with_and_operator(self):
        # Maranhão = 21
        # Piauí = 22
        response = requests.get(self.bcim_base_uri + "unidades-federativas/filter/geocodigo/eq/22/and/nome/eq/Maranhão/")
        self.assertEquals(response.status_code, 200)

        names_list = self.aux_get_attributes_from_features(response, "nome")
        self.assertEquals(names_list, [])

    # WARNING: This test don't pass and this problem must be solved by the url interpretor
    def test_precedence_between_AND_operator_and_OR_operator(self):
        '''
        Independent of which order you put AND or OR operator, the result must be the same
        (AND operator is always be the first to be considered)
        # Maranhão = 21
        # Piauí = 22
        '''
        response = requests.get(self.bcim_base_uri + "unidades-federativas/filter/geocodigo/eq/22/or/nome/eq/Maranhão/and/geocodigo/eq/21/")
        self.assertEquals(response.status_code, 200)

        names_list = self.aux_get_attributes_from_features(response, "nome")
        self.assertEquals(names_list, ["Maranhão", "Piauí"])

        response = requests.get(self.bcim_base_uri + "unidades-federativas/filter/nome/eq/Maranhão/and/geocodigo/eq/21/or/geocodigo/eq/22/")
        self.assertEquals(response.status_code, 200)

        names_list = self.aux_get_attributes_from_features(response, "nome")
        self.assertEquals(names_list, ["Maranhão", "Piauí"])

#python manage.py test hyper_resource.tests.RequestOptionsTest --testrunner=hyper_resource.tests.NoDbTestRunner
class RequestOptionsTest(AbstractRequestTest):

    # --------------- TESTS FOR FEATURE COLLECTION ---------------------------------
    # tests for feature/geometry collection simple path
    def test_options_for_feature_collection_simple_path(self):
        response = requests.options(self.bcim_base_uri + "aldeias-indigenas/")
        self.assertEquals(response.status_code, 200)

        response_keys = self.aux_get_keys_from_response(response)
        self.assertListEqual(response_keys, self.simple_path_options_dict_keys)

        id_objeto_context_keys_list = self.aux_get_keys_from_acontext_attrs(response, "id_objeto")
        self.assertListEqual(id_objeto_context_keys_list, self.keys_from_attrs_context)
        nome_context_keys_list = self.aux_get_keys_from_acontext_attrs(response, "nome")
        self.assertListEqual(nome_context_keys_list, self.keys_from_attrs_context)
        nomeabrev_context_keys_list = self.aux_get_keys_from_acontext_attrs(response, "nomeabrev")
        self.assertListEqual(nomeabrev_context_keys_list, self.keys_from_attrs_context)
        geometriaaproximada_context_keys_list = self.aux_get_keys_from_acontext_attrs(response, "geometriaaproximada")
        self.assertListEqual(geometriaaproximada_context_keys_list, self.keys_from_attrs_context)
        codigofunai_context_keys_list = self.aux_get_keys_from_acontext_attrs(response, "codigofunai")
        self.assertListEqual(codigofunai_context_keys_list, self.keys_from_attrs_context)
        terraindigena_context_keys_list = self.aux_get_keys_from_acontext_attrs(response, "terraindigena")
        self.assertListEqual(terraindigena_context_keys_list, self.keys_from_attrs_context)
        etnia_context_keys_list = self.aux_get_keys_from_acontext_attrs(response, "etnia")
        self.assertListEqual(etnia_context_keys_list, self.keys_from_attrs_context)
        geom_context_keys_list = self.aux_get_keys_from_acontext_attrs(response, "geom")
        self.assertListEqual(geom_context_keys_list, self.keys_from_attrs_context)

        operations_names = self.aux_get_supported_operations_names(response)
        self.assertListEqual(operations_names, self.spatial_collection_operation_names)

        response_dict = self.aux_get_dict_from_response(response)
        self.assertEquals(response_dict["@type"], 'FeatureCollection')

    def test_options_for_feature_collection_simple_path_with_accept_header(self):
        response = requests.options(self.bcim_base_uri + "aldeias-indigenas/", headers={'accept': 'application/octet-stream'})
        self.assertEquals(response.status_code, 200)

        response_keys = self.aux_get_keys_from_response(response)
        self.assertListEqual(response_keys, self.simple_path_options_dict_keys)

        id_objeto_context_keys_list = self.aux_get_keys_from_acontext_attrs(response, "id_objeto")
        self.assertListEqual(id_objeto_context_keys_list, self.keys_from_attrs_context)
        nome_context_keys_list = self.aux_get_keys_from_acontext_attrs(response, "nome")
        self.assertListEqual(nome_context_keys_list, self.keys_from_attrs_context)
        nomeabrev_context_keys_list = self.aux_get_keys_from_acontext_attrs(response, "nomeabrev")
        self.assertListEqual(nomeabrev_context_keys_list, self.keys_from_attrs_context)
        geometriaaproximada_context_keys_list = self.aux_get_keys_from_acontext_attrs(response, "geometriaaproximada")
        self.assertListEqual(geometriaaproximada_context_keys_list, self.keys_from_attrs_context)
        codigofunai_context_keys_list = self.aux_get_keys_from_acontext_attrs(response, "codigofunai")
        self.assertListEqual(codigofunai_context_keys_list, self.keys_from_attrs_context)
        terraindigena_context_keys_list = self.aux_get_keys_from_acontext_attrs(response, "terraindigena")
        self.assertListEqual(terraindigena_context_keys_list, self.keys_from_attrs_context)
        etnia_context_keys_list = self.aux_get_keys_from_acontext_attrs(response, "etnia")
        self.assertListEqual(etnia_context_keys_list, self.keys_from_attrs_context)
        geom_context_keys_list = self.aux_get_keys_from_acontext_attrs(response, "geom")
        self.assertListEqual(geom_context_keys_list, self.keys_from_attrs_context)

        operations_names = self.aux_get_supported_operations_names(response)
        self.assertListEqual(operations_names, self.spatial_collection_operation_names)

        response_dict = self.aux_get_dict_from_response(response)
        self.assertEquals(response_dict["@type"], 'GeobufCollection')


    # tests for feature/geometry collection attributes
    def test_options_for_feature_collection_only_attributes(self):
        attrs = ["geom", "nome"]
        response = requests.options(self.bcim_base_uri + "aldeias-indigenas/" + attrs[0] + "," + attrs[1])
        self.assertEquals(response.status_code, 200)

        response_dict_keys = self.aux_get_keys_from_response(response)
        self.assertListEqual(response_dict_keys, self.non_simple_path_dict_keys)

        context_keys = self.aux_get_keys_from_response_context(response)
        self.assertListEqual(context_keys, attrs)

        nome_context_keys_list = self.aux_get_keys_from_acontext_attrs(response, "nome")
        self.assertListEqual(nome_context_keys_list, self.keys_from_attrs_context)
        geom_context_keys_list = self.aux_get_keys_from_acontext_attrs(response, "geom")
        self.assertListEqual(geom_context_keys_list, self.keys_from_attrs_context)

        operations_names = self.aux_get_supported_operations_names(response)
        self.assertListEqual(operations_names, self.spatial_collection_operation_names)

        response_dict = self.aux_get_dict_from_response(response)
        self.assertEquals(response_dict["@type"], 'FeatureCollection')

    def test_options_for_feature_collection_only_attributes_with_accept_header(self):
        attrs = ["geom", "nome"]
        response = requests.options(self.bcim_base_uri + "aldeias-indigenas/" + attrs[0] + "," + attrs[1],
                                    headers={'accept': 'application/octet-stream'})
        self.assertEquals(response.status_code, 200)

        response_dict_keys = self.aux_get_keys_from_response(response)
        self.assertListEqual(response_dict_keys, self.non_simple_path_dict_keys)

        context_keys = self.aux_get_keys_from_response_context(response)
        self.assertListEqual(context_keys, attrs)

        nome_context_keys_list = self.aux_get_keys_from_acontext_attrs(response, "nome")
        self.assertListEqual(nome_context_keys_list, self.keys_from_attrs_context)
        geom_context_keys_list = self.aux_get_keys_from_acontext_attrs(response, "geom")
        self.assertListEqual(geom_context_keys_list, self.keys_from_attrs_context)

        operations_names = self.aux_get_supported_operations_names(response)
        self.assertListEqual(operations_names, self.spatial_collection_operation_names)

        response_dict = self.aux_get_dict_from_response(response)
        self.assertEquals(response_dict["@type"], 'GeobufCollection')

    def test_options_for_feature_collection_only_geometric_attribute(self):
        attrs = ["geom"]
        response = requests.options(self.bcim_base_uri + "aldeias-indigenas/" + attrs[0])
        self.assertEquals(response.status_code, 200)

        response_dict_keys = self.aux_get_keys_from_response(response)
        self.assertListEqual(response_dict_keys, self.non_simple_path_dict_keys)

        acontext_keys = self.aux_get_keys_from_response_context(response)
        self.assertListEqual(acontext_keys, attrs)

        geom_context_keys_list = self.aux_get_keys_from_acontext_attrs(response, "geom")
        self.assertListEqual(geom_context_keys_list, self.keys_from_attrs_context)

        operations_names = self.aux_get_supported_operations_names(response)
        self.assertListEqual(operations_names, self.spatial_collection_operation_names)

        response_dict = self.aux_get_dict_from_response(response)
        self.assertEquals(response_dict["@type"], 'GeometryCollection')

    def test_options_for_feature_collection_only_geometric_attribute_accept_header(self):
        attrs = ["geom"]
        response = requests.options(self.bcim_base_uri + "aldeias-indigenas/" + attrs[0],
                                    headers={'accept': 'application/octet-stream'})
        self.assertEquals(response.status_code, 200)

        response_dict_keys = self.aux_get_keys_from_response(response)
        self.assertListEqual(response_dict_keys, self.non_simple_path_dict_keys)

        context_keys = self.aux_get_keys_from_response_context(response)
        self.assertListEqual(context_keys, attrs)

        geom_context_keys_list = self.aux_get_keys_from_acontext_attrs(response, "geom")
        self.assertListEqual(geom_context_keys_list, self.keys_from_attrs_context)

        operations_names = self.aux_get_supported_operations_names(response)
        self.assertListEqual(operations_names, self.spatial_collection_operation_names)

        response_dict = self.aux_get_dict_from_response(response)
        self.assertEquals(response_dict["@type"], 'GeobufCollection')

    def test_options_for_feature_collection_only_alphanumeric_attributes(self):
        alpha_attrs = ["nome", "nomeabrev"]
        response = requests.options(self.bcim_base_uri + "aldeias-indigenas/" + alpha_attrs[0] + "," + alpha_attrs[1])
        self.assertEquals(response.status_code, 200)

        response_dict_keys = self.aux_get_keys_from_response(response)
        self.assertListEqual(response_dict_keys, self.non_simple_path_dict_keys)

        context_dict_keys = self.aux_get_keys_from_response_context(response)
        self.assertListEqual(context_dict_keys, alpha_attrs)

        nome_context_keys_list = self.aux_get_keys_from_acontext_attrs(response, "nome")
        self.assertListEqual(nome_context_keys_list, self.keys_from_attrs_context)
        nomeabrev_context_keys_list = self.aux_get_keys_from_acontext_attrs(response, "nomeabrev")
        self.assertListEqual(nomeabrev_context_keys_list, self.keys_from_attrs_context)

        operations_names = self.aux_get_supported_operations_names(response)
        self.assertListEqual(operations_names, self.collection_operation_names)

        response_dict = self.aux_get_dict_from_response(response)
        self.assertEquals(response_dict["@type"], 'Collection')

    def test_options_for_feature_collection_only_alphanumeric_attributes_with_accept_header(self):
        alpha_attrs = ["nome", "nomeabrev"]
        response = requests.options(self.bcim_base_uri + "aldeias-indigenas/" + alpha_attrs[0] + "," + alpha_attrs[1],
                                    headers={'accept': 'application/octet-stream'})
        self.assertEquals(response.status_code, 200)

        response_dict_keys = self.aux_get_keys_from_response(response)
        self.assertListEqual(response_dict_keys, self.non_simple_path_dict_keys)

        context_dict_keys = self.aux_get_keys_from_response_context(response)
        self.assertListEqual(context_dict_keys, alpha_attrs)

        nome_context_keys_list = self.aux_get_keys_from_acontext_attrs(response, "nome")
        self.assertListEqual(nome_context_keys_list, self.keys_from_attrs_context)
        nomeabrev_context_keys_list = self.aux_get_keys_from_acontext_attrs(response, "nomeabrev")
        self.assertListEqual(nomeabrev_context_keys_list, self.keys_from_attrs_context)

        operations_names = self.aux_get_supported_operations_names(response)
        self.assertListEqual(operations_names, [])

        response_dict = self.aux_get_dict_from_response(response)
        self.assertEquals(response_dict["@type"], 'bytes')


    # tests for feature/geometry collection operation
    def test_options_for_feature_collection_operation_with_geometry_collection_return(self):
        response = requests.options(self.bcim_base_uri + "aldeias-indigenas/within/" + self.bcim_base_uri + "unidades-federativas/ES")
        self.assertEquals(response.status_code, 200)

        response_dict_keys = self.aux_get_keys_from_response(response)
        self.assertListEqual(response_dict_keys, self.non_simple_path_dict_keys)

        context_dict_keys = self.aux_get_keys_from_response_context(response)
        self.assertListEqual(context_dict_keys, ['within'])

        within_context_keys_list = self.aux_get_keys_from_acontext_attrs(response, "within")
        self.assertListEqual(within_context_keys_list, ["@id", "@type"])

        supported_operation_names = self.aux_get_supported_operations_names(response)
        self.assertEquals(supported_operation_names, self.spatial_collection_operation_names)

        response_dict = self.aux_get_dict_from_response(response)
        self.assertEquals(response_dict["@type"], 'FeatureCollection')

    def test_options_for_feature_collection_operation_with_geometry_collection_return_and_accept_header(self):
        response = requests.options(
            self.bcim_base_uri + "aldeias-indigenas/within/" + self.bcim_base_uri + "unidades-federativas/ES",
            headers={'accept': 'application/octet-stream'}
        )
        self.assertEquals(response.status_code, 200)

        response_dict_keys = self.aux_get_keys_from_response(response)
        self.assertListEqual(response_dict_keys, self.non_simple_path_dict_keys)

        context_dict_keys = self.aux_get_keys_from_response_context(response)
        self.assertListEqual(context_dict_keys, ['within'])

        within_context_keys_list = self.aux_get_keys_from_acontext_attrs(response, "within")
        self.assertListEqual(within_context_keys_list, ["@id", "@type"])

        supp_oper_for_ret_type = self.aux_get_supported_operations_names(response)
        self.assertEquals(supp_oper_for_ret_type, self.spatial_collection_operation_names)

        response_dict = self.aux_get_dict_from_response(response)
        self.assertEquals(response_dict["@type"], 'GeobufCollection')

    def test_options_for_feature_collection_count_resource(self):
        response = requests.options(self.bcim_base_uri + "aldeias-indigenas/count_resource")
        self.assertEquals(response.status_code, 200)

        response_dict_keys = self.aux_get_keys_from_response(response)
        self.assertListEqual(response_dict_keys, self.non_simple_path_dict_keys)

        supported_operations_names = self.aux_get_supported_operations_names(response)
        self.assertEquals(supported_operations_names, [])

        context_dict_keys = self.aux_get_keys_from_response_context(response)
        self.assertListEqual(context_dict_keys, ['count_resource'])

        count_resource_context_keys_list = self.aux_get_keys_from_acontext_attrs(response, "count_resource")
        self.assertListEqual(count_resource_context_keys_list, ["@id", "@type"])

        response_dict = self.aux_get_dict_from_response(response)
        self.assertEquals(response_dict["@type"], 'int')

    def test_options_for_feature_collection_count_resource_accept_octet_stream(self):
        response = requests.options(self.bcim_base_uri + "aldeias-indigenas/count_resource",
                                    headers={'accept': 'application/octet-stream'})
        self.assertEquals(response.status_code, 200)

        response_dict_keys = self.aux_get_keys_from_response(response)
        self.assertListEqual(response_dict_keys, self.non_simple_path_dict_keys)

        supported_operations_names = self.aux_get_supported_operations_names(response)
        self.assertEquals(supported_operations_names, [])

        context_dict_keys = self.aux_get_keys_from_response_context(response)
        self.assertListEqual(context_dict_keys, ['count_resource'])

        count_resource_context_keys_list = self.aux_get_keys_from_acontext_attrs(response, "count_resource")
        self.assertListEqual(count_resource_context_keys_list, ["@id", "@type"])

        response_dict = self.aux_get_dict_from_response(response)
        self.assertEquals(response_dict["@type"], 'bytes')


    # --------------- TESTS FOR COLLECTION ---------------------------------
    # tests for collection simple path
    def test_options_for_collection_simple_path(self):
        response = requests.options(self.controle_base_uri + 'gasto-list/')
        self.assertEquals(response.status_code, 200)

        response_keys = self.aux_get_keys_from_response(response)
        self.assertListEqual(response_keys, self.simple_path_options_dict_keys)

        id_context_keys_list = self.aux_get_keys_from_acontext_attrs(response, "id")
        self.assertListEqual(id_context_keys_list, self.keys_from_attrs_context)
        data_keys_list = self.aux_get_keys_from_acontext_attrs(response, "data")
        self.assertListEqual(data_keys_list, self.keys_from_attrs_context)
        tipo_gasto_context_keys_list = self.aux_get_keys_from_acontext_attrs(response, "tipo_gasto")
        self.assertListEqual(tipo_gasto_context_keys_list, self.keys_from_attrs_context)
        usuario_context_keys_list = self.aux_get_keys_from_acontext_attrs(response, "usuario")
        self.assertListEqual(usuario_context_keys_list, self.keys_from_attrs_context)
        valor_context_keys_list = self.aux_get_keys_from_acontext_attrs(response, "valor")
        self.assertListEqual(valor_context_keys_list, self.keys_from_attrs_context)

        operation_name = self.aux_get_supported_operations_names(response)
        self.assertListEqual(operation_name, self.collection_operation_names)

        response_dict = self.aux_get_dict_from_response(response)
        self.assertEquals(response_dict["@type"], 'Collection')

    def test_options_for_collection_simple_path_with_accept_header(self):
        response = requests.options(self.controle_base_uri + 'gasto-list/', headers={'accept': 'application/octet-stream'})
        self.assertEquals(response.status_code, 200)

        response_keys = self.aux_get_keys_from_response(response)
        self.assertListEqual(response_keys, self.simple_path_options_dict_keys)

        id_context_keys_list = self.aux_get_keys_from_acontext_attrs(response, "id")
        self.assertListEqual(id_context_keys_list, self.keys_from_attrs_context)
        data_keys_list = self.aux_get_keys_from_acontext_attrs(response, "data")
        self.assertListEqual(data_keys_list, self.keys_from_attrs_context)
        tipo_gasto_context_keys_list = self.aux_get_keys_from_acontext_attrs(response, "tipo_gasto")
        self.assertListEqual(tipo_gasto_context_keys_list, self.keys_from_attrs_context)
        usuario_context_keys_list = self.aux_get_keys_from_acontext_attrs(response, "usuario")
        self.assertListEqual(usuario_context_keys_list, self.keys_from_attrs_context)
        valor_context_keys_list = self.aux_get_keys_from_acontext_attrs(response, "valor")
        self.assertListEqual(valor_context_keys_list, self.keys_from_attrs_context)

        operation_name = self.aux_get_supported_operations_names(response)
        self.assertListEqual(operation_name, [])

        response_dict = self.aux_get_dict_from_response(response)
        self.assertEquals(response_dict["@type"], 'bytes')

    # tests for collection attributes
    def test_options_for_collection_only_attributes(self):
        response = requests.options(self.controle_base_uri + 'gasto-list/data,valor')
        self.assertEquals(response.status_code, 200)

        response_keys = self.aux_get_keys_from_response(response)
        self.assertListEqual(response_keys, self.non_simple_path_dict_keys)

        context_keys = self.aux_get_keys_from_response_context(response)
        self.assertListEqual(context_keys, ['data', 'valor'])

        data_context_keys_list = self.aux_get_keys_from_acontext_attrs(response, "data")
        self.assertListEqual(data_context_keys_list, self.keys_from_attrs_context)
        valor_context_keys_list = self.aux_get_keys_from_acontext_attrs(response, "valor")
        self.assertListEqual(valor_context_keys_list, self.keys_from_attrs_context)

        operation_names = self.aux_get_supported_operations_names(response)
        self.assertListEqual(operation_names, self.collection_operation_names)

        response_dict = self.aux_get_dict_from_response(response)
        self.assertEquals(response_dict["@type"], 'Collection')

    def test_options_for_collection_only_attributes_with_accept_header(self):
        attrs = ['data', 'valor']
        response = requests.options(self.controle_base_uri + 'gasto-list/' + attrs[0] + ',' + attrs[1],
                                    headers={'Accept': 'application/octet-stream'})
        self.assertEquals(response.status_code, 200)

        response_keys = self.aux_get_keys_from_response(response)
        self.assertListEqual(response_keys, self.non_simple_path_dict_keys)

        context_keys = self.aux_get_keys_from_response_context(response)
        self.assertListEqual(context_keys, attrs)

        data_context_keys_list = self.aux_get_keys_from_acontext_attrs(response, "data")
        self.assertListEqual(data_context_keys_list, self.keys_from_attrs_context)
        valor_context_keys_list = self.aux_get_keys_from_acontext_attrs(response, "valor")
        self.assertListEqual(valor_context_keys_list, self.keys_from_attrs_context)

        operation_names = self.aux_get_supported_operations_names(response)
        self.assertListEqual(operation_names, [])

        response_dict = self.aux_get_dict_from_response(response)
        self.assertEquals(response_dict["@type"], 'bytes')

    # tests for collection operation
    def test_options_for_collection_operation_with_collection_return(self):
        response = requests.options(self.controle_base_uri + 'usuario-list/group_by_count/nome')
        self.assertEquals(response.status_code, 200)

        response_keys = self.aux_get_keys_from_response(response)
        self.assertEquals(response_keys, self.non_simple_path_dict_keys)

        acontext_keys = self.aux_get_keys_from_response_context(response)
        self.assertEquals(acontext_keys, ['count', 'nome'])

        nome_context_keys = self.aux_get_keys_from_acontext_attrs(response, "nome")
        self.assertEquals(nome_context_keys, self.keys_from_attrs_context)
        count_context_keys = self.aux_get_keys_from_acontext_attrs(response, "count")
        self.assertEquals(count_context_keys, self.keys_from_attrs_context)

        supported_operations_names = self.aux_get_supported_operations_names(response)
        self.assertEquals(supported_operations_names, self.collection_operation_names)

        response_dict = self.aux_get_dict_from_response(response)
        self.assertEquals(response_dict['@type'], "Collection")

    def test_options_for_collection_operation_with_collection_return_and_accept_header(self):
        response = requests.options(self.controle_base_uri + 'usuario-list/group_by_count/nome',
                                headers={"Accept": "application/octet-stream"})
        self.assertEquals(response.status_code, 200)

        response_keys = self.aux_get_keys_from_response(response)
        self.assertEquals(response_keys, self.non_simple_path_dict_keys)

        acontext_keys = self.aux_get_keys_from_response_context(response)
        self.assertEquals(acontext_keys, ['count', 'nome'])

        nome_context_keys = self.aux_get_keys_from_acontext_attrs(response, "nome")
        self.assertEquals(nome_context_keys, self.keys_from_attrs_context)
        count_context_keys = self.aux_get_keys_from_acontext_attrs(response, "count")
        self.assertEquals(count_context_keys, self.keys_from_attrs_context)

        supported_operations_names = self.aux_get_supported_operations_names(response)
        self.assertEquals(supported_operations_names, [])

        response_dict = self.aux_get_dict_from_response(response)
        self.assertEquals(response_dict['@type'], "bytes")

    def test_options_for_collection_operation_with_integer_return(self):
        response = requests.options(self.controle_base_uri + 'usuario-list/count_resource')
        self.assertEquals(response.status_code, 200)

        response_keys = self.aux_get_keys_from_response(response)
        self.assertEquals(response_keys, self.non_simple_path_dict_keys)

        acontext_keys = self.aux_get_keys_from_response_context(response)
        self.assertEquals(acontext_keys, ['count_resource'])

        count_resource_context_keys = self.aux_get_keys_from_acontext_attrs(response, "count_resource")
        self.assertEquals(count_resource_context_keys, ['@id', '@type'])

        supported_operations_names = self.aux_get_supported_operations_names(response)
        self.assertEquals(supported_operations_names, [])

        response_dict = self.aux_get_dict_from_response(response)
        self.assertEquals(response_dict['@type'], "int")

    def test_options_for_collection_operation_with_integer_return_and_accept_header(self):
        response = requests.options(self.controle_base_uri + 'usuario-list/count_resource',
                                headers={"Accept": "application/octet-stream"})
        self.assertEquals(response.status_code, 200)

        response_keys = self.aux_get_keys_from_response(response)
        self.assertEquals(response_keys, self.non_simple_path_dict_keys)

        acontext_keys = self.aux_get_keys_from_response_context(response)
        self.assertEquals(acontext_keys, ['count_resource'])

        count_resource_context_keys = self.aux_get_keys_from_acontext_attrs(response, "count_resource")
        self.assertEquals(count_resource_context_keys, ['@id', '@type'])

        supported_operations_names = self.aux_get_supported_operations_names(response)
        self.assertEquals(supported_operations_names, [])

        response_dict = self.aux_get_dict_from_response(response)
        self.assertEquals(response_dict['@type'], "bytes")


    # --------------- TESTS FOR FEATURE RESOURCE ---------------------------------
    # tests for feature simple path
    def test_options_for_feature_resource_simple_path(self):
        response = requests.options(self.bcim_base_uri + 'unidades-federativas/ES')
        self.assertEquals(response.status_code, 200)

        response_dict_keys = self.aux_get_keys_from_response(response)
        self.assertListEqual(response_dict_keys, self.simple_path_options_dict_keys)

        acontext_keys = self.aux_get_keys_from_response_context(response)
        self.assertListEqual(acontext_keys, ['geocodigo', 'geom', 'geometriaaproximada', 'id_objeto', 'iri_metadata', 'iri_style', 'nome', 'nomeabrev', 'sigla'])

        id_objeto_context_keys_list = self.aux_get_keys_from_acontext_attrs(response, "id_objeto")
        self.assertListEqual(id_objeto_context_keys_list, self.keys_from_attrs_context)
        nome_context_keys_list = self.aux_get_keys_from_acontext_attrs(response, "nome")
        self.assertListEqual(nome_context_keys_list, self.keys_from_attrs_context)
        nomeabrev_context_keys_list = self.aux_get_keys_from_acontext_attrs(response, "nomeabrev")
        self.assertListEqual(nomeabrev_context_keys_list, self.keys_from_attrs_context)
        geometriaaproximada_context_keys_list = self.aux_get_keys_from_acontext_attrs(response, "geometriaaproximada")
        self.assertListEqual(geometriaaproximada_context_keys_list, self.keys_from_attrs_context)
        geocodigo_context_keys_list = self.aux_get_keys_from_acontext_attrs(response, "geocodigo")
        self.assertListEqual(geocodigo_context_keys_list, self.keys_from_attrs_context)
        sigla_context_keys_list = self.aux_get_keys_from_acontext_attrs(response, "sigla")
        self.assertListEqual(sigla_context_keys_list, self.keys_from_attrs_context)
        geom_context_keys_list = self.aux_get_keys_from_acontext_attrs(response, "geom")
        self.assertListEqual(geom_context_keys_list, self.keys_from_attrs_context)
        iri_metadata_context_keys_list = self.aux_get_keys_from_acontext_attrs(response, "iri_metadata")
        self.assertListEqual(iri_metadata_context_keys_list, self.keys_from_attrs_context)
        iri_style_context_keys_list = self.aux_get_keys_from_acontext_attrs(response, "iri_style")
        self.assertListEqual(iri_style_context_keys_list, self.keys_from_attrs_context)

        operations_names = self.aux_get_supported_operations_names(response)
        self.assertListEqual(operations_names, self.spatial_operation_names)

        response_dict = self.aux_get_dict_from_response(response)
        self.assertEquals(response_dict["@type"], 'Feature')

    def test_options_for_feature_resource_simple_path_with_accept_header(self):
        response = requests.options(self.bcim_base_uri + 'unidades-federativas/ES',
                                    headers={'accept': 'application/octet-stream'})
        self.assertEquals(response.status_code, 200)

        response_dict_keys = self.aux_get_keys_from_response(response)
        self.assertListEqual(response_dict_keys, self.simple_path_options_dict_keys)

        acontext_keys = self.aux_get_keys_from_response_context(response)
        self.assertListEqual(acontext_keys, ['geocodigo', 'geom', 'geometriaaproximada', 'id_objeto', 'iri_metadata', 'iri_style', 'nome', 'nomeabrev', 'sigla'])

        id_objeto_context_keys_list = self.aux_get_keys_from_acontext_attrs(response, "id_objeto")
        self.assertListEqual(id_objeto_context_keys_list, self.keys_from_attrs_context)
        nome_context_keys_list = self.aux_get_keys_from_acontext_attrs(response, "nome")
        self.assertListEqual(nome_context_keys_list, self.keys_from_attrs_context)
        nomeabrev_context_keys_list = self.aux_get_keys_from_acontext_attrs(response, "nomeabrev")
        self.assertListEqual(nomeabrev_context_keys_list, self.keys_from_attrs_context)
        geometriaaproximada_context_keys_list = self.aux_get_keys_from_acontext_attrs(response, "geometriaaproximada")
        self.assertListEqual(geometriaaproximada_context_keys_list, self.keys_from_attrs_context)
        geocodigo_context_keys_list = self.aux_get_keys_from_acontext_attrs(response, "geocodigo")
        self.assertListEqual(geocodigo_context_keys_list, self.keys_from_attrs_context)
        sigla_context_keys_list = self.aux_get_keys_from_acontext_attrs(response, "sigla")
        self.assertListEqual(sigla_context_keys_list, self.keys_from_attrs_context)
        geom_context_keys_list = self.aux_get_keys_from_acontext_attrs(response, "geom")
        self.assertListEqual(geom_context_keys_list, self.keys_from_attrs_context)
        iri_metadata_context_keys_list = self.aux_get_keys_from_acontext_attrs(response, "iri_metadata")
        self.assertListEqual(iri_metadata_context_keys_list, self.keys_from_attrs_context)
        iri_style_context_keys_list = self.aux_get_keys_from_acontext_attrs(response, "iri_style")
        self.assertListEqual(iri_style_context_keys_list, self.keys_from_attrs_context)

        operations_names = self.aux_get_supported_operations_names(response)
        self.assertListEqual(operations_names, self.spatial_operation_names)

        response_dict = self.aux_get_dict_from_response(response)
        self.assertEquals(response_dict["@type"], 'Geobuf')


    # tests for feature attributes
    def test_options_for_feature_resource_only_attributes(self):
        attrs = ["geom", "nome"]
        response = requests.options(self.bcim_base_uri + 'unidades-federativas/ES/' + attrs[0] + "," + attrs[1],)
        self.assertEquals(response.status_code, 200)

        response_dict_keys = self.aux_get_keys_from_response(response)
        self.assertListEqual(response_dict_keys, self.non_simple_path_dict_keys)

        context_keys = self.aux_get_keys_from_response_context(response)
        self.assertListEqual(context_keys, attrs)

        nome_context_keys_list = self.aux_get_keys_from_acontext_attrs(response, "nome")
        self.assertListEqual(nome_context_keys_list, self.keys_from_attrs_context)
        geom_context_keys_list = self.aux_get_keys_from_acontext_attrs(response, "geom")
        self.assertListEqual(geom_context_keys_list, self.keys_from_attrs_context)

        operations_names = self.aux_get_supported_operations_names(response)
        self.assertListEqual(operations_names, self.spatial_operation_names)

        response_dict = self.aux_get_dict_from_response(response)
        self.assertEquals(response_dict["@type"], 'Feature')

    def test_options_for_feature_resource_only_attributes_with_accept_header(self):
        attrs = ["geom", "nome"]
        response = requests.options(self.bcim_base_uri + 'unidades-federativas/ES/' + attrs[0] + "," + attrs[1],
                                    headers={'accept': 'application/octet-stream'})
        self.assertEquals(response.status_code, 200)

        response_dict_keys = self.aux_get_keys_from_response(response)
        self.assertListEqual(response_dict_keys, self.non_simple_path_dict_keys)

        context_keys = self.aux_get_keys_from_response_context(response)
        self.assertListEqual(context_keys, attrs)

        nome_context_keys_list = self.aux_get_keys_from_acontext_attrs(response, "nome")
        self.assertListEqual(nome_context_keys_list, self.keys_from_attrs_context)
        geom_context_keys_list = self.aux_get_keys_from_acontext_attrs(response, "geom")
        self.assertListEqual(geom_context_keys_list, self.keys_from_attrs_context)

        operations_names = self.aux_get_supported_operations_names(response)
        self.assertListEqual(operations_names, self.spatial_operation_names)

        response_dict = self.aux_get_dict_from_response(response)
        self.assertEquals(response_dict["@type"], 'Geobuf')

    def test_options_for_feature_resource_only_alphanumeric_attributes(self):
        alpha_attrs = ["geocodigo", "nome"]
        response = requests.options(self.bcim_base_uri + 'unidades-federativas/ES/' + alpha_attrs[0] + "," + alpha_attrs[1])
        self.assertEquals(response.status_code, 200)

        response_dict_keys = self.aux_get_keys_from_response(response)
        self.assertListEqual(response_dict_keys, self.non_simple_path_dict_keys)

        context_keys = self.aux_get_keys_from_response_context(response)
        self.assertListEqual(context_keys, alpha_attrs)

        nome_context_keys_list = self.aux_get_keys_from_acontext_attrs(response, "nome")
        self.assertListEqual(nome_context_keys_list, self.keys_from_attrs_context)
        geocodigo_context_keys_list = self.aux_get_keys_from_acontext_attrs(response, "geocodigo")
        self.assertListEqual(geocodigo_context_keys_list, self.keys_from_attrs_context)

        operations_names = self.aux_get_supported_operations_names(response)
        self.assertListEqual(operations_names, self.basic_operations_names)

        response_dict = self.aux_get_dict_from_response(response)
        self.assertEquals(response_dict["@type"], 'Thing')

    def test_options_for_feature_resource_only_alphanumeric_attributes_with_accept_header(self):
        alpha_attrs = ["geocodigo", "nome"]
        response = requests.options(self.bcim_base_uri + 'unidades-federativas/ES/' + alpha_attrs[0] + "," + alpha_attrs[1],
                                    headers={'accept': 'application/octet-stream'})
        self.assertEquals(response.status_code, 200)

        response_dict_keys = self.aux_get_keys_from_response(response)
        self.assertListEqual(response_dict_keys, self.non_simple_path_dict_keys)

        context_keys = self.aux_get_keys_from_response_context(response)
        self.assertListEqual(context_keys, alpha_attrs)

        nome_context_keys_list = self.aux_get_keys_from_acontext_attrs(response, "nome")
        self.assertListEqual(nome_context_keys_list, self.keys_from_attrs_context)
        geocodigo_context_keys_list = self.aux_get_keys_from_acontext_attrs(response, "geocodigo")
        self.assertListEqual(geocodigo_context_keys_list, self.keys_from_attrs_context)

        operations_names = self.aux_get_supported_operations_names(response)
        self.assertListEqual(operations_names, [])

        response_dict = self.aux_get_dict_from_response(response)
        self.assertEquals(response_dict["@type"], 'bytes')

    def test_options_for_feature_resource_only_geometric_attribute(self):
        geom_attrs = ["geom"]
        response = requests.options(self.bcim_base_uri + 'unidades-federativas/ES/' + geom_attrs[0])
        self.assertEquals(response.status_code, 200)

        response_dict_keys = self.aux_get_keys_from_response(response)
        self.assertListEqual(response_dict_keys, self.non_simple_path_dict_keys)

        context_keys = self.aux_get_keys_from_response_context(response)
        self.assertListEqual(context_keys, geom_attrs)

        geom_context_keys_list = self.aux_get_keys_from_acontext_attrs(response, "geom")
        self.assertListEqual(geom_context_keys_list, self.keys_from_attrs_context)

        operations_names = self.aux_get_supported_operations_names(response)
        self.assertListEqual(operations_names, self.spatial_operation_names)

        response_dict = self.aux_get_dict_from_response(response)
        self.assertEquals(response_dict["@type"], 'GeometryField')

    def test_options_for_feature_resource_only_geometric_attribute_with_accept_header(self):
        alpha_attrs = ["geom"]
        response = requests.options(self.bcim_base_uri + 'unidades-federativas/ES/' + alpha_attrs[0],
                                    headers={'accept': 'application/octet-stream'})
        self.assertEquals(response.status_code, 200)

        response_dict_keys = self.aux_get_keys_from_response(response)
        self.assertListEqual(response_dict_keys, self.non_simple_path_dict_keys)

        context_keys = self.aux_get_keys_from_response_context(response)
        self.assertListEqual(context_keys, alpha_attrs)

        geom_context_keys_list = self.aux_get_keys_from_acontext_attrs(response, "geom")
        self.assertListEqual(geom_context_keys_list, self.keys_from_attrs_context)

        operations_names = self.aux_get_supported_operations_names(response)
        self.assertListEqual(operations_names, self.spatial_operation_names)

        response_dict = self.aux_get_dict_from_response(response)
        self.assertEquals(response_dict["@type"], 'Geobuf')

    def test_options_for_feature_resource_pointfield_attribute(self):
        response = requests.options(self.bcim_base_uri + 'aldeias-indigenas/623/geom')
        self.assertEquals(response.status_code, 200)

        response_dict_keys = self.aux_get_keys_from_response(response)
        self.assertListEqual(response_dict_keys, self.non_simple_path_dict_keys)

        operations_names = self.aux_get_supported_operations_names(response)
        self.assertListEqual(operations_names, self.spatial_operation_names)

        context_keys = self.aux_get_keys_from_response_context(response)
        self.assertListEqual(context_keys, ['geom'])

        geom_context_keys_list = self.aux_get_keys_from_acontext_attrs(response, "geom")
        self.assertListEqual(geom_context_keys_list, self.keys_from_attrs_context)

        response_dict = self.aux_get_dict_from_response(response)
        self.assertEquals(response_dict["@type"], 'PointField')

    def test_options_for_feature_resource_pointfield_attribute_accept_octet_stream(self):
        response = requests.options(self.bcim_base_uri + 'aldeias-indigenas/623/geom', headers={"Accept": "application/octet-stream"})
        self.assertEquals(response.status_code, 200)

        response_dict_keys = self.aux_get_keys_from_response(response)
        self.assertListEqual(response_dict_keys, self.non_simple_path_dict_keys)

        operations_names = self.aux_get_supported_operations_names(response)
        self.assertListEqual(operations_names, self.spatial_operation_names)

        context_keys = self.aux_get_keys_from_response_context(response)
        self.assertListEqual(context_keys, ['geom'])

        geom_context_keys_list = self.aux_get_keys_from_acontext_attrs(response, "geom")
        self.assertListEqual(geom_context_keys_list, self.keys_from_attrs_context)

        response_dict = self.aux_get_dict_from_response(response)
        self.assertEquals(response_dict["@type"], 'Geobuf')


    # tests for feature operations
    def test_options_for_feature_resource_operation_with_geometry_return(self):
        response = requests.options(self.bcim_base_uri + 'unidades-federativas/ES/buffer/1.2')
        self.assertEquals(response.status_code, 200)

        response_dict_keys = self.aux_get_keys_from_response(response)
        self.assertListEqual(response_dict_keys, self.non_simple_path_dict_keys)

        a_context_keys = self.aux_get_keys_from_response_context(response)
        self.assertListEqual(a_context_keys, ['buffer'])

        buffer_context_keys_list = self.aux_get_keys_from_acontext_attrs(response, "buffer")
        self.assertListEqual(buffer_context_keys_list, ["@id", "@type"])

        operations_names = self.aux_get_supported_operations_names(response)
        self.assertListEqual(operations_names, self.spatial_operation_names)

        response_dict = self.aux_get_dict_from_response(response)
        self.assertEquals(response_dict["@type"], 'Feature')

    def test_options_for_feature_resource_operation_with_geometry_return_accept_header(self):
        response = requests.options(self.bcim_base_uri + 'unidades-federativas/ES/buffer/1.2',
                                    headers={'Accept': 'application/octet-stream'})
        self.assertEquals(response.status_code, 200)

        response_dict_keys = self.aux_get_keys_from_response(response)
        self.assertListEqual(response_dict_keys, self.non_simple_path_dict_keys)

        a_context_keys = self.aux_get_keys_from_response_context(response)
        self.assertListEqual(a_context_keys, ['buffer'])

        buffer_context_keys_list = self.aux_get_keys_from_acontext_attrs(response, "buffer")
        self.assertListEqual(buffer_context_keys_list, ["@id", "@type"])

        operations_names = self.aux_get_supported_operations_names(response)
        self.assertListEqual(operations_names, self.spatial_operation_names)

        response_dict = self.aux_get_dict_from_response(response)
        self.assertEquals(response_dict["@type"], 'Geobuf')

    def test_options_for_feature_resource_area_operation(self):
        response = requests.options(self.bcim_base_uri + 'unidades-federativas/ES/area')
        self.assertEquals(response.status_code, 200)

        response_dict_keys = self.aux_get_keys_from_response(response)
        self.assertListEqual(response_dict_keys, self.non_simple_path_dict_keys)

        a_context_keys = self.aux_get_keys_from_response_context(response)
        self.assertListEqual(a_context_keys, ['area'])

        area_context_keys_list = self.aux_get_keys_from_acontext_attrs(response, "area")
        self.assertListEqual(area_context_keys_list, ["@id", "@type"])

        operations_names = self.aux_get_supported_operations_names(response)
        self.assertListEqual(operations_names, [])

        response_dict = self.aux_get_dict_from_response(response)
        self.assertEquals(response_dict["@type"], 'float')

    def test_options_for_feature_resource_area_operation_accept_octet_stream(self):
        response = requests.options(self.bcim_base_uri + 'unidades-federativas/ES/area',
                                    headers={'Accept': 'application/octet-stream'})
        self.assertEquals(response.status_code, 200)

        response_dict_keys = self.aux_get_keys_from_response(response)
        self.assertListEqual(response_dict_keys, self.non_simple_path_dict_keys)

        a_context_keys = self.aux_get_keys_from_response_context(response)
        self.assertListEqual(a_context_keys, ['area'])

        area_context_keys_list_context_keys_list = self.aux_get_keys_from_acontext_attrs(response, "area")
        self.assertListEqual(area_context_keys_list_context_keys_list, ["@id", "@type"])

        operations_names = self.aux_get_supported_operations_names(response)
        self.assertListEqual(operations_names, [])

        response_dict = self.aux_get_dict_from_response(response)
        self.assertEquals(response_dict["@type"], 'bytes')

    def test_options_for_feature_resource_operation_with_point_return(self):
        response = requests.options(self.bcim_base_uri + 'unidades-federativas/ES/point_on_surface')
        self.assertEquals(response.status_code, 200)

        response_dict_keys = self.aux_get_keys_from_response(response)
        self.assertListEqual(response_dict_keys, self.non_simple_path_dict_keys)

        a_context_keys = self.aux_get_keys_from_response_context(response)
        self.assertListEqual(a_context_keys, ['point_on_surface'])

        point_on_surface_context_keys_list = self.aux_get_keys_from_acontext_attrs(response, "point_on_surface")
        self.assertListEqual(point_on_surface_context_keys_list, ["@id", "@type"])

        operations_names = self.aux_get_supported_operations_names(response)
        self.assertListEqual(operations_names, self.spatial_operation_names)

        response_dict = self.aux_get_dict_from_response(response)
        self.assertEquals(response_dict["@type"], 'Point')

    def test_options_for_feature_resource_operation_with_point_return_accept_header(self):
        response = requests.options(self.bcim_base_uri + 'unidades-federativas/ES/point_on_surface',
                                    headers={'Accept': 'application/octet-stream'})
        self.assertEquals(response.status_code, 200)

        response_dict_keys = self.aux_get_keys_from_response(response)
        self.assertListEqual(response_dict_keys, self.non_simple_path_dict_keys)

        a_context_keys = self.aux_get_keys_from_response_context(response)
        self.assertListEqual(a_context_keys, ['point_on_surface'])

        point_on_surface_context_keys_list = self.aux_get_keys_from_acontext_attrs(response, "point_on_surface")
        self.assertListEqual(point_on_surface_context_keys_list, ["@id", "@type"])

        operations_names = self.aux_get_supported_operations_names(response)
        self.assertListEqual(operations_names, self.spatial_operation_names)

        response_dict = self.aux_get_dict_from_response(response)
        self.assertEquals(response_dict["@type"], 'Geobuf')


    # --------------- TESTS FOR NON SPATIAL RESOURCE ---------------------------------
    # tests for NonSpatialResource simple path
    def test_options_for_non_spatial_resource_simple_path(self):
        response = requests.options(self.controle_base_uri + "usuario-list/1/")
        self.assertEquals(response.status_code, 200)

        response_keys = self.aux_get_keys_from_response(response)
        self.assertListEqual(response_keys, self.simple_path_options_dict_keys)

        acontext_keys = self.aux_get_keys_from_response_context(response)
        self.assertListEqual(acontext_keys, ['avatar', 'data_nascimento', 'email', 'id', 'nome', 'nome_usuario', 'senha'])

        id_context_keys_list = self.aux_get_keys_from_acontext_attrs(response, "id")
        self.assertListEqual(id_context_keys_list, self.keys_from_attrs_context)
        nome_context_keys_list = self.aux_get_keys_from_acontext_attrs(response, "nome")
        self.assertListEqual(nome_context_keys_list, self.keys_from_attrs_context)
        nome_usuario_context_keys_list = self.aux_get_keys_from_acontext_attrs(response, "nome_usuario")
        self.assertListEqual(nome_usuario_context_keys_list, self.keys_from_attrs_context)
        senha_context_keys_list = self.aux_get_keys_from_acontext_attrs(response, "senha")
        self.assertListEqual(senha_context_keys_list, self.keys_from_attrs_context)
        data_nascimento_context_keys_list = self.aux_get_keys_from_acontext_attrs(response, "data_nascimento")
        self.assertListEqual(data_nascimento_context_keys_list, self.keys_from_attrs_context)
        email_context_keys_list = self.aux_get_keys_from_acontext_attrs(response, "email")
        self.assertListEqual(email_context_keys_list, self.keys_from_attrs_context)
        avatar_context_keys_list = self.aux_get_keys_from_acontext_attrs(response, "avatar")
        self.assertListEqual(avatar_context_keys_list, self.keys_from_attrs_context)

        operation_names = self.aux_get_supported_operations_names(response)
        self.assertListEqual(operation_names, self.basic_operations_names)

        response_dict = self.aux_get_dict_from_response(response)
        self.assertEquals(response_dict["@type"], 'Thing')

    def test_options_for_non_spatial_resource_simple_path_with_accept_header(self):
        response = requests.options(self.controle_base_uri + "usuario-list/1/",
                                    headers={'Accept': "application/octet-stream"})
        self.assertEquals(response.status_code, 200)

        response_keys = self.aux_get_keys_from_response(response)
        self.assertListEqual(response_keys, self.simple_path_options_dict_keys)

        acontext_keys = self.aux_get_keys_from_response_context(response)
        self.assertListEqual(acontext_keys, ['avatar', 'data_nascimento', 'email', 'id', 'nome', 'nome_usuario', 'senha'])

        id_context_keys_list = self.aux_get_keys_from_acontext_attrs(response, "id")
        self.assertListEqual(id_context_keys_list, self.keys_from_attrs_context)
        nome_context_keys_list = self.aux_get_keys_from_acontext_attrs(response, "nome")
        self.assertListEqual(nome_context_keys_list, self.keys_from_attrs_context)
        nome_usuario_context_keys_list = self.aux_get_keys_from_acontext_attrs(response, "nome_usuario")
        self.assertListEqual(nome_usuario_context_keys_list, self.keys_from_attrs_context)
        senha_context_keys_list = self.aux_get_keys_from_acontext_attrs(response, "senha")
        self.assertListEqual(senha_context_keys_list, self.keys_from_attrs_context)
        data_nascimento_context_keys_list = self.aux_get_keys_from_acontext_attrs(response, "data_nascimento")
        self.assertListEqual(data_nascimento_context_keys_list, self.keys_from_attrs_context)
        email_context_keys_list = self.aux_get_keys_from_acontext_attrs(response, "email")
        self.assertListEqual(email_context_keys_list, self.keys_from_attrs_context)
        avatar_context_keys_list = self.aux_get_keys_from_acontext_attrs(response, "avatar")
        self.assertListEqual(avatar_context_keys_list, self.keys_from_attrs_context)

        operation_names = self.aux_get_supported_operations_names(response)
        self.assertListEqual(operation_names, [])

        response_dict = self.aux_get_dict_from_response(response)
        self.assertEquals(response_dict["@type"], 'bytes')

    # tests for NonSpatialResource only attributes
    def test_options_for_non_spatial_resource_only_attributes(self):
        response = requests.options(self.controle_base_uri + "usuario-list/1/nome,email")
        self.assertEquals(response.status_code, 200)

        response_keys = self.aux_get_keys_from_response(response)
        self.assertListEqual(response_keys, self.non_simple_path_dict_keys)

        acontext_keys = self.aux_get_keys_from_response_context(response)
        self.assertListEqual(acontext_keys, ['email', 'nome'])

        nome_context_keys_list = self.aux_get_keys_from_acontext_attrs(response, "nome")
        self.assertListEqual(nome_context_keys_list, self.keys_from_attrs_context)
        email_context_keys_list = self.aux_get_keys_from_acontext_attrs(response, "email")
        self.assertListEqual(email_context_keys_list, self.keys_from_attrs_context)

        supported_operations_names = self.aux_get_supported_operations_names(response)
        self.assertListEqual(supported_operations_names, self.basic_operations_names)

        response_dict = self.aux_get_dict_from_response(response)
        self.assertEquals(response_dict["@type"], 'Thing')

    def test_options_for_non_spatial_resource_only_attributes_with_accept_header(self):
        response = requests.options(self.controle_base_uri + "usuario-list/1/nome,email",
                                    headers={'Accept': "application/octet-stream"})
        self.assertEquals(response.status_code, 200)

        response_keys = self.aux_get_keys_from_response(response)
        self.assertListEqual(response_keys, self.non_simple_path_dict_keys)

        acontext_keys = self.aux_get_keys_from_response_context(response)
        self.assertListEqual(acontext_keys, ['email', 'nome'])

        nome_context_keys_list = self.aux_get_keys_from_acontext_attrs(response, "nome")
        self.assertListEqual(nome_context_keys_list, self.keys_from_attrs_context)
        email_context_keys_list = self.aux_get_keys_from_acontext_attrs(response, "email")
        self.assertListEqual(email_context_keys_list, self.keys_from_attrs_context)

        operation_names = self.aux_get_supported_operations_names(response)
        self.assertListEqual(operation_names, [])

        response_dict = self.aux_get_dict_from_response(response)
        self.assertEquals(response_dict["@type"], 'bytes')


    # ------------------- TESTS FOR ENTRY POINTS -------------------------------------
    def test_options_for_feature_entrypoint(self):
        response = requests.options(self.bcim_base_uri)
        self.assertEquals(response.status_code, 200)

        #self.assertEqual(response.headers['Link'],
        #'<http://luc00557196:8000/api/bcim/>; rel="http://schema.org/EntryPoint" , <http://luc00557196:8000/api/bcim.jsonld>; rel="http://www.w3.org/ns/json-ld#context"; type="application/ld+json"')

        a_context_keys = self.aux_get_keys_from_response_context(response)
        self.assertListEqual(a_context_keys, ['aglomerados rurais de extensao urbana', 'aglomerados rurais isolado',
                                              'aldeias indigenas', 'areas de desenvolvimento de controle', 'areas edificadas',
                                              'bancos de areia', 'barragens', 'brejos e pantanos', 'capitais', 'cidades',
                                              'corredeiras', 'curvas batimetricas', 'curvas de nivel', 'dunas', 'eclusas',
                                              'edificacoes agropecuarias de extracao vegetal e pesca',
                                              'edificacoes de construcao aeroportuaria', 'edificacoes de construcao portuaria',
                                              'edificacoes de metro ferroviaria', 'edificacoes industrial', 'edificacoes publica militar',
                                              'edificacoes religiosa', 'elementos fisiografico natural',
                                              'estacoes geradoras de energia eletrica', 'extracoes minerais', 'fozes maritima',
                                              'fundeadouros', 'hidreletricas', 'ilhas', 'mangues', 'marcos de limite', 'massas dagua',
                                              'municipios', 'outros limites oficiais', 'paises', 'picos', 'pistas de ponto pouso',
                                              'pontes', 'pontos cotados altimetricos', 'pontos cotados batimetricos', 'postos fiscais',
                                              'quedas dagua', 'recifes', 'rochas em agua', 'sinalizacoes', 'sumidouros vertedouros',
                                              'termeletricas', 'terras indigenas', 'terrenos sujeito a inundacao',
                                              'torres de energia', 'travessias', 'trechos de drenagem', 'trechos de massa dagua',
                                              'trechos dutos', 'trechos ferroviarios', 'trechos hidroviarios', 'trechos rodoviarios',
                                              'tuneis', 'unidades de conservacao nao snuc', 'unidades de protecao integral',
                                              'unidades de uso sustentavel', 'unidades federativas', 'vegetacoes de restinga', 'vilas'])

        response_dict = self.aux_get_dict_from_response(response)

        self.assertEquals("https://www.hydra-cg.com/spec/latest/core/#hydra:entrypoint", response_dict["@id"])
        self.assertEquals("http://geojson.org/geojson-ld/vocab.html#FeatureCollection",
                          response_dict["@context"]['aglomerados rurais de extensao urbana']["@id"])

    def test_options_for_raster_entrypoint(self):
        response = requests.options(self.raster_base_uri)
        self.assertEquals(response.status_code, 200)

        a_context_keys = self.aux_get_keys_from_response_context(response)
        self.assertEquals(a_context_keys, ['imagem-exemplo-tile1-list',
                                           'imagem-exemplo1-list',
                                           'imagem-exemplo2-list',
                                           'imagem-exemplo4-tile2-list'])

        response_dict = self.aux_get_dict_from_response(response)

        self.assertEquals("https://www.hydra-cg.com/spec/latest/core/#hydra:entrypoint", response_dict["@id"])
        # todo: find more specific vocabulary for raster
        self.assertEquals("https://schema.org/Thing",
                          response_dict["@context"]['imagem-exemplo-tile1-list']["@id"])

    def test_options_for_non_spatial_entrypoint(self):
        response = requests.options(self.controle_base_uri)
        self.assertEquals(response.status_code, 200)

        a_context_keys = self.aux_get_keys_from_response_context(response)
        self.assertListEqual(a_context_keys, ['gasto-list', 'tipo-gasto-list', 'usuario-list'])

        response_dict = self.aux_get_dict_from_response(response)

        self.assertEquals("https://www.hydra-cg.com/spec/latest/core/#hydra:entrypoint", response_dict["@id"])
        # todo: find more specific vocabulary for non spatial resource
        self.assertEquals("https://schema.org/Thing",
                          response_dict["@context"]['gasto-list']["@id"])

#python manage.py test hyper_resource.tests.GetRequestContextTest --testrunner=hyper_resource.tests.NoDbTestRunner
class GetRequestContextTest(AbstractRequestTest):

    # --------------- TESTS FOR FEATURE RESOURCE ---------------------------------
    # tests for feature resource simple path
    def test_suffixed_request_to_feature_resource_simple_path(self):
        response = requests.get(self.bcim_base_uri + "unidades-federativas/ES.jsonld")
        self.assertEquals(response.status_code, 200)

        response_dict_keys = self.aux_get_keys_from_response(response)
        self.assertListEqual(response_dict_keys, self.simple_path_options_dict_keys)

        acontext_keys = self.aux_get_keys_from_response_context(response)
        self.assertListEqual(acontext_keys, ['geocodigo', 'geom', 'geometriaaproximada', 'id_objeto', 'iri_metadata', 'iri_style', 'nome', 'nomeabrev', 'sigla'])

        id_objeto_context_keys_list = self.aux_get_keys_from_acontext_attrs(response, "id_objeto")
        self.assertListEqual(id_objeto_context_keys_list, self.keys_from_attrs_context)
        nome_context_keys_list = self.aux_get_keys_from_acontext_attrs(response, "nome")
        self.assertListEqual(nome_context_keys_list, self.keys_from_attrs_context)
        nomeabrev_context_keys_list = self.aux_get_keys_from_acontext_attrs(response, "nomeabrev")
        self.assertListEqual(nomeabrev_context_keys_list, self.keys_from_attrs_context)
        geometriaaproximada_context_keys_list = self.aux_get_keys_from_acontext_attrs(response, "geometriaaproximada")
        self.assertListEqual(geometriaaproximada_context_keys_list, self.keys_from_attrs_context)
        geocodigo_context_keys_list = self.aux_get_keys_from_acontext_attrs(response, "geocodigo")
        self.assertListEqual(geocodigo_context_keys_list, self.keys_from_attrs_context)
        sigla_context_keys_list = self.aux_get_keys_from_acontext_attrs(response, "sigla")
        self.assertListEqual(sigla_context_keys_list, self.keys_from_attrs_context)
        geom_context_keys_list = self.aux_get_keys_from_acontext_attrs(response, "geom")
        self.assertListEqual(geom_context_keys_list, self.keys_from_attrs_context)

        operations_names = self.aux_get_supported_operations_names(response)
        self.assertListEqual(operations_names, self.spatial_operation_names)

        response_dict = self.aux_get_dict_from_response(response)
        self.assertEquals(response_dict["@type"], 'Feature')

    # tests for feature resource attributes
    def test_suffixed_request_to_feature_resource_only_attributes(self):
        response = requests.get(self.bcim_base_uri + "unidades-federativas/ES/geom,geocodigo,sigla.jsonld")
        self.assertEquals(response.status_code, 200)

        response_dict_keys = self.aux_get_keys_from_response(response)
        self.assertListEqual(response_dict_keys, self.non_simple_path_dict_keys)

        acontext_keys = self.aux_get_keys_from_response_context(response)
        self.assertListEqual(acontext_keys, ['geocodigo', 'geom', 'sigla'])

        geocodigo_context_keys_list = self.aux_get_keys_from_acontext_attrs(response, "geocodigo")
        self.assertListEqual(geocodigo_context_keys_list, self.keys_from_attrs_context)
        sigla_context_keys_list = self.aux_get_keys_from_acontext_attrs(response, "sigla")
        self.assertListEqual(sigla_context_keys_list, self.keys_from_attrs_context)
        geom_context_keys_list = self.aux_get_keys_from_acontext_attrs(response, "geom")
        self.assertListEqual(geom_context_keys_list, self.keys_from_attrs_context)

        operations_names = self.aux_get_supported_operations_names(response)
        self.assertListEqual(operations_names, self.spatial_operation_names)

        response_dict = self.aux_get_dict_from_response(response)
        self.assertEquals(response_dict["@type"], 'Feature')

    def test_suffixed_request_to_feature_resource_only_alphanumeric_attributes(self):
        response = requests.get(self.bcim_base_uri + "unidades-federativas/ES/geocodigo,sigla.jsonld")
        self.assertEquals(response.status_code, 200)

        response_dict_keys = self.aux_get_keys_from_response(response)
        self.assertListEqual(response_dict_keys, self.non_simple_path_dict_keys)

        acontext_keys = self.aux_get_keys_from_response_context(response)
        self.assertListEqual(acontext_keys, ['geocodigo', 'sigla'])

        geocodigo_context_keys_list = self.aux_get_keys_from_acontext_attrs(response, "geocodigo")
        self.assertListEqual(geocodigo_context_keys_list, self.keys_from_attrs_context)
        sigla_context_keys_list = self.aux_get_keys_from_acontext_attrs(response, "sigla")
        self.assertListEqual(sigla_context_keys_list, self.keys_from_attrs_context)

        operations_names = self.aux_get_supported_operations_names(response)
        self.assertListEqual(operations_names, self.basic_operations_names)

        response_dict = self.aux_get_dict_from_response(response)
        self.assertEquals(response_dict["@type"], 'Thing')

    def test_suffixed_request_to_feature_resource_only_geometric_attribute(self):
        response = requests.get(self.bcim_base_uri + "unidades-federativas/ES/geom.jsonld")
        self.assertEquals(response.status_code, 200)

        response_dict_keys = self.aux_get_keys_from_response(response)
        self.assertListEqual(response_dict_keys, self.non_simple_path_dict_keys)

        acontext_keys = self.aux_get_keys_from_response_context(response)
        self.assertListEqual(acontext_keys, ['geom'])

        geom_context_keys_list = self.aux_get_keys_from_acontext_attrs(response, "geom")
        self.assertListEqual(geom_context_keys_list, self.keys_from_attrs_context)

        operations_names = self.aux_get_supported_operations_names(response)
        self.assertListEqual(operations_names, self.spatial_operation_names)

        response_dict = self.aux_get_dict_from_response(response)
        self.assertEquals(response_dict["@type"], 'GeometryField')

    # tests for feature resource operations
    def test_sufixed_request_to_feature_resource_operation_with_float_return(self):
        response = requests.get(self.bcim_base_uri + 'unidades-federativas/ES/area.jsonld')
        self.assertEquals(response.status_code, 200)

        response_dict_keys = self.aux_get_keys_from_response(response)
        self.assertListEqual(response_dict_keys, self.non_simple_path_dict_keys)

        a_context_keys = self.aux_get_keys_from_response_context(response)
        self.assertListEqual(a_context_keys, ['area'])

        area_context_keys_list = self.aux_get_keys_from_acontext_attrs(response, "area")
        self.assertListEqual(area_context_keys_list, ["@id", "@type"])

        operations_names = self.aux_get_supported_operations_names(response)
        self.assertListEqual(operations_names, [])

        response_dict = self.aux_get_dict_from_response(response)
        self.assertEquals(response_dict["@type"], 'float')

    def test_suffixed_request_to_feature_resource_operation_with_geometry_return(self):
        response = requests.get(self.bcim_base_uri + 'unidades-federativas/ES/buffer/1.2.jsonld')
        self.assertEquals(response.status_code, 200)

        response_dict_keys = self.aux_get_keys_from_response(response)
        self.assertListEqual(response_dict_keys, self.non_simple_path_dict_keys)

        a_context_keys = self.aux_get_keys_from_response_context(response)
        self.assertListEqual(a_context_keys, ['buffer'])

        buffer_context_keys_list = self.aux_get_keys_from_acontext_attrs(response, "buffer")
        self.assertListEqual(buffer_context_keys_list, ["@id", "@type"])

        operations_names = self.aux_get_supported_operations_names(response)
        self.assertListEqual(operations_names, self.spatial_operation_names)

        response_dict = self.aux_get_dict_from_response(response)
        self.assertEquals(response_dict["@type"], 'Feature')

    def test_suffixed_request_to_feature_resource_point_on_surface_operation(self):
        response = requests.get(self.bcim_base_uri + 'unidades-federativas/ES/point_on_surface.jsonld')
        self.assertEquals(response.status_code, 200)

        response_dict_keys = self.aux_get_keys_from_response(response)
        self.assertListEqual(response_dict_keys, self.non_simple_path_dict_keys)

        a_context_keys = self.aux_get_keys_from_response_context(response)
        self.assertListEqual(a_context_keys, ['point_on_surface'])

        point_on_surface_context_keys_list = self.aux_get_keys_from_acontext_attrs(response, "point_on_surface")
        self.assertListEqual(point_on_surface_context_keys_list, ["@id", "@type"])

        operations_names = self.aux_get_supported_operations_names(response)
        self.assertListEqual(operations_names, self.spatial_operation_names)

        response_dict = self.aux_get_dict_from_response(response)
        self.assertEquals(response_dict["@type"], 'Point')


    # --------------- TESTS FOR FEATURE COLLECTION ---------------------------------
    # tests for feature collection simple path
    def test_suffixed_request_to_feature_collection_resource_simple_path(self):
        response = requests.get(self.bcim_base_uri + "unidades-federativas.jsonld")
        self.assertEquals(response.status_code, 200)

        response_dict_keys = self.aux_get_keys_from_response(response)
        self.assertListEqual(response_dict_keys, self.simple_path_options_dict_keys)

        acontext_keys = self.aux_get_keys_from_response_context(response)
        self.assertListEqual(acontext_keys, ['geocodigo', 'geom', 'geometriaaproximada', 'id_objeto', 'iri_metadata', 'iri_style', 'nome', 'nomeabrev', 'sigla'])

        id_objeto_context_keys_list = self.aux_get_keys_from_acontext_attrs(response, "id_objeto")
        self.assertListEqual(id_objeto_context_keys_list, self.keys_from_attrs_context)
        nome_context_keys_list = self.aux_get_keys_from_acontext_attrs(response, "nome")
        self.assertListEqual(nome_context_keys_list, self.keys_from_attrs_context)
        nomeabrev_context_keys_list = self.aux_get_keys_from_acontext_attrs(response, "nomeabrev")
        self.assertListEqual(nomeabrev_context_keys_list, self.keys_from_attrs_context)
        geometriaaproximada_context_keys_list = self.aux_get_keys_from_acontext_attrs(response, "geometriaaproximada")
        self.assertListEqual(geometriaaproximada_context_keys_list, self.keys_from_attrs_context)
        geocodigo_context_keys_list = self.aux_get_keys_from_acontext_attrs(response, "geocodigo")
        self.assertListEqual(geocodigo_context_keys_list, self.keys_from_attrs_context)
        sigla_context_keys_list = self.aux_get_keys_from_acontext_attrs(response, "sigla")
        self.assertListEqual(sigla_context_keys_list, self.keys_from_attrs_context)
        geom_context_keys_list = self.aux_get_keys_from_acontext_attrs(response, "geom")
        self.assertListEqual(geom_context_keys_list, self.keys_from_attrs_context)

        operations_names = self.aux_get_supported_operations_names(response)
        self.assertListEqual(operations_names, self.spatial_collection_operation_names)

        response_dict = self.aux_get_dict_from_response(response)
        self.assertEquals(response_dict["@type"], 'FeatureCollection')

    # tests for feature collection attributes
    def test_suffixed_request_to_feature_collection_resource_only_attributes(self):
        response = requests.get(self.bcim_base_uri + "aldeias-indigenas/nome,geom.jsonld")
        self.assertEquals(response.status_code, 200)

        response_dict_keys = self.aux_get_keys_from_response(response)
        self.assertListEqual(response_dict_keys, self.non_simple_path_dict_keys)

        acontext_keys = self.aux_get_keys_from_response_context(response)
        self.assertListEqual(acontext_keys, ['geom', 'nome'])

        nome_context_keys_list = self.aux_get_keys_from_acontext_attrs(response, "nome")
        self.assertListEqual(nome_context_keys_list, self.keys_from_attrs_context)
        geom_context_keys_list = self.aux_get_keys_from_acontext_attrs(response, "geom")
        self.assertListEqual(geom_context_keys_list, self.keys_from_attrs_context)

        operations_names = self.aux_get_supported_operations_names(response)
        self.assertListEqual(operations_names, self.spatial_collection_operation_names)

        response_dict = self.aux_get_dict_from_response(response)
        self.assertEquals(response_dict["@type"], 'FeatureCollection')

    def test_suffixed_request_feature_collection_only_geometric_attribute(self):
        response = requests.get(self.bcim_base_uri + "aldeias-indigenas/geom.jsonld")
        self.assertEquals(response.status_code, 200)

        response_dict_keys = self.aux_get_keys_from_response(response)
        self.assertListEqual(response_dict_keys, self.non_simple_path_dict_keys)

        acontext_keys = self.aux_get_keys_from_response_context(response)
        self.assertListEqual(acontext_keys, ['geom'])

        geom_context_keys_list = self.aux_get_keys_from_acontext_attrs(response, "geom")
        self.assertListEqual(geom_context_keys_list, self.keys_from_attrs_context)

        operations_names = self.aux_get_supported_operations_names(response)
        self.assertListEqual(operations_names, self.spatial_collection_operation_names)

        response_dict = self.aux_get_dict_from_response(response)
        self.assertEquals(response_dict["@type"], 'GeometryCollection')

    def test_suffixed_request_feature_collection_only_alphanumeric_attributes(self):
        response = requests.get(self.bcim_base_uri + "aldeias-indigenas/nome,nomeabrev.jsonld")
        self.assertEquals(response.status_code, 200)

        response_dict_keys = self.aux_get_keys_from_response(response)
        self.assertListEqual(response_dict_keys, self.non_simple_path_dict_keys)

        context_dict_keys = self.aux_get_keys_from_response_context(response)
        self.assertListEqual(context_dict_keys, ['nome', 'nomeabrev'])

        nome_context_keys_list = self.aux_get_keys_from_acontext_attrs(response, "nome")
        self.assertListEqual(nome_context_keys_list, self.keys_from_attrs_context)
        nomeabrev_context_keys_list = self.aux_get_keys_from_acontext_attrs(response, "nomeabrev")
        self.assertListEqual(nomeabrev_context_keys_list, self.keys_from_attrs_context)

        operations_names = self.aux_get_supported_operations_names(response)
        self.assertListEqual(operations_names, self.collection_operation_names)

        response_dict = self.aux_get_dict_from_response(response)
        self.assertEquals(response_dict["@type"], 'Collection')

    # tests for feature collection operations
    def test_suffixed_request_feature_collection_operation_with_geometry_collection_return(self):
        response = requests.get(self.bcim_base_uri + "aldeias-indigenas/within/" + self.bcim_base_uri + "unidades-federativas/ES.jsonld")
        self.assertEquals(response.status_code, 200)

        response_dict_keys = self.aux_get_keys_from_response(response)
        self.assertListEqual(response_dict_keys, self.non_simple_path_dict_keys)

        context_dict_keys = self.aux_get_keys_from_response_context(response)
        self.assertListEqual(context_dict_keys, ['within'])

        within_context_keys_list = self.aux_get_keys_from_acontext_attrs(response, "within")
        self.assertListEqual(within_context_keys_list, ["@id", "@type"])

        supported_operation_names = self.aux_get_supported_operations_names(response)
        self.assertEquals(supported_operation_names, self.spatial_collection_operation_names)

        response_dict = self.aux_get_dict_from_response(response)
        self.assertEquals(response_dict["@type"], 'FeatureCollection')

    def test_suffixed_request_feature_collection_operation_with_integer_return(self):
        response = requests.get(self.bcim_base_uri + "aldeias-indigenas/count_resource.jsonld")
        self.assertEquals(response.status_code, 200)

        response_dict_keys = self.aux_get_keys_from_response(response)
        self.assertListEqual(response_dict_keys, self.non_simple_path_dict_keys)

        supported_operations_names = self.aux_get_supported_operations_names(response)
        self.assertEquals(supported_operations_names, [])

        context_dict_keys = self.aux_get_keys_from_response_context(response)
        self.assertListEqual(context_dict_keys, ['count_resource'])

        count_resource_context_keys_list = self.aux_get_keys_from_acontext_attrs(response, "count_resource")
        self.assertListEqual(count_resource_context_keys_list, ["@id", "@type"])

        response_dict = self.aux_get_dict_from_response(response)
        self.assertEquals(response_dict["@type"], 'int')


    # --------------- TESTS FOR NON SPATIAL RESOURCE ---------------------------------
    # tests for nonspatialresource simple path
    def test_suffixed_request_to_non_spatial_resource_simple_path(self):
        response = requests.get(self.controle_base_uri + "usuario-list/1.jsonld")
        self.assertEquals(response.status_code, 200)

        response_dict_keys = self.aux_get_keys_from_response(response)
        self.assertListEqual(response_dict_keys, self.simple_path_options_dict_keys)

        acontext_keys = self.aux_get_keys_from_response_context(response)
        self.assertListEqual(acontext_keys, ['avatar', 'data_nascimento', 'email', 'id', 'nome', 'nome_usuario', 'senha'])

        avatar_context_keys_list = self.aux_get_keys_from_acontext_attrs(response, "avatar")
        self.assertListEqual(avatar_context_keys_list, self.keys_from_attrs_context)
        data_nascimento_context_keys_list = self.aux_get_keys_from_acontext_attrs(response, "data_nascimento")
        self.assertListEqual(data_nascimento_context_keys_list, self.keys_from_attrs_context)
        email_context_keys_list = self.aux_get_keys_from_acontext_attrs(response, "email")
        self.assertListEqual(email_context_keys_list, self.keys_from_attrs_context)
        id_context_keys_list = self.aux_get_keys_from_acontext_attrs(response, "id")
        self.assertListEqual(id_context_keys_list, self.keys_from_attrs_context)
        nome_context_keys_list = self.aux_get_keys_from_acontext_attrs(response, "nome")
        self.assertListEqual(nome_context_keys_list, self.keys_from_attrs_context)
        nome_usuario_context_keys_list = self.aux_get_keys_from_acontext_attrs(response, "nome_usuario")
        self.assertListEqual(nome_usuario_context_keys_list, self.keys_from_attrs_context)
        senha_context_keys_list = self.aux_get_keys_from_acontext_attrs(response, "senha")
        self.assertListEqual(senha_context_keys_list, self.keys_from_attrs_context)

        operations_names = self.aux_get_supported_operations_names(response)
        self.assertListEqual(operations_names, self.basic_operations_names)

        response_dict = self.aux_get_dict_from_response(response)
        self.assertEquals(response_dict["@type"], 'Thing')

    # tests for nonspatialresource attributes
    def test_suffixed_request_to_non_spatial_resource_only_attributes(self):
        response = requests.get(self.controle_base_uri + "usuario-list/1/nome,email.jsonld")
        self.assertEquals(response.status_code, 200)

        response_keys = self.aux_get_keys_from_response(response)
        self.assertListEqual(response_keys, self.non_simple_path_dict_keys)

        acontext_keys = self.aux_get_keys_from_response_context(response)
        self.assertListEqual(acontext_keys, ['email', 'nome'])

        nome_context_keys_list = self.aux_get_keys_from_acontext_attrs(response, "nome")
        self.assertListEqual(nome_context_keys_list, self.keys_from_attrs_context)
        email_context_keys_list = self.aux_get_keys_from_acontext_attrs(response, "email")
        self.assertListEqual(email_context_keys_list, self.keys_from_attrs_context)

        supported_operations_names = self.aux_get_supported_operations_names(response)
        self.assertListEqual(supported_operations_names, self.basic_operations_names)

        response_dict = self.aux_get_dict_from_response(response)
        self.assertEquals(response_dict["@type"], 'Thing')


    # --------------- TESTS FOR COLLECTION ---------------------------------
    # tests for collection simple path
    def test_suffixed_request_to_collection_resource_simple_path(self):
        response = requests.get(self.controle_base_uri + "usuario-list.jsonld")
        self.assertEquals(response.status_code, 200)

        response_dict_keys = self.aux_get_keys_from_response(response)
        self.assertListEqual(response_dict_keys, self.simple_path_options_dict_keys)

        acontext_keys = self.aux_get_keys_from_response_context(response)
        self.assertListEqual(acontext_keys, ['avatar', 'data_nascimento', 'email', 'id', 'nome', 'nome_usuario', 'senha'])

        avatar_context_keys_list = self.aux_get_keys_from_acontext_attrs(response, "avatar")
        self.assertListEqual(avatar_context_keys_list, self.keys_from_attrs_context)
        data_nascimento_context_keys_list = self.aux_get_keys_from_acontext_attrs(response, "data_nascimento")
        self.assertListEqual(data_nascimento_context_keys_list, self.keys_from_attrs_context)
        email_context_keys_list = self.aux_get_keys_from_acontext_attrs(response, "email")
        self.assertListEqual(email_context_keys_list, self.keys_from_attrs_context)
        id_context_keys_list = self.aux_get_keys_from_acontext_attrs(response, "id")
        self.assertListEqual(id_context_keys_list, self.keys_from_attrs_context)
        nome_context_keys_list = self.aux_get_keys_from_acontext_attrs(response, "nome")
        self.assertListEqual(nome_context_keys_list, self.keys_from_attrs_context)
        nome_usuario_context_keys_list = self.aux_get_keys_from_acontext_attrs(response, "nome_usuario")
        self.assertListEqual(nome_usuario_context_keys_list, self.keys_from_attrs_context)
        senha_context_keys_list = self.aux_get_keys_from_acontext_attrs(response, "senha")
        self.assertListEqual(senha_context_keys_list, self.keys_from_attrs_context)

        operations_names = self.aux_get_supported_operations_names(response)
        self.assertListEqual(operations_names, self.collection_operation_names)

        response_dict = self.aux_get_dict_from_response(response)
        self.assertEquals(response_dict["@type"], 'Collection')

    # tests for collection attributes
    def test_suffixed_request_to_collection_resource_only_attributes(self):
        response = requests.get(self.controle_base_uri + 'gasto-list/data,valor.jsonld')
        self.assertEquals(response.status_code, 200)

        response_keys = self.aux_get_keys_from_response(response)
        self.assertListEqual(response_keys, self.non_simple_path_dict_keys)

        context_keys = self.aux_get_keys_from_response_context(response)
        self.assertListEqual(context_keys, ['data', 'valor'])

        data_context_keys_list = self.aux_get_keys_from_acontext_attrs(response, "data")
        self.assertListEqual(data_context_keys_list, self.keys_from_attrs_context)
        valor_context_keys_list = self.aux_get_keys_from_acontext_attrs(response, "valor")
        self.assertListEqual(valor_context_keys_list, self.keys_from_attrs_context)

        operation_names = self.aux_get_supported_operations_names(response)
        self.assertListEqual(operation_names, self.collection_operation_names)

        response_dict = self.aux_get_dict_from_response(response)
        self.assertEquals(response_dict["@type"], 'Collection')

    # tests for collection operation

    # tests for collection collect operation


    # ------------------- TESTS FOR ENTRY POINTS -------------------------------------

#python manage.py test hyper_resource.tests.JoinOperationTest --testrunner=hyper_resource.tests.NoDbTestRunner
class JoinOperationTest(AbstractGetRequestTest):
    def setUp(self):
        super(JoinOperationTest, self).setUp()
        self.pesquisa_esporte_base_url = "http://172.30.10.86/esporte-list/"
        self.munic_2015_base_uri = "http://172.30.10.86/api/munic-2015/"
        self.pib_municipio = "http://172.30.10.86/api/pib-municipio/"
        self.feature_keys = ["geometry", "id", "properties", "type"]

    def aux_get_first_joined_dict_attributes_from_first_feature(self, response):
        first_feature = self.aux_get_first_feature(response)
        first_joined_alfa_dict = first_feature['properties']['__joined__'][0]
        return sorted( list(first_joined_alfa_dict.keys()) )

    def aux_get_first_feature_joined_length(self, response):
        first_feature = self.aux_get_first_feature(response)
        return len(first_feature['properties']['__joined__'])

    # --------------- TESTS FOR NON SPATIAL RESOURCE ---------------------------------
    def test_join_operation_for_non_spatial_resource_one_to_one_rel(self):
        pass

    def test_join_operation_for_non_spatial_resource_one_to_one_rel_accept_octet_stream(self):
        pass

    def test_join_operation_for_non_spatial_resource_one_to_many_rel(self):
        pass

    def test_join_operation_for_non_spatial_resource_one_to_many_rel_accept_octet_stream(self):
        pass

    # --------------- TESTS FOR FEATURE RESOURCE ---------------------------------
    def test_join_operation_for_feature_resource_one_to_one_rel(self):
        response = requests.get(self.bcim_base_uri + "municipios/3304557/join/geocodigo&geocodigo/" + self.munic_2015_base_uri + "planejamento-urbano-list/3243/")
        self.assertEquals(response.status_code, 200)
        self.assertEquals(response.headers['content-type'], 'application/vnd.geo+json')

        response_dict_keys = self.aux_get_keys_from_response(response)
        self.assertEquals(response_dict_keys, self.feature_keys)

        feature_properties_keys = self.aux_get_first_feature_properties_keys(response)
        self.assertEquals(feature_properties_keys, ["__joined__", "anodereferencia", "geocodigo", "geometriaaproximada", "nome", "nomeabrev"])

        joined_dicts_len = self.aux_get_first_feature_joined_length(response)
        self.assertEquals(joined_dicts_len, 1)

        joined_alfanumeric_attrs = self.aux_get_first_joined_dict_attributes_from_first_feature(response)
        self.assertEquals(joined_alfanumeric_attrs, ['ano_lei_codigo_obras', 'ano_lei_criacao',
                                                     'ano_lei_legis_sob_area_zona_espe_inte_social',
                                                     'ano_lei_legis_sob_zona_area_espe_inter',
                                                     'ano_lei_legis_sobre_parc_solo',
                                                     'ano_lei_legis_sobre_zone_uso_ocupa_solo',
                                                     'ano_lei_legislacao_sobre_contri_melhoria',
                                                     'ano_lei_legislacao_sobre_dire_superficie',
                                                     'ano_lei_legislacao_sobre_estu_impa_vizinhanca',
                                                     'ano_lei_legislacao_sobre_estu_pre_impa_ambiental',
                                                     'ano_lei_legislacao_sobre_legitimacao_posse',
                                                     'ano_lei_legislacao_sobre_ope_urba_consorciada',
                                                     'ano_lei_legislacao_sobre_regula_fundiaria',
                                                     'ano_lei_legislacao_sobre_servi_administrativa',
                                                     'ano_lei_legislacao_sobre_solo_cria_outorga_onerosa_dir_construi',
                                                     'ano_lei_legislacao_sobre_tombamento',
                                                     'ano_lei_legislacao_sobre_uni_conservacao',
                                                     'ano_lei_legislacao_sobre_usuca_espe_imovel_urbano',
                                                     'ano_lei_legislacao_sobre_zonea_ambi_zonea_ecologico_economico',
                                                     'ano_lei_lei_perimetro_urba',
                                                     'ano_leilegislacao_sobre_conce_uso_espe_fins_moradia',
                                                     'ano_ultima_atualizacao', 'caract_orgao_gestor_plane_urba_munic',
                                                     'codigo_municipio', 'codigo_obras_existencia', 'codigo_uf',
                                                     'geocodigo', 'id_planejamento_urbano',
                                                     'informacoes_sob_gestor_escolaridade',
                                                     'legis_sobre_parc_solo_existencia',
                                                     'legislacao_sobre_area_zona_espec_inter_social_existencia',
                                                     'legislacao_sobre_conce_uso_espe_fins_moradia',
                                                     'legislacao_sobre_contri_melhoria_existencia',
                                                     'legislacao_sobre_dire_superficie',
                                                     'legislacao_sobre_estu_impa_vizinhanca_existencia',
                                                     'legislacao_sobre_estu_pre_impa_ambiental',
                                                     'legislacao_sobre_legitimacao_posse',
                                                     'legislacao_sobre_ope_urba_consorciada_existencia',
                                                     'legislacao_sobre_regula_fundiaria',
                                                     'legislacao_sobre_servi_administrativa',
                                                     'legislacao_sobre_solo_cria_outorga_onerosa_dir_construir_exist',
                                                     'legislacao_sobre_tombamento',
                                                     'legislacao_sobre_uni_conservacao',
                                                     'legislacao_sobre_usuca_espe_imovel_urbano',
                                                     'legislacao_sobre_zona_area_espe_inter_existencia',
                                                     'legislacao_sobre_zone_uso_ocupa_solo_existencia',
                                                     'legislacao_sobre_zonea_ambi_zonea_ecologico_economico',
                                                     'lei_perimetro_urba_existencia', 'nome',
                                                     'o_municipio_elabo_plano_diretor', 'plano_diretor_existencia'] )

    def test_join_operation_for_feature_resource_one_to_one_rel_accept_octet_stream(self):
        response = requests.get(self.bcim_base_uri + "municipios/3304557/join/geocodigo&geocodigo/" + self.munic_2015_base_uri + "planejamento-urbano-list/3243/",
                                headers={"accept": "application/octet-stream"})
        self.assertEquals(response.status_code, 200)
        self.assertEquals(response.headers['content-type'], 'application/octet-stream')

    def test_join_operation_for_feature_resource_one_to_many_rel(self):
        response = requests.get(self.bcim_base_uri + "municipios/3304557/join/geocodigo&cod_municipio/" + self.pib_municipio + "faturamento-list/filter/cod_municipio/eq/3304557")
        self.assertEquals(response.status_code, 200)
        self.assertEquals(response.headers['content-type'], 'application/vnd.geo+json')

        response_keys = self.aux_get_keys_from_response(response)
        self.assertEquals(response_keys, self.feature_keys)

        feature_properties_keys = self.aux_get_first_feature_properties_keys(response)
        self.assertEquals(feature_properties_keys, ['__joined__', 'anodereferencia', 'geocodigo', 'geometriaaproximada', 'nome', 'nomeabrev'])

        joined_dicts_len = self.aux_get_first_feature_joined_length(response)
        self.assertEquals(joined_dicts_len, 6)

        joined_dict_attrs = self.aux_get_first_joined_dict_attributes_from_first_feature(response)
        self.assertEquals(joined_dict_attrs, ['ano', 'cod_municipio', 'id', 'id_municipio', 'impostos_produtos',
                                              'num_habitantes', 'valor_bruto_adm', 'valor_bruto_agro',
                                              'valor_bruto_ind', 'valor_bruto_serv'])

    def test_join_operation_for_feature_resource_one_to_many_rel_accept_octet_stream(self):
        response = requests.get(self.bcim_base_uri + "municipios/3304557/join/geocodigo&cod_municipio/" + self.pib_municipio + "faturamento-list/filter/cod_municipio/eq/3304557",
                                headers={"Accept": "application/octet-stream"})
        self.assertEquals(response.status_code, 200)
        self.assertEquals(response.headers['content-type'], 'application/octet-stream')


    # --------------- TESTS FOR FEATURE COLLECTION ---------------------------------
    def test_join_operation_for_feature_collection_with_filter(self):
        response = requests.get(self.bcim_base_uri + "unidades-federativas/filter/sigla/in/RJ&ES&MG/join/geocodigo&cod_estado/" + self.pesquisa_esporte_base_url + "cond-funcionamento-list/filter/cod_estado/in/31&32&33&35/")
        self.assertEquals(response.status_code, 200)
        self.assertEquals(response.headers['content-type'], 'application/vnd.geo+json')

        response_dict_keys = self.aux_get_keys_from_response(response)
        self.assertEquals(response_dict_keys, self.feature_collection_keys)

        first_feature_keys = self.aux_get_first_feature_keys(response)
        self.assertEquals(first_feature_keys, self.feature_keys)

        first_feature_properties_keys = self.aux_get_first_feature_properties_keys(response)
        self.assertEquals(first_feature_properties_keys, ["__joined__", "geocodigo", "nome", "nomeabrev", "sigla"])

        joined_alfanumeric_attrs = self.aux_get_first_joined_dict_attributes_from_first_feature(response)
        self.assertEquals(joined_alfanumeric_attrs, ['ano', 'autodromo_func', 'autodromo_parado', 'cod_estado',
                                                     'compl_aqua_func', 'compl_aqua_parado', 'compl_esp_func',
                                                     'compl_esp_parado', 'est_func', 'est_parado', 'gin_func',
                                                     'gin_parado', 'id', 'id_estado', 'kartodromo_func',
                                                     'kartodromo_parado'] )

    def test_join_operation_for_feature_collection_with_filter_accept_octet_stream(self):
        response = requests.get(self.bcim_base_uri + "unidades-federativas/filter/sigla/in/RJ&ES&MG/join/geocodigo&cod_estado/" + self.pesquisa_esporte_base_url + "cond-funcionamento-list/filter/cod_estado/in/31&32&33&35/",
                                headers={"accept": "application/octet-stream"})
        self.assertEquals(response.status_code, 200)
        self.assertEquals(response.headers['content-type'], 'application/octet-stream')

#python manage.py test hyper_resource.tests.OptionsForJoinOperationTest --testrunner=hyper_resource.tests.NoDbTestRunner
class OptionsForJoinOperationTest(AbstractRequestTest):
    def setUp(self):
        super(OptionsForJoinOperationTest, self).setUp()
        self.pesquisa_esporte_base_url = "http://172.30.10.86/esporte-list/"
        self.munic_2015_base_uri = "http://172.30.10.86/api/munic-2015/"
        self.pib_municipio_base_uri = "http://172.30.10.86/api/pib-municipio/"
        self.keys_from_external_attr_context = ['@id', '@type', 'hydra:Link', 'hydra:method']

    # --------------- TESTS FOR FEATURE RESOURCE ---------------------------------
    # todo: provisory test, full context must be implemented
    def test_options_for_feature_resource_join_operation_one_to_one_rel(self):

        response = requests.options(self.bcim_base_uri + "municipios/3304557/join/geocodigo&geocodigo/" + self.munic_2015_base_uri + "planejamento-urbano-list/3243/")
        self.assertEquals(response.status_code, 200)

        response_keys = self.aux_get_keys_from_response(response)
        self.assertEquals(response_keys, self.simple_path_options_dict_keys)

        supported_operations_names = self.aux_get_supported_operations_names(response)
        self.assertEquals(supported_operations_names, self.spatial_operation_names)

        acontext_keys = self.aux_get_keys_from_response_context(response)
        self.assertEquals(acontext_keys, ['anodereferencia', 'geocodigo', 'geom', 'geometriaaproximada', 'id_objeto', 'iri_metadata', 'iri_style', 'nome', 'nomeabrev'])

        geocodigo_acontext_keys = self.aux_get_keys_from_acontext_attrs(response, "geocodigo")
        self.assertEquals(geocodigo_acontext_keys, self.keys_from_attrs_context)

        response_dict = self.aux_get_dict_from_response(response)
        self.assertEquals(response_dict["@type"], "Feature")


        # todo: test for join full context
        '''
        response = requests.options(self.bcim_base_uri + "municipios/3304557/join/geocodigo&geocodigo/" + self.munic_2015_base_uri + "planejamento-urbano-list/3243/")
        self.assertEquals(response.status_code, 200)

        response_keys = self.aux_get_keys_from_response(response)
        self.assertEquals(response_keys, self.non_simple_path_dict_keys)

        supported_operations_names = self.aux_get_supported_operations_names(response)
        self.assertEquals(supported_operations_names, self.spatial_operation_names)

        acontext_keys = self.aux_get_keys_from_response_context(response)
        self.assertEquals(acontext_keys, ['ano_lei_codigo_obras', 'ano_lei_criacao', 'ano_lei_legis_sob_area_zona_espe_inte_social',
                                          'ano_lei_legis_sob_zona_area_espe_inter', 'ano_lei_legis_sobre_parc_solo',
                                          'ano_lei_legis_sobre_zone_uso_ocupa_solo', 'ano_lei_legislacao_sobre_contri_melhoria',
                                          'ano_lei_legislacao_sobre_dire_superficie', 'ano_lei_legislacao_sobre_estu_impa_vizinhanca',
                                          'ano_lei_legislacao_sobre_estu_pre_impa_ambiental', 'ano_lei_legislacao_sobre_legitimacao_posse',
                                          'ano_lei_legislacao_sobre_ope_urba_consorciada', 'ano_lei_legislacao_sobre_regula_fundiaria',
                                          'ano_lei_legislacao_sobre_servi_administrativa', 'ano_lei_legislacao_sobre_solo_cria_outorga_onerosa_dir_construi',
                                          'ano_lei_legislacao_sobre_tombamento', 'ano_lei_legislacao_sobre_uni_conservacao',
                                          'ano_lei_legislacao_sobre_usuca_espe_imovel_urbano', 'ano_lei_legislacao_sobre_zonea_ambi_zonea_ecologico_economico',
                                          'ano_lei_lei_perimetro_urba', 'ano_leilegislacao_sobre_conce_uso_espe_fins_moradia',
                                          'ano_ultima_atualizacao', 'anodereferencia', 'caract_orgao_gestor_plane_urba_munic',
                                          'codigo_municipio', 'codigo_obras_existencia', 'codigo_uf', 'geocodigo', 'geom',
                                          'geometriaaproximada', 'http://172.30.10.86/api/munic-2015/planejamento-urbano-list/3243/:geocodigo',
                                          'http://172.30.10.86/api/munic-2015/planejamento-urbano-list/3243/:nome', 'id_objeto',
                                          'id_planejamento_urbano', 'informacoes_sob_gestor_escolaridade', 'iri_metadata',
                                          'iri_style', 'legis_sobre_parc_solo_existencia', 'legislacao_sobre_area_zona_espec_inter_social_existencia',
                                          'legislacao_sobre_conce_uso_espe_fins_moradia', 'legislacao_sobre_contri_melhoria_existencia',
                                          'legislacao_sobre_dire_superficie', 'legislacao_sobre_estu_impa_vizinhanca_existencia',
                                          'legislacao_sobre_estu_pre_impa_ambiental', 'legislacao_sobre_legitimacao_posse',
                                          'legislacao_sobre_ope_urba_consorciada_existencia', 'legislacao_sobre_regula_fundiaria',
                                          'legislacao_sobre_servi_administrativa', 'legislacao_sobre_solo_cria_outorga_onerosa_dir_construir_exist',
                                          'legislacao_sobre_tombamento', 'legislacao_sobre_uni_conservacao', 'legislacao_sobre_usuca_espe_imovel_urbano',
                                          'legislacao_sobre_zona_area_espe_inter_existencia', 'legislacao_sobre_zone_uso_ocupa_solo_existencia',
                                          'legislacao_sobre_zonea_ambi_zonea_ecologico_economico', 'lei_perimetro_urba_existencia', 'nome',
                                          'nomeabrev', 'o_municipio_elabo_plano_diretor', 'plano_diretor_existencia'])

        # 'geocodigo' is present in the feature and in the external resourse, hence 'geocodigo' in the external resource must be preffixed
        external_geocodigo_acontext_keys = self.aux_get_keys_from_acontext_attrs(response, "http://172.30.10.86/api/munic-2015/planejamento-urbano-list/3243/:geocodigo")
        self.assertEquals(external_geocodigo_acontext_keys, self.keys_from_external_attr_context)
        external_codigo_municipio_acontext_keys = self.aux_get_keys_from_acontext_attrs(response, "codigo_municipio")
        self.assertEquals(external_codigo_municipio_acontext_keys, self.keys_from_external_attr_context)
        # 'geocodigo' (without preffix) comes from the feature
        geocodigo_acontext_keys = self.aux_get_keys_from_acontext_attrs(response, "geocodigo")
        self.assertEquals(geocodigo_acontext_keys, self.keys_from_attrs_context)
        join_acontext_keys = self.aux_get_keys_from_acontext_attrs(response, "join")
        self.assertEquals(join_acontext_keys, self.keys_from_oper_context)

        response_dict = self.aux_get_dict_from_response(response)
        self.assertEquals(response_dict["@type"], "Feature")
        '''

    """
    def test_options_for_feature_resource_join_operation_one_to_many_rel(self):
        response = requests.options(self.bcim_base_uri + "municipios/3304557/join/geocodigo&cod_municipio/" +
                                    self.pib_municipio_base_uri + "faturamento-list/filter/cod_municipio/eq/3304557")
        self.assertEquals(response.status_code, 200)

        response_keys = self.aux_get_keys_from_response(response)
        self.assertEquals(response_keys, self.non_simple_path_dict_keys)

        supported_operations_names = self.aux_get_supported_operations_names(response)
        self.assertEquals(supported_operations_names, self.spatial_operation_names)

        acontext_keys = self.aux_get_keys_from_response_context(response)
        self.assertEquals(acontext_keys, ['ano_lei_codigo_obras', 'ano_lei_criacao', 'ano_lei_legis_sob_area_zona_espe_inte_social',
                                          'ano_lei_legis_sob_zona_area_espe_inter', 'ano_lei_legis_sobre_parc_solo',
                                          'ano_lei_legis_sobre_zone_uso_ocupa_solo', 'ano_lei_legislacao_sobre_contri_melhoria',
                                          'ano_lei_legislacao_sobre_dire_superficie', 'ano_lei_legislacao_sobre_estu_impa_vizinhanca',
                                          'ano_lei_legislacao_sobre_estu_pre_impa_ambiental', 'ano_lei_legislacao_sobre_legitimacao_posse',
                                          'ano_lei_legislacao_sobre_ope_urba_consorciada', 'ano_lei_legislacao_sobre_regula_fundiaria',
                                          'ano_lei_legislacao_sobre_servi_administrativa', 'ano_lei_legislacao_sobre_solo_cria_outorga_onerosa_dir_construi',
                                          'ano_lei_legislacao_sobre_tombamento', 'ano_lei_legislacao_sobre_uni_conservacao',
                                          'ano_lei_legislacao_sobre_usuca_espe_imovel_urbano', 'ano_lei_legislacao_sobre_zonea_ambi_zonea_ecologico_economico',
                                          'ano_lei_lei_perimetro_urba', 'ano_leilegislacao_sobre_conce_uso_espe_fins_moradia', 'ano_ultima_atualizacao',
                                          'caract_orgao_gestor_plane_urba_munic', 'codigo_municipio', 'codigo_obras_existencia',
                                          'codigo_uf', 'http://172.30.10.86/api/pib-municipio/faturamento-list:geocodigo', 'id_planejamento_urbano',
                                          'informacoes_sob_gestor_escolaridade', 'legis_sobre_parc_solo_existencia',
                                          'legislacao_sobre_area_zona_espec_inter_social_existencia', 'legislacao_sobre_conce_uso_espe_fins_moradia',
                                          'legislacao_sobre_contri_melhoria_existencia', 'legislacao_sobre_dire_superficie',
                                          'legislacao_sobre_estu_impa_vizinhanca_existencia', 'legislacao_sobre_estu_pre_impa_ambiental',
                                          'legislacao_sobre_legitimacao_posse', 'legislacao_sobre_ope_urba_consorciada_existencia',
                                          'legislacao_sobre_regula_fundiaria', 'legislacao_sobre_servi_administrativa',
                                          'legislacao_sobre_solo_cria_outorga_onerosa_dir_construir_exist', 'legislacao_sobre_tombamento',
                                          'legislacao_sobre_uni_conservacao', 'legislacao_sobre_usuca_espe_imovel_urbano',
                                          'legislacao_sobre_zona_area_espe_inter_existencia', 'legislacao_sobre_zone_uso_ocupa_solo_existencia',
                                          'legislacao_sobre_zonea_ambi_zonea_ecologico_economico', 'lei_perimetro_urba_existencia', '(joined) nome', # same attribute name on different resources
                                          'o_municipio_elabo_plano_diretor', 'plano_diretor_existencia',
                                          'anodereferencia', 'geocodigo', 'geom', 'geometriaaproximada', 'id_objeto', 'iri_metadata', 'iri_style', 'nome', 'nomeabrev', 'spatialize'])

        response_dict = self.aux_get_dict_from_response(response)
        self.assertEquals(response_dict["@type"], "Feature")

    def test_options_for_feature_resource_join_operation__one_to_one_rel_accept_octet_stream(self):
        response = requests.options(self.bcim_base_uri + "municipios/3304557/join/geocodigo&geocodigo/" + self.munic_2015_base_uri + "planejamento-urbano-list/3243/",
                                    headers={"Accept": "application/octet-stream"})
        self.assertEquals(response.status_code, 200)

        response_keys = self.aux_get_keys_from_response(response)
        self.assertEquals(response_keys, self.non_simple_path_dict_keys)

        supported_operations_names = self.aux_get_supported_operations_names(response)
        self.assertEquals(supported_operations_names, self.spatial_operation_names)

        acontext_keys = self.aux_get_keys_from_response_context(response)
        self.assertEquals(acontext_keys, ['(joined) ano_lei_codigo_obras', '(joined) ano_lei_criacao', '(joined) ano_lei_legis_sob_area_zona_espe_inte_social',
                                          '(joined) ano_lei_legis_sob_zona_area_espe_inter', '(joined) ano_lei_legis_sobre_parc_solo',
                                          '(joined) ano_lei_legis_sobre_zone_uso_ocupa_solo', '(joined) ano_lei_legislacao_sobre_contri_melhoria',
                                          '(joined) ano_lei_legislacao_sobre_dire_superficie', '(joined) ano_lei_legislacao_sobre_estu_impa_vizinhanca',
                                          '(joined) ano_lei_legislacao_sobre_estu_pre_impa_ambiental', '(joined) ano_lei_legislacao_sobre_legitimacao_posse',
                                          '(joined) ano_lei_legislacao_sobre_ope_urba_consorciada', '(joined) ano_lei_legislacao_sobre_regula_fundiaria',
                                          '(joined) ano_lei_legislacao_sobre_servi_administrativa', '(joined) ano_lei_legislacao_sobre_solo_cria_outorga_onerosa_dir_construi',
                                          '(joined) ano_lei_legislacao_sobre_tombamento', '(joined) ano_lei_legislacao_sobre_uni_conservacao',
                                          '(joined) ano_lei_legislacao_sobre_usuca_espe_imovel_urbano', '(joined) ano_lei_legislacao_sobre_zonea_ambi_zonea_ecologico_economico',
                                          '(joined) ano_lei_lei_perimetro_urba', '(joined) ano_leilegislacao_sobre_conce_uso_espe_fins_moradia', '(joined) ano_ultima_atualizacao',
                                          '(joined) caract_orgao_gestor_plane_urba_munic', '(joined) codigo_municipio', '(joined) codigo_obras_existencia',
                                          '(joined) codigo_uf', '(joined) geocodigo', '(joined) id_planejamento_urbano',
                                          '(joined) informacoes_sob_gestor_escolaridade', '(joined) legis_sobre_parc_solo_existencia',
                                          '(joined) legislacao_sobre_area_zona_espec_inter_social_existencia', '(joined) legislacao_sobre_conce_uso_espe_fins_moradia',
                                          '(joined) legislacao_sobre_contri_melhoria_existencia', '(joined) legislacao_sobre_dire_superficie',
                                          '(joined) legislacao_sobre_estu_impa_vizinhanca_existencia', '(joined) legislacao_sobre_estu_pre_impa_ambiental',
                                          '(joined) legislacao_sobre_legitimacao_posse', '(joined) legislacao_sobre_ope_urba_consorciada_existencia',
                                          '(joined) legislacao_sobre_regula_fundiaria', '(joined) legislacao_sobre_servi_administrativa',
                                          '(joined) legislacao_sobre_solo_cria_outorga_onerosa_dir_construir_exist', '(joined) legislacao_sobre_tombamento',
                                          '(joined) legislacao_sobre_uni_conservacao', '(joined) legislacao_sobre_usuca_espe_imovel_urbano',
                                          '(joined) legislacao_sobre_zona_area_espe_inter_existencia', '(joined) legislacao_sobre_zone_uso_ocupa_solo_existencia',
                                          '(joined) legislacao_sobre_zonea_ambi_zonea_ecologico_economico', '(joined) lei_perimetro_urba_existencia', '(joined) nome', # same attribute name on different resources
                                          '(joined) o_municipio_elabo_plano_diretor', '(joined) plano_diretor_existencia',
                                          'anodereferencia', 'geocodigo', 'geom', 'geometriaaproximada', 'id_objeto', 'iri_metadata', 'iri_style', 'nome', 'nomeabrev', 'spatialize'])

        response_dict = self.aux_get_dict_from_response(response)
        self.assertEquals(response_dict["@type"], "Geobuf")

    # --------------- TESTS FOR FEATURE COLLECTION ---------------------------------
    def test_join_operation_with_filter(self):
        response = requests.options(self.bcim_base_uri + "unidades-federativas/filter/sigla/in/RJ&ES&MG/join/geocodigo&cod_estado/" +
                                    self.pesquisa_esporte_base_url + "cond-funcionamento-list/filter/cod_estado/in/31&32&33&35/")
        self.assertEquals(response.status_code, 200)

        response_dict_keys = self.aux_get_keys_from_response(response)
        self.assertEquals(response_dict_keys, self.non_simple_path_dict_keys)

        acontext_keys = self.aux_get_keys_from_response_context(response)
        self.assertEquals(acontext_keys, ["join"])

        join_context_keys_list = self.aux_get_keys_from_acontext_attrs(response, 'join')
        self.assertListEqual(join_context_keys_list, ["@id", "@type"])

        supported_operations_names = self.aux_get_supported_operations_names(response)
        self.assertListEqual(supported_operations_names, self.spatial_collection_operation_names)

        response_dict = self.aux_get_dict_from_response(response)
        self.assertEquals(response_dict["@type"], 'FeatureCollection')
    """

#python manage.py test hyper_resource.tests.PaginationTest --testrunner=hyper_resource.tests.NoDbTestRunner
class PaginationTest(AbstractRequestTest):
    '''
    def test_collection_simple_path_pagination(self):
        response = requests.get(self.controle_base_uri + "gasto-list/")
        self.assertEquals(response.status_code, 200)
        # the string must be hardcoded, if not, the test fails
        expected_link = '<http://luc00557196:8000/controle-list/>; rel="up" , <http://luc00557196:8000/controle-list/gasto-list.jsonld>; rel="http://www.w3.org/ns/json-ld#context"; type="application/ld+json" , <http://luc00557196:8000/controle-list/gasto-list/offset_limit/101&100>; rel="next" '
        #expected_link = '<' + HOST + 'api/bcim/>; rel="up" , <' + HOST + 'api/bcim/aldeias-indigenas.jsonld>; rel="http://www.w3.org/ns/json-ld#context"; type="application/ld+json" , <' + HOST + 'api/bcim/aldeias-indigenas/offset_limit/101&100>; rel="next" '
        self.assertEquals(response.headers["link"], expected_link)
    '''

    '''
    def test_feature_collection_simle_path_ordering_by_geometry_longitude(self):
        response = requests.get(self.bcim_base_uri + "unidades-federativas/order_by/geom")
        self.assertEquals(response.status_code, 200)

        response_dict = self.aux_get_dict_from_response(response)
        features_names_ordered_by_longitude = [ uf['properties']['nome'] for uf in response_dict['features'] ]
        expected_names_ordered_by_longitude = ['Acre', 'Amazonas', 'Rondônia', 'Roraima', 'Mato Grosso', 'Pará',
                                               'Mato Grosso do Sul', 'Rio Grande do Sul', 'Amapá', 'Paraná',
                                               'Santa Catarina', 'Goiás', 'São Paulo', 'Minas Gerais', 'Tocantins',
                                               'Maranhão', 'Distrito Federal', 'Bahia', 'Piauí', 'Rio de Janeiro',
                                               'Espírito Santo', 'Ceará', 'Pernambuco', 'Paraíba', 'Rio Grande do Norte',
                                               'Sergipe', 'Alagoas']
        self.assertListEqual(features_names_ordered_by_longitude, expected_names_ordered_by_longitude)
    '''

    def test_options_for_collection_simple_path_pagination(self):
        response = requests.options(self.controle_base_uri + "gasto-list/")
        self.assertEquals(response.status_code, 200)
        expected_link = '<http://luc00557196:8000/controle-list/>; rel="up" , <http://luc00557196:8000/controle-list/gasto-list.jsonld>; rel="http://www.w3.org/ns/json-ld#context"; type="application/ld+json" , <http://luc00557196:8000/controle-list/gasto-list/offset_limit/1001&1000>; rel="next" '
        self.assertEquals(response.headers["link"], expected_link)

    def test_collection_pagination_with_offset_limit_operation(self):
        response = requests.get(self.controle_base_uri + "gasto-list/offset_limit/1001&1000")
        self.assertEquals(response.status_code, 200)
        expected_link = '<http://luc00557196:8000/controle-list/>; rel="up" , <http://luc00557196:8000/controle-list/gasto-list/offset_limit/1001&1000.jsonld>; rel="http://www.w3.org/ns/json-ld#context"; type="application/ld+json" , <http://luc00557196:8000/controle-list/gasto-list/offset_limit/2001&1000>; rel="next" '
        self.assertEquals(response.headers["link"], expected_link)

    def test_options_for_collection_pagination_with_offset_limit_operation(self):
        response = requests.options(self.controle_base_uri + "gasto-list/offset_limit/1001&1000")
        self.assertEquals(response.status_code, 200)
        expected_link = '<http://luc00557196:8000/controle-list/>; rel="up" , <http://luc00557196:8000/controle-list/gasto-list/offset_limit/1001&1000.jsonld>; rel="http://www.w3.org/ns/json-ld#context"; type="application/ld+json" , <http://luc00557196:8000/controle-list/gasto-list/offset_limit/2001&1000>; rel="next" '
        self.assertEquals(response.headers["link"], expected_link)

    # Pagination for feature collection must be specific for each case
    # In this specific "aldeias-indigenas" case we are dealing with Poits and don't make sense paginate about 200 Points
    def test_feature_collection_simple_path_pagination(self):
        response = requests.get(self.bcim_base_uri + "aldeias-indigenas/")
        self.assertEquals(response.status_code, 200)
        expected_link = '<http://luc00557196:8000/api/bcim/aldeias-indigenas/offset_limit/1001&100>; rel="next" '
        self.assertNotIn(expected_link, response.headers["link"])

