# -*- coding: utf-8 -*-
import ast
import re
import json
import random
import jwt
import requests

from django.contrib.gis.db.models.functions import AsGeoJSON
from django.contrib.gis.gdal import SpatialReference
from django.db.models.base import ModelBase
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
# Create your views here.
from django.utils.http import quote_etag
from requests import ConnectionError
from requests import HTTPError
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.gis.geos import GEOSGeometry, GeometryCollection
from hyper_resource.contexts import *
from rest_framework.negotiation import BaseContentNegotiation
from django.contrib.gis.db import models
from abc import ABCMeta, abstractmethod
from datetime import datetime
from django.core.cache import cache
import hashlib
from hyper_resource.models import  FactoryComplexQuery, OperationController, BusinessModel, ConverterType
from image_generator.img_generator import BuilderPNG

SECRET_KEY = '-&t&pd%%((qdof5m#=cp-=-3q+_+pjmu(ru_b%e+6u#ft!yb$$'

HTTP_IF_NONE_MATCH = 'HTTP_IF_NONE_MATCH'
HTTP_IF_MATCH = 'HTTP_IF_MATCH'
HTTP_IF_UNMODIFIED_SINCE = 'HTTP_IF_UNMODIFIED_SINCE'
HTTP_IF_MODIFIED_SINCE = 'HTTP_IF_MODIFIED_SINCE'
HTTP_ACCEPT = 'HTTP_ACCEPT'
CONTENT_TYPE = 'CONTENT_TYPE'
ETAG = 'Etag'
CONTENT_TYPE_GEOJSON = "application/vnd.geo+json"
CONTENT_TYPE_JSON = "application/json"
CONTENT_TYPE_LD_JSON = "application/ld+json"
CONTENT_TYPE_OCTET_STREAM = "application/octet-stream"
CONTENT_TYPE_IMAGE_PNG = "image/png"
SUPPORTED_CONTENT_TYPES = (CONTENT_TYPE_GEOJSON, CONTENT_TYPE_JSON,CONTENT_TYPE_LD_JSON, CONTENT_TYPE_OCTET_STREAM, CONTENT_TYPE_IMAGE_PNG)

class IgnoreClientContentNegotiation(BaseContentNegotiation):
    def select_parser(self, request, parsers):
        """
        Select the first parser in the `.parser_classes` list.
        """
        return parsers[0]

    def select_renderer(self, request, renderers, format_suffix):
        """
        Select the first renderer in the `.renderer_classes` list.
        """
        return (renderers[0], renderers[0].media_type)

class BaseContext(object):

    def __init__(self, contextclassname, serializer_object=None):
        self.serializer_object = serializer_object
        self.contextclassname = contextclassname

    def options(self, request):
        response = Response(self.getContextData(request), status=status.HTTP_200_OK, content_type="application/ld+json")
        response = self.createLinkOfContext(request, response)
        return response

    def addContext(self, request, response):
        return self.createLinkOfContext(request, response)

    def createLinkOfContext(self, request, response, properties=None):
        # if properties is None:
        #     url = reverse('context:detail', args=[self.contextclassname], request=request)
        # else:
        #     url = reverse('context:detail-property', args=[self.contextclassname, ",".join(properties)], request=request)

        # pega a url absoluta, desde o host
        url = request.build_absolute_uri()
        # se houver uma barra no final da url ela é retirada
        url = url if url[-1] != '/' else url[:-1]
        # e adicionamos '.jsonld' ao ínvés da barra
        url = url + ".jsonld"

        # este link de contexto, quando clicado em um navegador,
        # deve levar a uma representação de uma requisição OPTIONS
        # da página atual

        # 'rel' é de relationship, isso significa que o tercho '<ulr>'
        # representa um contexto para algo, neste caso este relacionamento
        # é representado por dados no formato jsonld
        context_link = ' <'+url+'>; rel=\"http://www.w3.org/ns/json-ld#context\"; type=\"application/ld+json\" '
        if "Link" not in response:
            response['Link'] = context_link
        else:
            response['Link'] += "," + context_link

        return response

    def getHydraData(self, request):
        #classobject = Class.objects.get(name=self.contextclassname)
        #serializerHydra = HydraSerializer(classobject, request)
        return {}

    def addIriTamplate(self, context, request, serializer_object):
        url = request.build_absolute_uri()
        iriTemplate = {
            "@context": "http://www.w3.org/ns/hydra/context.jsonld",
            "@type": "IriTemplate",
            "template": url if url[-1] != '/' else url[:-1] +"{/attribute}",
            "variableRepresentation": "BasicRepresentation",
            "mapping": []
        }
        if serializer_object is not None:
            # percorre uma lista de atributos identificadores
            # encontrados no serializer
            for attr in serializer_object.Meta.identifiers:
                iriTemplate['mapping'].append({
                    "@type": "IriTemplateMapping",
                    "variable": "attribute",
                    "property": attr,
                    "required": True
                })
        else:
            iriTemplate['mapping'].append({
                "@type": "IriTemplateMapping",
                "variable": "attribute",
                "property": "hydra:supportedProperties",
                "required": True
            })

        context['iriTemplate'] = iriTemplate
        return context

    def getContextData(self, request):
        try:
            classobject = None #Class.objects.get(name=self.contextclassname)
        except:
            return ""
        serializer = None #ContextSerializer(classobject)
        contextdata = {} #serializer.data
        hydradata = self.getHydraData(request)
        if "@context" in hydradata:
            hydradata["@context"].update(contextdata["@context"])
        contextdata.update(hydradata)
        contextdata = self.addIriTamplate(contextdata, request, self.serializer_object)
        return contextdata


class RequiredObject:
    """
    Responds an object with four attributes:
    representation of what was required, content_type, object, dict=>dic[status] = status_code
    """
    def __init__(self, representation_object, content_type, origin_object, status_code, etag=None):
        self.representation_object = representation_object # the resource serialized data
        self.content_type = content_type # the Content-Type Response header
        self.origin_object = origin_object # the resource without serialization
        self.status_code = status_code # the Response status code
        self.etag = etag

