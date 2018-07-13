from hyper_resource.resources.SpatialResource import SpatialResource


class RasterResource(SpatialResource):
    def default_file_name(self):
        return self.object_model.model_class_name() + '_' + str(self.object_model.pk) + '.tiff'

    def default_resource_type(self):
        return 'Raster'

    def get_object_model_raster(self, kwargs):
        pass