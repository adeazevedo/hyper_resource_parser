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
from hyper_resource.views import AbstractResource, FeatureCollectionResource, AbstractCollectionResource
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

class FeatureCollectionResourceTest(SimpleTestCase):
    def setUp(self):
        self.attributes_functions = ['filter/sigla/in/rj,es,go/', 'filter/sigla/uppercase/in/rj,es,go/and/data/between/2017-02-01,2017-06-30/', 'filter/sigla/in/rj,es,go/and/geom/within/{"type":"Polygon","coordinates":[[[-41.881710164667396,-21.297482165015307],[-28.840495695785098,-21.297482165015307],[-28.840495695785098,-17.886950999070834],[-41.881710164667396,-17.886950999070834],[-41.881710164667396,-21.297482165015307]]]}']
        self.fc = FeatureCollectionResource()

    def test_is_filter_operation(self):
        self.assertTrue(self.fc.path_has_filter_operation('filter/sigla/in/rj,es,go/and/geom'))
        self.assertFalse( self.fc.path_has_filter_operation('/filter'))
        self.assertTrue('filter/sigla/uppercase/in/rj,es,go/and/data/between/2017-02-01,2017-06-30/')

    def test_get_objects_serialized_by_filter_operation(self):
        pass


    def test_q_objects_from_filter_operation(self):
        return True
        result = self.fc.q_objects_from_filter_operation('filter/sigla/eq/ES')[0]
        self.assertEquals(result.__repr__(), Q(sigla='ES').__repr__())
        result = self.fc.q_objects_from_filter_operation('filter/sigla/eq/ES/')[0]
        self.assertEquals(result.__repr__(), Q(sigla='ES').__repr__())
        result = self.fc.q_objects_from_filter_operation('filter/sigla/in/ES,RJ')[0]
        self.assertEquals(result.__repr__(), Q(sigla__in=['ES,RJ']).__repr__())
        result = self.fc.q_objects_from_filter_operation('filter/sigla/in/ES,RJ/')[0]
        self.assertEquals(result, Q(sigla__in=['ES,RJ']))
        result1 = self.fc.q_objects_from_filter_operation('filter/sigla/in/ES,RJ/and/data/between/2017-02-01,2017-06-30')[0]
        result2 = self.fc.q_objects_from_filter_operation('filter/sigla/in/ES,RJ/and/data/between/2017-02-01,2017-06-30')[1]
        self.assertEquals(result1, Q(sigla__in=['ES,RJ']))
        self.assertEquals(result2, Q(data='ES,RJ'))

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