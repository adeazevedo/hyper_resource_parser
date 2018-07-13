
from hyper_resource.views import BaseModel
from hyper_resource.resources.SpatialCollectionResource import SpatialCollectionResource


class RasterCollectionResource(SpatialCollectionResource):
    field_names = []

    def fields_to_web(self):
       return self.field_names

    def spatial_field_name(self):
        return self.serializer_class.Meta.geo_field

    def initialize_object(self, request, *args, **kwargs):
        self.object_model = BaseModel().get_iris_raster(self, kwargs)
        self.current_object_state = self.object_model
        self.set_basic_context_resource(request)
        self.is_entry_point = True