class AbstractResource(APIView):
    """
    AbstractResource is the main view class.
    All other views are subclasses of this,
    directly or indirectly
    """

    __metaclass__ = ABCMeta

    # store the serializer_class for this view
    serializer_class = None
    contextclassname= ''


    def __init__(self):
        # when this class is instatiated we call the construct of APIView
        super(AbstractResource, self).__init__()
        self.current_object_state = None
        self.object_model = None # store the object model for this view
        self.name_of_last_operation_executed = None
        self.context_resource = None # the context for the requests to this view
        self.initialize_context()
        self.iri_metadata = None
        self.operation_controller = OperationController()
        self.token_need = self.token_is_need() # determines if requests from this view needs token
        self.e_tag = None # the Etag for requests for this view
        self.temporary_content_type = None

    # indicates wich is the content negotiation class
    content_negotiation_class = IgnoreClientContentNegotiation

    def generate_e_tag(self, data):
        """
        Creates a Etag based in the object data
        :param data:
        :return:
        """
        return str(hash(data))

    def set_etag_in_header(self, response, e_tag):
        """
        Receives a Response abject and add a Etag
        as one of this headers
        :param response:
        :param e_tag:
        :return:
        """
        if not response.streaming:
            response[ETAG] = e_tag
        return response

    #should be overrided
    def hashed_value(self, object):
        """
        Return a hash code for a object
        :param object:
        :return:
        """
        return hash(self.object)

    #should be overrided
    def inject_e_tag(self, etag=None):
        """
        If the 'object_model' attribute of this view is not None
        and the 'e_tag' attribute is None, this method attributes
        a Etag for the 'e_tag' attribute.
        If the 'object_model' is not None and the 'e_tag' is not None
        this method just append the received 'etag' to the 'e_tag' attribute
        of this view
        :param etag:
        :return:
        """

        # ATENTION: if self.object_model is None we can have a e_tag without a object_model
        if self.e_tag is None and self.object_model is not None:
            self.e_tag = self.hashed_value(self.object_model)
            return
        if etag is not None:
            self.e_tag += str(etag)
            return

    def jwt_algorithm(self):
        """
        Returns a string that represents wich JWT algorithm will be used
        to secure tranmissions between two parts (client and server)
        :return:
        """
        return 'HS256'

    def token_is_ok(self, a_token):
        """
        Verify the validity of the received token, based on application 'SECRET_KEY'
        and the JWT algorithm chosen. In the case of 'a_token' isn't a valid token
        this function will raise a jwt.InvalidTokenError, returning False (the token
        is not valid)
        :param a_token:
        :return:
        """
        try:
            payload = jwt.decode(a_token, SECRET_KEY, algorithm=self.jwt_algorithm())
            return True
        except jwt.InvalidTokenError:
            return False

    def token_is_need(self):
        """
        Determines if requests for this view needs token or not
        :return:
        """
        return  False

    def add_key_value_in_header(self, response, key, value ):
        """
        This function receives a Response object and appends
        a header and his respective value
        :param response:
        :param key:
        :param value:
        :return:
        """
        response[key] = value

    def add_url_in_header(self, url, response, rel):
        """
        Mounts a 'Link' header with the received url and wich relationship
        this url represents relative to the current request.
        If the 'Link' header already exists in the Response object, the received
        url and the relationship (rel) is appended to the 'Link' header
        :param url:
        :param response:
        :param rel:
        :return:
        """
        link = ' <'+url+'>; rel=\"'+rel+'\" '
        if "Link" not in response:
            response['Link'] = link
        else:
            response['Link'] += "," + link
        return response

    def add_base_headers(self, request, response):
        """
        Adds the 'Link' header in the Response object containing
        a url representing the father url for this request and
        a url representing a context for the requested resource
        :param request:
        :param response:
        :return:
        """
        iri_base = request.build_absolute_uri() # the absolute iri for this request
        if self.contextclassname not in iri_base: # if the context class name isn't in the absolute iri ...
            return; #...  do nothing
        idx = iri_base.index(self.contextclassname)
        # gets the absolute iri from the begin until the context class name
        iri_father = iri_base[:idx]
        # adds 'Link' header in the Response object,
        # relating the father iri from this request with a 'up' relationship
        self.add_url_in_header(iri_father,response, 'up')
        # the second url appended to 'Link' header is the absolute url minus the bar
        # with '.jsonld', the 'rel' is the relationship represented by w3.org url
        self.add_url_in_header(iri_base[:-1] + '.jsonld',response, rel='http://www.w3.org/ns/json-ld#context"; type="application/ld+json')

    def dispatch(self, request, *args, **kwargs):
        """
        If the request needs authentication this method
        verifies the authenticity of token (passed through HTTP_AUTHORIZATION header)
        and pass the request forward if everything is ok or send a 401 (unauthorized)
        response otherwise. If the request don't need authentication we simply pass the
        request forward
        :param request:
        :param args:
        :param kwargs:
        :return:
        """

        if self.token_is_need():
            http_auth = 'HTTP_AUTHORIZATION'

            # the HTTP_AUTHORIZATION header, if this exists in the request, needs to starts with 'Bearer'
            if http_auth in request.META and request.META[http_auth].startswith('Bearer'):
                # get the HTTP_AUTHORIZATION header value (without 'Bearer' and edge whitespaces)
                a_token = request.META['HTTP_AUTHORIZATION'][7:].strip()
                if self.token_is_ok(a_token):
                    # if token is valid, pass the request forward for APIView dispatch method
                    return super(AbstractResource, self).dispatch(request, *args, **kwargs)

            # if HTTP_AUTHORIZATION header does'nt exists or not starts with 'Bearer',
            # a response saing 'token is need' is returned with a 401 (unauthorized) code
            resp = HttpResponse(json.dumps({"token": "token is needed or it is not ok"}), status=401,  content_type=CONTENT_TYPE_JSON)
            # plus a WWW-Authenticate header is send informing how to access the resource
            resp['WWW-Authenticate'] = 'Bearer realm="Access to the staging site"'
            return resp
        else:
            # if token isn't needed, just call the superclsse dispath method
            return  super(AbstractResource, self).dispatch(request, *args, **kwargs)

    #@abstractmethod #Could be override
    def initialize_context(self):
        """
        Sets 'self.context_resource' with a context class instance, reference to this view
        and sets the 'resource' attribute of the context object with this view
        (subclass of AbstractResource) as the his value
        :return:
        """
        # __class__ shows in wich class this instruction is being executed
        # (this works on the subclasses and not is this classe)
        # __module__ shows in wich module is this classe (the all doted path)
        # at this point we'll have something like this: bcim.UnidadeFederacaoList (where we'll stract bcim)
        # we then split the result in a list where we get only the first element and append '.context'
        # in the final we'll have something like 'bcim.contexts' that is the context class for the app
        context_module_name = self.__class__.__module__.split('.')[0] + '.contexts'
        # importing the context class reference to the previous string
        context_module = importlib.import_module(context_module_name)
        # getting the view class name and appending 'Context'
        # remember, this name isn't 'AbstractResource', the name is a subclasse of 'AbstractResource'
        # in the final we'll have something like this: UnidadeFederacaoListContext
        context_class_name = self.__class__.__name__ + 'Context'
        # getting the context class inside the module reference at this view class (bcim.contexts, in this case)
        context_class = getattr(context_module, context_class_name )
        # 'self.context_resource' is then a instance of
        # the context class of this view (a subclass of AbstractResource)
        self.context_resource = context_class()
        # the context class instance has the 'resource' attribute,
        # his value is the view instance of the resource
        # in the case of the exemple above, the value of 'self.context_resource.resource'
        # is a UnidadeFederativaList object
        self.context_resource.resource = self

    # todo
    def path_request_is_ok(self, a_path):
        return True

    def operations_with_parameters_type(self):
        """
        Returns a geometric operations dict for FeatureModel or returns a empty dict
        for BusinessModel. This dict lists all the possible operations for this
        resources (FeatureModel or BusinessModel)
        :return:
        """
        dic = self.object_model.operations_with_parameters_type()
        return dic

    def model_class(self):
        """
        Returns the model class reference to this view (subcalss of AbstractResource)
        :return:
        """
        return self.serializer_class.Meta.model #return self.object_model.model_class()

    def model_class_name(self):
        """
        Returns the model class name reference to this view
        :return:
        """
        return self.model_class().__name__

    def attribute_names_to_web(self):
        """
        Returns a list of model field NAMES reference to this view (or subclasses)
        :return:
        """
        # BusinessModel.fields() returns a list of model field provided by Django database API
        return [field.name for field in self.object_model.fields()]
        #return self.serializer_class.Meta.fields

    def field_for(self, attribute_name):
        """
        If attribute_name matchs with any fields of the model fields list,
        return this matched field. If has no matches, return None
        :param attribute_name:
        :return:
        """
        fields_model = self.object_model.fields()
        for field in fields_model:
            if field.name == attribute_name:
                return field
        return None

    def fields_to_web_for_attribute_names(self, attribute_names):
        """
        Receives a list of attribute names and compare to the list of models fields.
        Returns the list of matched models fields or a empty list if none of the fields matches
        :param attribute_names:
        :return:
        """
        # gets the models fields list
        fields_model = self.object_model.fields()
        return [field for field in fields_model if field.name in attribute_names ]

    def fields_to_web(self):
        """
        Returns a list of model FIELDS that matches with the list of field names
        of this model
        :return:
        """
        # AbstractResource.attribute_names_to_web() gets a list of model field names
        return self.fields_to_web_for_attribute_names(self.attribute_names_to_web())

        # OBS: AbstractResource.attribute_names_to_web() calls BusinessModel.fields() and returns names
        # AbstractResource.fields_to_web() call BusinessModel.fields() and returns the fields
        # Is realy necessary or can i keep just one of their?

    def _base_path(self, full_path):
        """
        Receives the url (full_path) and returns the full
        url excluding the path after the context class name
        :param full_path:
        :return:
        """
        # arr will be a list of each part of the url (full_path) separated by '/'
        arr = full_path.split('/')
        # gets the index of context class name in the url
        ind = arr.index(self.contextclassname)
        # gets the full url until the context class name (including this) and ignore the rest of urls
        return '/'.join(arr[:ind+1])

    # ERROR: AbstractResource._set_context_to_model() is not used and contexModel() does not exists
    def _set_context_to_model(self):
        self.context_resource.contextModel(self.object_model)

    def _set_context_to_attributes(self, attribute_name_array):
        """
        Receives a list of model attribute names and sets a context dict
        formed by this attributes in the context_resource for this view
        (subclass of AbstractResource)
        :param attribute_name_array:
        :return:
        """
        # the command below sets a context dict references to the model fields
        # and stores this in the ContextResource.context_dict attribute of
        # AbstractResource.context_resource attribute of this view
        self.context_resource.set_context_to_attributes(attribute_name_array)

    def _set_context_to_only_one_attribute(self, attribute_name):
        """
        Sets a context for the received model attribute in AbstractResource.context_resource.
        If 'attribute_name' represents a geometric attribute, also sets the supported operations context
        to the context of this attribute
        :param attribute_name:
        :return:
        """
        # AbstractResource.field_for() returns the model field corresponding 'atribute_name' if this exists
        attribute_type = self.field_for(attribute_name)
        # AbstractResource.current_object_state is the object model in a determinated moment
        self.context_resource.set_context_to_only_one_attribute(self.current_object_state, attribute_name, attribute_type)

    def _set_context_to_operation(self, operation_name):
        """
        Sets a context to the AbstractResource.context_resource.dict_resource attribute
        reference to the operation defined by operation_name
        :param operation_name:
        :return:
        """
        self.context_resource.set_context_to_operation(self.current_object_state, operation_name)

    def set_basic_context_resource(self, request ):
        """
        Fill the context of this view (AbstractResource.context_resource)
        with the basic informations of the request (host, basic_path and complement_path)
        :param request:
        :return:
        """
        # sets AbstractResource.context_resource.host with HTTP_HOST request header value
        self.context_resource.host = request.META['HTTP_HOST']
        # get the PATH_INFO request header value (the entire url before the host ip and port) and
        # sets AbstractResource.contex_resource.basic_path PATH_INFO value without the string after context class name
        self.context_resource.basic_path = self._base_path(request.META['PATH_INFO'])
        if len(self.kwargs.values()):
            # if has any arguments AbstractResource.context_resourece.complement_path is the first one
            self.context_resource.complement_path = list(self.kwargs.values())[0]
        else:
            # if hasn't arguments AbstractResource.context_resourece.complement_path is a empty string
            self.context_resource.complement_path = ''

    def key_is_identifier(self, key):
        """
        Verify if the received 'key' is between the
        AbstractResource.serializer_class identifiers list
        :param key:
        :return:
        """
        return key in self.serializer_class.Meta.identifiers

    def dic_with_only_identitier_field(self, dict_params):
        """
        Receives a dict of fields and return another dict with
        only identifier fields (those present in AbstractResource.serializer_class
        identifiers list) and his respective values
        :param dict_params:
        :return:
        """
        dic = dict_params.copy()
        a_dict = {}
        for key, value in dic.items():
            if self.key_is_identifier(key):
                a_dict[key] = value

        return a_dict

    '''
    def get_object(self, arr_of_term=[]):
        first_term = arr_of_term[0]
        if self.is_attribute(self, first_term):
            self.current_object_state =  getattr(self.object_model, first_term, None)
            arr_of_term = arr_of_term[1:]

        for term in arr_of_term:
            self.current_object_state = getattr(self.current_object_state, term, None)
        return  self.current_object_state
    '''
    def attributes_functions_name_template(self):
        return 'attributes_functions'

    def get_object(self, a_dict):
        """
        Receives a_dict, get only the identifier fields
        and use them to query the instaces in the database
        that matches with the identifiers dict
        :param a_dict:
        :return:
        """
        dicti = self.dic_with_only_identitier_field(a_dict)
        #queryset = self.model_class().objects.all()
        #obj = get_object_or_404(queryset, **dicti)
        obj = get_object_or_404(self.model_class(), **dicti)
        #self.check_object_permissions(self.request, obj)
        return obj

    def serialized_data(self, request, object_or_list_of_object, is_many):
        """
        Returns the serialized data from a sigle object or a list of them
        :param request:
        :param object_or_list_of_object:
        :param is_many:
        :return:
        """
        return self.serializer_class(object_or_list_of_object, many=is_many, context={'request': request}).data

    def default_content_type(self):
        """
        Returns the default Response Content=Type (application/json)
        :return:
        """
        return CONTENT_TYPE_JSON

    def content_type_or_default_content_type(self, requestOrNone):
        """
        Receives the Request object and defines wich Response Content-Type
        will be returned using the Accept Request header. If the Accept Request
        header value match with one of the supported Response Content-Types, the
        Accept (Request) and Content-Type (Response) will be the same, otherwise
        the default content-type will be returned
        :param requestOrNone:
        :return:
        """
        if requestOrNone is None:
            return self.default_content_type()

        a_content_type = requestOrNone.META.get(HTTP_ACCEPT, '')
        if a_content_type not in SUPPORTED_CONTENT_TYPES:
            return self.default_content_type()
        return a_content_type

    #todo
    def basic_response(self, request, serialized_object, status, content_type):
        """
        A basic response with data, status code and Content-Type
        :param request:
        :param serialized_object:
        :param status:
        :param content_type:
        :return:
        """
        return Response(data=serialized_object, status=status, content_type=content_type)

    #Answer if a client's etag is equal server's etag
    def conditional_etag_match(self, request):
        """
        Return True if Request If-None-Match header value matches with the Etag cached value.
        If the generated request key is not in the cache key set or if Request If-None-Match header
        value not matches with the Etag cache value, return False
        :param request:
        :return:
        """
        # mounts a key based on Request Accept header or default Content-Type
        key = self.get_key_cache(request)
        # the cache stores a tuple of Etag and the serialized data
        tuple_etag_serialized_data = cache.get(key)
        # if typle_etag_serialized_data is None, this means that the key not correspond none of the cache keys
        # hence the resource isn't in cache
        if tuple_etag_serialized_data is None:
            return False
        # compare the Request If-None-Match header value with the Etag value of the cache
        return tuple_etag_serialized_data[0] == request.META.get(HTTP_IF_NONE_MATCH, '')

    #Answer if a get(request) is conditional
    def is_conditional_get(self, request):
        """
        Return True if If-None-Match or Unmodified-Sice header exists in the request
        or return False otherwise
        :param request:
        :return:
        """
        return request.META.get(HTTP_IF_NONE_MATCH, None) is not None or \
               request.META.get(HTTP_IF_UNMODIFIED_SINCE,  None) is not None

    #Should be overrided
    # Answer a formatted string(iri + accept) which is a key to retrieve an object in the cache
    def get_key_cache(self, request, a_content_type=None):
        """
        Mounts a cache key based on the request. If a_content_type is defined
        the key returned is the absolute uri + a_content_type. Otherwise, the
        key will be the absolute_uri + the content-type returned by
        AbstractResource.content_type_or_default_content_type()
        :param request:
        :param a_content_type:
        :return:
        """
        if a_content_type is not None:
            return self.request.build_absolute_uri() + a_content_type
        return self.request.build_absolute_uri() + self.content_type_or_default_content_type(request)

    def set_key_with_data_in_cache(self, key, etag, data, seconds=3600):
        """
        Sets 'etag' and 'data' in cache as a tuple indexed by 'key'.
        If 'key' already corresponds a cache key, nothing is done.
        :param key:
        :param etag:
        :param data:
        :param seconds:
        :return:
        """
        if isinstance(data, memoryview):
            return
        if cache.get(key) is None:
            cache.set(key,(etag, data), 3600)

    def resource_in_cache_or_None(self, request):
        """
        Return the cached resource if the generated request key
        (generated through AbstractResource.get_key_cache()) and the
        If-None-Match header value matches with the cache key and cached
        etag respectivitly. Return False otherwise
        :param request:
        :return:
        """
        key = self.get_key_cache(request)
        return cache.get(key)

    def is_image_content_type(self, request, **kwargs):
        """
        Return True if the resulted Content-Type of the Request object is image/png,
        or if the parameter 'format' of the request is 'png'
        :param request:
        :param kwargs:
        :return:
        """
        return self.content_type_or_default_content_type(request) == CONTENT_TYPE_IMAGE_PNG or kwargs.get('format', None) == "png"

    def accept_is_binary(self, request):
        """
        Return True if the Request Accept header value is application/octet-stream
        :param request:
        :return:
        """
        return request.META.get(HTTP_ACCEPT, '') == CONTENT_TYPE_OCTET_STREAM

    # Should be overrided
    def is_binary_content_type(self,required_object ):
        """
        Receives the required object and returns True
        if his Content-Type is application/octet-stream
        :param required_object:
        :return:
        """
        return required_object.content_type == CONTENT_TYPE_OCTET_STREAM

    # Should be overrided
    def response_base_get_binary(self, request, required_object):
        """
        Returns a Response to a required object with application/octet-stream Content-Type
        and storing the data in cache. If the required object is a str instance, the response
        will be a geobuf (until 10x smaller than a regular JSON)
        :param request:
        :param required_object:
        :return:
        """
        # 'key' will be absolute uri + application/octet-stream
        key = self.get_key_cache(request, CONTENT_TYPE_OCTET_STREAM)
        import geobuf
        if isinstance(required_object.representation_object, dict) and 'type' in required_object.representation_object:
            # if representation object is a dict is an GeoJson
            # geobuf minimize the response size
            result = geobuf.encode(required_object.representation_object) # GeoJSON or TopoJSON -> Geobuf string
        else:
            result = required_object.representation_object

        if isinstance(result, dict):
            value_to_e_tag = json.dumps(result)
        else:
            value_to_e_tag =  result
        # e_tag is a hash of the result
        e_tag = self.generate_e_tag(value_to_e_tag)
        # sets the e_tag and the result in cache binded to a key
        self.set_key_with_data_in_cache(key, e_tag, result)
        # mounts the HttpResponse with result as data and application/octet-stream as Content-Type
        resp = HttpResponse(result, content_type=CONTENT_TYPE_OCTET_STREAM)
        # set Etag as a Response header
        self.set_etag_in_header(resp, e_tag)
        return resp

    # todo: verify image responses processment
    #Should be overrided
    def response_base_get_with_image(self, request, required_object):
        # 'queryset' is the requested resource without serialization
        queryset = required_object.origin_object

        image = self.get_png(self.current_object_state, request)
        required_object.representation_object = image
        key = self.get_key_cache(request, CONTENT_TYPE_IMAGE_PNG)
        e_tag = self.generate_e_tag(image)
        self.set_key_with_data_in_cache(key,e_tag, image)
        resp = HttpResponse(image, content_type=CONTENT_TYPE_IMAGE_PNG)
        self.set_etag_in_header(resp, e_tag)
        return resp

    #Should be overrided
    def response_base_object_in_cache(self, request ):
        """
        Returns a cached Response (if this is in cache)
        defining wich Content-Type the response has
        :param request:
        :return:
        """
        # AbstractResource.resource_in_cache_or_None return de cached data
        # if the mounted key based on Accept Request header matches one of the cached keys
        tuple_etag_serialized_data = self.resource_in_cache_or_None(request)
        if tuple_etag_serialized_data is not None:
            if request.META[HTTP_ACCEPT] in [CONTENT_TYPE_IMAGE_PNG, CONTENT_TYPE_OCTET_STREAM]:
                # if Accept Request header value is application/octet-stream or image/png
                # the Response Content-Type will be the same value
                resp = HttpResponse(tuple_etag_serialized_data[1], content_type=request.META[HTTP_ACCEPT])
            else:
                # if Accept Request header value isn't application/octet-stream nor image/png
                # the Content-Type will be the Accept value or the default Content-Type
                resp = Response(data=tuple_etag_serialized_data[1],status=200, content_type=self.content_type_or_default_content_type(request))

            # set etag in Response header
            self.set_etag_in_header(resp, tuple_etag_serialized_data[0])
            return resp

    #Should be overrided
    def response_base_get(self, request, *args, **kwargs):
        """
        Returns a Response for the Request. If the response is in cache
        returns the cached resource. If the response isn't in cache
        responds with a regular response, treating images and binary requests
        as such and caching the response
        :param request:
        :param args:
        :param kwargs:
        :return:
        """

        # AbstractResource.resource_in_cache_or_None() returns the requested resource from cache
        # if the key formed by absolute uri + accept or absolute uri + default Content-Type
        # matches one of the cache keys. Returns None othewise
        resource = self.resource_in_cache_or_None(request)
        if resource is not None:
            # returns a response from the cache
            return self.response_base_object_in_cache(request )

        # if the resource is not in cache, use the subclass basic_get() that returns a RequiredObject instance
        required_object = self.basic_get(request, *args, **kwargs)
        # if Required object has some error, return this
        status = required_object.status_code
        if status in [400,401,404]:
            return Response({'Error ': 'The request has problem. Status:' + str(status)}, status=status)
        if status in [500]:
            return Response({'Error ': 'The server can not process this request. Status:' + str(status)}, status=status)

        # todo: verify image responses processment
        if self.is_image_content_type(request, **kwargs):
            return self.response_base_get_with_image(request, required_object)

        # if RequiredObject has application/octect-stream Content-Type
        # the Response is a geobuf (smaller than a regular JSON)
        if self.is_binary_content_type(required_object):
            return self.response_base_get_binary(request, required_object)

        # mounts a cache key with RequiredObject.content_type
        key = self.get_key_cache(request, a_content_type=required_object.content_type)
        # sets the e_tag and data in cache binding to the key
        self.set_key_with_data_in_cache(key, self.e_tag, required_object.representation_object )

        # return the Response with the requested resource representation and Etag header
        resp =  Response(data=required_object.representation_object,status=200, content_type=required_object.content_type)
        self.set_etag_in_header(resp, self.e_tag)
        return resp

    #Should be overrided
    def response_conditional_get(self, request, *args, **kwargs):
        """
        Return a 304 Response, if If-None-Math header matches with
        the cached Etag, or a regular Response otherwise
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        # 'a_content_type' is the Accept Request header of a default Content-Type
        a_content_type = self.content_type_or_default_content_type(request)
        # verify if the Request If-None-Match header match with cached Etag
        if self.conditional_etag_match(request):
            # if matches, a 304 (Not modified) Response is returnes
            return Response(data={},status=304, content_type=a_content_type)
        # if not matches return a regular Response (with database requests)
        return self.response_base_get(request, *args, **kwargs)

    #Could be overrided
    def get(self, request, *args, **kwargs):
        """
        Receive the request and decide if this will be a regular response
        or a cached response
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        #return super(AbstractResource, self).get(request, *args, **kwargs)
        resp = None
        # responds with a conditional get if the request has If-None-Match or If-Unmodified-Since header
        if self.is_conditional_get(request):
           resp = self.response_conditional_get(request, *args, **kwargs)
        else:
        # otherwise responds with a regular get (can be responsed with cached data)
        # QUESTION: AbstractResource.response_base_get() must consider cache check?
        # After all, if AbstractResouce.is_conditional_get() return False this means that the Request hasn't
        # If-None-Match or If-Unmodified-Since headers
           resp = self.response_base_get(request, *args, **kwargs)

        # add the Link header in Response
        self.add_base_headers(request, resp)

        return resp

    # Could be overrided
    def patch(self, request, *args, **kwargs):
        """
        Just repass the request to APIView.patch()
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        return super(AbstractResource, self).patch(request, *args, **kwargs)

    # Could be overrided
    def head(self, request, *args, **kwargs):
        """
        Just returns a 200 status code for HEAD requests
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        resp =  Response(status=status.HTTP_200_OK)
        return resp

    # Could be overrided
    def put(self, request, *args, **kwargs):
        """
        Update the database resource if the request body is valid or
        return a 400 Response otherwise
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        # return a object from database using the arguments as filter
        obj = self.get_object(kwargs)
        # get the PUT request body and compares to the database resouce to determines if the request body is valid or not
        serializer = self.serializer_class(obj, data=request.data, context={'request': request})
        if serializer.is_valid():
            # if the request data is valid, alter the database resouce and returns a 204 response
            serializer.save()
            resp =  Response(status=status.HTTP_204_NO_CONTENT)
            return resp
        # if request data isn't valid, return a 400 response status
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # Could be overrided
    def delete(self, request, *args, **kwargs):
        """
        Use request arguments to delete resource from database
        and returns a 204 status code
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        obj = self.get_object(kwargs)
        obj.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def operation_names_model(self):
        """
        Returns a list with the name of all object model methods
        :return:
        """
        return self.object_model.operation_names()

    def attribute_names_model(self):
        """
        Returns a list of all public attributes of the object model
        :return:
        """
        return self.object_model.attribute_names()

    def is_private(self, attribute_or_method_name):
        """
        Return True if 'attribute_or_method_name' is private
        :param attribute_or_method_name:
        :return:
        """
        return attribute_or_method_name.startswith('__') and attribute_or_method_name.endswith('__')

    def is_not_private(self, attribute_or_method_name):
        """
        Return True if 'attribute_or_method_name' is public (is not private)
        :param attribute_or_method_name:
        :return:
        """
        return not self.is_private(attribute_or_method_name)

    def is_operation(self, operation_name):
        """
        Return True if 'operation_name' is the name of any object model methods
        :param operation_name:
        :return:
        """
        return operation_name in self.operation_names_model()

    def is_attribute(self, attribute_name):
        """
        Returns True if 'attribute_name' is between the object model attribute names list
        :param attribute_name:
        :return:
        """
        return self.object_model.is_attribute(attribute_name)

    def is_spatial_attribute(self, attribute_name):
        return False

    def _has_method(self,  method_name):
        """
        Return True if 'method_name' is between the list of object models method names
        :param method_name:
        :return:
        """
        return method_name in self.operation_names_model()

    def is_simple_path(self, attributes_functions_str):
        """
        Returns True if the rreceived url parameters (attributes_functions_str)
        is None or is length 0 string
        :param attributes_functions_str:
        :return:
        """
        return attributes_functions_str is None or len(attributes_functions_str) == 0

    def path_has_operations(self, attributes_functions_name):
        """
        Return True if the received url parameters (attribute_functions_name') has some name
        between the list of object model method names list
        :param attributes_functions_name:
        :return:
        """
        # tranform the url fragment in a list of names
        attrs_functs = attributes_functions_name.split('/')
        # gets the methods names for this object model
        operations = self.operation_names_model()
        # verify if some name of the url fragment is betbeen the object model operations list
        for att_func in attrs_functs:
            if  att_func in operations:
                return True
        return False

    def path_has_only_attributes(self,  attributes_functions_name):
        """
        Return True if 'attributes_functions_name' (a string with a piece of
        url representing the functions or attributes for a url) is a path with
        only object model attributes
        :param attributes_functions_name:
        :return:
        """
        # tranform the url fragment in a list of names
        tem_list = attributes_functions_name.split('/')
        # remove empty strings from list
        attrs_functs = [value for value in tem_list if value != '' ]
        # if the list has more than one element, the path hasn't only attributes
        if len(attrs_functs) > 1:
            return False
        # if the first element of the list has ',' the path has only attributes
        if ',' in attrs_functs[0]:
            return True
        # if the first element of the list is between the object model method names, the path hasn't only attributes
        if self._has_method(attrs_functs[0]):
            return False
        # return True if the first element of the list is between the object model attribute names list
        return self.object_model.is_attribute(attrs_functs[0])

    def transform_path_with_url_as_array(self, arr_of_term):
        """
        Receive url parameters (arr_of_term) each parameter as a array element.
        If there is some url inside this array (any element 'www.' or 'http:' or 'https:'),
        each element of this array references to this url is merged in a single element.
        :param arr_of_term - url parameters:
        :return:
        """
        arr = []
        http_str = ''
        # remove empty strings from list
        arr_term =  [ele for ele in arr_of_term if ele != '']

        found_url = False
        # storing the number of elements of the list
        size_of_term = len(arr_term)

        for idx, token in enumerate(arr_term): # token is each url parameter
            # if 'token' is 'https', 'http' or has 'www.', 'found_url' turns True
            if self.token_is_http_or_https_or_www(token.lower()):
                found_url = True

            if found_url:
                if self.token_is_http_or_https(token):
                    # if token is 'http' or 'https', append it to 'http_str' with '//'
                    http_str += token + '//'
                elif self.is_end_of_term(token):
                    # if 'token' is a logical operator (or, and, *or, *and), 'found_url' turns False
                    found_url = False
                    # append 'http_str' (may be a empty string or 'http//' or 'https//') and 'token' to 'arr'
                    arr.append(http_str)
                    arr.append(token)
                    # 'http_str' turn a empty string
                    http_str = ''
                elif (idx == size_of_term -1):
                    # if the current index represents the penultimate element
                    # of the array of terms, 'found_url' turns False
                    found_url = False

                    # so, we concatenate 'token' to '/' and append to 'arr'. 'http_str' turns a empty string again
                    http_str+= token + '/'
                    arr.append(http_str)
                    http_str = ''

                else:
                    # if 'token' isn't 'http:', 'https:', a logical operator nor the penultimate element of list
                    # we just concatenate 'token' with '/' and then concatenate with 'http_str'
                    http_str += token + '/'
            else:
                # if token, in this iteration, hasn't 'http', 'https' nor 'www.', just append token to 'arr'
                arr.append(token)
        return arr

    def attributes_functions_splitted_by_url(self, attributes_functions_str_url):
        """
        Receive a string with parameters for an url (the addres of requested resource)
        if this parameters contains another url inside it, return a list with two elements:
        the second element of the list will be this url and the first element
        will be the remaining string. If this piece of url doesn't contains another url
        return a list with one element, the 'attributes_functions_str_url' without changes
        :param attributes_functions_str_url:
        :return:
        """
        # try to find the 'http:' substring
        res = attributes_functions_str_url.lower().find('http:')
        if res == -1:
            # if 'http:' wasn't finded, search for 'https:'
            res = attributes_functions_str_url.lower().find('https:')
            if res == -1:
                # if 'https:' wasn't finded, search for 'www.'
                res = attributes_functions_str_url.lower().find('www.')
                if res == -1:
                    # if no one was finded, return the original 'attributes_functions_str_url' in the list form
                    return [attributes_functions_str_url]

        # Example: received string - /foo/bar/eq/http://192.168.0.25/example
        # the first element of the list will be: /foo/bar/eq/
        # the second element of the list will be: http://192.168.0.25/example
        return [attributes_functions_str_url[0:res], attributes_functions_str_url[res:]]

    def path_has_url(self, attributes_functions_str_url):
        """
        Receives a string with a piece of url representing the functions or attributes
        for this url and returns True if this string has 'http:', 'https:' or 'www.' substrings
        :param attributes_functions_str_url:
        :return:
        """
        return (attributes_functions_str_url.find('http:') > -1) or (attributes_functions_str_url.find('https:') > -1)\
               or (attributes_functions_str_url.find('www.') > -1)

    def _execute_attribute_or_method(self, object, attribute_or_method_name, array_of_attribute_or_method_name):
        """
        Return the value of 'object' attribute represented for
        'attribute_or_method_name' if this represents an 'object'
        attribute or return the value returned for 'object' method
        if 'attribute_or_method_name' represents an 'object' method
        :param object - the model object:
        :param attribute_or_method_name - a attribute or a method for this object:
        :param array_of_attribute_or_method_name - array of parameters for the operation (attribute_or_method_name):
        :return:
        """
        dic = {}
        parameters = []
        # verify if 'attribute_or_method_name' represents a operation of 'object'
        if OperationController().is_operation(object, attribute_or_method_name):
            # verify if 'attribute_or_method_name' represents a 'object' operation and, if this is True
            # verify if this operation has parameters
            # OBS: this second verification turn the first 'if' redundant
            if OperationController().operation_has_parameters(object, attribute_or_method_name):

                # this part of code refers to Q object (Query object from django)
                parameters = array_of_attribute_or_method_name[0].split('&')
                array_of_attribute_or_method_name = array_of_attribute_or_method_name[1:]

        # 'obj' is the value of the 'object' attribute if 'attribute_or_method_name' represents an 'object' attribute
        # or 'obj' is the value returned by 'object' method if 'attribute_or_method_name' represents an 'object' method,
        # 'parameters' may be used as parameter of 'attribute_or_method_name' is this case
        obj = self._value_from_object(object, attribute_or_method_name, parameters)

        # if 'array_of_attribute_or_method_name' is empty, just return the value of 'object' attribute/method
        if len(array_of_attribute_or_method_name) == 0:
            return obj

        # if the operation 'attribute_or_method_name' has parameters (array_of_attribute_or_method_name > 0)
        # active this method recursively sending:
        # - the value of 'object' attribute/method as the object,
        # - the first element of 'array_of_attribute_or_method_name' as the method/attribute of this object's method/attribute
        # (yes, the method/attribute of the method/attribute)
        # and the rest of the elements of 'array_of_attribute_or_method_name' as the parameters of this method/attribute
        return self._execute_attribute_or_method(obj, array_of_attribute_or_method_name[0], array_of_attribute_or_method_name[1:])

    def is_operation_and_has_parameters(self, attribute_or_method_name):
        """
        Return True if 'attribute_or_method_name' represents a operations
        for the geometric type of the FeatureModel instance geometric field,
        to return True this operation must have parameters. This is also valid
        for BusinessModel instance, but istead of geometric field we consider
        regular alphanumeric fields
        :param attribute_or_method_name:
        :return:
        """
        # 'dic' will be a dict with geometric operations for FeatureModel instance
        # (indeed operations for the type of geometric field in FeatureModel instance)
        # or a empty dict to BusinessModel
        dic = self.operations_with_parameters_type()

        # verify if the attribute/method name received represents a key of operations dict
        # and if it is True verify if this operations has parameters (verify if this Type_Called has parameters)
        return (attribute_or_method_name in dic) and len(dic[attribute_or_method_name].parameters)

    # method without use
    def function_name(self, attributes_functions_str):
        functions_dic = self.operations_with_parameters_type()
        if str(attributes_functions_str[-1]) in functions_dic:
            return str(attributes_functions_str[-1])
        return str(attributes_functions_str[-2])

    def response_resquest_with_attributes(self,  attributes_functions_name):
        """
        Return a response to the requested resource containing
        only the requested attributes/methods values (not the entire resource)
        :param attributes_functions_name - the attributes from the request resource:
        :return:
        """
        a_dict = {}
        # transform the parameters (separated by ',') in a list of arguments
        attributes = attributes_functions_name.strip().split(',')
        #self.current_object = self.object_model
        for attr_name in attributes:
            # gets the attribute value from the object model of this resource and stores in 'obj'
            # notice: we consider that 'attr_name' represents a attribute of object model or
            # a method without parameters ([])
            obj = self._value_from_object(self.object_model, attr_name, [])
            # sets 'a_dict' (the response data) with the name of the attribute/method as the index
            # and 'obj' as his respective value
            a_dict[attr_name] = obj

        # 'a_dict' turns the AbstractResource.current_object_state
        self.current_object_state = a_dict

        # return 'a_dict' as response body, application/json as Content-Type and 200 as response status code
        return (a_dict, CONTENT_TYPE_JSON, self.object_model, {'status': 200})

    def all_parameters_converted(self, attribute_or_function_name, parameters):
        """
        Receive a operation name 'attribute_or_function_name' and verifies if
        this is a FeatureModel or BusinessModel operation, and verify if the operation has parameters.
        If this is True convert each 'parameters' element into the respective type required
        by the operation (of FeatureModel or BusinessModel) represented by 'attribute_or_function_name'.
        The list of converted parameters is finally returned. If 'attribute_or_function_name' doesn't
        represent a FeatureModel or BusinessModel operation or it operation haven't parameters
        this method just repass the 'parameters' list to be converted by AbstractResouce.parametersConverted()
        into followed types: bool, int, float or GEOSGeometry.
        As previously, the list of converted parameters is finally returned
        :param attribute_or_function_name - the string representing a attribute of a function name of object model:
        :param parameters - the parameters list for the operation represented in 'attribute_or_function_name':
        :return:
        """
        parameters_converted = []
        # if 'attribute_or_function_name' is a operation (with parameters)
        # of geometric field of the FeatureModel instace or a operation for BusinessModel instance ...
        if self.is_operation_and_has_parameters(attribute_or_function_name):
            # - AbstractResource.operations_with_parameters_type()
            # return a operations dict to an FeatureModel instance field type (the geometric field)
            # or a empty dict to an BusinessModel
            # - we'll use 'attribute_or_function_name' to get a specific operations in this dict
            # and finally we'll get the parameters type for this operation and stores in 'parameters_type'
            # - 'parameters_type' will be something like this: [float, int]
            parameters_type = self.operations_with_parameters_type()[attribute_or_function_name].parameters
            for i in range(0, len(parameters)):
                # here, each parameter value in 'parameters' will be converted
                # to the expected type in a operation represented by
                # 'attribute_or_function_name' for this object model
                # ex: first iteration - float('1.2'), second iteration - int('5')
                # the values in 'parameter' probably will be string pieces from url
                parameters_converted.append(parameters_type[i](parameters[i]))

            # return a list like [1.2, 5]
            return parameters_converted

        # if 'attribute_or_function_name' isn't a operation of FeatureModel or BusinessModel with parameters
        # we just convert the received 'parameters' (a list of string) into a list of elements with
        # the fallwed types: bool, int, float or GEOSGeometry
        return self.parametersConverted(parameters)

    def is_attribute_for(self, object, attribute_or_function_name):
        """
        Return True if 'atribute_or_function_name' represents an 'object' attribute
        :param object:
        :param attribute_or_function_name:
        :return:
        """
        # - hasattr() verifies if 'atribute_or_function_name' is an 'object' attribute
        # - getattr() gets 'atribute_or_function_name' if this represents an 'object' attribute
        # if 'atribute_or_function_name' represents an 'object' method, return this (i.e. returns a callable object)
        return  hasattr(object, attribute_or_function_name) and not callable(getattr(object, attribute_or_function_name))

    def _value_from_object(self, object, attribute_or_function_name, parameters):
        """
        If 'attribute_or_function_name' is an 'object' attribute, return his value.
        If 'attribute_or_function_name' is an 'object' operation, return the value
        returned by this operation using the received 'parameters' to do it if necessary
        :param object - the model object:
        :param attribute_or_function_name - a attribute or a method for this object:
        :param parameters:
        :return:
        """
        # exclude the blank spaces of 'attribute_or_function_name' edges
        attribute_or_function_name_striped = attribute_or_function_name.strip()
        # 'attribute_or_function_name_striped' turns the last operation executed
        self.name_of_last_operation_executed = attribute_or_function_name_striped

        if self.is_attribute_for(object, attribute_or_function_name):
            # if 'atribute_or_function_name' represents an 'object' attribute return his value
            return getattr(object, attribute_or_function_name_striped)

        # if 'atribute_or_function_name' isn't an 'object' attribute, this represents an 'object' operation
        # in this case, we verify if this operation has parameters (received by this method)
        if len(parameters)> 0:

            if (isinstance(object, BusinessModel) or isinstance(object, GEOSGeometry)):
                # if 'object' is a BusinessModel or GOESGeomety instance, we repass operation name
                # ('attribute_or_function_name_striped') and his parameters to
                # AbstractResouce.all_parameters_converted() to convert each parameter to the required
                # type by the operation, represented for 'attribute_or_function_name_striped'. In the case of
                # GEOSGeometry instances, the parameters could be converted to one of the followed types:
                # bool, int, float or GEOSGeometry (AbstractResouce.all_parameters_converted() process only
                # FeatureModel and BusinessModel instance and repass the other instances to
                # AbstractResouce.parametersConverted())
                params = self.all_parameters_converted(attribute_or_function_name_striped, parameters)
            else:
                # ConverterType.convert_parameters() convert 'parameters' values to match with
                # 'attribute_or_function_name' operation parameters types of 'object' type
                # Example: 'parameters' = ['1.2', '5', 'test']
                #           Type_Called.parameters = [float, int, str]
                #           return = [1.2, 5, 'test']
                # OBS: Type_Called is the operation itself references to 'attribute_or_function_name' operation of object type
                params = ConverterType().convert_parameters(type(object), attribute_or_function_name, parameters)

            # after the 'params' convertion above, we execute the 'object' method
            # (represented by 'attribute_or_function_name_striped') sending the 'params'
            # list and return his value
            return getattr(object, attribute_or_function_name_striped)(*params)

        # if there's no parameters, we simply get the 'object' method/operation with getattr(),
        # execute this (observer the '()') and return the value returned by this method
        return getattr(object, attribute_or_function_name_striped)()

    def parametersConverted(self, params_as_array):
        """
        Convert each string in 'params_as_array' to one of this type:
        bool, int, float, GEOSGeometry or if the string is an url, try to
        request this url and convert the response data to GEOSGeometry.
        If the request fails or return a status code representing a error,
        raise ConnectionError or HTTPError
        :param params_as_array - a array of strings (probably pieces from url):
        :return:
        """
        paramsConveted = []

        for value in params_as_array:

            # if the parameter is 'true' or 'false'
            # convert it to bool and append to list
            if value.lower() == 'true':
                paramsConveted.append(True)
                continue
            elif value.lower() == 'false':
                paramsConveted.append(False)
                continue

            # if parameter is not 'true' nor 'false'
            # we try to convert to int, if it fails,
            # we try to convert to float, if it still fails,
            # we tru to convert to GEOSGeometry
            try:
                paramsConveted.append(int( value ) )
                continue
            except ValueError:
                pass
            try:
               paramsConveted.append( float( value ) )
               continue
            except ValueError:
                pass
            try:
               paramsConveted.append( GEOSGeometry( value ) )
               continue
            except ValueError:
                pass
            try:
                # if the parameter starts with 'http', we make a request to this parameter
                http_str = (value[0:4]).lower()
                if (http_str == 'http'):
                    resp = requests.get(value)
                    # if this request return a response status between 400 and 599, we raise a HttpError
                    if 400 <= resp.status_code <= 599:
                        raise HTTPError({resp.status_code: resp.reason})

                    # if the request not return an error status, we get the response body in JSON format
                    js = resp.json()

                    # if 'type' is 'feature' or 'featurecollection' it has an 'geometry'
                    if (js.get("type") and js["type"].lower() in ['feature', 'featurecollection']):
                        # in this case, we get the geometric data from this JSON response
                        a_geom = js["geometry"]
                    else:
                        # otherwise, we simply get the entire dict
                        a_geom = js
                    # finally, we convert 'a_geom' to json and then convert the result to GEOSGeometry
                    # appending this to paramsConvertd list. OBS: you must notice that we consider that
                    # the request from the parameter will bring us a geometric resource
                    paramsConveted.append(GEOSGeometry((json.dumps(a_geom))))
            except (ConnectionError,  HTTPError) as err:
                print('Error: '.format(err))
                #paramsConveted.append (value)

        return paramsConveted

    def generate_tmp_file(self, suffix='', length_name=10):
        return ''.join([random.choice('0123456789ABCDEF') for i in range(length_name)]) + suffix

    def get_style_file(self, request):
        if 'HTTP_LAYERSTYLE' in request.META:
            layer_style_url = request.META['HTTP_LAYERSTYLE']
            response = requests.get(layer_style_url)
            if response.status_code == 200:
                file_name = self.generate_tmp_file(suffix="_tmp_style.xml")
                with open(file_name, "w+") as st:
                    st.write(response.text.encode('UTF-8'))
                    st.close()
                return file_name
        return None

    def get_png(self, queryset, request):
        style = self.get_style_file(request)

        if isinstance(queryset, GEOSGeometry):
            wkt = queryset.wkt
            geom_type = queryset.geom_type
        else:
            wkt = queryset.geom.wkt
            geom_type = queryset.geom.geom_type

        config = {'wkt': wkt, 'type': geom_type}
        if style is not None:
            config["style"] = style
            config["deleteStyle"] = True
        builder_png = BuilderPNG(config)
        return builder_png.generate()

