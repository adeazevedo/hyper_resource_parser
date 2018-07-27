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

#python manage.py test hyper_resource.tests.CollectOperationTest --testrunner=hyper_resource.tests.NoDbTestRunner
class CollectOperationTest(SimpleTestCase):
    def setUp(self):
        self.bcim_base_uri = "http://" + HOST + "api/bcim/"
        self.feature_collection_keys = ["features", "type"]
        self.geometry_collection_keys = ["geometries", "type"]
        self.feature_keys = ["geometry", "properties", "type"]
        self.geometry_keys = ["coordinates", "type"]

    # tests auxiliary functions
    def aux_get_dict_from_response(self, response):
        json_response = json.loads(response.text)
        return dict(json_response)

    def aux_get_list_from_response(self, response):
        json_response = json.loads(response.text)
        return list(json_response)

    def aux_get_keys_from_response(self, response):
        response_dict = self.aux_get_dict_from_response(response)
        response_dict_keys = list(response_dict.keys())
        response_dict_keys.sort()
        return response_dict_keys

    def aux_get_keys_from_first_feature(self, response):
        response_dict = self.aux_get_dict_from_response(response)
        first_feature = response_dict["features"][0]
        first_feature_keys = list(first_feature.keys())
        first_feature_keys.sort()
        return first_feature_keys

    def aux_get_keys_from_first_element(self, response):
        response_list = self.aux_get_list_from_response(response)
        first_element_keys = list(response_list[0].keys())
        first_element_keys.sort()
        return first_element_keys

    def aux_get_keys_from_first_geometry(self, response):
        response_dict = self.aux_get_dict_from_response(response)
        first_geometry = response_dict["geometries"][0]
        first_geometry_keys = list(first_geometry.keys())
        first_geometry_keys.sort()
        return first_geometry_keys

    # FeatureCollection return
    def test_collect_operation_with_feature_collection_return(self):
        response = requests.get(self.bcim_base_uri + "aldeias-indigenas/collect/nome&geom/buffer/0.2/")
        self.assertEquals(response.status_code, 200)

        response_dict_keys = self.aux_get_keys_from_response(response)
        self.assertEquals(response_dict_keys, self.feature_collection_keys)

        first_feature_keys = self.aux_get_keys_from_first_feature(response)
        self.assertEquals(first_feature_keys, self.feature_keys)

    def test_collect_operation_with_feature_collection_return_accept_header(self):
        response = requests.get(self.bcim_base_uri + "aldeias-indigenas/collect/nome&geom/buffer/0.2/",
                                headers={'Accept': 'application/octet-stream'})
        self.assertEquals(response.status_code, 200)
        self.assertEquals(response.headers['content-type'], 'application/octet-stream')

    def test_collect_operation_with_non_spatial_operation_and_feature_collection_return(self):
        response = requests.get(self.bcim_base_uri + "aldeias-indigenas/collect/geom&nome/upper")
        self.assertEquals(response.status_code, 200)

        response_dict_keys = self.aux_get_keys_from_response(response)
        self.assertEquals(response_dict_keys, self.feature_collection_keys)

        first_feature_keys = self.aux_get_keys_from_first_feature(response)
        self.assertEquals(first_feature_keys, self.feature_keys)

        response_dict = self.aux_get_dict_from_response(response)
        self.assertEquals(list(response_dict["features"][0]["properties"].keys()), ["upper"]) # possible conceitual error

    def test_collect_operation_with_non_spatial_operation_and_feature_collection_return_accept_header(self):
        response = requests.get(self.bcim_base_uri + "aldeias-indigenas/collect/geom&nome/upper",
                                headers={'Accept': 'application/octet-stream'})
        self.assertEquals(response.status_code, 200)
        self.assertEquals(response.headers['content-type'], 'application/octet-stream')

    # GeometryCollection
    def test_collect_operation_with_geomtry_collection_return(self):
        response = requests.get(self.bcim_base_uri + "aldeias-indigenas/collect/geom/buffer/0.2/")
        self.assertEquals(response.status_code, 200)

        response_dict_keys = self.aux_get_keys_from_response(response)
        self.assertEquals(response_dict_keys, self.geometry_collection_keys)

        first_geometry_keys = self.aux_get_keys_from_first_geometry(response)
        self.assertEquals(first_geometry_keys, self.geometry_keys)

    def test_collect_operation_with_geomtry_collection_return_accept_header(self):
        response = requests.get(self.bcim_base_uri + "aldeias-indigenas/collect/geom/buffer/0.2/",
                                headers={'Accept': 'application/octet-stream'})
        self.assertEquals(response.status_code, 200)
        self.assertEquals(response.headers['content-type'], 'application/octet-stream')

    # list return
    def test_collect_operation_with_spatial_operation_and_float_return(self):
        response = requests.get(self.bcim_base_uri + "aldeias-indigenas/collect/nome&geom/area")
        self.assertEquals(response.status_code, 200)

        first_element_keys = self.aux_get_keys_from_first_element(response)
        self.assertEquals(first_element_keys, ["area", "nome"])

    def test_collect_operation_with_spatial_operation_and_float_return_accept_header(self):
        response = requests.get(self.bcim_base_uri + "aldeias-indigenas/collect/nome&geom/area",
                                headers={'Accept': 'application/octet-stream'})
        self.assertEquals(response.status_code, 200)
        self.assertEquals(response.headers['content-type'], 'application/octet-stream')

    def test_collect_operation_with_alphanumeric_operation(self):
        response = requests.get(self.bcim_base_uri + "aldeias-indigenas/collect/nome/upper")
        self.assertEquals(response.status_code, 200)

        first_element_keys = self.aux_get_keys_from_first_element(response)
        self.assertEquals(first_element_keys, ["upper"])

    def test_collect_operation_with_alphanumeric_operation_accept_header(self):
        response = requests.get(self.bcim_base_uri + "aldeias-indigenas/collect/nome/upper",
                                headers={'Accept': 'application/octet-stream'})
        self.assertEquals(response.status_code, 200)
        self.assertEquals(response.headers['content-type'], 'application/octet-stream')

    # projection
    def test_collect_operation_with_projection(self):
        response = requests.get(self.bcim_base_uri + "aldeias-indigenas/projection/nome,geom/collect/nome&geom/buffer/0.5")
        self.assertEquals(response.status_code, 200)

        response_keys = self.aux_get_keys_from_response(response)
        self.assertListEqual(response_keys, self.feature_collection_keys)

        first_feature_keys = self.aux_get_keys_from_first_feature(response)
        self.assertListEqual(first_feature_keys, self.feature_keys)

        response_dict = self.aux_get_dict_from_response(response)
        self.assertEquals(list(response_dict["features"][0]["properties"].keys()), ["nome"])

    def test_collect_operation_with_projection_accept_header(self):
        response = requests.get(self.bcim_base_uri + "aldeias-indigenas/collect/nome/upper",
                                headers={'Accept': 'application/octet-stream'})
        self.assertEquals(response.status_code, 200)
        self.assertEquals(response.headers['content-type'], 'application/octet-stream')

    def test_collect_operation_with_projection_diferent_from_collect_attrs(self):
        response = requests.get(self.bcim_base_uri + "aldeias-indigenas/projection/geom/collect/nome&geom/buffer/0.5")
        self.assertEquals(response.status_code, 400)

