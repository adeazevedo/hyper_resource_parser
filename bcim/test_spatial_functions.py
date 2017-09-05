
from django.test import SimpleTestCase

import json
import requests
from django.contrib.gis.geos import GEOSGeometry
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import permissions
from rest_framework import permissions
from django.test.runner import DiscoverRunner

class NoDbTestRunner(DiscoverRunner):
   """ A test runner to test without database creation/deletion """

   def setup_databases(self, **kwargs):
     pass

   def teardown_databases(self, old_config, **kwargs):
     pass

#python manage.py test app --testrunner=app.filename.NoDbTestRunner
#python manage.py test bcim.tests  --testrunner=bcim.tests.NoDbTestRunner
#python manage.py test bcim.test_spatial_functions  --testrunner=bcim.test_spatial_functions.NoDbTestRunner

class EDGVDetailTestCase(SimpleTestCase):
    def setUp(self):
        self.json_type = type('str')
        #self.host_base = 'http://172.30.10.61:8000'
        self.host_base = 'http://127.0.0.1:8001'
        self.featureString = 'Feature'
        self.polygonString = 'Polygon'
        self.pointString = 'Point'
        self.multilineString = 'MultiLineString'
        self.lineString = 'LineString'
    def url_feature(self):
        return ''

    def test_feature(self):
        if len(self.url_feature())==0:
            return True
        an_url = self.host_base + self.url_feature()
        req = requests.get(an_url)
        self.assertEquals(req.json()['type'], self.featureString)

class UnidadeFederacaoDetailSpatialQueryTestCase(EDGVDetailTestCase):
    #testa se uma feature(multipoligon) contém um ponto dado em WKT
    def test_uf_sigla_contains_point(self):
        an_url = self.host_base + '/instituicoes/ibge/bcim/unidades-federativas/RJ/contains/POINT(-42 -21)/'
        req = requests.get(an_url)
        is_true = req.json().values().__iter__().__next__()== True
        self.assertTrue(is_true)
    #testa se uma feature(multipolygon) contém um ponto dado em geojson
    def test_uf_sigla_contains_point_as_geojson(self):
        an_url = self.host_base + '/instituicoes/ibge/bcim/unidades-federativas/RJ/contains/{ "type": "Point", "coordinates": [ -42, -21]}/'
        req = requests.get(an_url)
        is_true = req.json().values().__iter__().__next__()== True
        self.assertTrue(is_true)

    def test_uf_sigla_transform_area(self):
        an_url = self.host_base + '/instituicoes/ibge/bcim/unidades-federativas/RJ/transform/3857&True/area'
        req = requests.get(an_url)
        is_true = isinstance(req.json().values().__iter__().__next__(), float)
        self.assertTrue(is_true)

    #testa se a boundary de uma feature(multipolygon) responde multilinestring
    #testa se a boundary de uma feature(polygon) responde linestring
    def test_uf_sigla_boundery(self):
        an_url = self.host_base + '/instituicoes/ibge/bcim/unidades-federativas/RJ/boundary/'
        req = requests.get(an_url)
        self.assertEquals(req.json()['type'], self.multilineString)
        an_url = self.host_base + '/instituicoes/ibge/bcim/unidades-federativas/MG/boundary/'
        req = requests.get(an_url)
        self.assertEquals(req.json()['type'], self.lineString)

    #testa se o envelope de uma feature(polygon) responde um polygon
    def test_uf_sigla_envelope(self):
        an_url = self.host_base + '/instituicoes/ibge/bcim/unidades-federativas/MG/envelope/'
        req = requests.get(an_url)
        self.assertEquals(req.json()['type'], self.polygonString)

    #testa o centroid de uma feature(polygon)
    #primeiro obtém o centroid no formato geojson
    def test_uf_sigla_centroid(self):
        an_url = self.host_base + '/instituicoes/ibge/bcim/unidades-federativas/MG/centroid/'
        req = requests.get(an_url)
        self.assertEquals(req.json()['type'], self.pointString)
        an_url = self.host_base + '/instituicoes/ibge/bcim/unidades-federativas/MG/contains/' + self.host_base + '/instituicoes/ibge/bcim/unidades-federativas/MG/centroid/'
        req = requests.get(an_url)
        self.assertTrue(req.json().values().__iter__().__next__()== True)

class AldeiaIndigenaDetailTestCase(EDGVDetailTestCase):
    #testa se a url requisitada responde uma feature
    def test_adeia_indigena(self):
        an_url = self.host_base + '/instituicoes/ibge/bcim/aldeias-indigenas/587'
        req = requests.get(an_url)
        self.assertEquals(req.json()['type'], self.featureString)

    #testa se o evenvolpe de um ponto responde um ponto
    def test_adeia_indigena_envelope(self):
        an_url = self.host_base + '/instituicoes/ibge/bcim/aldeias-indigenas/587/envelope/'
        req = requests.get(an_url)
        self.assertEquals(req.json()['type'], self.pointString)

    # testa se um ponto está dentro de um envelope criado a partir de uma url
    def test_adeia_indigena_within_envelope_by_url(self):
        an_url = self.host_base + '/instituicoes/ibge/bcim/aldeias-indigenas/587/within/' + self.host_base + '/instituicoes/ibge/bcim/unidades-federativas/ES/envelope/'
        req = requests.get(an_url)
        self.assertTrue(req.json().values().__iter__().__next__()== True)


class TrechoFerroviarioDetailTestCase(EDGVDetailTestCase):
    #usado no test_feature para verificar se a url requisitada responde uma feature
    def url_feature(self):
        return '/instituicoes/ibge/bcim/trechos-ferroviarios/12711/'

"""
class UnidadeFederacaoListSpatialQueryTestCase(SimpleTestCase):
    def test_uf_sigla_contains_point(self):
        an_url = 'http://172.30.10.120:8000/ibge/bcim/aldeias-indigenas/'
        req = requests.get(an_url)
        value = json.loads(req.json())["type"]
        self.assertEquals(value,'FeatureCollection')
"""