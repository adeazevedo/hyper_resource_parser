
import json

from django.http import HttpResponse
from django.contrib.gis.geos import GEOSGeometry
from django.contrib.gis.gdal import SpatialReference

from rest_framework.response import Response

from hyper_resource.models import buffer
from hyper_resource.views import RequiredObject
from hyper_resource.resources.RasterResource import RasterResource
from hyper_resource.views import BaseModel, CONTENT_TYPE_IMAGE_TIFF, CONTENT_TYPE_JSON, CONTENT_TYPE_GEOJSON


class TiffResource(RasterResource):
    def default_content_type(self):
        return CONTENT_TYPE_IMAGE_TIFF

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
           return RequiredObject(a_value.obj, CONTENT_TYPE_IMAGE_TIFF, self.object_model,200)

        else:
            a_value = {self.name_of_last_operation_executed: a_value}

        return RequiredObject(a_value, CONTENT_TYPE_JSON, self.object_model, 200)

    def basic_get(self, request, *args, **kwargs):
        self.object_model = BaseModel().get_model_object_raster(self, kwargs)
        self.current_object_state = self.object_model
        self.set_basic_context_resource(request)
        self.e_tag = str(hash(self.object_model))

        attributes_functions_str = kwargs.get(self.attributes_functions_name_template())

        if self.is_simple_path(attributes_functions_str):
            required_object = RequiredObject(self.object_model.vsi_buffer(),  self.content_type_or_default_content_type(request), self.object_model, 200)

        elif self.path_has_only_attributes(attributes_functions_str):
            str_attribute = attributes_functions_str.replace(' ', '').replace('/', '')
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

    def get(self, request, *args, **kwargs):
        required_object = self.basic_get(request, *args, **kwargs)

        if required_object.content_type == CONTENT_TYPE_IMAGE_TIFF:
            response = HttpResponse(required_object.representation_object, required_object.content_type)
            response['Content-Disposition'] = 'attachment; filename=' + self.default_file_name()

            return response

        return Response(data=required_object.representation_object,status=200, content_type=required_object.content_type)

    def get_old(self, request, *args, **kwargs):
        self.object_model = self.get_object_model_raster(kwargs)
        self.current_object_state = self.object_model
        self.set_basic_context_resource(request)

        response = HttpResponse(self.object_model.rast.vsi_buffer, content_type="image/tiff")
        response['Content-Disposition'] = 'attachment; filename=' + self.default_file_name()

        return response
