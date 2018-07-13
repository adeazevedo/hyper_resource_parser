
from django.db.models import QuerySet, OneToOneField, Model

from rest_framework.response import Response

from hyper_resource.views import CONTENT_TYPE_JSON
from hyper_resource.resources.AbstractResource import AbstractResource


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
                self.current_object_state = serializer_cls(self.current_object_state, many=True, context={'request': self.request}).data

            elif isinstance(self.current_object_state.field, OneToOneField):
                self.current_object_state = serializer_cls(self.current_object_state, context={'request': self.request}).data

            else:
                self.current_object_state = serializer_cls(self.current_object_state, many=True, context={'request': self.request}).data

        a_value = {self.name_of_last_operation_executed: self.current_object_state}

        return a_value, CONTENT_TYPE_JSON, self.object_model, {'status': 200}

    def basic_get(self, request, *args, **kwargs):
        self.object_model = self.get_object(kwargs)
        self.current_object_state = self.object_model
        self.set_basic_context_resource(request)
        attributes_functions_str = kwargs.get(self.attributes_functions_name_template())

        if self.is_simple_path(attributes_functions_str):
            serializer = self.serializer_class(self.object_model, context={'request': self.request})
            output = (serializer.data, CONTENT_TYPE_JSON, self.object_model, {'status': 200})

        elif self.path_has_only_attributes(attributes_functions_str):
            output = self.response_request_with_attributes(attributes_functions_str.replace(' ', ''))
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

        response = Response(data=dict_for_response[0], content_type=dict_for_response[1])
        self.add_base_headers(request, response)

        return response

    def options(self, request, *args, **kwargs):
        response = super(NonSpatialResource, self).options(request, *args, **kwargs)
        self.basic_get(request, *args, **kwargs)

        response.data = self.context_resource.context()
        response['content-type'] = 'application/ld+json'

        return response