class NonSpatialResource(AbstractResource):

    def response_of_request(self,  attributes_functions_str):
        att_funcs = attributes_functions_str.split('/')
        if (not self.is_operation(att_funcs[0])) and self.is_attribute(att_funcs[0]):
            att_funcs = att_funcs[1:]

        self.current_object_state = self._execute_attribute_or_method(self.object_model, att_funcs[0], att_funcs[1:])

        if hasattr(self.current_object_state, 'model') and issubclass(self.current_object_state.model, Model):
            class_name = self.current_object_state.model.__name__ + 'Serializer'
            serializer_cls = self.object_model.class_for_name(self.serializer_class.__module__, class_name)
            if isinstance(self.current_object_state, QuerySet):
                self.current_object_state = serializer_cls(self.current_object_state, many=True,
                                                           context={'request': self.request}).data
            elif isinstance(self.current_object_state.field, OneToOneField):
                self.current_object_state = serializer_cls(self.current_object_state, context={'request': self.request}).data
            else:
                self.current_object_state = serializer_cls(self.current_object_state, many=True, context={'request': self.request}).data

        a_value = {self.name_of_last_operation_executed: self.current_object_state}

        return (a_value, CONTENT_TYPE_JSON, self.object_model, {'status': 200})

    def basic_get(self, request, *args, **kwargs):

        self.object_model = self.get_object(kwargs)
        self.current_object_state = self.object_model
        self.set_basic_context_resource(request)
        # self.request.query_params.
        attributes_functions_str = kwargs.get(self.attributes_functions_name_template())

        if self.is_simple_path(attributes_functions_str):

            serializer = self.serializer_class(self.object_model, context={'request': self.request})
            output = (serializer.data, CONTENT_TYPE_JSON, self.object_model, {'status': 200})

        elif self.path_has_only_attributes(attributes_functions_str):
            output = self.response_resquest_with_attributes(attributes_functions_str.replace(" ", ""))
            dict_attribute = output[0]
            if len(attributes_functions_str.split(',')) > 1:
                self._set_context_to_attributes(dict_attribute.keys())
            else:
                self._set_context_to_only_one_attribute(attributes_functions_str)
        elif self.path_has_url(attributes_functions_str.lower()):
            output = self.response_request_attributes_functions_str_with_url( attributes_functions_str)
            self.context_resource.set_context_to_object(self.current_object_state, self.name_of_last_operation_executed)
        else:
            output = self.response_of_request(attributes_functions_str)
            self._set_context_to_operation(self.name_of_last_operation_executed)

        return output

    def get(self, request, *args, **kwargs):

        dict_for_response = self.basic_get(request, *args, **kwargs)
        status = dict_for_response[3]['status']
        if status in [400, 401,404]:
            return Response({'Error ': 'The request has problem. Status:' + str(status)}, status=status)

        if status in [500]:
           return Response({'Error ': 'The server can not process this request. Status:' + str(status)}, status=status)

        accept = request.META['HTTP_ACCEPT']


        return Response(data=dict_for_response[0], content_type=dict_for_response[1])

    def options(self, request, *args, **kwargs):
        self.basic_get(request, *args, **kwargs)
        #return self.context_resource.context()
        return Response ( data=self.context_resource.context(), content_type='application/ld+json' )

