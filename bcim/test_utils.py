from django.test import SimpleTestCase

import json

from django.contrib.gis.geos import GEOSGeometry
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import permissions
from rest_framework import permissions
from django.test.runner import DiscoverRunner
import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'bc_edgv.settings'


#python manage.py test bcim.test_utils  --testrunner=bcim.test_utils.NoDbTestRunner

class NoDbTestRunner(DiscoverRunner):
   """ A test runner to test without database creation/deletion """

   def setup_databases(self, **kwargs):
     pass

   def teardown_databases(self, old_config, **kwargs):
     pass


#python manage.py test bcim.test_utils  --testrunner=bcim.test_utils.NoDbTestRunner
from django.test import SimpleTestCase
from bcim.utils import APIViewHypermedia

class APIViewHypermediaTestCase(SimpleTestCase):
    def setUp(self):

        self.api =  APIViewHypermedia()


    def test_attributes_functions_str_has_url(self):
        self.assertTrue(self.api.attributes_functions_str_has_url('/ibge/bcim/aldeias-indigenas/within/http://127.0.0.1:8001/ibge/bcim/estados/ES'))
        self.assertTrue(self.api.attributes_functions_str_has_url('/ibge/bcim/aldeias-indigenas/within/https://127.0.0.1:8001/ibge/bcim/estados/ES'))
        self.assertTrue(self.api.attributes_functions_str_has_url('/ibge/bcim/aldeias-indigenas/within/http://www.inde.gov.br/ibge/bcim/estados/ES'))
        self.assertTrue(self.api.attributes_functions_str_has_url('/ibge/bcim/aldeias-indigenas/within/https://www.inde.gov.br/ibge/bcim/estados/ES'))
        self.assertTrue(self.api.attributes_functions_str_has_url('/ibge/bcim/aldeias-indigenas/within/www.inde.gov.br/ibge/bcim/estados/ES'))
        self.assertFalse(self.api.attributes_functions_str_has_url('/ibge/bcim/aldeias-indigenas/within/127.0.0.1:8001/ibge/bcim/estados/ES'))

    def test_attributes_functions_splitted_by_url(self):
        arr = self.api.attributes_functions_splitted_by_url('/ibge/bcim/aldeias-indigenas/within/http://127.0.0.1:8001/ibge/bcim/estados/ES')
        self.assertTrue(arr[0] == '/ibge/bcim/aldeias-indigenas/within/' )
        self.assertTrue(arr[1] == 'http://127.0.0.1:8001/ibge/bcim/estados/ES' )



