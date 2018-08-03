
from django.db.models import QuerySet, OneToOneField, Model

from rest_framework.response import Response

from hyper_resource.views import *
from hyper_resource.resources.AbstractResource import AbstractResource
from copy import deepcopy


class NonSpatialResource(AbstractResource):
    '''
    def response_of_request(self,  attributes_functions_str):
        att_funcs = attributes_functions_str.split('/')
        if (not self.is_operation(att_funcs[0])) and self.is_attribute(att_funcs[0]):
            att_funcs = att_funcs[1:]

        self.current_object_state = self._execute_attribute_or_method(self.object_model, att_funcs[0], att_funcs[1:])

        if hasattr(self.current_object_state, 'model') and issubclass(self.current_object_state.model, Model):
            class_name = self.current_object_state.model.__name__ + 'Serializer'
            serializer_cls = self.object_model.class_for_name(self.serializer_class.__module__, class_name)

            if isinstance(self.current_object_state, QuerySet):
                self.current_object_state = serializer_cls(self.current_object_state, many=True, context={'request': self.request}).data

            elif isinstance(self.current_object_state.field, OneToOneField):
                self.current_object_state = serializer_cls(self.current_object_state, context={'request': self.request}).data

            else:
                self.current_object_state = serializer_cls(self.current_object_state, many=True, context={'request': self.request}).data

        a_value = {self.name_of_last_operation_executed: self.current_object_state}

        return a_value, CONTENT_TYPE_JSON, self.object_model, {'status': 200}
    '''

    def operation_name_method_dic(self):
        return super(NonSpatialResource, self).operation_name_method_dic()

    #todo: HARCODED METHOD IMPLEMENTATION. Need to create NonSpatialOperationController and override 'dict_all_operation_dict' method
    def array_of_operation_name(self):
        return ['spatialize']

    # same signature in FeatureResource
    def response_request_attributes_functions_str_with_url(self, attributes_functions_str, request=None):
        pass

    def required_object_for_simple_path(self, request):
        # django context object is required when the serializer has HyperlinkedrelatedField
        serializer = self.serializer_class(self.object_model, context={'request': request})
        return RequiredObject(serializer.data, self.content_type_or_default_content_type(request), self.object_model, 200)

    def required_object_for_only_attributes(self, request, attributes_functions_str):
        object = self.get_objects_by_only_attributes(attributes_functions_str)
        serialized_object = self.get_objects_serialized_by_only_attributes(attributes_functions_str, object)
        return RequiredObject(serialized_object, self.content_type_or_default_content_type(request), object, 200)

    def get_objects_by_only_attributes(self, attribute_names_str):
        attr_list = self.remove_last_slash(attribute_names_str).split(',')
        obj_dict = {}
        for attr_name in attr_list:
            attr_value = self._value_from_object(self.object_model, attr_name, [])
            obj_dict[attr_name] = attr_value
        return obj_dict

    def get_objects_serialized_by_only_attributes(self, attribute_names_str, objects):
        # NonSpatialObjects don't need a complex serialization, this method is here just to keep the code design
        # remember these three steps:
        # 1. get the object(s) by a "get_objects_by_something" method like
        # 2. serialize the returned object(s) by a "get_objects_serialized_by_something" method like
        # 3. and finally return a RequiredObject with the serialized_data, a content_type and the original object
        return objects

    def get_objects_from_spatialize_operation(self, request, attributes_functions_str):
        spatialize_operation = self.build_spatialize_operation(request, attributes_functions_str)

        if spatialize_operation.right_join_data['type'] == 'FeatureCollection':
            return self.join_non_spatial_on_feature_collection(spatialize_operation)
        return self.join_non_spatial_on_feature(spatialize_operation)

    def join_non_spatial_on_feature(self, spatialize_operation):
        if spatialize_operation.left_join_data[ spatialize_operation.left_join_attr ] != \
        spatialize_operation.right_join_data['properties'][ spatialize_operation.right_join_attr ]:
            return None

        for alpha_attr, alpha_data in spatialize_operation.left_join_data.items():
            spatialize_operation.right_join_data['properties']['joined__' + alpha_attr] = alpha_data

        return spatialize_operation.right_join_data

    def join_non_spatial_on_feature_collection(self, spatialize_operation):
        for feature in spatialize_operation.right_join_data['features']:
            if spatialize_operation.left_join_data[ spatialize_operation.left_join_attr ] == \
                feature['properties'][ spatialize_operation.right_join_attr ]:

                copied_feature = deepcopy(feature)
                for alpha_attr, alpha_data in spatialize_operation.left_join_data.items():
                    copied_feature['properties']['joined__' + alpha_attr] = alpha_data
                return copied_feature # only one location joined on alphanumeric data

    # todo: refactor 'response_request_with_attributes()' of the other classes to implement to behaviour of get_objects_serialized_by_only_attributes
    '''
    def response_request_with_attributes(self, attributes_functions_name, request=None):
        a_dict = {}
        attributes = attributes_functions_name.strip().split(',')

        for attr_name in attributes:
            obj = self._value_from_object(self.object_model, attr_name, [])
            a_dict[attr_name] = obj

        self.current_object_state = a_dict
    '''

    def basic_get(self, request, *args, **kwargs):
        self.object_model = self.get_object(kwargs)
        self.current_object_state = self.object_model
        self.set_basic_context_resource(request)
        attributes_functions_str = kwargs.get(self.attributes_functions_name_template())

        if self.is_simple_path(attributes_functions_str):
            return self.required_object_for_simple_path(request)
        elif self.path_has_only_attributes(attributes_functions_str):
            return self.required_object_for_only_attributes(request, attributes_functions_str)

        res = self.get_requiredObject_from_method_to_execute(request, attributes_functions_str)
        if res is None:
            return self.required_object_for_invalid_sintax(attributes_functions_str)
        return res

    def get(self, request, format=None, *args, **kwargs):
        if format == 'jsonld':
            return self.options(request, *args, **kwargs)

        required_object = self.basic_get(request, *args, **kwargs)
        status = required_object.status_code

        if status == 400:
            return Response(required_object.representation_object, status=required_object.status_code, content_type=required_object.content_type)

        if status in [401,404]:
            return Response({'Error ': 'The request has problem. Status:' + str(status)}, status=status)

        if status in [500]:
           return Response({'Error ': 'The server can not process this request. Status:' + str(status)}, status=status)

        response = Response(data=required_object.representation_object, content_type=required_object.content_type)
        self.add_base_headers(request, response)

        return response

    def define_resource_type_by_only_attributes(self, request, attributes_functions_str):
        r_type = self.resource_type_or_default_resource_type(request)
        if r_type != self.default_resource_type():
            return r_type

        attrs_functs_arr = self.remove_last_slash(attributes_functions_str).split(',')
        if len(attrs_functs_arr) == 1:
            # the field type has priority over default resource type
            return type(self.field_for(attrs_functs_arr[0]))

        return self.default_resource_type()

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
        return self.required_object_for_invalid_sintax(attributes_functions_str, message="This request has invalid attribute or operation: ")

    def options(self, request, *args, **kwargs):
        required_object = self.basic_options(request, *args, **kwargs)
        if required_object.status_code == 200:
            response = Response(required_object.representation_object, content_type=required_object.content_type, status=200)
            self.add_base_headers(request, response)
        else:
            response = Response(data={"This request is not supported": self.kwargs.get("attributes_functions", None)},
                                status=required_object.status_code)
        return response