class StyleResource(AbstractResource):
    pass

class SpatialResource(AbstractResource):

    def __init__(self):
        super(SpatialResource, self).__init__()
        self.iri_style = None

    def get_geometry_object(self, object_model):
        return getattr(object_model, self.geometry_field_name(), None)

    def geometry_field_name(self):
        return self.serializer_class.Meta.geo_field

    def make_geometrycollection_from_featurecollection(self, feature_collection):
        geoms = []
        features = json.loads(feature_collection)
        for feature in features['features']:
            feature_geom = json.dumps(feature['geometry'])
            geoms.append(GEOSGeometry(feature_geom))
        return GeometryCollection(tuple(geoms))

    def all_parameters_converted(self, attribute_or_function_name, parameters):
        parameters_converted = []
        if self.is_operation_and_has_parameters(attribute_or_function_name):
            parameters_type = self.operations_with_parameters_type()[attribute_or_function_name].parameters
            for i in range(0, len(parameters)):
                if GEOSGeometry == parameters_type[i]:
                    if not (parameters[i][0] == '{' or parameters[i][0] == '['):
                        parameters_converted.append(GEOSGeometry(parameters[i]))

                    else:
                        geometry_dict = json.loads(parameters[i])

                        if isinstance(geometry_dict, dict) and geometry_dict['type'].lower() == 'feature':
                            parameters_converted.append(parameters_type[i](json.dumps(geometry_dict['geometry'])))
                        elif isinstance(geometry_dict, dict) and geometry_dict['type'].lower() == 'featurecollection':
                            geometry_collection = self.make_geometrycollection_from_featurecollection(parameters[i])
                            parameters_converted.append(parameters_type[i](geometry_collection))
                        else:
                            parameters_converted.append(parameters_type[i](parameters[i]))
                else:
                    parameters_converted.append(parameters_type[i](parameters[i]))


            return parameters_converted

        return self.parametersConverted(parameters)

    def _value_from_objectOLD(self, object, attribute_or_function_name, parameters):

        attribute_or_function_name_striped = attribute_or_function_name.strip()
        self.name_of_last_operation_executed = attribute_or_function_name_striped
        if len(parameters):
            params = self.all_parameters_converted(attribute_or_function_name_striped, parameters)
            return getattr(object, attribute_or_function_name_striped)(*params)

        return getattr(object, attribute_or_function_name_striped)

    def parametersConverted(self, params_as_array):
        paramsConveted = []

        for value in params_as_array:
            if value.lower() == 'true':
                paramsConveted.append(True)
                continue
            elif value.lower() == 'false':
                paramsConveted.append(False)
                continue

            try:
                paramsConveted.append(int( value ) )
                continue
            except ValueError:
                pass
            try:
               paramsConveted.append( float( value ) )
               continue
            except ValueError:
                pass
            try:
               paramsConveted.append( GEOSGeometry( value ) )
               continue
            except ValueError:
                pass
            try:
                http_str = (value[0:4]).lower()
                if (http_str == 'http'):
                    resp = requests.get(value)
                    if 400 <= resp.status_code <= 599:
                        raise HTTPError({resp.status_code: resp.reason})
                    js = resp.json()

                    if (js.get("type") and js["type"].lower() in ['feature', 'featurecollection']):
                        a_geom = js["geometry"]
                    else:
                        a_geom = js
                    paramsConveted.append(GEOSGeometry((json.dumps(a_geom))))
            except (ConnectionError,  HTTPError) as err:
                print('Error: '.format(err))
                #paramsConveted.append (value)

        return paramsConveted

    def dict_as_geojson(self, a_dict):
        d = {}
        d["type"] = "Feature"
        d["geometry"] = a_dict[self.geometry_field_name()]
        a_dict.pop(self.geometry_field_name(), None)
        d["properties"] = a_dict
        return d



