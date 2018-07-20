
import re
import jwt
import geobuf
import random

from django.db import connection
from django.shortcuts import get_object_or_404
from django.contrib.gis.gdal import GDALRaster
from django.contrib.gis.db.models import Extent, Union, MakeLine
from django.http import HttpResponse, StreamingHttpResponse, FileResponse

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.negotiation import BaseContentNegotiation

from abc import ABCMeta
from datetime import datetime
from django.core.cache import cache

#from hyper_resource import views
from hyper_resource.contexts import *
from hyper_resource.views import IgnoreClientContentNegotiation, HTTP_ACCEPT, CONTENT_TYPE_JSON, SUPPORTED_CONTENT_TYPES, \
ACCESS_CONTROL_ALLOW_METHODS, CORS_ALLOW_HEADERS, CORS_EXPOSE_HEADERS, RequiredObject
from hyper_resource.models import  FactoryComplexQuery, SpatialCollectionOperationController, BaseOperationController, BusinessModel, ConverterType

from image_generator.img_generator import BuilderPNG


class AbstractResource(APIView):
    """
    AbstractResource is the main view class.
    All other views are subclasses of this,
    directly or indirectly
    """

    __metaclass__ = ABCMeta

    serializer_class = None
    contextclassname = ''

    def __init__(self):
        super(AbstractResource, self).__init__()

        self.current_object_state = None
        self.object_model = None
        self.name_of_last_operation_executed = None
        self.context_resource = None
        self.initialize_context()
        self.iri_metadata = None
        self.operation_controller = BaseOperationController()
        self.token_need = self.token_is_need()
        self.e_tag = None
        self.temporary_content_type = None
        self.resource_type = None
        self.is_entry_point = False

    # Indicates which is the content negotiation class
    content_negotiation_class = IgnoreClientContentNegotiation

    def cache_enabled(self):
        return False

    def generate_e_tag(self, data):
        return str(hash(data))

    def set_etag_in_header(self, response, e_tag):
        if not response.streaming:
            response[ETAG] = e_tag

        return response

    # Should be overridden
    def hashed_value(self, object):
        return hash(self.object)

    # Should be overridden
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

        # ATTENTION: if self.object_model is None we can have a e_tag without a object_model
        if self.e_tag is None and self.object_model is not None:
            self.e_tag = self.hashed_value(self.object_model)
            return

        if etag:
            self.e_tag += str(etag)
            return

    def jwt_algorithm(self):
        return 'HS256'

    def token_is_ok(self, a_token):
        try:
            payload = jwt.decode(a_token, SECRET_KEY, algorithm=self.jwt_algorithm())
            return True

        except jwt.InvalidTokenError:
            return False

    def token_is_need(self):
        return False

    def token_is_http_or_https(self, token):
        return token.lower() in ['http:', 'https:']

    def token_is_http(self, token):
        return 'http:' == token

    def token_is_https(self, token):
        return 'https:' == token

    def token_is_www(self, token):
        return token.find('www.') > -1

    def token_is_http_or_https_or_www(self, token):
        return self.token_is_http_or_https(token) or self.token_is_www(token)

    def is_end_of_term(self, term):
        return term in self.logical_operators()

    def logical_operators(self):
        return FactoryComplexQuery().logical_operators()

    def add_key_value_in_header(self, response, key, value):
        response[key] = value

    def add_url_in_header(self, url, response, rel):
        link = ' <{0}>; rel="{1}" '.format(url, rel)

        if 'Link' not in response:
            response['Link'] = link
        else:
            response['Link'] += ',' + link

        return response

    def access_control_allow_origin_str(self):
        return '*'

    def access_control_allow_methods_str(self):
        return ', '.join(ACCESS_CONTROL_ALLOW_METHODS)

    def access_control_allow_headers_str(self):
        return ', '.join(CORS_ALLOW_HEADERS)

    def access_control_expose_headers_str(self):
        return ', '.join(CORS_EXPOSE_HEADERS)

    def add_cors_header_in_header(self, response):
        response['access-control-allow-origin'] = self.access_control_allow_origin_str()
        response['access-control-allow-methods'] = self.access_control_allow_methods_str()
        response['access-control-allow-headers'] = self.access_control_allow_headers_str()
        response['access-control-expose-headers'] = self.access_control_expose_headers_str()

    def add_base_headers(self, request, response):
        """
        Adds the 'Link' header in the Response object containing
        a url representing the father url for this request and
        a url representing a context for the requested resource
        :param request:
        :param response:
        :return:
        """
        iri_base = request.build_absolute_uri()  # the absolute iri for this request

        if self.contextclassname not in iri_base:  # if the context class name isn't in the absolute iri ...
            return

        idx = iri_base.index(self.contextclassname)

        # gets the absolute iri from the begin until the context class name
        iri_father = iri_base[:idx]

        # adds 'Link' header in the Response object,
        # relating the father iri from this request with a 'up' relationship
        self.add_url_in_header(iri_father, response, 'up')

        # the second url appended to 'Link' header is the absolute url minus the bar
        # with '.jsonld', the 'rel' is the relationship represented by w3.org url
        self.add_url_in_header(iri_base[:-1] + '.jsonld', response,
                               rel='http://www.w3.org/ns/json-ld#context"; type="application/ld+json')
        self.add_cors_header_in_header(response)

        if self.is_entry_point:
            self.add_url_in_header(iri_base, response, rel='http://schema.org/EntryPoint')

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

        # if token isn't needed, just call the superclass dispatch method
        if not self.token_is_need():
            return super(AbstractResource, self).dispatch(request, *args, **kwargs)

        http_auth = request.META.get(['HTTP_AUTHORIZATION']) or ''

        # the HTTP_AUTHORIZATION header, if this exists in the request, needs to starts with 'Bearer'
        if http_auth.startswith('Bearer'):

            # get the HTTP_AUTHORIZATION header value (without 'Bearer' and edge whitespaces)
            a_token = request.META['HTTP_AUTHORIZATION'][7:].strip()

            if self.token_is_ok(a_token):
                # if token is valid, pass the request forward for APIView dispatch method
                return super(AbstractResource, self).dispatch(request, *args, **kwargs)

        # if HTTP_AUTHORIZATION header doesn't exists or not starts with 'Bearer',
        # a response saying 'token is need' is returned with a 401 (unauthorized) code
        resp = HttpResponse(json.dumps({'token': 'token is needed or it is not ok'}), status=401,
                            content_type=CONTENT_TYPE_JSON)

        # plus a WWW-Authenticate header is send informing how to access the resource
        resp['WWW-Authenticate'] = 'Bearer realm="Access to the staging site"'
        return resp

    # @abstractmethod
    # Could be override
    def initialize_context(self):
        context_module_name = self.__class__.__module__.split('.')[0] + '.contexts'
        context_module = importlib.import_module(context_module_name)
        context_class_name = self.__class__.__name__ + 'Context'
        context_class = getattr(context_module, context_class_name)
        self.context_resource = context_class()
        self.context_resource.resource = self

    def required_context_for_simple_path(self, request):
        resource_type = self.resource_type_or_default_resource_type(request)
        return RequiredObject(self.context_resource.context(resource_type), CONTENT_TYPE_LD_JSON, self.object_model, 200)

    def required_context_for_only_attributes(self, request, attributes_functions_str):
        context = self.get_context_by_only_attributes(request, attributes_functions_str)
        return RequiredObject(context, CONTENT_TYPE_LD_JSON, self.object_model, 200)

    def required_context_for_operation(self, request, attributes_functions_str):
        if self.get_operation_name_from_path(attributes_functions_str) is None:
            return RequiredObject(
                representation_object={"This request has invalid attribute or operation: ": attributes_functions_str},
                content_type=CONTENT_TYPE_JSON, origin_object=self, status_code=400)

        context = self.get_context_for_operation(request, attributes_functions_str)
        return RequiredObject(context, CONTENT_TYPE_LD_JSON, self.object_model, 200)

    def get_context_by_only_attributes(self, request, attributes_functions_str):
        attrs_list = self.remove_last_slash(attributes_functions_str).split(",")
        if len(attrs_list) > 1:
            self._set_context_to_attributes(attrs_list)
        else:
            self._set_context_to_only_one_attribute(attrs_list[0])

        context = self.context_resource.dict_context
        return context

    def get_context_for_operation(self, request, attributes_functions_str):
        operation_name = self.get_operation_name_from_path(attributes_functions_str)
        self.context_resource.set_context_to_operation(self.object_model, operation_name)
        context = self.context_resource.dict_context
        resource_type = self.define_resource_type_by_operation(request, operation_name)
        self.context_resource.set_context_to_resource_type(request, self.object_model, resource_type)
        context['hydra:supportedOperations'] = self.context_resource.supportedOperationsFor(self.object_model, resource_type)

        return context

    # must be overided
    def required_object_for_simple_path(self, request):
        pass

    # todo
    def path_request_is_ok(self, a_path):
        return True

    def operations_with_parameters_type(self):
        dic = self.object_model.operations_with_parameters_type()
        return dic

    def model_class(self):
        return self.serializer_class.Meta.model

    def model_class_name(self):
        return self.model_class().__name__

    def table_name(self):
        return self.model_class().objects.model._meta.db_table

    def pk_name(self):
        return self.model_class().objects.model._meta.pk.name

    def attribute_names_to_web(self):
        return [field.name for field in self.object_model.fields()]

    def field_for(self, attribute_name):
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
        return [field for field in fields_model if field.name in attribute_names]

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
        # Is really necessary or can i keep just one of their?

    def _base_path(self, full_path):
        arr = full_path.split('/')
        ind = arr.index(self.contextclassname)

        return '/'.join(arr[:ind + 1])

    def _set_context_to_attributes(self, attribute_name_array):
        self.context_resource.set_context_to_attributes(attribute_name_array)

    def _set_context_to_only_one_attribute(self, attribute_name):
        attribute_type = self.field_for(attribute_name)
        self.context_resource.set_context_to_only_one_attribute(self.current_object_state, attribute_name,
                                                                attribute_type)

    def _set_context_to_operation(self, operation_name):
        self.context_resource.set_context_to_operation(self.current_object_state, operation_name)

    def set_basic_context_resource(self, request):
        self.context_resource.host = request.META['HTTP_HOST']
        self.context_resource.basic_path = self._base_path(request.META['PATH_INFO'])

        if len(self.kwargs.values()):
            self.context_resource.complement_path = list(self.kwargs.values())[0]
        else:
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

    def attributes_functions_name_template(self):
        return 'attributes_functions'

    def get_object(self, a_dict):
        """
        Receives a_dict, get only the identifier fields
        and use them to query the instances in the database
        that matches with the identifiers dict
        :param a_dict:
        :return:
        """
        dicti = self.dic_with_only_identitier_field(a_dict)

        obj = get_object_or_404(self.model_class(), **dicti)

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
        return CONTENT_TYPE_JSON

    def default_resource_type(self):
        return 'Thing'

    # must be overridden
    def define_resource_type(self, request, attributes_functions_str):
        pass

    # must be overrided
    def define_resource_type_by_only_attributes(self, request, attributes_functions_str):
        pass

    # must be overrided
    def define_resource_type_by_operation(self, request, operation_name):
        pass

    def content_type_or_default_content_type(self, request):
        if request is None:
            return self.default_content_type()

        a_content_type = request.META.get(HTTP_ACCEPT, '')

        if a_content_type not in SUPPORTED_CONTENT_TYPES:
            return self.default_content_type()

        return a_content_type

    def dict_by_accept_resource_type(self):
        dict_ = {
            CONTENT_TYPE_OCTET_STREAM: bytes
        }

        return dict_

    def resource_type_for_accept_header(self, accept):
        return self.dict_by_accept_resource_type()[accept] if accept in self.dict_by_accept_resource_type() else None

    def resource_type_or_default_resource_type(self, request):
        if request is None:
            return self.default_resource_type()

        accept = request.META.get(HTTP_ACCEPT, '')

        if accept not in SUPPORTED_CONTENT_TYPES:
            return self.default_resource_type()

        return self.resource_type_for_accept_header(accept)

    # todo
    def basic_response(self, request, serialized_object, status, content_type):
        return Response(data=serialized_object, status=status, content_type=content_type)

    # Answer if a client's etag is equal server's etag
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

        # if tuple_etag_serialized_data is None, this means that the key not correspond none of the cache keys
        # hence the resource isn't in cache
        if tuple_etag_serialized_data is None:
            return False

        # compare the Request If-None-Match header value with the Etag value of the cache
        return tuple_etag_serialized_data[0] == request.META.get(HTTP_IF_NONE_MATCH, '')

    # Answer if a get(request) is conditional
    def is_conditional_get(self, request):
        return request.META.get(HTTP_IF_NONE_MATCH) is not None or \
               request.META.get(HTTP_IF_UNMODIFIED_SINCE) is not None

    # Should be overridden
    # Answer a formatted string(iri + accept) which is a key to retrieve an object in the cache
    def get_key_cache(self, request, a_content_type=None):
        if a_content_type:
            return self.request.build_absolute_uri() + a_content_type

        return self.request.build_absolute_uri() + self.content_type_or_default_content_type(request)

    def set_key_with_data_in_cache(self, key, etag, data, seconds=3600):
        if isinstance(data, memoryview) or not self.cache_enabled():
            return

        if cache.get(key) is None:
            cache.set(key, (etag, data), seconds)

    def resource_in_cache(self, request):
        """
        Return the cached resource if the generated request key
        (generated through AbstractResource.get_key_cache()) and the
        If-None-Match header value matches with the cache key and cached
        etag respectivitly. Return False otherwise
        :param request:
        :return: resource in cache or None if not found
        """
        if not self.cache_enabled():
            return

        key = self.get_key_cache(request)

        return cache.get(key)

    def is_image_content_type(self, request, **kwargs):
        return self.content_type_or_default_content_type(request) == CONTENT_TYPE_IMAGE_PNG or kwargs.get(
            'format') == 'png'

    def accept_is_binary(self, request):
        return request.META.get(HTTP_ACCEPT, '') == CONTENT_TYPE_OCTET_STREAM

    # Should be overridden
    def is_binary_content_type(self, required_object):
        return required_object.content_type == CONTENT_TYPE_OCTET_STREAM

    # Should be overridden
    def response_base_get_binary(self, request, required_object):
        # 'key' will be absolute uri + application/octet-stream
        key = self.get_key_cache(request, CONTENT_TYPE_OCTET_STREAM)

        if isinstance(required_object.representation_object, dict) and 'type' in required_object.representation_object:
            # if representation object is a dict is an GeoJson
            # geobuf minimize the response size
            result = geobuf.encode(required_object.representation_object)  # GeoJSON or TopoJSON -> Geobuf string

        else:
            result = str(required_object.representation_object).encode()

        if isinstance(result, dict):
            value_to_e_tag = json.dumps(result)

        else:
            value_to_e_tag = result

        e_tag = self.generate_e_tag(value_to_e_tag)
        self.set_key_with_data_in_cache(key, e_tag, result)

        resp = HttpResponse(result, content_type=CONTENT_TYPE_OCTET_STREAM)
        self.set_etag_in_header(resp, e_tag)

        return resp

    # todo: verify image responses processment
    # Should be overridden
    def response_base_get_with_image(self, request, required_object):
        # 'queryset' is the requested resource without serialization
        queryset = required_object.origin_object

        image = self.get_png(queryset, request)
        required_object.representation_object = image
        key = self.get_key_cache(request, CONTENT_TYPE_IMAGE_PNG)
        e_tag = self.generate_e_tag(image)

        self.set_key_with_data_in_cache(key, e_tag, image)
        resp = HttpResponse(image, content_type=CONTENT_TYPE_IMAGE_PNG)
        self.set_etag_in_header(resp, e_tag)

        return resp

    # Should be overridden
    def response_base_object_in_cache(self, request):
        """
        Returns a cached Response (if this is in cache)
        defining wich Content-Type the response has
        :param request:
        :return:
        """
        # AbstractResource.resource_in_cache_or_None return de cached data
        # if the mounted key based on Accept Request header matches one of the cached keys
        tuple_etag_serialized_data = self.resource_in_cache(request)

        if tuple_etag_serialized_data is not None:
            if request.META[HTTP_ACCEPT] in [CONTENT_TYPE_IMAGE_PNG, CONTENT_TYPE_OCTET_STREAM]:
                # if Accept Request header value is application/octet-stream or image/png
                # the Response Content-Type will be the same value
                resp = HttpResponse(tuple_etag_serialized_data[1], content_type=request.META[HTTP_ACCEPT])

            else:
                # if Accept Request header value isn't application/octet-stream nor image/png
                # the Content-Type will be the Accept value or the default Content-Type
                resp = Response(data=tuple_etag_serialized_data[1], status=200,
                                content_type=self.content_type_or_default_content_type(request))

            # set etag in Response header
            self.set_etag_in_header(resp, tuple_etag_serialized_data[0])

            return resp

    # Should be overridden
    def response_base_get(self, request, *args, **kwargs):
        """
        Returns a Response for the Request. If the response is in cache

        """
        # AbstractResource.resource_in_cache() returns the requested resource from cache
        # if the key formed by absolute uri + accept or absolute uri + default Content-Type
        # matches one of the cache keys. Returns None otherwise
        resource = self.resource_in_cache(request)

        if resource:
            # returns a response from the cache
            return self.response_base_object_in_cache(request)

        # if the resource is not in cache, use the subclass basic_get() that returns a RequiredObject instance
        required_object = self.basic_get(request, *args, **kwargs)

        # if Required object has some error, return this
        status = required_object.status_code

        if status in [400, 401, 404]:
            return Response(required_object.representation_object, status=status)

        if status in [500]:
            return Response({'Error ': 'The server can not process this request. Status:' + str(status)}, status=status)

        # todo: verify image responses processment
        if self.is_image_content_type(request, **kwargs):
            return self.response_base_get_with_image(request, required_object)

        # if RequiredObject has application/octet-stream Content-Type
        # the Response is a geobuf (smaller than a regular JSON)
        if self.is_binary_content_type(required_object):
            return self.response_base_get_binary(request, required_object)

        # mounts a cache key with RequiredObject.content_type
        key = self.get_key_cache(request, a_content_type=required_object.content_type)

        # sets the e_tag and data in cache binding to the key
        self.set_key_with_data_in_cache(key, self.e_tag, required_object.representation_object)

        # return the Response with the requested resource representation and Etag header
        resp = Response(data=required_object.representation_object, status=200,
                        content_type=required_object.content_type)
        self.set_etag_in_header(resp, self.e_tag)

        return resp

    # Should be overridden
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
        # if matches, a 304 (Not modified) Response is returns
        if self.conditional_etag_match(request):
            return Response(data={}, status=304, content_type=a_content_type)

        # if not matches return a regular Response (with database requests)
        return self.response_base_get(request, *args, **kwargs)

    # If client request .png into IRI chance header's accept to image/png and removes .png from IRI. Affordance for user.
    def change_request_if_image_png_into_IRI(self, request):
        if 'attributes_functions' in self.kwargs and self.kwargs['attributes_functions'][-4:] == '.png':
            self.kwargs['attributes_functions'] = self.kwargs['attributes_functions'][:-4]
            request.META[HTTP_ACCEPT] = 'image/png'

    # Should be overridden
    def basic_get(self, request, *args, **kwargs):
        pass

    # Could be overridden
    def get(self, request, *args, **kwargs):
        """
        Receive the request and decide if this will be a regular response
        or a cached response
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        if 'HTTP_ETAG' in request.META:
            etag = request.META['HTTP_ETAG']

        # responds with a conditional get if the request has If-None-Match or If-Unmodified-Since header
        if self.is_conditional_get(request):
            resp = self.response_conditional_get(request, *args, **kwargs)

        else:
            # otherwise responds with a regular get (can be responded with cached data)
            # QUESTION: AbstractResource.response_base_get() must consider cache check?
            # After all, if AbstractResource.is_conditional_get() return False this means that the Request hasn't
            # If-None-Match or If-Unmodified-Since headers
            resp = self.response_base_get(request, *args, **kwargs)

        # add the Link header in Response
        self.add_base_headers(request, resp)

        return resp

    # Could be overridden
    def patch(self, request, *args, **kwargs):
        return super(AbstractResource, self).patch(request, *args, **kwargs)

    # Could be overridden
    def head(self, request, *args, **kwargs):
        resp = Response(data={}, status=status.HTTP_200_OK,
                        content_type=self.content_type_or_default_content_type(request))
        self.add_base_headers(request, resp)

        return resp

    # Could be overridden
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
            # if the request data is valid, alter the database resource and returns a 204 response
            serializer.save()
            resp = Response(status=status.HTTP_204_NO_CONTENT)
            return resp

        # if request data isn't valid, return a 400 response status
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # Could be overridden
    def delete(self, request, *args, **kwargs):
        obj = self.get_object(kwargs)
        obj.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)

    def options(self, request, *args, **kwargs):
        response = super(AbstractResource, self).options(request, *args, **kwargs)
        self.add_base_headers(request, response)

        return response

    def operation_names_model(self):
        return self.object_model.operation_names()

    def attribute_names_model(self):
        return self.object_model.attribute_names()

    def is_private(self, attribute_or_method_name):
        return attribute_or_method_name.startswith('__') and attribute_or_method_name.endswith('__')

    def is_not_private(self, attribute_or_method_name):
        return not self.is_private(attribute_or_method_name)

    def is_operation(self, operation_name):
        return operation_name in self.operation_names_model()

    def is_attribute(self, attribute_name):
        return self.object_model.is_attribute(attribute_name)

    def is_spatial_attribute(self, attribute_name):
        return False

    def _has_method(self, method_name):
        return method_name in self.operation_names_model()

    def is_simple_path(self, attributes_functions_str):
        return attributes_functions_str is None or len(attributes_functions_str) == 0

    def path_has_operations(self, attributes_functions_name):
        attrs_functs = self.remove_last_slash(attributes_functions_name).split('/')

        operations = self.operation_names_model()

        for att_func in attrs_functs:
            oper_name = att_func[1:] if '*' in att_func else att_func

            if oper_name in operations:
                return True

        return False

    def path_has_only_attributes(self, attributes_functions_name):
        attrs_functs = self.remove_last_slash(attributes_functions_name).split('/')

        if len(attrs_functs) > 1:
            return False

        if ',' in attrs_functs[0]:
            return True

        if self._has_method(attrs_functs[0]):
            return False

        return self.object_model.is_attribute(attrs_functs[0])

    def is_complex_request(self, request):
        absolute_uri = request.scheme + '://' + request.get_host() + request.path
        compx_req_marker_idx = absolute_uri.find('!')

        if compx_req_marker_idx == -1 or absolute_uri.count('!') != 2:
            return False

        uri_after_marker = absolute_uri[compx_req_marker_idx:]
        operation_name = uri_after_marker[1:uri_after_marker.index('/')-1]

        return operation_name in self.operation_controller.dict_all_operation_dict()

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
        arr_term = [ele for ele in arr_of_term if ele != '']
        found_url = False

        # storing the number of elements of the list
        size_of_term = len(arr_term)

        for idx, token in enumerate(arr_term):  # token is each url parameter

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

                elif idx == size_of_term - 1:
                    # if the current index represents the penultimate element
                    # of the array of terms, 'found_url' turns False
                    found_url = False

                    # so, we concatenate 'token' to '/' and append to 'arr'. 'http_str' turns a empty string again
                    http_str += token + '/'
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

    def dict_as_geojson(self, a_dict):
        d = {
            'type': 'Feature',
            'geometry': a_dict[self.geometry_field_name()],
            'properties': a_dict}

        a_dict.pop(self.geometry_field_name(), None)

        return d

    def attributes_functions_splitted_by_url(self, attributes_functions_str_url):
        res = attributes_functions_str_url.lower().find('http:')
        if res == -1:
            res = attributes_functions_str_url.lower().find('https:')
            if res == -1:
                res = attributes_functions_str_url.lower().find('www.')
                if res == -1:
                    return [attributes_functions_str_url]

        if '/*' in attributes_functions_str_url:
            param_inx = attributes_functions_str_url.index('/*')
            param = attributes_functions_str_url[param_inx+2:]
            return [attributes_functions_str_url[0:res], attributes_functions_str_url[res:param_inx], param]

        return [attributes_functions_str_url[0:res], attributes_functions_str_url[res:], None]

    def path_has_url(self, attributes_functions_str_url):
        return attributes_functions_str_url.find('http:') > -1 \
               or attributes_functions_str_url.find('https:') > -1 \
               or attributes_functions_str_url.find('www.') > -1

    def get_url_arr_from_arr_of_tuples(self, arr_of_tuples):
        url_as_arr = []
        for url_tuple in arr_of_tuples:
            url_arr = list(url_tuple)
            url = [self.remove_last_slash(url) for url in url_arr if url != ''][0]
            url_as_arr.append(url)
        return url_as_arr

    def remove_last_slash(self, url_as_str):
        url = url_as_str.strip()
        url = url[:-1] if url[-1] == '*' else url
        return url[:-1] if url.endswith('/') else url

    def attribute_functions_str_with_url_splitted_by_slash(self, attributes_functions_str_url):
        att_functions_str_url = attributes_functions_str_url
        #exp = r"(?=https{0,1}:.+?\*)https{0,1}:.+?\*"
        exp = r'(?=https{0,1}:.+?\*)(https{0,1}:.+?\*)|(https{0,1}:.+?\/?$)'
        #exp = r'(?=https{0,1}:.+?\*)https{0,1}:.+?[*]|[/]$'
        url_as_arr_of_tuples = re.findall(exp, att_functions_str_url, re.IGNORECASE)

        url_as_arr = self.get_url_arr_from_arr_of_tuples(url_as_arr_of_tuples)

        token = '_*+_TOKEN__$URL-#_Num:'
        for index, url_str in enumerate(url_as_arr):
            att_functions_str_url = att_functions_str_url.replace(url_str, token + str(index), 1)# + '/*', 1)
        att_functions_str_url_as_array = att_functions_str_url.split('/')
        for idx, url_str in enumerate(url_as_arr):
            att_functions_str_url_as_array[att_functions_str_url_as_array.index(token + str(idx))] = url_str if url_str[-1] not in ['*', '/'] else url_str[:-1]

        return att_functions_str_url_as_array if att_functions_str_url_as_array[-1] != '*' else att_functions_str_url_as_array[:-1]

    def attribute_functions_str_splitted_by_slash(self, attributes_functions_str_url):
        att_functions_str_url = self.remove_last_slash(attributes_functions_str_url)
        if self.path_has_url(att_functions_str_url):
            return self.attribute_functions_str_with_url_splitted_by_slash(att_functions_str_url)

        else:
            return att_functions_str_url.split('/')

    def _execute_attribute_or_method(self, object, attribute_or_method_name, array_of_attribute_or_method_name):
        parameters = []

        if self.operation_controller.is_operation(object, attribute_or_method_name):
            if self.operation_controller.operation_has_parameters(object, attribute_or_method_name):
                parameters = array_of_attribute_or_method_name[0].split('&') if len(
                    array_of_attribute_or_method_name) > 0 else []
                array_of_attribute_or_method_name = array_of_attribute_or_method_name[1:]

        obj = self._value_from_object(object, attribute_or_method_name, parameters)

        if len(array_of_attribute_or_method_name) == 0:
            return obj

        return self._execute_attribute_or_method(obj, array_of_attribute_or_method_name[0],
                                                 array_of_attribute_or_method_name[1:])

    def array_of_operation_name(self):
        collection_operations_array = list(self.operation_controller.dict_all_operation_dict().keys())
        return collection_operations_array

    def get_operation_name_from_path(self, attributes_functions_str):
        attributes_functions_str = attributes_functions_str.lower()
        arr_att_funcs = self.remove_last_slash(attributes_functions_str).split('/')
        first_part_name = arr_att_funcs[0]
        if first_part_name not in self.array_of_operation_name():
            return None
        return first_part_name

    def is_operation_and_has_parameters(self, attribute_or_method_name):
        dic = self.operations_with_parameters_type()

        return (attribute_or_method_name in dic) and len(dic[attribute_or_method_name].parameters)

    # method without use
    def function_name(self, attributes_functions_str):
        functions_dic = self.operations_with_parameters_type()

        if str(attributes_functions_str[-1]) in functions_dic:
            return str(attributes_functions_str[-1])

        return str(attributes_functions_str[-2])

    def response_request_with_attributes(self, attributes_functions_name):
        """
        Return a response to the requested resource containing
        only the requested attributes/methods values (not the entire resource)
        :param attributes_functions_name - the attributes from the request resource
        :return:
        """
        a_dict = {}

        # transform the parameters (separated by ',') in a list of arguments
        attributes = attributes_functions_name.strip().split(',')

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
        return a_dict, CONTENT_TYPE_JSON, self.object_model, {'status': 200}

    def all_parameters_converted(self, attribute_or_function_name, parameters):
        parameters_converted = []

        if self.is_operation_and_has_parameters(attribute_or_function_name):
            parameters_type = self.operations_with_parameters_type()[attribute_or_function_name].parameters

            for i in range(len(parameters)):
                if parameters_type[i] == GEOSGeometry:
                    ct = ConverterType()

                    if ct.path_is_feature_collection(parameters[i]):
                        param_converted = ct.make_geometrycollection_from_featurecollection(json.loads(parameters[i]))

                    else:  # if parameters[i] is GeometryCollection (GeoJson) or WKT ...
                        param_converted = parameters_type[i](parameters[i])

                    parameters_converted.append(param_converted)

                else:
                    parameters_converted.append(parameters_type[i](parameters[i]))

            return parameters_converted

        return self.parametersConverted(parameters)

    def is_attribute_for(self, object, attribute_or_function_name):
        return hasattr(object, attribute_or_function_name) and not callable(getattr(object, attribute_or_function_name))

    def _value_from_object(self, object, attribute_or_function_name, parameters):
        attribute_or_function_name_striped = attribute_or_function_name.strip()
        self.name_of_last_operation_executed = attribute_or_function_name_striped

        if self.is_attribute_for(object, attribute_or_function_name):
            return getattr(object, attribute_or_function_name_striped)

        if len(parameters) > 0:

            if isinstance(object, BusinessModel) or isinstance(object, GEOSGeometry):
                params = self.all_parameters_converted(attribute_or_function_name_striped, parameters)

            else:
                params = ConverterType().convert_parameters(type(object), attribute_or_function_name, parameters)

            return getattr(object, attribute_or_function_name_striped)(*params)

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
        parameters_converted = []

        for value in params_as_array:

            # if the parameter is 'true' or 'false'
            # convert it to bool and append to list
            if value.lower() == 'true':
                parameters_converted.append(True)
                continue

            elif value.lower() == 'false':
                parameters_converted.append(False)
                continue

            # if parameter is not 'true' nor 'false'
            # we try to convert to int, if it fails,
            # we try to convert to float, if it still fails,
            # we try to convert to GEOSGeometry
            try:
                parameters_converted.append(int(value))
                continue
            except ValueError:
                pass
            try:
                parameters_converted.append(float(value))
                continue
            except ValueError:
                pass
            try:
                parameters_converted.append(GEOSGeometry(value))
                continue
            except ValueError:
                pass
            try:
                # if the parameter starts with 'http', we make a request to this parameter
                http_str = (value[0:4]).lower()

                if http_str == 'http':
                    resp = requests.get(value)

                    # if this request return a response status between 400 and 599, we raise a HttpError
                    if 400 <= resp.status_code <= 599:
                        raise HTTPError({resp.status_code: resp.reason})

                    # if the request not return an error status, we get the response body in JSON format
                    js = resp.json()

                    # if 'type' is 'feature' or 'featurecollection' it has an 'geometry'
                    if js.get('type') and js['type'].lower() in ['feature', 'featurecollection']:
                        # in this case, we get the geometric data from this JSON response
                        a_geom = js['geometry']

                    else:
                        # otherwise, we simply get the entire dict
                        a_geom = js

                    # finally, we convert 'a_geom' to json and then convert the result to GEOSGeometry
                    # appending this to params_converted list. OBS: you must notice that we consider that
                    # the request from the parameter will bring us a geometric resource
                    parameters_converted.append(GEOSGeometry((json.dumps(a_geom))))

            except (ConnectionError, HTTPError) as err:
                print('Error: '.format(err))

        return parameters_converted

    def generate_tmp_file(self, suffix='', length_name=10):
        return ''.join([random.choice('0123456789ABCDEF') for i in range(length_name)]) + suffix

    def get_style_file(self, request):
        if 'HTTP_LAYERSTYLE' in request.META:
            layer_style_url = request.META['HTTP_LAYERSTYLE']
            response = requests.get(layer_style_url)

            if response.status_code == 200:
                file_name = self.generate_tmp_file(suffix='_tmp_style.xml')

                with open(file_name, 'w+') as st:
                    st.write(response.text.encode('UTF-8'))
                    st.close()

                return file_name

        return None

    def get_png(self, queryset, request):
        style = self.get_style_file(request)

        if isinstance(queryset, GEOSGeometry):
            config = {'wkt': queryset.wkt, 'type': queryset.geom_type}
        else:
            config = {'wkt': queryset.geom.wkt, 'type': queryset.geom.geom_type}

        if style is not None:
            config.update({
                'style': style,
                'deleteStyle': True
            })

        builder_png = BuilderPNG(config)

        return builder_png.generate()

    def split_complex_uri(self, complex_uri):
        init_marker_idx = complex_uri.index('!')
        fin_marker_idx = complex_uri.rindex('!')
        uri_before_operation = complex_uri[:init_marker_idx]
        uri_after_operation = complex_uri[fin_marker_idx+2:]
        operation_snippet = complex_uri[init_marker_idx+1:fin_marker_idx]

        return (uri_before_operation, operation_snippet, uri_after_operation)

    def get_absolute_uri(self, request):
        return request.scheme + '://' + request.get_host() + request.path

    # Must be overridden
    def execute_complex_request(self, request):
        pass

    def required_object_for_invalid_sintax(self, attributes_functions_str, message=None):
        representation_object = {
            'This request has invalid attribute or operation: ': attributes_functions_str,
        }

        if message:
            representation_object['Explanation'] = message

        required_obj =  RequiredObject(representation_object, CONTENT_TYPE_JSON, self, 400)

        return required_obj

    def required_object_for_complex_request(self, request):
        response = self.execute_complex_request(request)
        return RequiredObject(json.loads(response.json), self.content_type_or_default_content_type(request), self, 200)

    # must be overrided
    def required_object_for_spatialize_operation(self, request, attributes_functions_str):
        pass

    # must be overrided
    def get_objects_from_spatialize_operation(self, request, attributes_functions_str):
        pass

    def get_requested_data_from_spatialize_operation(self, request, attributes_functions_str):
        uri_before_oper, join_attrs, uri_or_data_after_oper = self.split_spatialize_uri(request, attributes_functions_str)

        data_before_oper = requests.get(uri_before_oper).json()
        if uri_or_data_after_oper.startswith('http://') or\
                uri_or_data_after_oper.startswith('https://') or\
                uri_or_data_after_oper.startswith('www.'):
            data_after_oper = requests.get(uri_or_data_after_oper, headers={'Accept': 'application/json'} ).json()
        else:
            data_after_oper = uri_or_data_after_oper

        dicti = {
                "left_join_data": data_before_oper,
                "left_join_attr": join_attrs[0],
                "rigth_join_attr": join_attrs[1],
                "right_join_data": data_after_oper
        }
        return dicti

    def split_spatialize_uri(self, request, attributes_functions_str):
        attrs_funcs_arr = self.remove_last_slash(attributes_functions_str).split('/')

        spatialize_oper_snippet = "/".join(attrs_funcs_arr[:2])
        absolute_uri = self.get_absolute_uri(request)
        uri_before_oper = absolute_uri[:absolute_uri.find( spatialize_oper_snippet )]

        join_attrs = attrs_funcs_arr[1].split('&')

        uri_after_oper = "/".join(attrs_funcs_arr[2:])

        return (uri_before_oper, join_attrs, uri_after_oper)

    # Responds a method to be executed.
    def get_operation_to_execute(self, operation_name):
        d = self.operation_name_method_dic()

        if operation_name is None:
            return None

        return d[operation_name]

    def operation_name_method_dic(self):
        pass


