from hyper_resource.resources.AbstractResource import *
from hyper_resource.resources.SpatialResource import SpatialResource


class FeatureResource(SpatialResource):
    def __init__(self):
        super(FeatureResource, self).__init__()

    def default_resource_type(self):
        return 'Feature'

    def dict_by_accept_resource_type(self):
        dict = {
            CONTENT_TYPE_OCTET_STREAM: 'Geobuf'
        }

        return dict

    def hashed_value(self, object_):
        dt = datetime.now()
        return self.__class__.__name__ + str(dt.microsecond)

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

    '''
    def get_requiredObject_from_method_to_execute(self, request, attributes_functions_str):
        operation_name = self.get_operation_name_from_path(attributes_functions_str)
        method_to_execute = self.get_operation_to_execute(operation_name)

        if method_to_execute is None:
            return None

        #attr_functions_str =  attributes_functions_str.replace(operation_name, self.get_real_operation_name(operation_name))
        return method_to_execute(*[request, attributes_functions_str])
    '''

    def operation_name_method_dic(self):
        dict = super(FeatureResource, self).operation_name_method_dic()
        dict.update({
            self.operation_controller.area_operation_name: self.required_object_for_spatial_operation,
            self.operation_controller.boundary_operation_name: self.required_object_for_spatial_operation,
            self.operation_controller.buffer_operation_name: self.required_object_for_spatial_operation,
            self.operation_controller.centroid_operation_name: self.required_object_for_spatial_operation,
            self.operation_controller.contains_operation_name: self.required_object_for_spatial_operation,
            self.operation_controller.convex_hull_operation_name: self.required_object_for_spatial_operation,
            self.operation_controller.coord_seq_operation_name: self.required_object_for_spatial_operation,
            self.operation_controller.coords_operation_name: self.required_object_for_spatial_operation,
            self.operation_controller.count_operation_name: self.required_object_for_spatial_operation,
            self.operation_controller.crosses_operation_name: self.required_object_for_spatial_operation,
            self.operation_controller.crs_operation_name: self.required_object_for_spatial_operation,
            self.operation_controller.difference_operation_name: self.required_object_for_spatial_operation,
            self.operation_controller.dims_operation_name: self.required_object_for_spatial_operation,
            self.operation_controller.disjoint_operation_name: self.required_object_for_spatial_operation,
            self.operation_controller.distance_operation_name: self.required_object_for_spatial_operation,
            self.operation_controller.empty_operation_name: self.required_object_for_spatial_operation,
            self.operation_controller.envelope_operation_name: self.required_object_for_spatial_operation,
            self.operation_controller.equals_operation_name: self.required_object_for_spatial_operation,
            self.operation_controller.equals_exact_operation_name: self.required_object_for_spatial_operation,
            self.operation_controller.ewkb_operation_name: self.required_object_for_spatial_operation,
            self.operation_controller.ewkt_operation_name: self.required_object_for_spatial_operation,
            self.operation_controller.extend_operation_name: self.required_object_for_spatial_operation,
            self.operation_controller.extent_operation_name: self.required_object_for_spatial_operation,
            self.operation_controller.geojson_operation_name: self.required_object_for_spatial_operation,
            self.operation_controller.geom_type_operation_name: self.required_object_for_spatial_operation,
            self.operation_controller.geom_typeid_operation_name: self.required_object_for_spatial_operation,
            self.operation_controller.get_coords_operation_name: self.required_object_for_spatial_operation,
            self.operation_controller.get_srid_operation_name: self.required_object_for_spatial_operation,
            self.operation_controller.get_x_operation_name: self.required_object_for_spatial_operation,
            self.operation_controller.get_y_operation_name: self.required_object_for_spatial_operation,
            self.operation_controller.get_z_operation_name: self.required_object_for_spatial_operation,
            self.operation_controller.has_cs_operation_name: self.required_object_for_spatial_operation,
            self.operation_controller.hasz_operation_name: self.required_object_for_spatial_operation,
            self.operation_controller.hex_operation_name: self.required_object_for_spatial_operation,
            self.operation_controller.hexewkb_operation_name: self.required_object_for_spatial_operation,
            self.operation_controller.index_operation_name: self.required_object_for_spatial_operation,
            self.operation_controller.intersection_operation_name: self.required_object_for_spatial_operation,
            self.operation_controller.intersects_operation_name: self.required_object_for_spatial_operation,
            self.operation_controller.interpolate_operation_name: self.required_object_for_spatial_operation,
            self.operation_controller.json_operation_name: self.required_object_for_spatial_operation,
            self.operation_controller.kml_operation_name: self.required_object_for_spatial_operation,
            self.operation_controller.length_operation_name: self.required_object_for_spatial_operation,
            self.operation_controller.normalize_operation_name: self.required_object_for_spatial_operation,
            self.operation_controller.num_coords_operation_name: self.required_object_for_spatial_operation,
            self.operation_controller.num_geom_operation_name: self.required_object_for_spatial_operation,
            self.operation_controller.num_points_operation_name: self.required_object_for_spatial_operation,
            self.operation_controller.ogr_operation_name: self.required_object_for_spatial_operation,
            self.operation_controller.overlaps_operation_name: self.required_object_for_spatial_operation,
            self.operation_controller.point_on_surface_operation_name: self.required_object_for_spatial_operation,
            self.operation_controller.relate_operation_name: self.required_object_for_spatial_operation,
            self.operation_controller.relate_pattern_operation_name: self.required_object_for_spatial_operation,
            self.operation_controller.ring_operation_name: self.required_object_for_spatial_operation,
            self.operation_controller.set_coords_operation_name: self.required_object_for_spatial_operation,
            self.operation_controller.set_srid_operation_name: self.required_object_for_spatial_operation,
            self.operation_controller.set_x_operation_name: self.required_object_for_spatial_operation,
            self.operation_controller.set_y_operation_name: self.required_object_for_spatial_operation,
            self.operation_controller.set_z_operation_name: self.required_object_for_spatial_operation,
            self.operation_controller.simple_operation_name: self.required_object_for_spatial_operation,
            self.operation_controller.simplify_operation_name: self.required_object_for_spatial_operation,
            self.operation_controller.srid_operation_name: self.required_object_for_spatial_operation,
            self.operation_controller.srs_operation_name: self.required_object_for_spatial_operation,
            self.operation_controller.sym_difference_operation_name: self.required_object_for_spatial_operation,
            self.operation_controller.touches_operation_name: self.required_object_for_spatial_operation,
            self.operation_controller.transform_operation_name: self.required_object_for_spatial_operation,
            self.operation_controller.union_operation_name: self.required_object_for_spatial_operation,
            self.operation_controller.valid_operation_name: self.required_object_for_spatial_operation,
            self.operation_controller.valid_reason_operation_name: self.required_object_for_spatial_operation,
            self.operation_controller.within_operation_name: self.required_object_for_spatial_operation,
            self.operation_controller.wkb_operation_name: self.required_object_for_spatial_operation,
            self.operation_controller.wkt_operation_name: self.required_object_for_spatial_operation,
            self.operation_controller.x_operation_name: self.required_object_for_spatial_operation,
            self.operation_controller.y_operation_name: self.required_object_for_spatial_operation,
            self.operation_controller.z_operation_name: self.required_object_for_spatial_operation,
        })
        return dict

    def required_object_for_simple_path(self, request):
        serializer = self.serializer_class(self.object_model)
        return RequiredObject(serializer.data, self.content_type_or_default_content_type(request), self.object_model, 200)

    def required_object_for_only_attributes(self, request, attributes_functions_str):
        attr_str = self.remove_last_slash(attributes_functions_str)
        return self.response_request_with_attributes(attr_str, request)

    def required_object_for_spatial_operation(self, request, attributes_functions_str):
        if self.path_has_url(attributes_functions_str.lower()):
            return self.response_request_attributes_functions_str_with_url(attributes_functions_str, request)
        return self.response_of_request(attributes_functions_str)

    def get_objects_from_spatialize_operation(self, request, attributes_functions_str):
        spatialize_operation = self.build_spatialize_operation(request, attributes_functions_str)

        if type(spatialize_operation.right_join_data) is list:
            return self.join_feature_on_list_response(spatialize_operation)
        return self.join_feature_on_dict_response(spatialize_operation)

    def join_feature_on_dict_response(self, spatialize_operation):
        if spatialize_operation.left_join_data['properties'][ spatialize_operation.left_join_attr ] !=\
                spatialize_operation.right_join_data[ spatialize_operation.right_join_attr ]:
            # the datas isn't 'joinable'
            return None

        for alfa_attr_name, alfa_attr_val in spatialize_operation.right_join_data.items():
            spatialize_operation.left_join_data['properties']['joined__' + alfa_attr_name] = alfa_attr_val
        return spatialize_operation.left_join_data

    def join_feature_on_list_response(self, spatialize_operation):
        for k, dicti in enumerate(spatialize_operation.right_join_data):
            if spatialize_operation.left_join_data['properties'][spatialize_operation.left_join_attr] == dicti[spatialize_operation.right_join_attr]:
                spatialize_operation.left_join_data['properties']['joined__' + str(k)] = dicti
                # To avoid insert a dict in Feature properties, you can duplicate the geometry for each
                # alphanumeric resource whose joined attribute value coincides

        return spatialize_operation.left_join_data

    def basic_get(self, request, *args, **kwargs):
        self.object_model = self.get_object(kwargs)
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

    '''
    def get_context_by_only_attributes(self, request, attributes_functions_str):
        attrs_funcs_str = self.remove_last_slash(attributes_functions_str)
        super(FeatureResource, self).get_context_by_only_attributes(request, attrs_funcs_str)

        resource_type = self.define_resource_type_by_only_attributes(request, attrs_funcs_str)
        self.context_resource.set_context_to_resource_type(request, self.object_model, resource_type)
        supported_operation_dict = self.context_resource.supportedOperationsFor(self.object_model, resource_type)

        context = self.context_resource.dict_context
        context['hydra:supportedOperations'] = supported_operation_dict
        return context
    '''

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

    def get(self, request, format=None, *args, **kwargs):
        self.change_request_if_image_png_into_IRI(request)
        return super(FeatureResource,self).get(request, *args, **self.kwargs)
