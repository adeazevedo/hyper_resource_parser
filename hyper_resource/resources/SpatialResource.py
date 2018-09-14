
import json

from django.contrib.gis.geos import GEOSGeometry, GeometryCollection

from rest_framework.response import Response

from hyper_resource.resources.AbstractResource import AbstractResource


class SpatialResource(AbstractResource):
    def __init__(self):
        super(SpatialResource, self).__init__()
        self.iri_style = None

    '''
    def spatial_field_name(self):
        return self.serializer_class.Meta.geo_field
    '''

    def make_geometrycollection_from_featurecollection(self, feature_collection):
        geoms = []
        features = json.loads(feature_collection)

        for feature in features['features']:
            feature_geom = json.dumps(feature['geometry'])
            geoms.append(GEOSGeometry(feature_geom))

        return GeometryCollection(tuple(geoms))

    def all_parameters_converted(self, attribute_or_function_name, parameters):
        parameters_converted = []

        if self.is_operation_and_has_parameters(attribute_or_function_name):
            parameters_type = self.operations_with_parameters_type()[attribute_or_function_name].parameters

            for i in range(len(parameters)):
                if GEOSGeometry == parameters_type[i]:
                    if not (parameters[i][0] == '{' or parameters[i][0] == '['):
                        parameters_converted.append(GEOSGeometry(parameters[i]))

                    else:
                        geometry_dict = json.loads(parameters[i])

                        if isinstance(geometry_dict, dict) and geometry_dict['type'].lower() == 'feature':
                            parameters_converted.append(parameters_type[i](json.dumps(geometry_dict['geometry'])))

                        elif isinstance(geometry_dict, dict) and geometry_dict['type'].lower() == 'featurecollection':
                            geometry_collection = self.make_geometrycollection_from_featurecollection(parameters[i])
                            parameters_converted.append(parameters_type[i](geometry_collection))
                        else:
                            parameters_converted.append(parameters_type[i](parameters[i]))
                else:
                    parameters_converted.append(parameters_type[i](parameters[i]))


            return parameters_converted

        return self.parametersConverted(parameters)

    def options(self, request, *args, **kwargs):
        self.basic_get(request, *args, **kwargs)
        resp = Response(data=self.context_resource.context(), content_type='application/ld+json' )
        self.add_base_headers(request, resp)

        return resp