class FeatureResource(SpatialResource):

    def __init__(self):
        super(FeatureResource, self).__init__()

    # Must be override
    def initialize_context(self):
        pass

    def is_spatial_attribute(self, attribute_name):
        return self.model.geo_field_name() == attribute_name.lower()

    def operations_with_parameters_type(self):

        dic = self.object_model.operations_with_parameters_type()
        return dic

    #Responds a List with four elements: value of what was requested, content_type, object, dict=>dic[status] = status_code
    def response_resquest_with_attributes(self, attributes_functions_name, request=None):
        a_dict ={}
        attributes = attributes_functions_name.strip().split(',')

        for attr_name in attributes:
           obj = self._value_from_object(self.object_model, attr_name, [])
           if isinstance(obj, GEOSGeometry):
               geom = obj
               obj = json.loads(obj.geojson)
               if len(attributes) == 1:
                   return RequiredObject(obj, self.content_type_or_default_content_type(request), geom, 200)
           a_dict[attr_name] = obj
        if self.geometry_field_name() in attributes:
            a_dict = self.dict_as_geojson(a_dict)
        self.current_object_state = a_dict
        return RequiredObject(a_dict, CONTENT_TYPE_JSON, self.object_model,  200)

    def response_request_attributes_functions_str_with_url(self, attributes_functions_str, request=None):
        # r':/+' matches string like: ':' followed by at least 1 occurence of '/'
        # substitute any occurences of ':/' to '://' in 'attributes_functions_str'
        attributes_functions_str = re.sub(r':/+', '://', attributes_functions_str)
        arr_of_two_url = self.attributes_functions_splitted_by_url(attributes_functions_str)
        resp = requests.get(arr_of_two_url[1])
        if resp.status_code in[400, 401, 404]:
            return RequiredObject({},CONTENT_TYPE_JSON, self.object_model,  resp.status_code)
        if resp.status_code == 500:
            return RequiredObject({},CONTENT_TYPE_JSON, self.object_model,resp.status_code)
        j = resp.text
        attributes_functions_str = arr_of_two_url[0] + j
        #external_etag = resp.headers['etag']
        #self.inject_e_tag(external_etag)
        return self.response_of_request(attributes_functions_str)

    def response_of_request(self,  attributes_functions_str):
        att_funcs = attributes_functions_str.split('/')
        self.current_object_state = self._execute_attribute_or_method(self.object_model, att_funcs[0], att_funcs[1:])
        a_value = self.current_object_state
        if isinstance(a_value, GEOSGeometry):
            geom = a_value
            a_value = json.loads(a_value.geojson)
            return RequiredObject(a_value, CONTENT_TYPE_GEOJSON, self.object_model,  200)
        elif isinstance(a_value, SpatialReference):
           a_value = { self.name_of_last_operation_executed: a_value.pretty_wkt}
        elif isinstance(a_value, memoryview) or isinstance(a_value, buffer):
           return RequiredObject(a_value, CONTENT_TYPE_OCTET_STREAM, self.object_model,200)
        else:
            a_value = {self.name_of_last_operation_executed: a_value}

        return RequiredObject(a_value, CONTENT_TYPE_JSON, self.object_model, 200)


    def response_base_get(self, request, *args, **kwargs):
        resource = self.resource_in_cache_or_None(request)
        if resource is not None:
            return self.response_base_object_in_cache(request )

        required_object = self.basic_get(request, *args, **kwargs)
        status = required_object.status_code
        if status in [400,401,404]:
            return Response({'Error ': 'The request has problem. Status:' + str(status)}, status=status)
        if status in [500]:
           return Response({'Error ': 'The server can not process this request. Status:' + str(status)}, status=status)

        if self.is_image_content_type(request, **kwargs):
           return self.response_base_get_with_image(request, required_object)

        if self.is_binary_content_type(required_object) or self.accept_is_binary(request):
            return self.response_base_get_binary(request, required_object)

        key = self.get_key_cache(request, a_content_type=required_object.content_type)

        self.set_key_with_data_in_cache(key, self.e_tag, required_object.representation_object )

        resp =  Response(data=required_object.representation_object,status=200, content_type=required_object.content_type)
        self.set_etag_in_header(resp, self.e_tag)
        return resp


    def basic_get(self, request, *args, **kwargs):

        self.object_model = self.get_object(kwargs)
        self.current_object_state = self.object_model
        self.set_basic_context_resource(request)
        self.e_tag = str(hash(self.object_model))
        # self.request.query_params.
        attributes_functions_str = kwargs.get(self.attributes_functions_name_template())
        if self.is_simple_path(attributes_functions_str):
            serializer = self.serializer_class(self.object_model)
            required_object = RequiredObject(serializer.data, self.content_type_or_default_content_type(request), self.object_model, 200)

        elif self.path_has_only_attributes(attributes_functions_str):
            str_attribute = attributes_functions_str.replace(" ", "").replace("/","")
            required_object = self.response_resquest_with_attributes(str_attribute , request)

            att_names = attributes_functions_str.split(',')
            if len(att_names) > 1:
                self._set_context_to_attributes(att_names)
            else:
                self._set_context_to_only_one_attribute(attributes_functions_str)
        elif self.path_has_url(attributes_functions_str.lower()):
            required_object = self.response_request_attributes_functions_str_with_url(attributes_functions_str, request)
            self.context_resource.set_context_to_object(self.current_object_state, self.name_of_last_operation_executed)
        else:
            s = str(attributes_functions_str)
            if s[-1] == '/':
               s = s[:-1]
            required_object = self.response_of_request(s)
            self._set_context_to_operation(self.name_of_last_operation_executed)
        self.inject_e_tag()
        self.temporary_content_type= required_object.content_type
        return required_object

    def basic_required_object(self, request, *args, **kwargs):

        return self.basic_get(request, *args, **kwargs)

    def default_content_type(self):
        return self.temporary_content_type if self.temporary_content_type is not None else CONTENT_TYPE_GEOJSON

    def options(self, request, *args, **kwargs):
        self.basic_get(request, *args, **kwargs)
        #return self.context_resource.context()
        return Response ( data=self.context_resource.context(), content_type='application/ld+json' )

