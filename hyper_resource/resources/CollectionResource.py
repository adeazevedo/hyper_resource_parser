from hyper_resource.models import CollectionResourceOperationController
from hyper_resource.resources.AbstractCollectionResource import AbstractCollectionResource
from copy import deepcopy

class CollectionResource(AbstractCollectionResource):
    def __init__(self):
        super(CollectionResource, self).__init__()
        self.queryset = None
        self.operation_controller = CollectionResourceOperationController()

    def operations_with_parameters_type(self):
        return self.operation_controller.collection_operations_dict()

    def get_objects_from_spatialize_operation(self, request, attributes_functions_str):
        spatialize_operation = self.build_spatialize_operation(request, attributes_functions_str)
        return self.join_dict_list_on_spatial_collection(spatialize_operation)

    def join_dict_list_on_spatial_collection(self, spatialize_operation):
        spatialized_data_list = []
        for original_feature in spatialize_operation.right_join_data['features']:
            updated_feature = deepcopy(original_feature)
            for position, dict_to_spatialize in enumerate(spatialize_operation.left_join_data):
                if updated_feature['properties'][spatialize_operation.right_join_attr] == dict_to_spatialize[spatialize_operation.left_join_attr]:
                    updated_feature['properties']['joined__' + str(position) ] = deepcopy(dict_to_spatialize)#.pop(position)

            if sorted(list(updated_feature['properties'].keys())) != sorted(list(original_feature['properties'].keys())):
                spatialized_data_list.append(updated_feature)

        return {'type': 'FeatureCollection', 'features': spatialized_data_list}

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
        context = super(CollectionResource, self).get_context_by_only_attributes(request, attributes_functions_str)
        resource_type = self.resource_type_or_default_resource_type(request)
        self.context_resource.set_context_to_resource_type(request, self.object_model, resource_type)

        context["@type"] = self.context_resource.get_dict_context()["@type"]
        supported_operations_list = self.context_resource.supportedOperationsFor(self.object_model, resource_type)
        context.update({'hydra:supportedOperations': supported_operations_list})

        return context