#python manage.py test hyper_resource.tests.RequestOptionsTest --testrunner=hyper_resource.tests.NoDbTestRunner
class RequestOptionsTest(SimpleTestCase):
    def setUp(self):
        #self.host = 'luc00557196.ibge.gov.br:8000/'
        #self.host = '192.168.0.10:8000/'
        self.bcim_base_uri = "http://" + HOST + "api/bcim/"
        self.controle_base_uri = "http://" + HOST + "controle-list/"
        self.simple_path_options_dict_keys = ['@context', '@id', '@type', 'hydra:iriTemplate', 'hydra:representationName', 'hydra:supportedOperations', 'hydra:supportedProperties']
        self.context_dict_keys = ["@context", '@id', '@type', 'hydra:supportedOperations']
        self.keys_from_attrs_context = ["@id", "@type", "hydra:supportedOperations"]
        self.spatial_operation_names = ['area', 'boundary', 'buffer', 'centroid', 'contains', 'convex_hull', 'coord_seq', 'coords', 'count', 'crosses',
                                        'crs', 'difference', 'dims', 'disjoint', 'distance', 'empty', 'envelope', 'equals', 'equals_exact', 'ewkb',
                                        'ewkt', 'extend', 'extent', 'geojson', 'geom_type', 'geom_typeid', 'get_coords', 'get_srid', 'get_x', 'get_y',
                                        'get_z', 'has_cs', 'hasz', 'hex', 'hexewkb', 'index', 'interpolate', 'intersection', 'intersects', 'json', 'kml',
                                        'length', 'normalize', 'num_coords', 'num_geom', 'num_points', 'ogr', 'overlaps', 'point_on_surface', 'relate',
                                        'relate_pattern', 'ring', 'set_coords', 'set_srid', 'set_x', 'set_y', 'set_z', 'simple', 'simplify', 'spatialize', 'srid',
                                        'srs', 'sym_difference', 'touches', 'transform', 'union', 'valid', 'valid_reason', 'within', 'wkb', 'wkt', 'x', 'y', 'z']
        self.spatial_collection_operation_names = ['bbcontains', 'bboverlaps', 'collect', 'contained', 'contains', 'contains_properly', 'count_resource',
                                                    'covers', 'covers_by', 'crosses', 'disjoint', 'distance_gt', 'distance_gte', 'distance_lt', 'distance_lte',
                                                    'distinct', 'dwithin', 'extent', 'filter', 'group_by', 'group_by_count', 'intersects', 'isvalid', 'left',
                                                    'make_line', 'offset_limit', 'overlaps', 'overlaps_above', 'overlaps_below', 'overlaps_left', 'overlaps_right',
                                                   'relate', 'right', 'spatialize', 'strictly_above', 'strictly_below', 'touches', 'union', 'within']
        self.basic_operations_names = ['spatialize']
        self.collection_operation_names = ['collect', 'count_resource', 'distinct', 'filter', 'group_by', 'group_by_count', 'offset_limit', 'spatialize']
        self.operators_names = ['between', 'eq', 'gt', 'gte', 'in', 'isnotnull', 'isnull', 'like', 'lt', 'lte', 'neq', 'notin', 'notlike']

    def aux_get_dict_from_response(self, response):
        json_response = json.loads(response.text)
        return dict(json_response)

    def aux_get_supported_operations_names(self, response):
        response_dict = self.aux_get_dict_from_response(response)
        operations_names = [operation_dict['hydra:operation'] for operation_dict in response_dict['hydra:supportedOperations']]
        operations_names.sort()
        return operations_names

    def aux_get_keys_from_response(self, response):
        response_dict = self.aux_get_dict_from_response(response)
        response_dict_keys = list(response_dict.keys())
        response_dict_keys.sort()
        return response_dict_keys

    def aux_get_keys_from_response_context(self, response):
        response_dict = self.aux_get_dict_from_response(response)
        context_keys = list(response_dict["@context"].keys())
        context_keys.sort()
        return context_keys

    def aux_get_attrs_context_keys_list_from_attr(self, response, attr_name):
        response_dict = self.aux_get_dict_from_response(response)
        context_dict = response_dict["@context"]
        attrs_context_keys_list = list( context_dict[attr_name].keys() )
        attrs_context_keys_list.sort()
        return attrs_context_keys_list


    # --------------- TESTS FOR FEATURE COLLECTION ---------------------------------
    # tests for feature/geometry collection simple path
    def test_options_for_feature_collection_simple_path(self):
        response = requests.options(self.bcim_base_uri + "aldeias-indigenas/")
        self.assertEquals(response.status_code, 200)

        response_keys = self.aux_get_keys_from_response(response)
        self.assertListEqual(response_keys, self.simple_path_options_dict_keys)

        id_objeto_context_keys_list = self.aux_get_attrs_context_keys_list_from_attr(response, "id_objeto")
        self.assertListEqual(id_objeto_context_keys_list, self.keys_from_attrs_context)
        nome_context_keys_list = self.aux_get_attrs_context_keys_list_from_attr(response, "nome")
        self.assertListEqual(nome_context_keys_list, self.keys_from_attrs_context)
        nomeabrev_context_keys_list = self.aux_get_attrs_context_keys_list_from_attr(response, "nomeabrev")
        self.assertListEqual(nomeabrev_context_keys_list, self.keys_from_attrs_context)
        geometriaaproximada_context_keys_list = self.aux_get_attrs_context_keys_list_from_attr(response, "geometriaaproximada")
        self.assertListEqual(geometriaaproximada_context_keys_list, self.keys_from_attrs_context)
        codigofunai_context_keys_list = self.aux_get_attrs_context_keys_list_from_attr(response, "codigofunai")
        self.assertListEqual(codigofunai_context_keys_list, self.keys_from_attrs_context)
        terraindigena_context_keys_list = self.aux_get_attrs_context_keys_list_from_attr(response, "terraindigena")
        self.assertListEqual(terraindigena_context_keys_list, self.keys_from_attrs_context)
        etnia_context_keys_list = self.aux_get_attrs_context_keys_list_from_attr(response, "etnia")
        self.assertListEqual(etnia_context_keys_list, self.keys_from_attrs_context)
        geom_context_keys_list = self.aux_get_attrs_context_keys_list_from_attr(response, "geom")
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

        id_objeto_context_keys_list = self.aux_get_attrs_context_keys_list_from_attr(response, "id_objeto")
        self.assertListEqual(id_objeto_context_keys_list, self.keys_from_attrs_context)
        nome_context_keys_list = self.aux_get_attrs_context_keys_list_from_attr(response, "nome")
        self.assertListEqual(nome_context_keys_list, self.keys_from_attrs_context)
        nomeabrev_context_keys_list = self.aux_get_attrs_context_keys_list_from_attr(response, "nomeabrev")
        self.assertListEqual(nomeabrev_context_keys_list, self.keys_from_attrs_context)
        geometriaaproximada_context_keys_list = self.aux_get_attrs_context_keys_list_from_attr(response, "geometriaaproximada")
        self.assertListEqual(geometriaaproximada_context_keys_list, self.keys_from_attrs_context)
        codigofunai_context_keys_list = self.aux_get_attrs_context_keys_list_from_attr(response, "codigofunai")
        self.assertListEqual(codigofunai_context_keys_list, self.keys_from_attrs_context)
        terraindigena_context_keys_list = self.aux_get_attrs_context_keys_list_from_attr(response, "terraindigena")
        self.assertListEqual(terraindigena_context_keys_list, self.keys_from_attrs_context)
        etnia_context_keys_list = self.aux_get_attrs_context_keys_list_from_attr(response, "etnia")
        self.assertListEqual(etnia_context_keys_list, self.keys_from_attrs_context)
        geom_context_keys_list = self.aux_get_attrs_context_keys_list_from_attr(response, "geom")
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
        self.assertListEqual(response_dict_keys, self.context_dict_keys)

        context_keys = self.aux_get_keys_from_response_context(response)
        self.assertListEqual(context_keys, attrs)

        nome_context_keys_list = self.aux_get_attrs_context_keys_list_from_attr(response, "nome")
        self.assertListEqual(nome_context_keys_list, self.keys_from_attrs_context)
        geom_context_keys_list = self.aux_get_attrs_context_keys_list_from_attr(response, "geom")
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
        self.assertListEqual(response_dict_keys, self.context_dict_keys)

        context_keys = self.aux_get_keys_from_response_context(response)
        self.assertListEqual(context_keys, attrs)

        nome_context_keys_list = self.aux_get_attrs_context_keys_list_from_attr(response, "nome")
        self.assertListEqual(nome_context_keys_list, self.keys_from_attrs_context)
        geom_context_keys_list = self.aux_get_attrs_context_keys_list_from_attr(response, "geom")
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
        self.assertListEqual(response_dict_keys, self.context_dict_keys)

        context_keys = self.aux_get_keys_from_response_context(response)
        self.assertListEqual(context_keys, attrs)

        geom_context_keys_list = self.aux_get_attrs_context_keys_list_from_attr(response, "geom")
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
        self.assertListEqual(response_dict_keys, self.context_dict_keys)

        context_keys = self.aux_get_keys_from_response_context(response)
        self.assertListEqual(context_keys, attrs)

        geom_context_keys_list = self.aux_get_attrs_context_keys_list_from_attr(response, "geom")
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
        self.assertListEqual(response_dict_keys, self.context_dict_keys)

        context_dict_keys = self.aux_get_keys_from_response_context(response)
        self.assertListEqual(context_dict_keys, alpha_attrs)

        nome_context_keys_list = self.aux_get_attrs_context_keys_list_from_attr(response, "nome")
        self.assertListEqual(nome_context_keys_list, self.keys_from_attrs_context)
        nomeabrev_context_keys_list = self.aux_get_attrs_context_keys_list_from_attr(response, "nomeabrev")
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
        self.assertListEqual(response_dict_keys, self.context_dict_keys)

        context_dict_keys = self.aux_get_keys_from_response_context(response)
        self.assertListEqual(context_dict_keys, alpha_attrs)

        nome_context_keys_list = self.aux_get_attrs_context_keys_list_from_attr(response, "nome")
        self.assertListEqual(nome_context_keys_list, self.keys_from_attrs_context)
        nomeabrev_context_keys_list = self.aux_get_attrs_context_keys_list_from_attr(response, "nomeabrev")
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
        self.assertListEqual(response_dict_keys, self.context_dict_keys)

        context_dict_keys = self.aux_get_keys_from_response_context(response)
        self.assertListEqual(context_dict_keys, ['within'])

        supp_oper_for_ret_type = self.aux_get_supported_operations_names(response)
        self.assertEquals(supp_oper_for_ret_type, self.spatial_collection_operation_names)

        response_dict = self.aux_get_dict_from_response(response)
        self.assertEquals(response_dict["@type"], 'FeatureCollection')

    def test_options_for_feature_collection_operation_with_geometry_collection_return_and_accept_header(self):
        response = requests.options(
            self.bcim_base_uri + "aldeias-indigenas/within/" + self.bcim_base_uri + "unidades-federativas/ES",
            headers={'accept': 'application/octet-stream'}
        )
        self.assertEquals(response.status_code, 200)

        response_dict_keys = self.aux_get_keys_from_response(response)
        self.assertListEqual(response_dict_keys, self.context_dict_keys)

        context_dict_keys = self.aux_get_keys_from_response_context(response)
        self.assertListEqual(context_dict_keys, ['within'])

        supp_oper_for_ret_type = self.aux_get_supported_operations_names(response)
        self.assertEquals(supp_oper_for_ret_type, self.spatial_collection_operation_names)

        response_dict = self.aux_get_dict_from_response(response)
        self.assertEquals(response_dict["@type"], 'GeobufCollection')

    def test_options_for_feature_collection_operation_with_integer_return(self):
        response = requests.options(self.bcim_base_uri + "aldeias-indigenas/count_resource")
        self.assertEquals(response.status_code, 200)

        response_dict_keys = self.aux_get_keys_from_response(response)
        self.assertListEqual(response_dict_keys, self.context_dict_keys)

        supp_oper_for_ret_type = self.aux_get_supported_operations_names(response)
        self.assertEquals(supp_oper_for_ret_type, [])

        context_dict_keys = self.aux_get_keys_from_response_context(response)
        self.assertListEqual(context_dict_keys, ['count_resource'])

        response_dict = self.aux_get_dict_from_response(response)
        self.assertEquals(response_dict["@type"], 'int')

    def test_options_for_feature_collection_operation_with_integer_return_and_accept_header(self):
        response = requests.options(self.bcim_base_uri + "aldeias-indigenas/count_resource",
                                    headers={'accept': 'application/octet-stream'})
        self.assertEquals(response.status_code, 200)

        response_dict_keys = self.aux_get_keys_from_response(response)
        self.assertListEqual(response_dict_keys, self.context_dict_keys)

        supp_oper_for_ret_type = self.aux_get_supported_operations_names(response)
        self.assertEquals(supp_oper_for_ret_type, [])

        context_dict_keys = self.aux_get_keys_from_response_context(response)
        self.assertListEqual(context_dict_keys, ['count_resource'])

        response_dict = self.aux_get_dict_from_response(response)
        self.assertEquals(response_dict["@type"], 'bytes')


    # tests for feature/geometry collection collect operation
    def test_options_collect_for_feature_collection_with_spatial_operation_geometry_return_type(self):
        attrs = ["geom", "nome"]
        response = requests.options(self.bcim_base_uri + "aldeias-indigenas/collect/" + attrs[1] + "&" + attrs[0] + "/buffer/0.2")
        self.assertEquals(response.status_code, 200)

        response_dict_keys = self.aux_get_keys_from_response(response)
        self.assertListEqual(response_dict_keys, self.context_dict_keys)

        context_dict_keys = self.aux_get_keys_from_response_context(response)
        attrs.append('buffer')
        attrs.sort()
        self.assertListEqual(context_dict_keys, attrs)

        nome_context_keys_list = self.aux_get_attrs_context_keys_list_from_attr(response, "nome")
        self.assertListEqual(nome_context_keys_list, self.keys_from_attrs_context)
        geom_context_keys_list = self.aux_get_attrs_context_keys_list_from_attr(response, "geom")
        self.assertListEqual(geom_context_keys_list, self.keys_from_attrs_context)
        buffer_context_keys_list = self.aux_get_attrs_context_keys_list_from_attr(response, "buffer")
        self.assertListEqual(buffer_context_keys_list, ["@id", "@type"])

        response_operations_name = self.aux_get_supported_operations_names(response)
        self.assertListEqual(response_operations_name, self.spatial_collection_operation_names)

        response_dict = self.aux_get_dict_from_response(response)
        self.assertEquals(response_dict["@type"], 'FeatureCollection')

    def test_options_collect_for_feature_collection_with_string_operation(self):
        attrs = ["geom", "sigla"]
        response = requests.options(self.bcim_base_uri + "unidades-federativas/collect/" + attrs[0] + "&" + attrs[1] + "/lower")
        self.assertEquals(response.status_code, 200)

        response_dict_keys = self.aux_get_keys_from_response(response)
        self.assertListEqual(response_dict_keys, self.context_dict_keys)

        context_dict_keys = self.aux_get_keys_from_response_context(response)
        attrs.append('lower')
        attrs.sort()
        self.assertListEqual(context_dict_keys, attrs)

        nome_context_keys_list = self.aux_get_attrs_context_keys_list_from_attr(response, "sigla")
        self.assertListEqual(nome_context_keys_list, self.keys_from_attrs_context)
        geom_context_keys_list = self.aux_get_attrs_context_keys_list_from_attr(response, "geom")
        self.assertListEqual(geom_context_keys_list, self.keys_from_attrs_context)
        upper_context_keys_list = self.aux_get_attrs_context_keys_list_from_attr(response, "lower")
        self.assertListEqual(upper_context_keys_list, ["@id", "@type"])

        response_operations_name = self.aux_get_supported_operations_names(response)
        self.assertListEqual(response_operations_name, self.spatial_collection_operation_names)

        response_dict = self.aux_get_dict_from_response(response)
        self.assertEquals(response_dict["@type"], 'FeatureCollection')

    def test_options_collect_for_feature_collection_with_spatial_operation_geometry_return_type_and_only_geometric_attribute(self):
        attrs = ["geom"]
        response = requests.options(
            self.bcim_base_uri + "aldeias-indigenas/collect/" + attrs[0] + "/buffer/0.2")
        self.assertEquals(response.status_code, 200)

        response_dict_keys = self.aux_get_keys_from_response(response)
        self.assertListEqual(response_dict_keys, self.context_dict_keys)

        context_dict_keys = self.aux_get_keys_from_response_context(response)
        attrs.append('buffer')
        attrs.sort()
        self.assertListEqual(context_dict_keys, attrs)

        geom_context_keys_list = self.aux_get_attrs_context_keys_list_from_attr(response, "geom")
        self.assertListEqual(geom_context_keys_list, self.keys_from_attrs_context)
        buffer_context_keys_list = self.aux_get_attrs_context_keys_list_from_attr(response, "buffer")
        self.assertListEqual(buffer_context_keys_list, ["@id", "@type"])

        response_operations_name = self.aux_get_supported_operations_names(response)
        self.assertListEqual(response_operations_name, self.spatial_collection_operation_names)

        response_dict = self.aux_get_dict_from_response(response)
        self.assertEquals(response_dict["@type"], 'GeometryCollection')

    def test_options_collect_for_feature_collection_with_string_operation_and_only_string_attribute(self):
        attrs = ["nome"]
        response = requests.options(self.bcim_base_uri + "aldeias-indigenas/collect/" + attrs[0] + "/upper")
        self.assertEquals(response.status_code, 200)

        response_dict_keys = self.aux_get_keys_from_response(response)
        self.assertListEqual(response_dict_keys, self.context_dict_keys)

        context_dict_keys = self.aux_get_keys_from_response_context(response)
        attrs.append('upper')
        attrs.sort()
        self.assertListEqual(context_dict_keys, attrs)

        geom_context_keys_list = self.aux_get_attrs_context_keys_list_from_attr(response, "nome")
        self.assertListEqual(geom_context_keys_list, self.keys_from_attrs_context)
        buffer_context_keys_list = self.aux_get_attrs_context_keys_list_from_attr(response, "upper")
        self.assertListEqual(buffer_context_keys_list, ["@id", "@type"])

        response_operations_name = self.aux_get_supported_operations_names(response)
        self.assertListEqual(response_operations_name, self.collection_operation_names)

        response_dict = self.aux_get_dict_from_response(response)
        self.assertEquals(response_dict["@type"], 'Collection')

    def test_options_collect_for_feature_collection_with_spatial_operation_geometry_return_type_and_accept_header(self):
        attrs = ["geom", "nome"]
        response = requests.options(
            self.bcim_base_uri + "aldeias-indigenas/collect/" + attrs[1] + "&" + attrs[0] + "/buffer/0.2",
            headers={'accept': 'application/octet-stream'}
        )
        self.assertEquals(response.status_code, 200)

        response_dict_keys = self.aux_get_keys_from_response(response)
        self.assertListEqual(response_dict_keys, self.context_dict_keys)

        context_dict_keys = self.aux_get_keys_from_response_context(response)
        attrs.append('buffer')
        attrs.sort()
        self.assertListEqual(context_dict_keys, attrs)

        nome_context_keys_list = self.aux_get_attrs_context_keys_list_from_attr(response, "nome")
        self.assertListEqual(nome_context_keys_list, self.keys_from_attrs_context)
        geom_context_keys_list = self.aux_get_attrs_context_keys_list_from_attr(response, "geom")
        self.assertListEqual(geom_context_keys_list, self.keys_from_attrs_context)
        buffer_context_keys_list = self.aux_get_attrs_context_keys_list_from_attr(response, "buffer")
        self.assertListEqual(buffer_context_keys_list, ["@id", "@type"])

        response_operations_name = self.aux_get_supported_operations_names(response)
        self.assertListEqual(response_operations_name, self.spatial_collection_operation_names)

        response_dict = self.aux_get_dict_from_response(response)
        self.assertEquals(response_dict["@type"], 'GeobufCollection')

    def test_options_collect_for_feature_collection_with_string_operation_type_and_accept_header(self):
        attrs = ["geom", "nome"]
        response = requests.options(
            self.bcim_base_uri + "aldeias-indigenas/collect/" + attrs[0] + "&" + attrs[1] + "/upper",
            headers={'accept': 'application/octet-stream'}
        )
        self.assertEquals(response.status_code, 200)

        response_dict_keys = self.aux_get_keys_from_response(response)
        self.assertListEqual(response_dict_keys, self.context_dict_keys)

        context_dict_keys = self.aux_get_keys_from_response_context(response)
        attrs.append('upper')
        attrs.sort()
        self.assertListEqual(context_dict_keys, attrs)

        nome_context_keys_list = self.aux_get_attrs_context_keys_list_from_attr(response, "nome")
        self.assertListEqual(nome_context_keys_list, self.keys_from_attrs_context)
        geom_context_keys_list = self.aux_get_attrs_context_keys_list_from_attr(response, "geom")
        self.assertListEqual(geom_context_keys_list, self.keys_from_attrs_context)
        buffer_context_keys_list = self.aux_get_attrs_context_keys_list_from_attr(response, "upper")
        self.assertListEqual(buffer_context_keys_list, ["@id", "@type"])

        response_operations_name = self.aux_get_supported_operations_names(response)
        self.assertListEqual(response_operations_name, self.spatial_collection_operation_names)

        response_dict = self.aux_get_dict_from_response(response)
        self.assertEquals(response_dict["@type"], 'GeobufCollection')

    def test_options_collect_for_feature_collection_with_spatial_operation_only_geometry_attr_and_accept_header(self):
        attrs = ["geom"]
        response = requests.options(
            self.bcim_base_uri + "aldeias-indigenas/collect/" + attrs[0] + "/buffer/0.2",
            headers={'accept': 'application/octet-stream'}
        )
        self.assertEquals(response.status_code, 200)

        response_dict_keys = self.aux_get_keys_from_response(response)
        self.assertListEqual(response_dict_keys, self.context_dict_keys)

        context_dict_keys = self.aux_get_keys_from_response_context(response)
        attrs.append('buffer')
        attrs.sort()
        self.assertListEqual(context_dict_keys, attrs)

        geom_context_keys_list = self.aux_get_attrs_context_keys_list_from_attr(response, "geom")
        self.assertListEqual(geom_context_keys_list, self.keys_from_attrs_context)
        buffer_context_keys_list = self.aux_get_attrs_context_keys_list_from_attr(response, "buffer")
        self.assertListEqual(buffer_context_keys_list, ["@id", "@type"])

        response_operations_name = self.aux_get_supported_operations_names(response)
        self.assertListEqual(response_operations_name, self.spatial_collection_operation_names)

        response_dict = self.aux_get_dict_from_response(response)
        self.assertEquals(response_dict["@type"], 'GeobufCollection')

    def test_options_collect_for_feature_collection_with_string_operation_only_alphanumeric_attr_and_accept_header(self):
        attrs = ["nome"]
        response = requests.options(
            self.bcim_base_uri + "aldeias-indigenas/collect/" + attrs[0] + "/upper",
            headers={'accept': 'application/octet-stream'}
        )
        self.assertEquals(response.status_code, 200)

        response_dict_keys = self.aux_get_keys_from_response(response)
        self.assertListEqual(response_dict_keys, self.context_dict_keys)

        context_dict_keys = self.aux_get_keys_from_response_context(response)
        attrs.append('upper')
        attrs.sort()
        self.assertListEqual(context_dict_keys, attrs)

        nome_context_keys_list = self.aux_get_attrs_context_keys_list_from_attr(response, "nome")
        self.assertListEqual(nome_context_keys_list, self.keys_from_attrs_context)
        upper_context_keys_list = self.aux_get_attrs_context_keys_list_from_attr(response, "upper")
        self.assertListEqual(upper_context_keys_list, ["@id", "@type"])

        response_operations_name = self.aux_get_supported_operations_names(response)
        self.assertListEqual(response_operations_name, [])

        response_dict = self.aux_get_dict_from_response(response)
        self.assertEquals(response_dict["@type"], 'bytes')


    # --------------- TESTS FOR COLLECTION ---------------------------------
    # tests for collection simple path
    def test_options_for_collection_simple_path(self):
        response = requests.options(self.controle_base_uri + 'gasto-list/')
        self.assertEquals(response.status_code, 200)

        response_keys = self.aux_get_keys_from_response(response)
        self.assertListEqual(response_keys, self.simple_path_options_dict_keys)

        id_context_keys_list = self.aux_get_attrs_context_keys_list_from_attr(response, "id")
        self.assertListEqual(id_context_keys_list, self.keys_from_attrs_context)
        data_keys_list = self.aux_get_attrs_context_keys_list_from_attr(response, "data")
        self.assertListEqual(data_keys_list, self.keys_from_attrs_context)
        tipo_gasto_context_keys_list = self.aux_get_attrs_context_keys_list_from_attr(response, "tipo_gasto")
        self.assertListEqual(tipo_gasto_context_keys_list, self.keys_from_attrs_context)
        usuario_context_keys_list = self.aux_get_attrs_context_keys_list_from_attr(response, "usuario")
        self.assertListEqual(usuario_context_keys_list, self.keys_from_attrs_context)
        valor_context_keys_list = self.aux_get_attrs_context_keys_list_from_attr(response, "valor")
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

        id_context_keys_list = self.aux_get_attrs_context_keys_list_from_attr(response, "id")
        self.assertListEqual(id_context_keys_list, self.keys_from_attrs_context)
        data_keys_list = self.aux_get_attrs_context_keys_list_from_attr(response, "data")
        self.assertListEqual(data_keys_list, self.keys_from_attrs_context)
        tipo_gasto_context_keys_list = self.aux_get_attrs_context_keys_list_from_attr(response, "tipo_gasto")
        self.assertListEqual(tipo_gasto_context_keys_list, self.keys_from_attrs_context)
        usuario_context_keys_list = self.aux_get_attrs_context_keys_list_from_attr(response, "usuario")
        self.assertListEqual(usuario_context_keys_list, self.keys_from_attrs_context)
        valor_context_keys_list = self.aux_get_attrs_context_keys_list_from_attr(response, "valor")
        self.assertListEqual(valor_context_keys_list, self.keys_from_attrs_context)

        operation_name = self.aux_get_supported_operations_names(response)
        self.assertListEqual(operation_name, [])

        response_dict = self.aux_get_dict_from_response(response)
        self.assertEquals(response_dict["@type"], 'bytes')

    def test_options_for_collection_only_attributes(self):
        attrs = ['data', 'valor']
        response = requests.options(self.controle_base_uri + 'gasto-list/' + attrs[0] + ',' + attrs[1])
        self.assertEquals(response.status_code, 200)

        response_keys = self.aux_get_keys_from_response(response)
        self.assertListEqual(response_keys, self.context_dict_keys)

        context_keys = self.aux_get_keys_from_response_context(response)
        self.assertListEqual(context_keys, attrs)

        data_context_keys_list = self.aux_get_attrs_context_keys_list_from_attr(response, "data")
        self.assertListEqual(data_context_keys_list, self.keys_from_attrs_context)
        valor_context_keys_list = self.aux_get_attrs_context_keys_list_from_attr(response, "valor")
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
        self.assertListEqual(response_keys, self.context_dict_keys)

        context_keys = self.aux_get_keys_from_response_context(response)
        self.assertListEqual(context_keys, attrs)

        data_context_keys_list = self.aux_get_attrs_context_keys_list_from_attr(response, "data")
        self.assertListEqual(data_context_keys_list, self.keys_from_attrs_context)
        valor_context_keys_list = self.aux_get_attrs_context_keys_list_from_attr(response, "valor")
        self.assertListEqual(valor_context_keys_list, self.keys_from_attrs_context)

        operation_names = self.aux_get_supported_operations_names(response)
        self.assertListEqual(operation_names, [])

        response_dict = self.aux_get_dict_from_response(response)
        self.assertEquals(response_dict["@type"], 'bytes')


    # --------------- TESTS FOR FEATURE RESOURCE ---------------------------------
    # tests for feature simple path
    def test_options_for_feature_resource_simple_path(self):
        response = requests.options(self.bcim_base_uri + 'unidades-federativas/ES')
        self.assertEquals(response.status_code, 200)

        response_dict_keys = self.aux_get_keys_from_response(response)
        self.assertListEqual(response_dict_keys, self.simple_path_options_dict_keys)

        id_objeto_context_keys_list = self.aux_get_attrs_context_keys_list_from_attr(response, "id_objeto")
        self.assertListEqual(id_objeto_context_keys_list, self.keys_from_attrs_context)
        nome_context_keys_list = self.aux_get_attrs_context_keys_list_from_attr(response, "nome")
        self.assertListEqual(nome_context_keys_list, self.keys_from_attrs_context)
        nomeabrev_context_keys_list = self.aux_get_attrs_context_keys_list_from_attr(response, "nomeabrev")
        self.assertListEqual(nomeabrev_context_keys_list, self.keys_from_attrs_context)
        geometriaaproximada_context_keys_list = self.aux_get_attrs_context_keys_list_from_attr(response, "geometriaaproximada")
        self.assertListEqual(geometriaaproximada_context_keys_list, self.keys_from_attrs_context)
        geocodigo_context_keys_list = self.aux_get_attrs_context_keys_list_from_attr(response, "geocodigo")
        self.assertListEqual(geocodigo_context_keys_list, self.keys_from_attrs_context)
        sigla_context_keys_list = self.aux_get_attrs_context_keys_list_from_attr(response, "sigla")
        self.assertListEqual(sigla_context_keys_list, self.keys_from_attrs_context)
        geom_context_keys_list = self.aux_get_attrs_context_keys_list_from_attr(response, "geom")
        self.assertListEqual(geom_context_keys_list, self.keys_from_attrs_context)

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

        id_objeto_context_keys_list = self.aux_get_attrs_context_keys_list_from_attr(response, "id_objeto")
        self.assertListEqual(id_objeto_context_keys_list, self.keys_from_attrs_context)
        nome_context_keys_list = self.aux_get_attrs_context_keys_list_from_attr(response, "nome")
        self.assertListEqual(nome_context_keys_list, self.keys_from_attrs_context)
        nomeabrev_context_keys_list = self.aux_get_attrs_context_keys_list_from_attr(response, "nomeabrev")
        self.assertListEqual(nomeabrev_context_keys_list, self.keys_from_attrs_context)
        geometriaaproximada_context_keys_list = self.aux_get_attrs_context_keys_list_from_attr(response, "geometriaaproximada")
        self.assertListEqual(geometriaaproximada_context_keys_list, self.keys_from_attrs_context)
        geocodigo_context_keys_list = self.aux_get_attrs_context_keys_list_from_attr(response, "geocodigo")
        self.assertListEqual(geocodigo_context_keys_list, self.keys_from_attrs_context)
        sigla_context_keys_list = self.aux_get_attrs_context_keys_list_from_attr(response, "sigla")
        self.assertListEqual(sigla_context_keys_list, self.keys_from_attrs_context)
        geom_context_keys_list = self.aux_get_attrs_context_keys_list_from_attr(response, "geom")
        self.assertListEqual(geom_context_keys_list, self.keys_from_attrs_context)

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
        self.assertListEqual(response_dict_keys, self.context_dict_keys)

        context_keys = self.aux_get_keys_from_response_context(response)
        self.assertListEqual(context_keys, attrs)

        nome_context_keys_list = self.aux_get_attrs_context_keys_list_from_attr(response, "nome")
        self.assertListEqual(nome_context_keys_list, self.keys_from_attrs_context)
        geom_context_keys_list = self.aux_get_attrs_context_keys_list_from_attr(response, "geom")
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
        self.assertListEqual(response_dict_keys, self.context_dict_keys)

        context_keys = self.aux_get_keys_from_response_context(response)
        self.assertListEqual(context_keys, attrs)

        nome_context_keys_list = self.aux_get_attrs_context_keys_list_from_attr(response, "nome")
        self.assertListEqual(nome_context_keys_list, self.keys_from_attrs_context)
        geom_context_keys_list = self.aux_get_attrs_context_keys_list_from_attr(response, "geom")
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
        self.assertListEqual(response_dict_keys, self.context_dict_keys)

        context_keys = self.aux_get_keys_from_response_context(response)
        self.assertListEqual(context_keys, alpha_attrs)

        nome_context_keys_list = self.aux_get_attrs_context_keys_list_from_attr(response, "nome")
        self.assertListEqual(nome_context_keys_list, self.keys_from_attrs_context)
        geocodigo_context_keys_list = self.aux_get_attrs_context_keys_list_from_attr(response, "geocodigo")
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
        self.assertListEqual(response_dict_keys, self.context_dict_keys)

        context_keys = self.aux_get_keys_from_response_context(response)
        self.assertListEqual(context_keys, alpha_attrs)

        nome_context_keys_list = self.aux_get_attrs_context_keys_list_from_attr(response, "nome")
        self.assertListEqual(nome_context_keys_list, self.keys_from_attrs_context)
        geocodigo_context_keys_list = self.aux_get_attrs_context_keys_list_from_attr(response, "geocodigo")
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
        self.assertListEqual(response_dict_keys, self.context_dict_keys)

        context_keys = self.aux_get_keys_from_response_context(response)
        self.assertListEqual(context_keys, geom_attrs)

        geom_context_keys_list = self.aux_get_attrs_context_keys_list_from_attr(response, "geom")
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
        self.assertListEqual(response_dict_keys, self.context_dict_keys)

        context_keys = self.aux_get_keys_from_response_context(response)
        self.assertListEqual(context_keys, alpha_attrs)

        geom_context_keys_list = self.aux_get_attrs_context_keys_list_from_attr(response, "geom")
        self.assertListEqual(geom_context_keys_list, self.keys_from_attrs_context)

        operations_names = self.aux_get_supported_operations_names(response)
        self.assertListEqual(operations_names, self.spatial_operation_names)

        response_dict = self.aux_get_dict_from_response(response)
        self.assertEquals(response_dict["@type"], 'Geobuf')


    # tests for feature operations
    def test_options_for_feature_resource_operation_with_geometry_return(self):
        response = requests.options(self.bcim_base_uri + 'unidades-federativas/ES/buffer/1.2')
        self.assertEquals(response.status_code, 200)

        response_dict_keys = self.aux_get_keys_from_response(response)
        self.assertListEqual(response_dict_keys, self.context_dict_keys)

        a_context_keys = self.aux_get_keys_from_response_context(response)
        self.assertListEqual(a_context_keys, ['buffer'])

        buffer_context_keys_list = self.aux_get_attrs_context_keys_list_from_attr(response, "buffer")
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
        self.assertListEqual(response_dict_keys, self.context_dict_keys)

        a_context_keys = self.aux_get_keys_from_response_context(response)
        self.assertListEqual(a_context_keys, ['buffer'])

        buffer_context_keys_list = self.aux_get_attrs_context_keys_list_from_attr(response, "buffer")
        self.assertListEqual(buffer_context_keys_list, ["@id", "@type"])

        operations_names = self.aux_get_supported_operations_names(response)
        self.assertListEqual(operations_names, self.spatial_operation_names)

        response_dict = self.aux_get_dict_from_response(response)
        self.assertEquals(response_dict["@type"], 'Geobuf')

    def test_options_for_feature_resource_operation_with_float_return(self):
        response = requests.options(self.bcim_base_uri + 'unidades-federativas/ES/area')
        self.assertEquals(response.status_code, 200)

        response_dict_keys = self.aux_get_keys_from_response(response)
        self.assertListEqual(response_dict_keys, self.context_dict_keys)

        a_context_keys = self.aux_get_keys_from_response_context(response)
        self.assertListEqual(a_context_keys, ['area'])

        buffer_context_keys_list = self.aux_get_attrs_context_keys_list_from_attr(response, "area")
        self.assertListEqual(buffer_context_keys_list, ["@id", "@type"])

        operations_names = self.aux_get_supported_operations_names(response)
        self.assertListEqual(operations_names, [])

        response_dict = self.aux_get_dict_from_response(response)
        self.assertEquals(response_dict["@type"], 'float')

    def test_options_for_feature_resource_operation_with_float_return_accept_header(self):
        response = requests.options(self.bcim_base_uri + 'unidades-federativas/ES/area',
                                    headers={'Accept': 'application/octet-stream'})
        self.assertEquals(response.status_code, 200)

        response_dict_keys = self.aux_get_keys_from_response(response)
        self.assertListEqual(response_dict_keys, self.context_dict_keys)

        a_context_keys = self.aux_get_keys_from_response_context(response)
        self.assertListEqual(a_context_keys, ['area'])

        buffer_context_keys_list = self.aux_get_attrs_context_keys_list_from_attr(response, "area")
        self.assertListEqual(buffer_context_keys_list, ["@id", "@type"])

        operations_names = self.aux_get_supported_operations_names(response)
        self.assertListEqual(operations_names, [])

        response_dict = self.aux_get_dict_from_response(response)
        self.assertEquals(response_dict["@type"], 'bytes')

    def test_options_for_feature_resource_operation_with_point_return(self):
        response = requests.options(self.bcim_base_uri + 'unidades-federativas/ES/point_on_surface')
        self.assertEquals(response.status_code, 200)

        response_dict_keys = self.aux_get_keys_from_response(response)
        self.assertListEqual(response_dict_keys, self.context_dict_keys)

        a_context_keys = self.aux_get_keys_from_response_context(response)
        self.assertListEqual(a_context_keys, ['point_on_surface'])

        buffer_context_keys_list = self.aux_get_attrs_context_keys_list_from_attr(response, "point_on_surface")
        self.assertListEqual(buffer_context_keys_list, ["@id", "@type"])

        operations_names = self.aux_get_supported_operations_names(response)
        self.assertListEqual(operations_names, self.spatial_operation_names)

        response_dict = self.aux_get_dict_from_response(response)
        self.assertEquals(response_dict["@type"], 'Point')

    def test_options_for_feature_resource_operation_with_point_return_accept_header(self):
        response = requests.options(self.bcim_base_uri + 'unidades-federativas/ES/point_on_surface',
                                    headers={'Accept': 'application/octet-stream'})
        self.assertEquals(response.status_code, 200)

        response_dict_keys = self.aux_get_keys_from_response(response)
        self.assertListEqual(response_dict_keys, self.context_dict_keys)

        a_context_keys = self.aux_get_keys_from_response_context(response)
        self.assertListEqual(a_context_keys, ['point_on_surface'])

        buffer_context_keys_list = self.aux_get_attrs_context_keys_list_from_attr(response, "point_on_surface")
        self.assertListEqual(buffer_context_keys_list, ["@id", "@type"])

        operations_names = self.aux_get_supported_operations_names(response)
        self.assertListEqual(operations_names, self.spatial_operation_names)

        response_dict = self.aux_get_dict_from_response(response)
        self.assertEquals(response_dict["@type"], 'Geobuf')


    # --------------- TESTS FOR NON SPATIAL RESOURCE ---------------------------------
    def test_options_for_non_spatial_resource_simple_path(self):
        response = requests.options(self.controle_base_uri + "usuario-list/1/")
        self.assertEquals(response.status_code, 200)

        response_keys = self.aux_get_keys_from_response(response)
        self.assertListEqual(response_keys, self.simple_path_options_dict_keys)

        id_context_keys_list = self.aux_get_attrs_context_keys_list_from_attr(response, "id")
        self.assertListEqual(id_context_keys_list, self.keys_from_attrs_context)
        nome_context_keys_list = self.aux_get_attrs_context_keys_list_from_attr(response, "nome")
        self.assertListEqual(nome_context_keys_list, self.keys_from_attrs_context)
        nome_usuario_context_keys_list = self.aux_get_attrs_context_keys_list_from_attr(response, "nome_usuario")
        self.assertListEqual(nome_usuario_context_keys_list, self.keys_from_attrs_context)
        senha_context_keys_list = self.aux_get_attrs_context_keys_list_from_attr(response, "senha")
        self.assertListEqual(senha_context_keys_list, self.keys_from_attrs_context)
        data_nascimento_context_keys_list = self.aux_get_attrs_context_keys_list_from_attr(response, "data_nascimento")
        self.assertListEqual(data_nascimento_context_keys_list, self.keys_from_attrs_context)
        email_context_keys_list = self.aux_get_attrs_context_keys_list_from_attr(response, "email")
        self.assertListEqual(email_context_keys_list, self.keys_from_attrs_context)
        avatar_context_keys_list = self.aux_get_attrs_context_keys_list_from_attr(response, "avatar")
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

        id_context_keys_list = self.aux_get_attrs_context_keys_list_from_attr(response, "id")
        self.assertListEqual(id_context_keys_list, self.keys_from_attrs_context)
        nome_context_keys_list = self.aux_get_attrs_context_keys_list_from_attr(response, "nome")
        self.assertListEqual(nome_context_keys_list, self.keys_from_attrs_context)
        nome_usuario_context_keys_list = self.aux_get_attrs_context_keys_list_from_attr(response, "nome_usuario")
        self.assertListEqual(nome_usuario_context_keys_list, self.keys_from_attrs_context)
        senha_context_keys_list = self.aux_get_attrs_context_keys_list_from_attr(response, "senha")
        self.assertListEqual(senha_context_keys_list, self.keys_from_attrs_context)
        data_nascimento_context_keys_list = self.aux_get_attrs_context_keys_list_from_attr(response, "data_nascimento")
        self.assertListEqual(data_nascimento_context_keys_list, self.keys_from_attrs_context)
        email_context_keys_list = self.aux_get_attrs_context_keys_list_from_attr(response, "email")
        self.assertListEqual(email_context_keys_list, self.keys_from_attrs_context)
        avatar_context_keys_list = self.aux_get_attrs_context_keys_list_from_attr(response, "avatar")
        self.assertListEqual(avatar_context_keys_list, self.keys_from_attrs_context)

        operation_names = self.aux_get_supported_operations_names(response)
        self.assertListEqual(operation_names, [])

        response_dict = self.aux_get_dict_from_response(response)
        self.assertEquals(response_dict["@type"], 'bytes')

    def test_options_for_non_spatial_resource_only_attributes(self):
        response = requests.options(self.controle_base_uri + "usuario-list/1/nome,email")
        self.assertEquals(response.status_code, 200)

        response_keys = self.aux_get_keys_from_response(response)
        self.assertListEqual(response_keys, self.context_dict_keys)

        nome_context_keys_list = self.aux_get_attrs_context_keys_list_from_attr(response, "nome")
        self.assertListEqual(nome_context_keys_list, self.keys_from_attrs_context)
        email_context_keys_list = self.aux_get_attrs_context_keys_list_from_attr(response, "email")
        self.assertListEqual(email_context_keys_list, self.keys_from_attrs_context)

        operation_names = self.aux_get_supported_operations_names(response)
        self.assertListEqual(operation_names, self.basic_operations_names)

        response_dict = self.aux_get_dict_from_response(response)
        self.assertEquals(response_dict["@type"], 'Thing')

    def test_options_for_non_spatial_resource_only_attributes_with_accept_header(self):
        response = requests.options(self.controle_base_uri + "usuario-list/1/nome,email",
                                    headers={'Accept': "application/octet-stream"})
        self.assertEquals(response.status_code, 200)

        response_keys = self.aux_get_keys_from_response(response)
        self.assertListEqual(response_keys, self.context_dict_keys)

        nome_context_keys_list = self.aux_get_attrs_context_keys_list_from_attr(response, "nome")
        self.assertListEqual(nome_context_keys_list, self.keys_from_attrs_context)
        email_context_keys_list = self.aux_get_attrs_context_keys_list_from_attr(response, "email")
        self.assertListEqual(email_context_keys_list, self.keys_from_attrs_context)

        operation_names = self.aux_get_supported_operations_names(response)
        self.assertListEqual(operation_names, [])

        response_dict = self.aux_get_dict_from_response(response)
        self.assertEquals(response_dict["@type"], 'bytes')