class AbstractCollectionResource(AbstractResource):

    def __init__(self):
        super(AbstractCollectionResource, self).__init__()
        self.queryset = None

    def token_is_http_or_https(self, token):
        """
        Return True if 'token' (part of absolute uri) is 'http\:' or 'https:'
        :param token:
        :return:
        """
        return  token.lower() in ['http:', 'https:']

    def token_is_http(self, token):
        return 'http:' == token

    def token_is_https(self, token):
        return 'https:' == token

    def token_is_www(self, token):
        """
        Return True if 'token' (part of absolute uri) has the 'www.' string
        :param token:
        :return:
        """
        return True if token.find('www.') > -1 else False

    def token_is_http_or_https_or_www(self, token):
        """
        Return True if 'token' (part of absolute uri) is 'http:', 'https:' or has the 'www.' string
        :param token:
        :return:
        """
        return  self.token_is_http_or_https(token) or self.token_is_www(token)

    def logical_operators(self):
        """
        Returns FactoryComplexQuery logical operators (or, and, *or, *and)
        :return:
        """
        return FactoryComplexQuery().logical_operators()

    def attributes_functions_str_is_filter_with_spatial_operation(self, attributes_functions_str):

        arr_str = attributes_functions_str.split('/')[1:]

        geom_ops = self.operation_controller.geometry_operations_dict()

        for str in arr_str:
            if self.is_spatial_attribute(str):
              ind = arr_str.index(str)
              if ind +1 <= len(arr_str):
                return arr_str[ind + 1] in geom_ops()

        return False

    def path_has_filter_operation(self, attributes_functions_str):
        att_funcs = attributes_functions_str.split('/')
        return len(att_funcs) > 1 and  (att_funcs[0].lower() == 'filter')

    def path_has_groupBy_operation(self, attributes_functions_str):
        att_funcs = attributes_functions_str.split('/')
        att_funcs = [ele for ele in att_funcs if ele != '']
        return len(att_funcs) == 2 and (att_funcs[0].lower() == 'groupby')

    def path_has_groupByCount_operation(self, attributes_functions_str):
        att_funcs = attributes_functions_str.split('/')
        att_funcs = [ele for ele in att_funcs if ele != '']
        return len(att_funcs) == 2 and (att_funcs[0].lower() == 'groupbycount')

    def path_has_distinct_operation(self, attributes_functions_str):
        att_funcs = attributes_functions_str.split('/')
        att_funcs = [ele for ele in att_funcs if ele != '']
        return len(att_funcs) == 2 and (att_funcs[0].lower() == 'distinct')

    def path_has_countResource_operation(self, attributes_functions_str):
        att_funcs = attributes_functions_str.split('/')
        att_funcs = [ele for ele in att_funcs if ele !='']
        return len(att_funcs) == 1 and  (att_funcs[0].lower() == 'countresource')

    def path_has_map_operation(self, attributes_functions_str):
        att_funcs = attributes_functions_str.split('/')
        return len(att_funcs) > 1 and (att_funcs[0].lower() == 'map')

    def path_has_offsetLimit_operation(self, attributes_functions_str):
        att_funcs = attributes_functions_str.split('/')
        att_funcs = [ele for ele in att_funcs if ele != '']
        return len(att_funcs) == 2 and  (att_funcs[0].lower() == 'offsetlimit')

    def q_object_for_filter_array_of_terms(self, array_of_terms):
        return FactoryComplexQuery().q_object_for_filter_expression(None, self.model_class(), array_of_terms)

    def q_object_for_filter_expression(self, attributes_functions_str):
        arr = attributes_functions_str.split('/')

        if self.path_has_url(attributes_functions_str):
           arr = self.transform_path_with_url_as_array(arr)

        return self.q_object_for_filter_array_of_terms(arr[1:])

    def get_objects_from_filter_operation(self, attributes_functions_str):
        q_object = self.q_object_for_filter_expression(attributes_functions_str)
        return self.model_class().objects.filter(q_object)

    def get_objects_from_map_operation(self, attributes_functions_str):
        q_object = self.q_object_for_filter_expression(attributes_functions_str)
        return self.model_class().objects.filter(q_object)

    def get_objects_from_distinct_operation(self, attributes_functions_str):
        attributes_functions_list = attributes_functions_str.split('/')
        attributes_functions_list = [attr_func for attr_func in attributes_functions_list if attr_func != '']
        parameters = attributes_functions_list[1:]
        return self.model_class().objects.distinct(*parameters)

    def get_objects_from_groupBy_operation(self, attributes_functions_str):
        attributes_functions_list = attributes_functions_str.split('/')
        attributes_functions_list = [attr_func for attr_func in attributes_functions_list if attr_func != '']
        parameters = attributes_functions_list[1:][0].split(',')
        return self.model_class().objects.values(*parameters)

    def get_objects_from_groupByCount_operation(self, attributes_functions_str):
        attributes_functions_list = attributes_functions_str.split('/')
        attributes_functions_list = [attr_func for attr_func in attributes_functions_list if attr_func != '']
        parameters = attributes_functions_list[1:][0].split(',')
        return self.model_class().objects.values(*parameters).annotate(count=Count(*parameters))

    def get_objects_from_offsetLimit_operation(self, attributes_functions_str):
        attributes_functions_list = attributes_functions_str.split('/')
        attributes_functions_list = [attr_func for attr_func in attributes_functions_list if attr_func != '']

        converted_params = self.converter_collection_operation_parameters(attributes_functions_list[0], attributes_functions_list[1:][0].split('&'))
        offset = converted_params[0]
        limit = converted_params[1]

        objects = self.model_class().objects.all()[offset:offset + limit]
        return objects

    def converter_collection_operation_parameters(self, operation_name, parameters):
        """
        Receive a operation name for a collection resource and a list of parameters
        for this operation. If this operation name corresponds to an collection operations
        dict key, convert each element into the parameters list to the expected type for
        the respective collection operation. Return the parameters intact if the operation
        name isn't in the collection operations dict.
        :param operation_name:
        :param parameters:
        :return:
        """
        # gets the dict whit all operations for collections
        collection_operations_dict = OperationController().collection_operations_dict()
        if operation_name in collection_operations_dict:
            # if operation_name is a collection operations dict key, return the related Type_Called
            type_called = collection_operations_dict[operation_name]
            # convert each element in 'parameter' to the respective parameter type in Type_Called.parameters
            converted_parameters = [ConverterType().value_converted(param, parameters[i]) for i, param in enumerate(type_called.parameters)]
            return converted_parameters

        # returning the parameters without convertion
        return parameters

    def operation_names_model(self):
        return self.operation_controller.collection_operations_dict()

    def basic_options(self, request, *args, **kwargs):
        self.object_model = self.model_class()()
        self.set_basic_context_resource(request)
        attributes_functions_str = self.kwargs.get("attributes_functions", None)

        if self.is_simple_path(attributes_functions_str):  # to get query parameters
            return {"data": {},"status": 200, "content_type": CONTENT_TYPE_JSON}

        elif self.path_has_only_attributes(attributes_functions_str):
            output = self.response_resquest_with_attributes(attributes_functions_str.replace(" ", ""))
            dict_attribute = output[0]
            if len(attributes_functions_str.split(',')) > 1:
                self._set_context_to_attributes(dict_attribute.keys())
            else:
                self._set_context_to_only_one_attribute(attributes_functions_str)
            return {"data": {},"status": 200, "content_type": CONTENT_TYPE_JSON}

        #elif self.path_has_url(attributes_functions_str.lower()):
        #    pass
        elif self.path_has_only_spatial_operation(attributes_functions_str):
            return {"data": self.get_objects_with_spatial_operation_serialized(attributes_functions_str), "status": 200,
                    "content_type": CONTENT_TYPE_JSON}

        elif self.path_has_operations(attributes_functions_str) and self.path_request_is_ok(attributes_functions_str):
            return {"data": self.get_objects_serialized_by_functions(attributes_functions_str),"status": 200, "content_type": CONTENT_TYPE_JSON}

        else:
            return {"data": "This request has invalid attribute or operation","status": 400, "content_type": CONTENT_TYPE_JSON}

    def options(self, request, *args, **kwargs):
        self.basic_options(request, *args, **kwargs)
        #return self.context_resource.context()
        return Response ( data=self.context_resource.context(), content_type='application/ld+json' )

    def basic_post(self, request):
        response =  Response(status=status.HTTP_201_CREATED, content_type=CONTENT_TYPE_JSON)
        response['Content-Location'] = request.path + str(self.object_model.pk)
        return response

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        if serializer.is_valid():
            obj =  serializer.save()
            self.object_model = obj
            return self.basic_post(request)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CollectionResource(AbstractCollectionResource):

    def operations_with_parameters_type(self):
        return self.operation_controller.collection_operations_dict()

    def get_objects_serialized(self):
        objects = self.model_class().objects.all()
        return self.serializer_class(objects, many=True, context={'request': self.request}).data

    def get_objects_by_only_attributes(self, attribute_names_str):
        arr = []
        attribute_names_str_as_array = attribute_names_str.split(',')

        return self.model_class().objects.values(*attribute_names_str_as_array)

    def get_objects_serialized_by_only_attributes(self, attribute_names_str, query_set):
        arr = []
        attribute_names_str_as_array = attribute_names_str.split(',')
        for obj in query_set:
            a_dic = {}
            for att_name in attribute_names_str_as_array:
                a_dic[att_name] = obj[att_name]
                arr.append(a_dic)
        return arr

    def get_objects_by_functions(self, attributes_functions_str):

        objects = []
        if self.path_has_filter_operation(attributes_functions_str):
            objects = self.get_objects_from_filter_operation(attributes_functions_str)
        return objects


    def get(self, request, *args, **kwargs):

        response = self.basic_get(request, *args, **kwargs)
        self.add_base_headers(request, response)
        return response

    def basic_get(self, request, *args, **kwargs):
        self.object_model = self.model_class()()
        self.set_basic_context_resource(request)
        attributes_functions_str = self.kwargs.get("attributes_functions", None)

        if self.is_simple_path(attributes_functions_str):  # to get query parameters
            objects = self.model_class().objects.all()
            serialized_data =  self.serializer_class(objects, many=True, context={'request': request}).data
            resp =  Response(data= serialized_data,status=200, content_type=CONTENT_TYPE_JSON)
            self.add_key_value_in_header(resp, ETAG, str(hash(objects)))
            return resp

        elif self.path_has_only_attributes(attributes_functions_str):
            query_set = self.get_objects_by_only_attributes(attributes_functions_str)
            serialized_data = self.get_objects_serialized_by_only_attributes(attributes_functions_str, query_set)
            resp =  Response(data= serialized_data,status=200, content_type=CONTENT_TYPE_JSON)
            self.add_key_value_in_header(resp, ETAG, str(hash(query_set)))
            return resp

        elif self.path_has_distinct_operation(attributes_functions_str):
            resp =  self.get_objects_from_distinct_operation(attributes_functions_str)
            return resp
        elif self.path_has_countResource_operation(attributes_functions_str):
            resp =  Response(data={"countResource": self.model_class().objects.count()},status=200, content_type=CONTENT_TYPE_JSON)
            return resp

        elif self.path_has_offsetLimit_operation(attributes_functions_str):
            query_set = self.get_objects_from_offsetLimit_operation(attributes_functions_str)
            serialized_data = self.serializer_class(query_set, many=True, context={'request': request}).data
            resp = Response(data=serialized_data, status=200, content_type=self.content_type_or_default_content_type(request))
            return resp

        elif self.path_has_operations(attributes_functions_str) and self.path_request_is_ok(attributes_functions_str):
            objects = self.get_objects_by_functions(attributes_functions_str)
            serialized_data = self.serializer_class(objects, many=True, context={'request': request} ).data
            resp =  Response(data= serialized_data,status=200, content_type=CONTENT_TYPE_JSON)
            self.add_key_value_in_header(resp, ETAG, str(hash(objects)))
            return resp

        else:

            return Response(data="This request has invalid attribute or operation", status=400, content_type=CONTENT_TYPE_JSON)

