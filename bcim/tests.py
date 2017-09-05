# Create your tests here.
from django.test import SimpleTestCase

import json
import httplib2

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


class UnidadeFederacaoTestCase(SimpleTestCase):

    def setUp(self):
        self.json_type = type('str')
        self.host_base = 'http://172.30.10.120:8000'
        self.url_uf_by_sigla = self.host_base + '/ibge/bcim/estados/RJ/'
        self.url_uf_by_geocodigo = self.host_base + '/ibge/bcim/estados/RJ/'
        self.h = httplib2.Http(".cache")

    def get_attribute_from_geojson(self, geoJSON, attribute):
        g = json.loads(geoJSON.decode())
        return g["properties"][attribute]
    """
    def test_uf_by_sigla(self):

        resp, gj = self.h.request(self.url_uf_by_sigla, "GET")
        sigla = self.get_attribute_from_geojson(gj, "sigla")
        self.assertEquals('RJ', sigla)

    def test_uf_by_geocodigo(self):
        geocodigo = '33'
        url = self.host_base + '/ibge/bcim/estados/' + geocodigo
        resp, gj = self.h.request(url, "GET")
        geocod = self.get_attribute_from_geojson(gj, "geocodigo")
        self.assertEquals(geocod, geocodigo)
    """
    def test_uf_by_id_objeto(self):
        id_objeto = '22279'
        url = self.host_base + '/ibge/bcim/estados/' + id_objeto
        resp, gj = self.h.request(url, "GET")
        idobj = json.loads(gj.decode())["id"]
        self.assertEquals(idobj, int(id_objeto))

