
from hyper_resource import views
from hyper_resource.views import RequiredObject
from hyper_resource.views import CONTENT_TYPE_JSON
from hyper_resource.models import CollectionResourceOperationController
from hyper_resource.resources.AbstractCollectionResource import AbstractCollectionResource


class CollectionResource(AbstractCollectionResource):
    def __init__(self):
        super(CollectionResource, self).__init__()
        self.queryset = None
        self.operation_controller = CollectionResourceOperationController()

    def operations_with_parameters_type(self):
        return self.operation_controller.collection_operations_dict()

    def get_objects_serialized(self):
        objects = self.model_class().objects.all()

        return self.serializer_class(objects, many=True, context={'request': self.request}).data

    def get_objects_by_only_attributes(self, attribute_names_str):
        attribute_names_str_as_array = self.remove_last_slash(attribute_names_str).split(',')

        return self.model_class().objects.values(*attribute_names_str_as_array)

    def get_objects_serialized_by_only_attributes(self, attribute_names_str, query_set):
        arr = []
        attribute_names_str_as_array = self.remove_last_slash(attribute_names_str).split(',')

        for obj in query_set:
            a_dic = {}

            for att_name in attribute_names_str_as_array:
                a_dic[att_name] = obj[att_name]

            arr.append(a_dic)

        return arr

    def get_objects_from_specialized_operation(self, attributes_functions_str):
        return self.get_objects_from_filter_operation(attributes_functions_str)

    def get_objects_by_functions(self, attributes_functions_str):
        objects = []

        if self.path_has_filter_operation(attributes_functions_str):
            objects = self.get_objects_from_filter_operation(attributes_functions_str)

        return objects

    def get_context_by_only_attributes(self, request, attributes_functions_str):
        resource_type = self.resource_type_or_default_resource_type(request)
        self.context_resource.set_context_to_resource_type(request, self.object_model, resource_type)

        return self.context_resource.dict_context

    def basic_get_OLD(self, request, *args, **kwargs):
        self.object_model = self.model_class()()
        self.set_basic_context_resource(request)
        self.inject_e_tag()
        attributes_functions_str = self.kwargs.get('attributes_functions', None)

        if self.is_simple_path(attributes_functions_str):  # to get query parameters
            query_set = self.model_class().objects.all()
            serializer = self.serializer_class(query_set, many=True, context={'request' : request})
            required_object = RequiredObject(serializer.data, self.content_type_or_default_content_type(request), query_set, 200)

            return required_object

        elif self.path_has_only_attributes(attributes_functions_str):
            query_set = self.get_objects_by_only_attributes(attributes_functions_str)
            serialized_data = self.get_objects_serialized_by_only_attributes(attributes_functions_str, query_set)

            return RequiredObject(serialized_data, self.content_type_or_default_content_type(request), query_set, 200)

        elif self.path_has_distinct_operation(attributes_functions_str):
            query_set =  self.get_objects_from_distinct_operation(attributes_functions_str)
            serializer = self.serializer_class(query_set, many=True, context={"request": request})

            return RequiredObject(serializer.data, self.content_type_or_default_content_type(request), query_set, 200)

        elif self.path_has_countresource_operation(attributes_functions_str):
            return RequiredObject({'countResource': self.model_class().objects.count()}, views.CONTENT_TYPE_JSON, self.object_model, 200)

        elif self.path_has_offsetlimit_operation(attributes_functions_str):
            query_set = self.get_objects_from_offset_limit_operation(attributes_functions_str)
            serializer = self.serializer_class(query_set, many=True, context={'request': request})

            return RequiredObject(serializer.data, self.content_type_or_default_content_type(request), query_set, 200)

        elif self.path_has_operations(attributes_functions_str) and self.path_request_is_ok(attributes_functions_str):
            query_set = self.get_objects_by_functions(attributes_functions_str)
            serialized_data = self.serializer_class(query_set, many=True, context={'request': request})

            return RequiredObject(serialized_data, self.content_type_or_default_content_type(request), query_set, 200)

        else:
            return RequiredObject(representation_object={'This request has invalid attribute or operation'},
                                  content_type=CONTENT_TYPE_JSON,
                                  origin_object=self,
                                  status_code=400)