class SpatialCollectionResource(AbstractCollectionResource):

    #todo
    def path_request_is_ok(self, attributes_functions_str):
        return True

    def geometry_field_name(self):
        return self.serializer_class.Meta.geo_field

    def operation_names_model(self):
        return self.operation_controller.feature_collection_operations_dict().keys()

    def path_has_only_spatial_operation(self, attributes_functions_str):
        pass

class FeatureCollectionResource(SpatialCollectionResource):

    def geometry_operations(self):
        return self.operation_controller.geometry_operations_dict()

    def geometry_field_name(self):
        return self.serializer_class.Meta.geo_field

    def is_spatial_attribute(self, attribute_name):
        return attribute_name == self.geometry_field_name()

    def is_spatial_operation(self, operation_name):
        return operation_name in self.geometry_operations()

    def path_has_only_spatial_operation(self, attributes_functions_str):

        att_funcs = attributes_functions_str.split('/')
        spatial_operation_names = self.geometry_operations().keys()

        if (len(att_funcs) > 1 and (att_funcs[0].lower() in spatial_operation_names)):
           return True

        return  (att_funcs[1].lower() in spatial_operation_names)

    def is_filter_with_spatial_operation(self, attributes_functions_str):
        att_funcs = attributes_functions_str.split('/')
        return (len(att_funcs) > 1 and (att_funcs[0].lower() in self.geometry_operations().keys())) or self.attributes_functions_str_is_filter_with_spatial_operation(attributes_functions_str)

    def operations_with_parameters_type(self):
        return self.operation_controller.feature_collection_operations_dict()

    def get_objects_from_spatial_operation(self, array_of_terms):
        q_object = self.q_object_for_filter_array_of_terms(array_of_terms)
        return self.model_class().objects.filter(q_object)

    def is_end_of_term(self, term):
        """
        Return True if 'term' is 'or', 'and', '*or' or '*and'
        :param term:
        :return:
        """
        return term in self.logical_operators()

    def inject_geometry_attribute_in_spatial_operation_for_path(self, arr_of_term):
        indexes = []
        for idx, term in enumerate(arr_of_term):
            if term in self.geometry_operations():
                indexes.append(idx)
        count = 0
        for i in indexes:
            arr_of_term.insert(i + count, self.geometry_field_name())
            count+=1

        return arr_of_term

    def path_has_geometry_attribute(self, term_of_path):
        return term_of_path.lower() == self.geometry_field_name()

    def get_objects_with_spatial_operation(self, attributes_functions_str):
        att_func_arr = attributes_functions_str.split('/')
        arr = att_func_arr
        if self.is_spatial_operation(att_func_arr[0]) and not self.path_has_geometry_attribute(att_func_arr[0]):
            if self.path_has_url(attributes_functions_str):
                arr = self.transform_path_with_url_as_array(att_func_arr)
            arr = self.inject_geometry_attribute_in_spatial_operation_for_path(arr)
        return self.get_objects_from_spatial_operation(arr)

    def get_objects_by_only_attributes(self, attribute_names_str):
        arr = []
        attribute_names_str_as_array = attribute_names_str.split(',')
        return self.model_class().objects.values(*attribute_names_str_as_array)

    def get_objects_serialized_by_only_attributes(self, attribute_names_str, objects):
        arr = []
        attribute_names_str_as_array = attribute_names_str.split(',')
        for dic in objects:
            a_dic = {}
            for att_name in attribute_names_str_as_array:
                a_dic[att_name] = dic[att_name] if not isinstance(dic[att_name], GEOSGeometry) else json.loads(dic[att_name].json)
                arr.append(a_dic)
        return arr

    def get_objects_by_functions(self, attributes_functions_str):

        objects = []
        #if self.path_has_filter_operation(attributes_functions_str) or self.path_has_spatial_operation(attributes_functions_str) or  self.is_filter_with_spatial_operation(attributes_functions_str):
        if self.path_has_filter_operation(attributes_functions_str) or self.is_filter_with_spatial_operation(attributes_functions_str):
            objects = self.get_objects_from_filter_operation(attributes_functions_str)
        elif self.path_has_map_operation(attributes_functions_str):
            objects = self.get_objects_from_map_operation(attributes_functions_str)

        return objects

    def hashed_value(self, object):
        dt = datetime.now()
        local_hash = self.__class__.__name__ + str(dt.microsecond)
        return local_hash

    def basic_response(self, request, objects):

        serialized_data =  self.serializer_class(objects, many=True, context={'request': request}).data
        resp =  Response(data= serialized_data,status=200, content_type=CONTENT_TYPE_JSON)
        dt = datetime.now()
        local_hash = self.hashed_value(None)
        self.add_key_value_in_header(resp, ETAG, local_hash)
        iri_with_content_type = request.build_absolute_uri() + request.META[HTTP_ACCEPT]
        cache.set(iri_with_content_type,(local_hash, serialized_data), 3600)
        return resp

    def required_object(self, request, objects):
        serialized_data =  self.serializer_class(objects, many=True, context={'request': request}).data
        required_obj =  RequiredObject(serialized_data,self.content_type_or_default_content_type(request), objects, 200)
        return required_obj

    def required_object_for_aggregation_operation(self, request, dic):
        required_obj =  RequiredObject(dic,self.content_type_or_default_content_type(request), dic, 200)
        return required_obj

    def basic_get(self, request, *args, **kwargs):

        self.object_model = self.model_class()()
        self.set_basic_context_resource(request)
        attributes_functions_str = self.kwargs.get("attributes_functions", None)
        self.inject_e_tag()
        if self.is_simple_path(attributes_functions_str):
            objects = self.model_class().objects.all()
            serializer = self.serializer_class(objects, many=True)
            required_object = RequiredObject(serializer.data, self.content_type_or_default_content_type(request), objects, 200)

        elif self.path_has_only_attributes(attributes_functions_str):
            objects = self.get_objects_by_only_attributes(attributes_functions_str)
            #serialized_data = self.get_objects_serialized_by_only_attributes(attributes_functions_str, objects)
            return RequiredObject(objects, self.content_type_or_default_content_type(request), objects, 200)

        #elif self.path_has_url(attributes_functions_str.lower()):
        #    pass
        elif self.path_has_countResource_operation(attributes_functions_str):
            return RequiredObject({"countResource": self.model_class().objects.count()}, CONTENT_TYPE_JSON, self.object_model, 200)

        elif self.path_has_offsetLimit_operation(attributes_functions_str):
            objects = self.get_objects_from_offsetLimit_operation(attributes_functions_str)
            return self.required_object(request, objects)

        elif self.path_has_distinct_operation(attributes_functions_str):
            objects =  self.get_objects_from_distinct_operation(attributes_functions_str)
            return self.required_object(request, objects)

        elif self.path_has_groupBy_operation(attributes_functions_str):
            objects =  self.get_objects_from_groupBy_operation(attributes_functions_str)
            return self.required_object_for_aggregation_operation(request, objects)

        elif self.path_has_groupByCount_operation(attributes_functions_str):
            objects =  self.get_objects_from_groupByCount_operation(attributes_functions_str)
            return self.required_object_for_aggregation_operation(request, objects)

        elif self.path_has_only_spatial_operation(attributes_functions_str):
            objects = self.get_objects_with_spatial_operation(attributes_functions_str)
            #return self.required_object(request, objects, self.content_type_or_default_content_type(request), objects, 200)
            return self.required_object(request, objects)

        elif self.path_has_operations(attributes_functions_str) and self.path_request_is_ok(attributes_functions_str):
            objects = self.get_objects_by_functions(attributes_functions_str)
            return self.required_object(request, objects)

        else:
            return RequiredObject({"This request has invalid attribute or operation"}, status=400, content_type=CONTENT_TYPE_JSON)

        self.temporary_content_type= required_object.content_type
        return required_object

    def basic_options(self, request, *args, **kwargs):
        self.object_model = self.model_class()()
        self.set_basic_context_resource(request)
        attributes_functions_str = self.kwargs.get("attributes_functions", None)

        if self.is_simple_path(attributes_functions_str):  # to get query parameters
            return

        elif self.path_has_only_attributes(attributes_functions_str):
            output = self.response_resquest_with_attributes(attributes_functions_str.replace(" ", ""))
            dict_attribute = output[0]
            if len(attributes_functions_str.split(',')) > 1:
                self._set_context_to_attributes(dict_attribute.keys())
            else:
                self._set_context_to_only_one_attribute(attributes_functions_str)
            return

        #elif self.path_has_url(attributes_functions_str.lower()):
        #    pass
        elif self.path_has_only_spatial_operation(attributes_functions_str):
            objects = self.get_objects_with_spatial_operation(attributes_functions_str)
            return self.basic_response(request, objects)

        elif self.path_has_operations(attributes_functions_str) and self.path_request_is_ok(attributes_functions_str):
            objects = self.get_objects_by_functions(attributes_functions_str)
            return self.basic_response(request, objects)


        else:
            return {"data": "This request has invalid attribute or operation","status": 400, "content_type": CONTENT_TYPE_JSON}