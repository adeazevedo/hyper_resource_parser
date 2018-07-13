
import re
import json
import requests

from django.contrib.gis.geos import GEOSGeometry
from django.contrib.gis.gdal import SpatialReference

from rest_framework.response import Response

from hyper_resource.models import buffer
from hyper_resource.views import RequiredObject
from hyper_resource.resources.SpatialResource import SpatialResource
from hyper_resource.views import CONTENT_TYPE_OCTET_STREAM, CONTENT_TYPE_JSON, CONTENT_TYPE_GEOJSON


class FeatureResource(SpatialResource):
    def __init__(self):
        super(FeatureResource, self).__init__()

    def default_resource_type(self):
        return 'Feature'

    def dict_by_accept_resource_type(self):
        dict_ = {
            CONTENT_TYPE_OCTET_STREAM: 'Geobuf'
        }

        return dict_

    # Must be overridden
    def initialize_context(self):
        pass

    def geometry_field_name(self):
        return self.serializer_class.Meta.geo_field

    def is_spatial_attribute(self, attribute_name):
        return self.model.geo_field_name() == attribute_name.lower()

    def operations_with_parameters_type(self):
        return self.object_model.operations_with_parameters_type()

    # Responds a List with four elements: value of what was requested, content_type, object, dict=>dic[status] = status_code
    def response_request_with_attributes(self, attributes_functions_name, request=None):
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

        if self.spatial_field_name() in attributes:
            a_dict = self.dict_as_geojson(a_dict)

        self.current_object_state = a_dict

        return RequiredObject(a_dict, CONTENT_TYPE_JSON, self.object_model,  200)

    def response_request_attributes_functions_str_with_url(self, attributes_functions_str, request=None):
        # r':/+' matches string like: ':' followed by at least 1 occurence of '/'
        # substitute any occurences of ':/' to '://' in 'attributes_functions_str'
        attributes_functions_str = re.sub(r':/+', '://', attributes_functions_str)
        arr_of_two_url_and_param = self.attributes_functions_splitted_by_url(attributes_functions_str)
        resp = requests.get(arr_of_two_url_and_param[1])
        if resp.status_code in[400, 401, 404]:
            return RequiredObject({},CONTENT_TYPE_JSON, self.object_model,  resp.status_code)
        if resp.status_code == 500:
            return RequiredObject({},CONTENT_TYPE_JSON, self.object_model,resp.status_code)
        j = resp.text

        if arr_of_two_url_and_param[2] is not None:
            attributes_functions_str = arr_of_two_url_and_param[0] + j + arr_of_two_url_and_param[2]
        else:
            attributes_functions_str = arr_of_two_url_and_param[0] + j
        #external_etag = resp.headers['etag']
        #self.inject_e_tag(external_etag)
        return self.response_of_request(attributes_functions_str)

    def response_of_request(self,  attributes_functions_str):
        att_funcs = attributes_functions_str.split('/')
        self.current_object_state = self._execute_attribute_or_method(self.object_model, att_funcs[0], att_funcs[1:])
        a_value = self.current_object_state

        if isinstance(a_value, GEOSGeometry):
            a_value = json.loads(a_value.geojson)

            return RequiredObject(a_value, CONTENT_TYPE_GEOJSON, self.object_model,  200)

        elif isinstance(a_value, SpatialReference):
           a_value = { self.name_of_last_operation_executed: a_value.wkt.strip('\n')}

        elif isinstance(a_value, memoryview) or isinstance(a_value, buffer):
           return RequiredObject(a_value.obj, CONTENT_TYPE_OCTET_STREAM, self.object_model, 200)

        else:
            a_value = {self.name_of_last_operation_executed: a_value}

        return RequiredObject(a_value, CONTENT_TYPE_JSON, self.object_model, 200)


    def response_base_get(self, request, *args, **kwargs):
        resource = self.resource_in_cache(request)

        if resource:
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

        attributes_functions_str = kwargs.get(self.attributes_functions_name_template())

        if self.is_simple_path(attributes_functions_str):
            serializer = self.serializer_class(self.object_model)
            required_object = RequiredObject(serializer.data, self.content_type_or_default_content_type(request), self.object_model, 200)

        elif self.path_has_only_attributes(attributes_functions_str):
            str_attribute = attributes_functions_str.replace(" ", "").replace("/","")
            required_object = self.response_request_with_attributes(str_attribute, request)

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

            if s.endswith('/'):
               s = s[:-1]

            required_object = self.response_of_request(s)
            self._set_context_to_operation(self.name_of_last_operation_executed)

        self.inject_e_tag()
        self.temporary_content_type= required_object.content_type

        return required_object

    def basic_required_object(self, request, *args, **kwargs):
        return self.basic_get(request, *args, **kwargs)

    def basic_options(self, request, *args, **kwargs):
        self.object_model = self.model_class()()
        self.set_basic_context_resource(request)
        attributes_functions_str = self.kwargs.get("attributes_functions", None)

        if self.is_simple_path(attributes_functions_str):
            return self.required_context_for_simple_path(request)
        if self.path_has_only_attributes(attributes_functions_str):
            return self.required_context_for_only_attributes(request, attributes_functions_str)
        if self.path_has_operations(attributes_functions_str):
            return self.required_context_for_operation(request, attributes_functions_str)

        return RequiredObject(
            representation_object={"This request has invalid attribute or operation: ": attributes_functions_str},
            content_type=CONTENT_TYPE_JSON, origin_object=self, status_code=400)

    def options(self, request, *args, **kwargs):
        required_object = self.basic_options(request, *args, **kwargs)
        if required_object.status_code == 200:
            response = Response(required_object.representation_object, content_type=required_object.content_type,
                                status=200)
            self.add_base_headers(request, response)
        else:
            response = Response(data={"This request is not supported": self.kwargs.get("attributes_functions", None)},
                                status=required_object.status_code)
        return response

    def get_context_by_only_attributes(self, request, attributes_functions_str):
        attrs_funcs_str = self.remove_last_slash(attributes_functions_str)
        super(FeatureResource, self).get_context_by_only_attributes(request, attrs_funcs_str)

        resource_type = self.define_resource_type_by_only_attributes(request, attrs_funcs_str)
        self.context_resource.set_context_to_resource_type(request, self.object_model, resource_type)
        supported_operation_dict = self.context_resource.supportedOperationsFor(self.object_model, resource_type)

        context = self.context_resource.dict_context
        context['hydra:supportedOperations'] = supported_operation_dict
        return context

    def default_content_type(self):
        return self.temporary_content_type if self.temporary_content_type is not None else CONTENT_TYPE_GEOJSON

    def define_resource_type_by_only_attributes(self, request, attributes_functions_str):
        attrs_functs_arr = self.remove_last_slash(attributes_functions_str).split(',')
        r_type = self.resource_type_or_default_resource_type(request)
        if r_type != self.default_resource_type():
            return r_type if self.geometry_field_name() in attrs_functs_arr else bytes

        if len(attrs_functs_arr) == 1:
            # the field type has priority over default resource type
            return type(self.field_for(attrs_functs_arr[0]))

        return r_type if self.geometry_field_name() in attrs_functs_arr else 'Thing'

    def define_resource_type_by_operation(self, request, operation_name):
        operation_type_called = self.operation_controller.dict_all_operation_dict()[operation_name]
        res_type_by_accept = self.resource_type_or_default_resource_type(request)

        if operation_type_called.return_type == GEOSGeometry:
            return res_type_by_accept
        elif issubclass(operation_type_called.return_type, GEOSGeometry):
            return res_type_by_accept if res_type_by_accept != self.default_resource_type() else operation_type_called.return_type
        else:
            res_type_by_accept = bytes if res_type_by_accept == 'Geobuf' else res_type_by_accept

        return operation_type_called.return_type if res_type_by_accept == self.default_resource_type() else res_type_by_accept

    def get(self, request, *args, **kwargs):
       self.change_request_if_image_png_into_IRI(request)
       return super(FeatureResource,self).get(request, *args, **self.kwargs)
