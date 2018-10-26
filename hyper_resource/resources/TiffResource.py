from django.contrib.gis.gdal import GDALRaster

from hyper_resource.resources.AbstractResource import *
from hyper_resource.resources.BaseModel import BaseModel
from hyper_resource.resources.RasterResource import RasterResource


class TiffResource(RasterResource):
    def default_content_type(self):
        return CONTENT_TYPE_IMAGE_TIFF

    def define_content_type_by_only_attributes(self, request, attributes_functions_str):
        attrs_arr = self.remove_last_slash(attributes_functions_str)
        if self.spatial_field_name() in attrs_arr:
            return self.content_type_or_default_content_type(request)

        if self.content_type_or_default_content_type(request) != self.default_content_type():
           return self.content_type_or_default_content_type(request)
        return CONTENT_TYPE_JSON

    def define_content_type_by_operation(self, request, operation_name):
        operation_type_called = self.operation_controller.dict_all_operation_dict()[operation_name]
        content_type_by_accept = self.content_type_or_default_content_type(request)

        if content_type_by_accept != self.default_content_type():
            return content_type_by_accept

        if issubclass(operation_type_called.return_type, memoryview) or issubclass(operation_type_called.return_type, buffer) or issubclass(operation_type_called.return_type, GDALRaster):
            return CONTENT_TYPE_IMAGE_TIFF

        if issubclass(operation_type_called.return_type, bytes):
            return CONTENT_TYPE_OCTET_STREAM

        return CONTENT_TYPE_JSON

    def default_resource_type(self):
        return 'Tiff'

    def define_resource_type_by_only_attributes(self, request, attributes_functions_str):
        attrs_arr = self.remove_last_slash(attributes_functions_str).split(",")
        resource_type_by_accept = self.resource_type_or_default_resource_type(request)

        if resource_type_by_accept != self.default_resource_type():
            return resource_type_by_accept

        if self.spatial_field_name() in attrs_arr:
            return self.default_resource_type()

        if len(attrs_arr) == 1:
            return type( self.field_for(attrs_arr[0]) )
        return 'Thing'

    def define_resource_type_by_operation(self, request, operation_name):
        operation_type_called = self.operation_controller.dict_all_operation_dict()[operation_name]
        res_type_by_accept = self.resource_type_or_default_resource_type(request)

        # 1°: Trying to define resource type by accept header ...
        if res_type_by_accept != self.default_resource_type():
            return res_type_by_accept

        # 2°: Defining resource type by operation return type ...
        return self.operation_controller.get_user_friendly_resource_type_name( operation_type_called.return_type )

    def required_object_for_simple_path(self, request):
        return RequiredObject(self.object_model.vsi_buffer(),  self.content_type_or_default_content_type(request), self.object_model, 200)

    def required_object_for_only_attributes(self, request, attributes_functions_str):
        if self.spatial_field_name() in self.remove_last_slash(attributes_functions_str).split(','):
            return self.required_object_for_simple_path(request)

        required_object = super(TiffResource, self).required_object_for_only_attributes(request, attributes_functions_str)
        required_object.content_type = self.define_content_type_by_only_attributes(request, attributes_functions_str)
        return required_object

    def get_object_serialized_by_only_attributes(self, attribute_names_str, objects):
        attrs_arr = self.remove_last_slash(attribute_names_str).split(',')
        return objects

    def operation_name_method_dic(self):
        dict = super(TiffResource, self).operation_name_method_dic()
        dict.update({
            self.operation_controller.bands_operation_name: self.required_object_for_spatial_operation,
            self.operation_controller.destructor_operation_name: self.required_object_for_spatial_operation,
            self.operation_controller.driver_operation_name: self.required_object_for_spatial_operation,
            self.operation_controller.extent_operation_name: self.required_object_for_spatial_operation,
            self.operation_controller.geotransform_operation_name: self.required_object_for_spatial_operation,
            self.operation_controller.height_operation_name: self.required_object_for_spatial_operation,
            self.operation_controller.info_operation_name: self.required_object_for_spatial_operation,
            self.operation_controller.metadata_operation_name: self.required_object_for_spatial_operation,
            self.operation_controller.name_operation_name: self.required_object_for_spatial_operation,
            self.operation_controller.origin_operation_name: self.required_object_for_spatial_operation,
            self.operation_controller.ptr_operation_name: self.required_object_for_spatial_operation,
            self.operation_controller.ptr_type_operation_name: self.required_object_for_spatial_operation,
            self.operation_controller.scale_operation_name: self.required_object_for_spatial_operation,
            self.operation_controller.skew_operation_name: self.required_object_for_spatial_operation,
            self.operation_controller.srid_operation_name: self.required_object_for_spatial_operation,
            self.operation_controller.srs_operation_name: self.required_object_for_spatial_operation,
            self.operation_controller.transform_operation_name: self.required_object_for_transform_operation,
            self.operation_controller.vsi_buffer_operation_name: self.required_object_for_spatial_operation,
            self.operation_controller.warp_operation_name: self.required_object_for_spatial_operation,
            self.operation_controller.width_operation_name: self.required_object_for_spatial_operation
        })
        return dict

    def operation_name_context_dic(self):
        dict = super(TiffResource, self).operation_name_context_dic()
        dict.update({
            self.operation_controller.bands_operation_name: self.required_context_for_operation,
            self.operation_controller.destructor_operation_name: self.required_context_for_operation,
            self.operation_controller.driver_operation_name: self.required_context_for_operation,
            self.operation_controller.extent_operation_name: self.required_context_for_operation,
            self.operation_controller.geotransform_operation_name: self.required_context_for_operation,
            self.operation_controller.height_operation_name: self.required_context_for_operation,
            self.operation_controller.info_operation_name: self.required_context_for_operation,
            self.operation_controller.metadata_operation_name: self.required_context_for_operation,
            self.operation_controller.name_operation_name: self.required_context_for_operation,
            self.operation_controller.origin_operation_name: self.required_context_for_operation,
            self.operation_controller.ptr_operation_name: self.required_context_for_operation,
            self.operation_controller.ptr_type_operation_name: self.required_context_for_operation,
            self.operation_controller.scale_operation_name: self.required_context_for_operation,
            self.operation_controller.skew_operation_name: self.required_context_for_operation,
            self.operation_controller.srid_operation_name: self.required_context_for_operation,
            self.operation_controller.srs_operation_name: self.required_context_for_operation,
            self.operation_controller.transform_operation_name: self.required_context_for_operation,
            self.operation_controller.vsi_buffer_operation_name: self.required_context_for_operation,
            self.operation_controller.warp_operation_name: self.required_context_for_operation,
            self.operation_controller.width_operation_name: self.required_context_for_operation,
        })
        return dict

    def required_object_for_transform_operation(self, request, attributes_functions_str):
        object = self.get_object_from_transform_operation(request, attributes_functions_str)
        content_type = self.define_content_type_by_operation(request, self.operation_controller.transform_operation_name)
        #{self.operation_controller.transform_operation_name: object}
        return RequiredObject(object.vsi_buffer, content_type, self.object_model, 200)

    def required_object_for_spatial_operation(self, request, attributes_functions_str):
        if self.path_has_url(attributes_functions_str.lower()):
            return self.response_request_attributes_functions_str_with_url(attributes_functions_str, request)
        return self.get_object_from_operation( request, self.remove_last_slash(attributes_functions_str) )

    def get_object_from_transform_operation(self, request, attributes_functions_str):
        srid = int( self.remove_last_slash(attributes_functions_str).split("/")[1] )
        return self.object_model.transform(srid)

    def get_object_from_operation(self, request, attributes_functions_str):
        att_funcs = attributes_functions_str.split('/')
        operation_name = self.get_operation_name_from_path(attributes_functions_str)
        content_type_by_operation = self.define_content_type_by_operation(request, operation_name)

        a_value = self._execute_attribute_or_method(self.object_model, att_funcs[0], att_funcs[1:])
        #if isinstance(a_value, GDALRaster):
        #    return RequiredObject( {operation_name: a_value.vsi_buffer} , content_type_by_operation, self.object_model, 200)

        if isinstance(a_value, memoryview) or isinstance(a_value, buffer):
            return RequiredObject( {operation_name: a_value.obj} , content_type_by_operation, self.object_model, 200)

        elif isinstance(a_value, bytes):
            return RequiredObject(a_value, content_type_by_operation, self.object_model, 200)

        elif isinstance(a_value, SpatialReference):
            return RequiredObject( {operation_name: a_value.wkt} , content_type_by_operation, self.object_model, 200)

        else:
            return RequiredObject( {operation_name: a_value} , content_type_by_operation, self.object_model, 200)

    def response_request_attributes_functions_str_with_url(self, attributes_functions_str, request=None):
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
        return self.get_object_from_operation(request, attributes_functions_str)

    def basic_get(self, request, *args, **kwargs):
        self.object_model = BaseModel().get_model_object_raster(self, kwargs)
        #self.object_model = self.get_object(kwargs)
        #self.object_model = BaseModel().create_model_object_raster(self, self.get_object(kwargs))
        self.current_object_state = self.object_model
        self.set_basic_context_resource(request)
        self.e_tag = str(hash(self.object_model))

        attributes_functions_str = kwargs.get(self.attributes_functions_name_template())

        if self.is_simple_path(attributes_functions_str):
            return self.required_object_for_simple_path(request)

        if self.path_has_only_attributes(attributes_functions_str):
            return self.required_object_for_only_attributes(request, attributes_functions_str)

        res = self.get_required_object_from_method_to_execute(request, attributes_functions_str)
        if res is None:
            return self.required_object_for_invalid_sintax(attributes_functions_str)
        return res

    def response_base_get(self, request, *args, **kwargs):
        if self.resource_in_cache(request):
            return self.response_base_object_in_cache(request)

        req_obj = self.basic_get(request, *args, **kwargs)

        if req_obj.status_code in [400, 401, 404]:
            return Response(req_obj.representation_object, status=req_obj.status_code)
        if req_obj.status_code in [500]:
            return Response({'Error ': 'The server can not process this request. Status:' + str(status)}, status=req_obj.status_code)

        if req_obj.content_type == CONTENT_TYPE_IMAGE_TIFF:
            response = HttpResponse(req_obj.representation_object, req_obj.content_type)
            response['Content-Disposition'] = 'attachment; filename=' + self.default_file_name()
            return response

        if self.is_binary_content_type(req_obj):
            return self.response_base_get_binary(request, req_obj)

        key = self.get_key_cache(request, a_content_type=req_obj.content_type)
        self.set_key_with_data_in_cache(key, self.e_tag, req_obj.representation_object)

        resp = Response(data=req_obj.representation_object, status=200, content_type=req_obj.content_type)
        self.set_etag_in_header(resp, self.e_tag)
        return resp

    '''
    def get(self, request, format=None, *args, **kwargs):
        required_object = self.basic_get(request, *args, **kwargs)

        if required_object.status_code != 200:
            return required_object

        if required_object.content_type == CONTENT_TYPE_IMAGE_TIFF:
            response = HttpResponse(required_object.representation_object, required_object.content_type)
            response['Content-Disposition'] = 'attachment; filename=' + self.default_file_name()
            return response

        if required_object.content_type == CONTENT_TYPE_OCTET_STREAM:
            return Response(data=bytes(required_object.representation_object),status=200, content_type=required_object.content_type)
            #self.response_base_get_binary(request, required_object)

        return Response(data=required_object.representation_object,status=200, content_type=required_object.content_type)
    '''
