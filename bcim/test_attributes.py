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

class UnidadeFederacaoDetailAttributes(EDGVDetailTestCase):
    #testa a sigla
    def test_uf_sigla_contains_point(self):
        an_url = self.host_base + '/ibge/bcim/estados/RJ/sigla'
        req = requests.get(an_url)
        is_true = req.json().values().__iter__().__next__()== 'RJ'
        self.assertTrue(is_true)
        an_url = self.host_base + '/ibge/bcim/estados/RJ/sigla&nome'
        req = requests.get(an_url)
        is_true = req.json().values().__iter__().__next__()== 'RJ'
        self.assertTrue(is_true)



