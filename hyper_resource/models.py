# -*- coding: utf-8 -*-
import importlib
import inspect
import json
import re
from datetime import date, datetime, time
from decimal import Decimal

import requests
from django.contrib.gis.db import models
from django.contrib.gis.db.models import Q, RasterField
# Create your models here.
from django.contrib.gis.gdal import OGRGeometry, GDALRaster
from django.contrib.gis.gdal import SpatialReference
from django.contrib.gis.geos import GEOSGeometry
from django.contrib.gis.geos import GeometryCollection
from django.contrib.gis.geos import LineString
from django.contrib.gis.geos import MultiLineString
from django.contrib.gis.geos import MultiPoint
from django.contrib.gis.geos import MultiPolygon
from django.contrib.gis.geos import Point
from django.contrib.gis.geos import Polygon
from django.contrib.gis.db.models import GeometryField
from django.contrib.gis.db.models import LineStringField
from django.contrib.gis.db.models import MultiLineStringField
from django.contrib.gis.db.models import MultiPointField
from django.contrib.gis.db.models import MultiPolygonField
from django.contrib.gis.db.models import PointField
from django.contrib.gis.db.models import PolygonField
from django.contrib.gis.db.models import ForeignKey
from requests import ConnectionError
from requests import HTTPError

GEOSGEOMETRY_SUBCLASSES = ['POINT', 'MULTIPOINT', 'LINESTRING', 'MULTILINESTRING', 'POLYGON', 'MULTIPOLYGON', 'GEOMETRYCOLLECTION']

import sys
if sys.version_info > (3,):
    buffer = memoryview
else:
    buffer = buffer

def dict_map_geo_field_geometry():
    """
    Returns a dict whose his keys are geometric types
    and his respective values is a geometric model
    :return:
    """
    dic = {}
    dic[GeometryField] = GEOSGeometry
    dic[LineStringField] = LineString
    dic[MultiLineStringField] = MultiLineString
    dic[MultiPointField] = MultiPoint
    dic[MultiPolygonField] = MultiPolygon
    dic[PointField] = Point
    dic[PolygonField] = Polygon
    return dic

def boolean_operator():
    return ['neq', 'eq','lt','lte','gt','gte','between','isnull','isnotnull', 'like','notlike','in','notin',
        '*neq', '*eq','*lt','*lte','*gt','*gte','*between','*isnull','isnotnull','*like','*notlike','*in','*notin']
def logical_operator():
    return ['or', 'and', '*or', '*and']

class Type_Called():
    """
    Type_called is a definition type that contains a name,
    a list of parameters and a return type
    """
    def __init__(self, a_name='', params=[], answer=None):
        self.name = a_name
        self.parameters = params
        self.return_type = answer

class JoinOperation():
    def __init__(self, left_join_data, left_join_attr, right_join_attr, right_join_data):
        self.left_join_data = left_join_data
        self.left_join_attr = left_join_attr
        self.right_join_attr = right_join_attr
        self.right_join_data = right_join_data

class ConverterType():

    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(ConverterType, cls).__new__(cls, *args, **kwargs)
        return cls._instance

    def value_has_url(self, value_str):
        return (value_str.find('http:') > -1) or (value_str.find('https:') > -1) or (value_str.find('www.') > -1)

    def path_is_feature_collection(self, path):
        try:
            path_as_json = json.loads(path)
        except json.decoder.JSONDecodeError:
            return False

        if 'type' in path_as_json.keys():
            return path_as_json['type'].lower() == 'featurecollection'
        else:
            return False

    def path_is_geometry_collection(self, path):
        try:
            path_as_json = json.loads(path)
        except json.decoder.JSONDecodeError:
            return False

        if 'type' in path_as_json:
            return path_as_json['type'].lower() == 'geometrycollection'
        else:
            return False

    def path_is_feature(self, path):
        try:
            path_as_json = json.loads(path)
        except json.decoder.JSONDecodeError:
            return False

        if 'type' in path_as_json:
            return path_as_json['type'].lower() == 'feature'
        else:
            return False

    def path_is_wkt(self, path):
        geos_subclasses = [geom_subcls.capitalize() for geom_subcls in GEOSGEOMETRY_SUBCLASSES]
        joined_geos_subclasses = "|".join(geos_subclasses)
        regex = r"(" + joined_geos_subclasses + ")\(.+\)$"
        return True if re.search(regex, path) is not None else False

    def make_geometrycollection_from_featurecollection(self, feature_collection):
        geoms = []
        #features = json.loads(feature_collection)
        gc = GeometryCollection()
        for feature in feature_collection['features']:
            feature_geom = json.dumps(feature['geometry'])
            geos_geom = (GEOSGeometry(feature_geom))
            gc.append(geos_geom)
        return gc

    def make_geometrycollection_from_dict(self, geom_collection_dict):
        gc = GeometryCollection()
        for geometry in geom_collection_dict['geometries']:
            geom_coordinates = json.dumps(geometry)
            geos_geom = (GEOSGeometry(geom_coordinates))
            gc.append(geos_geom)
        return gc

    def get_geos_geometry_from_request(self, url_as_str):
        resp = requests.get(url_as_str)
        if 400 <= resp.status_code <= 599:
            raise HTTPError({resp.status_code: resp.reason})
        if resp.headers['content-type'] == 'application/octet-stream':
            return GEOSGeometry(buffer(resp.content))

        elif resp.headers['content-type'] in ['application/json', 'application/geojson', 'application/vnd.geo+json']:
            js = resp.json()
            if (js.get("type") and js["type"].lower()=='feature'):
                return GEOSGeometry(json.dumps(js["geometry"]))

            elif  (js.get("type") and js["type"].lower()=='featurecollection'):
                return self.make_geometrycollection_from_featurecollection(js)

            else:
                return GEOSGeometry(json.dumps(js))

        return GEOSGeometry(resp.content)

    def convert_to_string(self, value_as_str):
        return str(value_as_str)

    def convert_to_int(self, value_as_str):
        return int(value_as_str)

    def convert_to_float(self, value_as_str):
        return float(value_as_str)

    def convert_to_decimal(self, value_as_str):
        return Decimal(value_as_str)

    def convert_to_date(self, value_as_str):
        return datetime.strptime(value_as_str, "%Y-%m-%d").date()

    def convert_to_datetime(self, value_as_str):
        return datetime.strptime(value_as_str, "%Y-%m-%d %H:%M:%S")

    def convert_to_time(self, value_as_str):
        return datetime.time.strptime(value_as_str, "%Y-%m-%d %H:%M:%S")

    def convert_to_geometry(self, value_as_str):
        try:
            if self.value_has_url(value_as_str):
               return self.get_geos_geometry_from_request(value_as_str)

            return GEOSGeometry(value_as_str)
        except (ValueError, ConnectionError, HTTPError) as err:
            print('Error: '.format(err))


    def operation_to_convert_value(self, a_type):
        d = {}
        d[str] = self.convert_to_string
        d[int] = self.convert_to_int
        d[float] = self.convert_to_float
        d[date] = self.convert_to_date
        d[datetime] = self.convert_to_datetime
        d[time] = self.convert_to_time
        d[models.CharField] = self.convert_to_string
        d[models.TextField] = self.convert_to_string
        d[models.IntegerField] = self.convert_to_int
        d[models.AutoField] = self.convert_to_int
        d[models.FloatField] = self.convert_to_float

        d[models.DecimalField] = self.convert_to_decimal

        d[models.TimeField] = self.convert_to_time
        d[models.DateTimeField] = self.convert_to_datetime
        d[models.DateField] = self.convert_to_date
        d[GeometryField] = self.convert_to_geometry
        d[PolygonField] = self.convert_to_geometry
        d[LineStringField] = self.convert_to_geometry
        d[PointField] = self.convert_to_geometry
        d[MultiPolygonField] = self.convert_to_geometry
        d[MultiLineString] = self.convert_to_geometry
        d[MultiLineStringField]= self.convert_to_geometry
        d[MultiPointField] = self.convert_to_geometry
        d[ForeignKey] = self.convert_to_int

        return d[a_type]

    def value_converted(self, a_type, value):
        object_method = self.operation_to_convert_value(a_type)
        return object_method(value)

    def convert_parameters(self, a_type, attribute_or_function_name, parameters):

        if a_type in BaseOperationController().dict_all_operation_dict():
            operation_dict = BaseOperationController().dict_all_operation_dict()[a_type]

            if attribute_or_function_name in operation_dict:
                type_called = operation_dict[attribute_or_function_name]

                return [ConverterType().value_converted(param, parameters[i]) for i, param in enumerate(type_called.parameters) ]

        return parameters

class QObjectFactory:

    def __init__(self, model_class, attribute_name, operation_or_operator, raw_value_as_str):
        self.model_class = model_class
        self.attribute_name = attribute_name
        self.operation_or_operator = operation_or_operator
        self.raw_value_as_str = raw_value_as_str

    def fields(self):
        return self.model_class._meta.fields

    def field_type(self):
        for field in self.fields():
            if field.name == self.attribute_name:
                return type(field)
        return None

    def convert_value_for(self, a_value):
        converter = ConverterType()
        field_type = self.field_type()
        if field_type is None:
            return None
        if isinstance(a_value, bool):
            return a_value
        #if (a_value.lower() == 'false' or a_value.lower() == 'true') and self.operation_or_operator == 'isnull':
        if (a_value.lower() == 'false' or a_value.lower() == 'true'):
            return  False if a_value.lower() == 'false' else True

        return converter.value_converted(self.field_type(), a_value)


    def q_object_base_range(self, oper_operation):
        dc = {}
        arr_value = self.raw_value_as_str.split('&')
        arr_value_converted = [ self.convert_value_for(a_value) for a_value in arr_value]
        dc[self.attribute_name + '__' + oper_operation] = arr_value_converted
        return Q(**dc)

    def q_object_for_in(self):
        return self.q_object_base_range('in')

    def q_object_for_between(self):
        return self.q_object_base_range('range')

    def q_object_for_eq(self):
        dc = {}
        dc[self.attribute_name] = self.convert_value_for(self.raw_value_as_str)
        return Q(**dc)

    def q_object_for_neq(self):
        dc = {}
        dc[self.attribute_name] = self.convert_value_for(self.raw_value_as_str)
        return ~Q(**dc)

    def q_object_for_spatial_operation(self):
        dc = {}
        value_conveted = self.convert_value_for(self.raw_value_as_str)
        dc[self.attribute_name + '__' + self.operation_or_operator] = value_conveted
        return Q(**dc)

    def q_object_operation_or_operator_in_dict(self):
        d = {}
        d['in'] = self.q_object_for_in
        d['eq'] = self.q_object_for_eq
        d['neq'] = self.q_object_for_neq
        d['between'] = self.q_object_for_between
        d['*in'] = self.q_object_for_in
        d['*eq'] = self.q_object_for_eq
        d['*neq'] = self.q_object_for_neq
        d['*between'] = self.q_object_for_between

        return d.get(self.operation_or_operator, self.q_object_for_spatial_operation)

    def q_object(self):
        object_method = self.q_object_operation_or_operator_in_dict()
        return object_method()

class FactoryComplexQuery:
    _instance = None
    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(FactoryComplexQuery, cls).__new__(cls, *args, **kwargs)
        return cls._instance

    def fields(self, model_class):
        return model_class._meta.fields

    def field_names(self, mode_class):
        return [field.name for field in self.fields(mode_class)]

    def base_operators(self):
        return boolean_operator()

    def logical_operators(self):
        return logical_operator()

    def is_attribute(self, att_name, model_class):
        return att_name in self.field_names(model_class)

    def is_logical_operator(self, op):
       return op.lower() in self.logical_operators()


    def q_object_with_logical_operator(self, q_object_expression_or_none, q_object, logical_operator_str):
        if q_object_expression_or_none is None:
            return q_object
        exp = (q_object_expression_or_none & q_object) if logical_operator_str.lower() in ['and', '*and'] else (q_object_expression_or_none | q_object)
        return exp

    def q_object_for_filter_expression(self, q_object_or_none, model_class, expression_as_array):
        #'sigla/in/rj,es,go/and/data/between/2017-02-01,2017-06-30/' = ['sigla','in','rj,es,go','and','data', 'between','2017-02-01,2017-06-30']
        if '' in expression_as_array:
            expression_as_array.remove('')

        if len(expression_as_array)  == 2 and expression_as_array[1].lower() in ['isnull', 'isnotnull']:
            boolean = expression_as_array[1].lower() == 'isnull'
            expression_as_array[1] = 'isnull'
            expression_as_array.append(boolean)

        if len(expression_as_array)  < 3:
            return q_object_or_none
        oper = expression_as_array[0]
        if self.is_logical_operator(oper):
           expression_as_array = expression_as_array[1:]

        if self.is_attribute(expression_as_array[0], model_class):
            qof = QObjectFactory(model_class, expression_as_array[0], expression_as_array[1], expression_as_array[2])
            #oper = qof.operation_or_operator
        else:
            if len(expression_as_array) > 3:
                qof = QObjectFactory(model_class, expression_as_array[1], expression_as_array[2], expression_as_array[3])
            else:
                qof = QObjectFactory(model_class, expression_as_array[0], expression_as_array[1],
                                     expression_as_array[2])
            oper = expression_as_array[0]

        q_object_expression = self.q_object_with_logical_operator(q_object_or_none, qof.q_object(), oper)

        return self.q_object_for_filter_expression(q_object_expression, model_class, expression_as_array[3:])

    def q_object_for_spatial_expression(self, q_object_or_none, model_class, expression_as_array):
        #'geom/within/Polygon(10,10, 30, 30, 40, 40 , 10 10)/and/data/between/2017-02-01,2017-06-30/' = ['sigla','in','rj,es,go','and','data', 'between','2017-02-01,2017-06-30']
        if len(expression_as_array)  < 3:
            return q_object_or_none

        if self.is_attribute(expression_as_array[0], model_class):
            qof = QObjectFactory(model_class, expression_as_array[0], expression_as_array[1], expression_as_array[2])
            oper = qof.operation_or_operator
        else:
            qof = QObjectFactory(model_class, expression_as_array[1], expression_as_array[2], expression_as_array[3])
            oper = expression_as_array[0]

        q_object_expression = self.q_object_with_logical_operator(q_object_or_none, qof.q_object(), oper)

        return self.q_object_for_filter_expression(q_object_expression, model_class, expression_as_array[3:])

# To execute in python console
#dir(ie20.rast)
#arr = ['bands', 'destructor', 'driver', 'extent', ...]
#s = [ ("self." + i + "_operation_name = " + "'" + i + "'" ) for i in arr]
#d = [ ("d[self." + i + "_operation_name] = Type_Called(" + "'" + i + "'" + ", [], object)" ) for i in arr]

class BaseOperationController(object):

    _instance = None
    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = object.__new__(cls, *args, **kwargs)
            cls._instance.initialize()
        return cls._instance

    def __init__(self):
        #super(BaseOperationController, self).__init__()
        self.initialize()

    #Have to be overrided
    def initialize(self):
        self.area_operation_name = 'area'
        self.boundary_operation_name = 'boundary'
        self.buffer_operation_name = 'buffer'
        self.centroid_operation_name = 'centroid'
        self.contains_operation_name = 'contains'
        self.convex_hull_operation_name = 'convex_hull'
        self.coord_seq_operation_name = 'coord_seq'
        self.coords_operation_name = 'coords'
        self.count_operation_name = 'count'
        self.crosses_operation_name = 'crosses'
        self.crs_operation_name = 'crs'
        self.difference_operation_name = 'difference'
        self.dims_operation_name = 'dims'
        self.disjoint_operation_name = 'disjoint'
        self.distance_operation_name = 'distance'
        self.empty_operation_name = 'empty'
        self.envelope_operation_name = 'envelope'
        self.equals_operation_name = 'equals'
        self.equals_exact_operation_name = 'equals_exact'
        self.ewkb_operation_name = 'ewkb'
        self.ewkt_operation_name = 'ewkt'
        self.extend_operation_name = 'extend'
        self.extent_operation_name = 'extent'
        self.geojson_operation_name = 'geojson'
        self.geom_type_operation_name = 'geom_type'
        self.geom_typeid_operation_name = 'geom_typeid'
        self.get_coords_operation_name = 'get_coords'
        self.get_srid_operation_name = 'get_srid'
        self.get_x_operation_name = 'get_x'
        self.get_y_operation_name = 'get_y'
        self.get_z_operation_name = 'get_z'
        self.has_cs_operation_name = 'has_cs'
        self.hasz_operation_name = 'hasz'
        self.hex_operation_name = 'hex'
        self.hexewkb_operation_name = 'hexewkb'
        self.index_operation_name = 'index'
        self.intersection_operation_name = 'intersection'
        self.intersects_operation_name = 'intersects'
        self.interpolate_operation_name = 'interpolate'
        self.json_operation_name = 'json'
        self.kml_operation_name = 'kml'
        self.length_operation_name = 'length'
        self.normalize_operation_name = 'normalize'
        self.num_coords_operation_name = 'num_coords'
        self.num_geom_operation_name = 'num_geom'
        self.num_points_operation_name = 'num_points'
        self.ogr_operation_name = 'ogr'
        self.overlaps_operation_name = 'overlaps'
        self.point_on_surface_operation_name = 'point_on_surface'
        self.relate_operation_name ='relate'
        self.relate_pattern_operation_name = 'relate_pattern'
        self.ring_operation_name = 'ring'
        #self.set_coords_operation_name = 'set_coords'
        #self.set_srid_operation_name = 'set_srid'
        #self.set_x_operation_name = 'set_x'
        #self.set_y_operation_name = 'set_y'
        #self.set_z_operation_name = 'set_z'
        self.simple_operation_name = 'simple'
        self.simplify_operation_name = 'simplify'
        self.srid_operation_name = 'srid'
        self.srs_operation_name = 'srs'
        self.sym_difference_operation_name = 'sym_difference'
        self.touches_operation_name = 'touches'
        self.transform_operation_name = 'transform'
        self.union_operation_name = 'union'
        self.valid_operation_name = 'valid'
        self.valid_reason_operation_name = 'valid_reason'
        self.within_operation_name = 'within'
        self.wkb_operation_name = 'wkb'
        self.wkt_operation_name = 'wkt'
        self.x_operation_name = 'x'
        self.y_operation_name = 'y'
        self.z_operation_name = 'z'
        self.join_operation_name = 'join'
        self.projection_operation_name = 'projection'

    '''
    def user_friendly_resource_type_dict(self):
        return {
            'str': 'Text',
            str: 'Text'
        }
    '''

    #Spatial Operations
    def geometry_operations_dict(self):
        dic = {}
        if len(dic) == 0:
            dic[self.area_operation_name] = Type_Called('area', [], float)
            dic[self.boundary_operation_name] = Type_Called('boundary', [], GEOSGeometry)
            dic[self.buffer_operation_name] = Type_Called('buffer', [float], GEOSGeometry)
            dic[self.centroid_operation_name] = Type_Called('centroid', [], Point)
            dic[self.contains_operation_name] = Type_Called('contains', [GEOSGeometry], bool)
            dic[self.convex_hull_operation_name] = Type_Called('convex_hull', [], Polygon)
            dic[self.coord_seq_operation_name] = Type_Called('coord_seq', [], tuple)
            dic[self.coords_operation_name] = Type_Called('coords', [], tuple)
            dic[self.count_operation_name] = Type_Called('count', [], int)
            dic[self.crosses_operation_name] = Type_Called('crosses', [GEOSGeometry], bool)
            dic[self.crs_operation_name] = Type_Called('crs', [], SpatialReference)
            dic[self.difference_operation_name] = Type_Called('difference', [GEOSGeometry], GEOSGeometry)
            dic[self.dims_operation_name] = Type_Called('dims', [], int)
            dic[self.disjoint_operation_name] = Type_Called('disjoint', [GEOSGeometry], bool)
            dic[self.distance_operation_name] = Type_Called('distance', [GEOSGeometry], float)
            dic[self.empty_operation_name] = Type_Called('empty', [], bool)
            dic[self.envelope_operation_name] = Type_Called('envelope', [], GEOSGeometry)
            dic[self.equals_operation_name] = Type_Called('equals', [GEOSGeometry], bool)
            dic[self.equals_exact_operation_name] = Type_Called('equals_exact', [GEOSGeometry, float], bool)
            dic[self.ewkb_operation_name] = Type_Called('ewkb', [], str)
            dic[self.ewkt_operation_name] = Type_Called('ewkt', [], str)
            dic[self.extend_operation_name] = Type_Called('extend', [], tuple)
            dic[self.extent_operation_name] = Type_Called('extent', [], tuple)
            dic[self.geojson_operation_name] = Type_Called('geojson', [], str)
            dic[self.geom_type_operation_name] = Type_Called('geom_type', [], str)
            dic[self.geom_typeid_operation_name] = Type_Called('geom_typeid', [], int)
            dic[self.get_coords_operation_name] = Type_Called('get_coords', [], tuple)
            dic[self.get_srid_operation_name] = Type_Called('get_srid', [], str)
            dic[self.get_x_operation_name] = Type_Called('get_x', [], str)
            dic[self.get_y_operation_name] = Type_Called('get_y', [], str)
            dic[self.get_z_operation_name] = Type_Called('get_z', [], str)
            dic[self.has_cs_operation_name] = Type_Called('has_cs', [], bool)
            dic[self.hasz_operation_name] = Type_Called('hasz', [], bool)
            dic[self.hex_operation_name] = Type_Called('hex', [], str)
            dic[self.hexewkb_operation_name] = Type_Called('hexewkb', [], str)
            dic[self.index_operation_name] = Type_Called('index', [], int)
            dic[self.intersection_operation_name] = Type_Called('intersection', [GEOSGeometry], GEOSGeometry)
            dic[self.intersects_operation_name] = Type_Called('intersects', [GEOSGeometry], bool)
            dic[self.interpolate_operation_name] = Type_Called('interpolate', [float], Point)
            dic[self.json_operation_name] = Type_Called('json', [], str)
            dic[self.kml_operation_name] = Type_Called('kml', [], str)
            dic[self.length_operation_name] = Type_Called('length', [], float)
            dic[self.normalize_operation_name] = Type_Called('normalize', [float], Point)
            dic[self.num_coords_operation_name] = Type_Called('num_coords', [], int)
            dic[self.num_geom_operation_name] = Type_Called('num_geom', [], int)
            dic[self.num_points_operation_name] = Type_Called('num_points', [], int)
            dic[self.ogr_operation_name] = Type_Called('ogr', [], OGRGeometry)
            dic[self.overlaps_operation_name] = Type_Called('overlaps', [GEOSGeometry], bool)
            dic[self.point_on_surface_operation_name] = Type_Called('point_on_surface', [], Point)
            dic[self.relate_operation_name] = Type_Called('relate', [GEOSGeometry], str)
            dic[self.relate_pattern_operation_name] = Type_Called('relate_pattern', [GEOSGeometry, str], str)
            dic[self.ring_operation_name] = Type_Called('ring', [], bool)
            #dic[self.set_coords_operation_name] = Type_Called('set_coords', [tuple], None)
            #dic[self.set_srid_operation_name] = Type_Called('set_srid', [str], None)
            #dic[self.set_x_operation_name] = Type_Called('set_x', [float], None)
            #dic[self.set_y_operation_name] = Type_Called('set_y', [float], None)
            #dic[self.set_z_operation_name] = Type_Called('set_z', [float], None)
            dic[self.simple_operation_name] = Type_Called('simple', [], bool)
            dic[self.simplify_operation_name] = Type_Called('simplify', [float, bool], GEOSGeometry)
            dic[self.srid_operation_name] = Type_Called('srid', [], int)
            dic[self.srs_operation_name] = Type_Called('srs', [], SpatialReference)
            dic[self.sym_difference_operation_name] = Type_Called('sym_difference', [GEOSGeometry], GEOSGeometry)
            dic[self.touches_operation_name] = Type_Called('touches', [GEOSGeometry], bool)
            dic[self.transform_operation_name] = Type_Called('transform', [int, bool], GEOSGeometry)
            dic[self.union_operation_name] = Type_Called('union', [GEOSGeometry], GEOSGeometry)
            dic[self.valid_operation_name] = Type_Called('valid', [GEOSGeometry], bool)
            dic[self.valid_reason_operation_name] = Type_Called('valid_reason', [GEOSGeometry], str)
            dic[self.within_operation_name] = Type_Called('within', [GEOSGeometry], bool)
            dic[self.wkb_operation_name] = Type_Called('wkb', [], str)
            dic[self.wkt_operation_name] = Type_Called('wkt', [], str)
            dic[self.x_operation_name] = Type_Called('x', [], float)
            dic[self.y_operation_name] = Type_Called('y', [], float)
            dic[self.z_operation_name] = Type_Called('z', [], float)
            dic[self.join_operation_name] = Type_Called('join', [tuple, object], GEOSGeometry)
            dic[self.projection_operation_name] = Type_Called('projection', [property], object)
            # dic['tuple'] = Type_Called('tuple', [], tuple)
            # dic['pop'] = Type_Called('pop', [], tuple)
            # dic['prepared'] = Type_Called('prepared', [], PreparedGeometry)
            return dic

    def point_operations_dict(self):
        dicti = self.geometry_operations_dict()
        return dicti

    def line_operations_dict(self):
        dicti = self.geometry_operations_dict()
        return dicti

    def polygon_operations_dict(self):
        dicti = self.geometry_operations_dict()
        return dicti

    def generic_object_operations_dict(self):
        d = {}
        d["join"] = Type_Called('join', [tuple, object], object)
        d['projection'] = Type_Called('projection', [property], object)
        return d

    def boolean_operations_dict(self):
        d = {}
        return d

    def int_operations_dict(self):
        d = {}
        return d

    def float_operations_dict(self):
        d = {}
        return d

    def date_operations_dict(self):
        d = {}
        return d

    def unicode_operations_dict(self):
        return self.string_operations_dict()

    def string_operations_dict(self):
        d = {}
        d['capitalize'] = Type_Called('capitalize', [], str)
        d['center'] = Type_Called('center', [int], str)
        d['count'] = Type_Called('count', [str], int)
        d['endswith'] = Type_Called('endswith', [str], bool)
        d['find'] = Type_Called('find', [str], int)
        d['isdigit'] = Type_Called('isdigit', [], bool)
        d['isalnum'] = Type_Called('isalnum', [], bool)
        d['isalpha'] = Type_Called('isalpha', [], bool)
        d['islower'] = Type_Called('islower', [], bool)
        d['isupper'] = Type_Called('isupper', [], bool)
        d['lower'] = Type_Called('lower', [], str)
        d['join'] = Type_Called('join', [str], bool)
        d['startswith'] = Type_Called('startswith', [str], bool)
        d['split'] = Type_Called('split', [str], list)
        d['upper'] = Type_Called('upper', [], str)
        return d

    def dict_by_type_geometry_operations_dict(self):

        dicti = {}
        # self.geometry_operation_dict() returns a dict with all geospatial operations
        # the index GEOSGeometry of 'dicti' contains another dict of geospetial operations
        dicti[GEOSGeometry] = self.geometry_operations_dict()
        dicti[Point] = self.point_operations_dict()
        dicti[Polygon] = self.polygon_operations_dict()
        dicti[LineString] = self.line_operations_dict()
        dicti[MultiPoint] = self.point_operations_dict()
        dicti[MultiPolygon] = self.polygon_operations_dict()
        dicti[MultiLineString] = self.line_operations_dict()
        dicti[GeometryCollection] = self.geometry_operations_dict()
        # all indexes above point to a dict returned by geometry_operations_dict(), direct or indirectly
        return dicti

    def dict_by_type_primitive_operations_dict(self):
        d = {}
        d[int]= self.int_operations_dict()
        d[float]= self.float_operations_dict()
        d[date]= self.date_operations_dict()
        d[str]= self.string_operations_dict()

        return d

    def dict_all_operation_dict(self):
        d =  self.dict_by_type_geometry_operations_dict()
        d.update(self.dict_by_type_primitive_operations_dict())
        d.update(self.int_operations_dict())
        d.update(self.float_operations_dict())
        d.update(self.date_operations_dict())
        d.update(self.string_operations_dict())
        d.update(self.geometry_operations_dict())
        d.update(self.generic_object_operations_dict())
        return d

    def is_operation(self, an_object, name):

        # Verify if the received object is a BusinessModel instance
        if isinstance(an_object, BusinessModel):
            # if 'name' represents any operation name of 'an_object' (BusinessModel instance, in this case)
            return an_object.is_operation(name)#return hasattr(an_object, name) and callable(getattr(an_object, name))

        # if 'an_object' isn't a BusinessModel instance, get the object type
        a_type=type(an_object)
        if a_type not in self.dict_all_operation_dict():
            # if the 'an_object' type isn't a key of the dict with all operations, this object hasn't a available operation
            return False

        # if 'an_object' type is one of the all operations dict keys
        # we get the operations dict references to this type
        operation_dict = self.dict_all_operation_dict()[a_type]
        # return True if 'name' is one of the operations dict keys for this type
        return name in operation_dict

    def operation_has_parameters(self, an_object, att_or_method_name):

        if isinstance(an_object, BusinessModel):
            # if 'an_object' is a BusinessModel instance, call BusinessModel.operation_has_parameters()
            # retorna True se a operação/método possuir algum parâmetro além de 'self'
            return an_object.operation_has_parameters(att_or_method_name)
        a_type=type(an_object)

        if isinstance(an_object, GeometryCollection):
            return att_or_method_name in self.dict_all_operation_dict()

        # if 'an_object' type isn't a index of dict of all operations (geometrics and alphanumerics)
        # this is not a available operation
        if a_type not in self.dict_all_operation_dict():
            return False

        # if the previous 'if' is False this means that a_type represents a index o of dict of all operations
        # in this case, we get the operations dict that this type is related
        operation_dict = self.dict_all_operation_dict()[a_type]
        if att_or_method_name in operation_dict:
            # if 'attr_of_method_name' is a index of 'an_object' type operations dict,
            # this means that 'attr_of_method_name' is a operation for 'an_object' type
            # the operation itself is represented by an Type_Called object
            type_called = operation_dict[att_or_method_name]
            # if the list of parameters of this Type_Called has langth bigger than 0, this operations has parameters
            return len(type_called.parameters) > 0
        # if 'attr_of_method_name' doesn't represent a operations of 'an_object' type, return False
        return False

class RasterOperationController(BaseOperationController):
    _instance = None
    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = object.__new__(cls, *args, **kwargs)
            cls._instance.initialize()
        return cls._instance

    '''
    def user_friendly_resource_type_dict(self):
        d = super(RasterOperationController, self).user_friendly_resource_type_dict()
        d.update({
            GDALRaster: "Tiff",
        })
        return d
    '''
    '''
    def get_user_friendly_resource_type_name(self, operation_return_type):
        return self.user_friendly_resource_type_dict()[operation_return_type]
    '''

    def initialize(self):
        self.bands_operation_name = 'bands'
        self.destructor_operation_name = 'destructor'
        self.driver_operation_name = 'driver'
        self.extent_operation_name = 'extent'
        self.geotransform_operation_name = 'geotransform'
        self.height_operation_name = 'height'
        self.info_operation_name = 'info'
        self.metadata_operation_name = 'metadata'
        self.name_operation_name = 'name'
        self.origin_operation_name = 'origin'
        self.ptr_operation_name = 'ptr'
        self.ptr_type_operation_name = 'ptr_type'
        self.scale_operation_name = 'scale'
        self.skew_operation_name = 'skew'
        self.srid_operation_name = 'srid'
        self.srs_operation_name = 'srs'
        self.transform_operation_name = 'transform'
        self.vsi_buffer_operation_name = 'vsi_buffer'
        self.warp_operation_name = 'warp'
        self.width_operation_name = 'width'
        self.join_operation_name = 'join' # DUPLICATED
        self.projection_operation_name = 'projection'# DUPLICATED

    def dict_all_operation_dict(self):
        d = {}
        d[self.bands_operation_name] = Type_Called('bands', [], object)
        d[self.destructor_operation_name] = Type_Called('destructor', [], object)           # not a Raster operation (is Band operation)
        d[self.driver_operation_name] = Type_Called('driver', [], str)                      # DONE
        d[self.extent_operation_name] = Type_Called('extent', [], str)                      # DONE
        d[self.geotransform_operation_name] = Type_Called('geotransform', [], object)       # DONE
        d[self.height_operation_name] = Type_Called('height', [], int)                      # DONE
        d[self.info_operation_name] = Type_Called('info', [], str)                          # DONE
        d[self.metadata_operation_name] = Type_Called('metadata', [], str)                  # DONE
        d[self.name_operation_name] = Type_Called('name', [], str)                          # DONE
        d[self.origin_operation_name] = Type_Called('origin', [], str)                      # DONE
        d[self.ptr_operation_name] = Type_Called('ptr', [], object)                         # not Raster operation (is Band operation)
        d[self.ptr_type_operation_name] = Type_Called('ptr_type', [], object)               # not Raster operation (is Band operation)
        d[self.scale_operation_name] = Type_Called('scale', [], list)                       # DONE
        d[self.skew_operation_name] = Type_Called('skew', [], object)                       # DONE
        d[self.srid_operation_name] = Type_Called('srid', [], int)                          # DONE
        d[self.srs_operation_name] = Type_Called('srs', [], SpatialReference)               # DONE
        d[self.transform_operation_name] = Type_Called('transform', [int], GDALRaster)      # missing 'srid' parameter
        d[self.vsi_buffer_operation_name] = Type_Called('vsi_buffer', [], bytes)            # Encoding error
        d[self.warp_operation_name] = Type_Called('warp', [], object)                       # missing arguments and Raster return type
        d[self.width_operation_name] = Type_Called('width', [], object)                     # DONE
        d[self.projection_operation_name] = Type_Called('projection', [property], object)       # DONE
        return d

class CollectionResourceOperationController(BaseOperationController):
    _instance = None
    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = object.__new__(cls, *args, **kwargs)
            cls._instance.initialize()
        return cls._instance

    def initialize(self):
        #abstract_collection
        self.filter_collection_operation_name = 'filter'
        self.collect_collection_operation_name = 'collect'
        self.count_resource_collection_operation_name = 'count-resource'
        self.offset_limit_collection_operation_name = 'offset-limit'
        self.distinct_collection_operation_name = 'distinct'
        self.group_by_count_collection_operation_name = 'group-by-count'
        self.filter_and_collect_collection_operation_name = 'filter-and-collect'
        self.filter_and_count_resource_collection_operation_name = 'filter-and-count-resource'
        self.offset_limit_and_collect_collection_operation_name = 'offset-limit-and-collect'
        self.join_operation_name = 'join'
        self.group_by_sum_collection_operation_name = "group-by-sum"
        self.projection_operation_name = 'projection'
        self.all_operations_dict = self.collection_operations_dict()

    # operations that return a subcollection of an collection
    def subcollection_operations_dict(self):
        dict = {}
        dict[self.filter_collection_operation_name] = Type_Called(self.filter_collection_operation_name, [Q], object)
        dict[self.offset_limit_collection_operation_name] = Type_Called(self.offset_limit_collection_operation_name, [int, int, list], object)
        dict[self.distinct_collection_operation_name] = Type_Called(self.distinct_collection_operation_name, [property], object)
        dict[self.filter_and_collect_collection_operation_name] = Type_Called(self.filter_and_collect_collection_operation_name, [list], object)
        dict[self.offset_limit_and_collect_collection_operation_name] = Type_Called(self.offset_limit_and_collect_collection_operation_name, [list], object)
        return dict

    def internal_collection_operations_dict(self):
        dict = {}
        dict[self.filter_and_collect_collection_operation_name] = Type_Called(self.filter_and_collect_collection_operation_name, [list], object)
        dict[self.filter_and_count_resource_collection_operation_name] = Type_Called(self.filter_and_count_resource_collection_operation_name, [list], int)
        dict[self.offset_limit_and_collect_collection_operation_name] = Type_Called(self.offset_limit_and_collect_collection_operation_name, [list], object)
        return dict

    def collect_operations_dict(self):
        dict = {}
        dict[self.collect_collection_operation_name] = Type_Called(self.collect_collection_operation_name, [property, 'operation'], object)
        dict[self.filter_and_collect_collection_operation_name] = Type_Called(self.filter_and_collect_collection_operation_name, [list], object)
        dict[self.offset_limit_and_collect_collection_operation_name] = Type_Called(self.offset_limit_and_collect_collection_operation_name, [list], object)
        return dict

        # Abstract collection Operations
    def collection_operations_dict(self):
        dict = {}
        dict[self.filter_collection_operation_name] = Type_Called(self.filter_collection_operation_name, [Q], object)
        dict[self.collect_collection_operation_name] = Type_Called(self.collect_collection_operation_name, [property, 'operation'], object)
        dict[self.count_resource_collection_operation_name] = Type_Called(self.count_resource_collection_operation_name, [], int)
        dict[self.offset_limit_collection_operation_name] = Type_Called(self.offset_limit_collection_operation_name, [int, int], object)
        dict[self.distinct_collection_operation_name] = Type_Called(self.distinct_collection_operation_name, [property], object)
        #dict[self.group_by_collection_operation_name] = Type_Called(self.group_by_collection_operation_name, [list], object)
        dict[self.group_by_count_collection_operation_name] = Type_Called(self.group_by_count_collection_operation_name, [list], object)
        dict[self.group_by_sum_collection_operation_name] = Type_Called(self.group_by_sum_collection_operation_name, [str, str], object)
        #dict[self.spatialize_collection_operation_name] = Type_Called(self.spatialize_collection_operation_name, [tuple, object], GEOSGeometry)
        #dict[self.spatialize_operation_name] = Type_Called(self.spatialize_operation_name, [tuple, object], GEOSGeometry)
        dict[self.projection_operation_name] = Type_Called(self.projection_operation_name, [property], object)
        return dict

    def dict_all_operation_dict(self):
        return self.collection_operations_dict()

    def set_filter_operation_return_type(self, new_filter_return_type):
        self.all_operations_dict[self.filter_collection_operation_name].return_type = new_filter_return_type

    def set_collect_operation_return_type(self, new_collect_return_type):
        self.all_operations_dict[self.collect_collection_operation_name].return_type = new_collect_return_type

    def expression_operator_expects_parameter(self, operator_name):
        return True if len(self.expression_operators_dict()[operator_name].parameters) > 0 else False

    def expression_operators_dict(self):
        d = {}
        d['neq'] = Type_Called('neq', [object], None)
        d['eq'] = Type_Called('eq', [object], None)
        d['lt'] = Type_Called('lt', [object], None)
        d['lte'] = Type_Called('lte', [object], None)
        d['gt'] = Type_Called('gt', [object], None)
        d['gte'] = Type_Called('gte', [object], None)
        d['between'] = Type_Called('between', [object, 'and', object], None)
        d['isnull'] = Type_Called('isnull', [], None)
        d['isnotnull'] = Type_Called('isnotnull', [], None)
        d['like'] = Type_Called('like', [object], None)
        d['notlike'] = Type_Called('notlike', [object], None)
        d['in'] = Type_Called('in', [list], None)
        d['notin'] = Type_Called('notin', [list], None)
        return d

    def expression_logical_operators(self):
        d = {}
        d['and'] = Type_Called('and', [], None)
        d['or'] = Type_Called('or', [], None)
        #d['not'] = Type_Called('not', [], None)
        return d

class SpatialCollectionOperationController(CollectionResourceOperationController):

    _instance = None
    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = object.__new__(cls, *args, **kwargs)
            cls._instance.initialize()
        return cls._instance

    def initialize(self):
        super(SpatialCollectionOperationController, self).initialize()
        self.bbcontaining_operation_name = 'bbcontains'
        self.bboverlaping_operation_name = 'bboverlaps'
        self.contained_operation_name = 'contained'
        self.containing_operation_name = 'contains'
        self.containing_properly_operation_name = 'contains-properly'
        self.covering_by_operation_name = 'covers-by'
        self.covering_operation_name = 'covers'
        self.crossing_operation_name = 'crosses'
        self.disjointing_operation_name = 'disjoint'
        self.intersecting_operation_name = 'intersects'
        self.isvalid_operation_name = 'isvalid'
        self.overlaping_operation_name = 'overlaps'
        self.relating_operation_name = 'relate'
        self.touching_operation_name = 'touches'
        self.within_operation_name = 'within'
        self.on_left_operation_name = 'left'
        self.on_right_operation_name = 'right'
        self.overlaping_left_operation_name = 'overlaps-left'
        self.overlaping_right_operation_name = 'overlaps-right'
        self.overlaping_above_operation_name = 'overlaps-above'
        self.overlaping_below_operation_name = 'overlaps-below'
        self.strictly_above_operation_name = 'strictly-above'
        self.strictly_below_operation_name = 'strictly-below'
        self.distance_gt_operation_name = 'distance-gt'
        self.distance_gte_operation_name = 'distance-gte'
        self.distance_lt_operation_name = 'distance-lt'
        self.distance_lte_operation_name = 'distance-lte'
        self.dwithin_operation_name = 'dwithin'

        self.union_collection_operation_name = 'union'
        self.extent_collection_operation_name = 'extent'
        self.make_line_collection_operation_name = 'make-line'

    #Abstract spatial collection Operations
    def spatial_collection_operations_dict(self):
        d = {}
        d[self.bbcontaining_operation_name] = Type_Called(self.bbcontaining_operation_name, [GEOSGeometry], GEOSGeometry)
        d[self.bboverlaping_operation_name] = Type_Called(self.bboverlaping_operation_name, [GEOSGeometry], GEOSGeometry)
        d[self.contained_operation_name]  = Type_Called(self.contained_operation_name, [GEOSGeometry], GEOSGeometry)
        d[self.containing_operation_name]  = Type_Called(self.containing_operation_name, [GEOSGeometry], GEOSGeometry)
        d[self.containing_properly_operation_name] = Type_Called(self.containing_properly_operation_name, [GEOSGeometry], GEOSGeometry)
        d[self.covering_by_operation_name] = Type_Called(self.covering_by_operation_name, [GEOSGeometry], GEOSGeometry)
        d[self.covering_operation_name]= Type_Called(self.covering_operation_name, [GEOSGeometry], GEOSGeometry)
        d[self.crossing_operation_name] = Type_Called(self.crossing_operation_name, [GEOSGeometry], GEOSGeometry)
        d[self.disjointing_operation_name]= Type_Called(self.disjointing_operation_name, [GEOSGeometry], GEOSGeometry)
        d[self.intersecting_operation_name]  = Type_Called(self.intersecting_operation_name, [GEOSGeometry], GEOSGeometry)
        d[self.isvalid_operation_name]  = Type_Called(self.isvalid_operation_name, [GEOSGeometry], GEOSGeometry)
        d[self.overlaping_operation_name] = Type_Called(self.overlaping_operation_name, [GEOSGeometry], GEOSGeometry)
        d[self.relating_operation_name] = Type_Called(self.relating_operation_name, [tuple], GEOSGeometry)
        d[self.touching_operation_name] = Type_Called(self.touching_operation_name, [GEOSGeometry], GEOSGeometry)
        d[self.within_operation_name] = Type_Called(self.within_operation_name, [GEOSGeometry], GEOSGeometry)
        d[self.on_left_operation_name] = Type_Called(self.on_left_operation_name, [GEOSGeometry], GEOSGeometry)
        d[self.on_right_operation_name] = Type_Called(self.on_right_operation_name, [GEOSGeometry], GEOSGeometry)
        d[self.overlaping_left_operation_name]  = Type_Called(self.overlaping_left_operation_name, [GEOSGeometry], GEOSGeometry)
        d[self.overlaping_right_operation_name] = Type_Called(self.overlaping_right_operation_name, [GEOSGeometry], GEOSGeometry)
        d[self.overlaping_above_operation_name] = Type_Called(self.overlaping_above_operation_name, [GEOSGeometry], GEOSGeometry)
        d[self.overlaping_below_operation_name] = Type_Called(self.overlaping_below_operation_name, [GEOSGeometry], GEOSGeometry)
        d[self.strictly_above_operation_name] = Type_Called(self.strictly_above_operation_name, [GEOSGeometry], GEOSGeometry)
        d[self.strictly_below_operation_name] = Type_Called(self.strictly_below_operation_name, [GEOSGeometry], GEOSGeometry)
        d[self.distance_gt_operation_name] = Type_Called(self.distance_gt_operation_name, [GEOSGeometry], GEOSGeometry)
        d[self.distance_gte_operation_name] = Type_Called(self.distance_gte_operation_name, [GEOSGeometry], GEOSGeometry)
        d[self.distance_lt_operation_name] = Type_Called(self.distance_lt_operation_name, [GEOSGeometry], GEOSGeometry)
        d[self.distance_lte_operation_name] = Type_Called(self.distance_lte_operation_name, [GEOSGeometry], GEOSGeometry)
        d[self.dwithin_operation_name] = Type_Called(self.dwithin_operation_name, [GEOSGeometry], bool)

        d[self.union_collection_operation_name] = Type_Called(self.union_collection_operation_name, [GEOSGeometry], GEOSGeometry)
        d[self.extent_collection_operation_name] = Type_Called(self.extent_collection_operation_name, [GEOSGeometry], tuple)
        d[self.make_line_collection_operation_name] = Type_Called(self.make_line_collection_operation_name, [GEOSGeometry], GEOSGeometry)
        d[self.join_operation_name] = Type_Called(self.join_operation_name, [tuple, object], GEOSGeometry)
        d[self.projection_operation_name] = Type_Called(self.projection_operation_name, [property], object)

        return d

    def feature_collection_operations_dict(self):
        return dict(self.collection_operations_dict(), **self.spatial_collection_operations_dict())

    def feature_collection_operations_names(self):
        return self.feature_collection_operations_dict().keys()

    #Responds a dict with all the operations
    def dict_all_operation_dict(self):
       return self.feature_collection_operations_dict()

    def is_operation(self, an_object, name):
      if isinstance(an_object, BusinessModel):
         return an_object.is_operation(name)

      if isinstance(an_object, GeometryCollection):
          return name in self.dict_all_operation_dict()

      a_type=type(an_object)

      if a_type not in self.dict_all_operation_dict():
         return False

      operation_dict = self.dict_all_operation_dict()[a_type]
      return name in operation_dict

    def expression_operators_dict(self):
        d = super(SpatialCollectionOperationController, self).expression_operators_dict()
        d.update({
            self.bbcontaining_operation_name:       Type_Called(self.bbcontaining_operation_name, [GEOSGeometry], None),
            self.bboverlaping_operation_name:       Type_Called(self.bboverlaping_operation_name, [GEOSGeometry], None),
            self.contained_operation_name:          Type_Called(self.contained_operation_name, [GEOSGeometry], None),
            self.containing_operation_name:         Type_Called(self.containing_operation_name, [GEOSGeometry], None),
            self.containing_properly_operation_name:Type_Called(self.containing_properly_operation_name, [GEOSGeometry], None),
            self.covering_by_operation_name:        Type_Called(self.covering_by_operation_name, [GEOSGeometry], None),
            self.covering_operation_name:           Type_Called(self.covering_operation_name, [GEOSGeometry], None),
            self.crossing_operation_name:           Type_Called(self.crossing_operation_name, [GEOSGeometry], None),
            self.disjointing_operation_name:        Type_Called(self.disjointing_operation_name, [GEOSGeometry], None),
            self.intersecting_operation_name:       Type_Called(self.intersecting_operation_name, [GEOSGeometry], None),
            self.isvalid_operation_name:            Type_Called(self.isvalid_operation_name, [GEOSGeometry], None),
            self.overlaping_operation_name:         Type_Called(self.overlaping_operation_name, [GEOSGeometry], None),
            self.relating_operation_name:           Type_Called(self.relating_operation_name, [GEOSGeometry], None),
            self.touching_operation_name:           Type_Called(self.touching_operation_name, [GEOSGeometry], None),
            self.within_operation_name:             Type_Called(self.within_operation_name, [GEOSGeometry], None),
            self.on_left_operation_name:            Type_Called(self.on_left_operation_name, [GEOSGeometry], None),
            self.on_right_operation_name:           Type_Called(self.on_right_operation_name, [GEOSGeometry], None),
            self.overlaping_left_operation_name:    Type_Called(self.overlaping_left_operation_name, [GEOSGeometry], None),
            self.overlaping_right_operation_name:   Type_Called(self.overlaping_right_operation_name, [GEOSGeometry], None),
            self.overlaping_above_operation_name:   Type_Called(self.overlaping_above_operation_name, [GEOSGeometry], None),
            self.overlaping_below_operation_name:   Type_Called(self.overlaping_below_operation_name, [GEOSGeometry], None),
            self.strictly_above_operation_name:     Type_Called(self.strictly_above_operation_name, [GEOSGeometry], None),
            self.strictly_below_operation_name:     Type_Called(self.strictly_below_operation_name, [GEOSGeometry], None),
            self.distance_gt_operation_name:        Type_Called(self.distance_gt_operation_name, [GEOSGeometry], None),
            self.distance_gte_operation_name:       Type_Called(self.distance_gte_operation_name, [GEOSGeometry], None),
            self.distance_lt_operation_name:        Type_Called(self.distance_lt_operation_name, [GEOSGeometry], None),
            self.distance_lte_operation_name:       Type_Called(self.distance_lte_operation_name, [GEOSGeometry], None),
            self.dwithin_operation_name:            Type_Called(self.dwithin_operation_name, [GEOSGeometry], None)
        })
        return d

class EntryPointResourceOperationController(CollectionResourceOperationController):
    _instance = None
    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = object.__new__(cls, *args, **kwargs)
            cls._instance.initialize()
        return cls._instance

    def initialize(self):
        self.filter_collection_operation_name = 'filter'
        self.collect_collection_operation_name = 'collect'
        self.count_resource_collection_operation_name = 'count-resource'
        self.offset_limit_collection_operation_name = 'offset-limit'
        self.projection_operation_name = 'projection'

    def collection_operations_dict(self):
        dict = {}
        dict[self.filter_collection_operation_name] = Type_Called(self.filter_collection_operation_name, [Q], object)
        dict[self.collect_collection_operation_name] = Type_Called(self.collect_collection_operation_name, [property, 'operation'], object)
        dict[self.count_resource_collection_operation_name] = Type_Called(self.count_resource_collection_operation_name, [], int)
        dict[self.offset_limit_collection_operation_name] = Type_Called(self.offset_limit_collection_operation_name, [int, int], object)
        dict[self.projection_operation_name] = Type_Called(self.projection_operation_name, [property], object)
        return dict

class BusinessModel(models.Model):
    class Meta:
        abstract = True

    def id(self):
        return self.pk

    def name_string(self):
        return self.__str__()

    def attribute_primary_key(self):
        return self.serializer_class.Meta.identifier

    def model_class(self):
        return type(self)

    def model_class_name(self):
        return self._meta.model_name

    def _key_is_identifier(self, key):
        return key in self.serializer_class.Meta.identifiers

    def dic_with_only_identitier_field(self, dict_params):
        dic = dict_params.copy()
        a_dict = {}
        for key, value in dic.items():
            if self._key_is_identifier(key):
                a_dict[key] = value
        return a_dict

    def all_operation_name_and_value(self):
        return inspect.getmembers(self, inspect.ismethod)

    def all_operation_name_and_args_length(self):
        return [(name, len( inspect.getargspec(method).args)) for name, method in self.all_operation_name_and_value()]

    def public_operations_name_and_value(self):
        return [(name, value) for name, value in self.all_operation_name_and_value() if not name.startwith('_')]

    def operation_names(self):
        return [ name for name, value in self.all_operation_name_and_value() ]

    def public_operation_names(self):
        return [ name for name, value in self.public_operations_name_and_value() ]

    def operation_has_parameters(self, att_or_method_name):
        return next((True for name, len_args in self.all_operation_name_and_args_length() if name == att_or_method_name and len_args > 1), False)

    def attribute_names(self):
        return [ attribute for attribute in dir(self) if not callable(getattr(self, attribute)) and self.is_not_private(attribute)]

    def fields(self):
        return self.model_class()._meta.fields

    def field_names(self):
        return [field.name for field in self.fields()]

    def is_private(self, attribute_or_method_name):
        return attribute_or_method_name.startswith('__') and attribute_or_method_name.endswith('__')

    def is_not_private(self, attribute_or_method_name):
        return not self.is_private(attribute_or_method_name)

    def is_operation(self, operation_name):
        return operation_name in self.operation_names()

    def is_public_operations(self, operation_name):
        return operation_name in self.public_operation_names()

    def is_attribute(self, attribute_name):
        return (attribute_name in dir(self) and not callable(getattr(self, attribute_name, None)))

    def operations_with_parameters_type(self):
        return {}

    def serializer_class(self, a_model_class_name):
        return self.class_for_name('serializers', a_model_class_name + 'Serializer')

    def class_for_name(self, module_name, class_name):
        # load the module, will raise ImportError if module cannot be loaded
        m = importlib.import_module(module_name)
        # get the class, will raise AttributeError if class cannot be found
        c = getattr(m, class_name)
        return c

    def table_name(self):
        return self.__class__.objects.model._meta.db_table

    def pk_name(self):
        return self.__class__.objects.model._meta.pk.name

class SpatialModel(BusinessModel):
    spatial_object = None

    class Meta:
        abstract = True

    #@abstractmethod #Must be overrided
    def get_geospatial_type(self):
        return None

    def geo_field(self):
        return [field for field in self.fields() if isinstance(field, self.get_geospatial_type())][0]

    def geo_field_name(self):
        return self.geo_field().name

    def get_spatial_object(self):
        """
        Returns SpatialObject(Raster for raster object and Gemetry for feature.
        """
        if self.spatial_object == None:
            # FeatureModel.geo_field_name() returns the name of geometric field of FeatureModel instance
            # getattr() gets the value of this geometric field (that is a geometric object containing geometric coordinates)
            self.spatial_object = getattr(self, self.geo_field_name(), None)
        return self.spatial_object

    def srs(self):
        #Responds the spatial reference system of the spatial object, as a SpatialReference instance.
        return self.get_spatial_object().srs

    def extent(self):
        #Responds the extent (boundary values) of the spatial object, as a 4-tuple (xmin, ymin, xmax, ymax) in the spatial reference system of the source.
        return self.get_spatial_object().extent

    def srid(self):
        #Responds the Spatial Reference System Identifier (SRID) of the spatial object.
        return self.get_spatial_object().srid

class FeatureModel(SpatialModel):

    class Meta:
        abstract = True

    def get_geospatial_type(self):
        return GeometryField

    def _get_type_geometry_object(self):
        geo_object = self.get_spatial_object()
        if geo_object is None:
            return None
        return type(geo_object)

    def get_geometry_type(self):
        geoType = self._get_type_geometry_object()
        return geoType if geoType is not None else dict_map_geo_field_geometry()[type(self.geo_field())]

    def operations_with_parameters_type(self):
        oc = BaseOperationController()
        return oc.dict_by_type_geometry_operations_dict()[self.get_geometry_type()]

    def centroid(self):
        return self.get_spatial_object().centroid

    def ring(self):
        return self.get_spatial_object().ring

    def crs(self):
        return self.get_spatial_object().crs

    def wkt(self):
        return self.get_spatial_object().wkt

    def hexewkb(self):
        return self.get_spatial_object().hexewkb

    def equals_exact(self, other_GEOSGeometry, tolerance=0):
        return self.get_spatial_object().equals_exact(other_GEOSGeometry, tolerance)

    def set_srid(self, a_srid):
        return self.get_spatial_object().set_srid(a_srid)

    def hex(self):
        return self.get_spatial_object().hex

    def has_cs(self):
        return self.get_spatial_object().has_cs

    def area(self):
        return self.get_spatial_object().area

    def wkb(self):
        return self.get_spatial_object().wkb

    def geojson(self):
        return self.get_spatial_object().geojson

    def relate(self, other_GEOSGeometry):
        return self.get_spatial_object().relate(other_GEOSGeometry)

    def set_coords(self, coords):
        return self.get_spatial_object().set_coords(coords)

    def simple(self):
        return self.get_spatial_object().simple

    def geom_type(self):
        return self.get_spatial_object().geom_type

    def set_y(self, y):
        return self.get_spatial_object().set_y(y)

    def normalize(self):
        return self.get_spatial_object().normalize

    def sym_difference(self, other_GEOSGeometry):
        return self.get_spatial_object().sym_difference(other_GEOSGeometry)

    def valid_reason(self):
        return self.get_spatial_object().valid_reason

    def geom_typeid(self):
        return self.get_spatial_object().geom_typeid

    def valid(self):
        return self.get_spatial_object().valid

    def ogr(self):
        return self.get_spatial_object().ogr

    def coords(self):
        return self.get_spatial_object().coords

    def num_coords(self):
        return self.get_spatial_object().num_coords

    def get_srid(self):
        return self.get_spatial_object().get_srid

    def distance(self, other_GEOSGeometry):
        return self.get_spatial_object().distance(other_GEOSGeometry)

    def json(self):
        return self.get_spatial_object().json

    def pop(self):
        return self.get_spatial_object().pop

    def ewkb(self):
        return self.get_spatial_object().ewkb

    def x(self):
        return self.get_spatial_object().x

    def simplify(self, tolerance=0.0, preserve_topology=False):
        return self.get_spatial_object().simplify(tolerance, preserve_topology)

    def set_z(self):
        return self.get_spatial_object().set_z

    def buffer(self, width, quadsegs=8):
        return self.get_spatial_object().buffer(width, quadsegs)

    def relate_pattern(self, other_GEOSGeometry, pattern):
        return self.get_spatial_object().relate_pattern(other_GEOSGeometry, pattern)

    def z(self):
        return self.get_spatial_object().z

    def num_geom(self):
        return self.get_spatial_object().num_geom

    def coord_seq(self):
        return self.get_spatial_object().coord_seq

    def dims(self):
        return self.get_spatial_object().dims

    def get_y(self):
        return self.get_spatial_object().get_y

    def tuple(self):
        return self.get_spatial_object().tuple

    def y(self):
        return self.get_spatial_object().y

    def convex_hull(self):
        return self.get_spatial_object().convex_hull

    def get_x(self):
        return self.get_spatial_object().get_x

    def index(self):
        return self.get_spatial_object().index

    def boundary(self):
        return self.get_spatial_object().boundary

    def kml(self):
        return self.get_spatial_object().kml

    def touches(self, other_GEOSGeometry):
        return self.get_spatial_object().touches(other_GEOSGeometry)

    def empty(self):
        return self.get_spatial_object().empty

    def get_z(self):
        return self.get_spatial_object().get_z

    def extent(self):
        return self.get_spatial_object().extent

    def union(self, other_GEOSGeometry):
        return self.get_spatial_object().union(other_GEOSGeometry)

    def intersects(self, other_GEOSGeometry):
        return self.get_spatial_object().intersects(other_GEOSGeometry)

    def contains(self, other_GEOSGeometry):
        return self.get_spatial_object().contains(other_GEOSGeometry)

    def hasz(self):
        return self.get_spatial_object().hasz

    def crosses(self, other_GEOSGeometry):
        return self.get_spatial_object().crosses(other_GEOSGeometry)

    def count(self):
        return self.get_spatial_object().count

    def num_points(self):
        return self.get_spatial_object().num_points

    def within(self, other_GEOSGeometry):
        return self.get_spatial_object().within(other_GEOSGeometry)

    def intersection(self, other_GEOSGeometry):
        return self.get_spatial_object().intersection(other_GEOSGeometry)

    def overlaps(self, other_GEOSGeometry):
        return self.get_spatial_object().overlaps(other_GEOSGeometry)

    def equals(self, other_GeosGeometry):
        return self.get_spatial_object().equals(other_GeosGeometry)

    def point_on_surface(self):
        return self.get_spatial_object().point_on_surface

    def difference(self, other_GEOSGeometry):
        return self.get_spatial_object().difference(other_GEOSGeometry)

    def set_x(self, x):
        return self.get_spatial_object().set_x(x)

    def get_coords(self):
        return self.get_spatial_object().get_coords

    def envelope(self):
        return self.get_spatial_object().envelope

    def prepared(self):
        return self.get_spatial_object().prepared

    def ewkt(self):
        return self.get_spatial_object().ewkt

    def length(self):
        return self.get_spatial_object().length

    def disjoint(self, other_GEOSGeometry):
        return self.get_spatial_object().disjoint(other_GEOSGeometry)

    def transform(self, srid, clone=True):
        return self.get_spatial_object().transform(srid, clone=True)

class RasterModel(SpatialModel):
    class Meta:
        abstract = True

    def get_geospatial_type(self):
        #Responds the type of the spatial field
        return RasterField

    def driver(self):
        "Responds to the name of the GDAL driver used to handle the input file"
        return self.get_spatial_object().driver.name

    def bands(self):
        #Responds a list of all bands of the source, as GDALBand instances.
        return self.get_spatial_object().bands

    def geotransform(self):
        """Responds a List of affine transformation matrix used to georeference the source, as a tuple of six coefficients
        which map pixel/line coordinates into georeferenced space.
        """
        return self.get_spatial_object().geotransform

    def height(self):
        #responds the height of the source in pixels (X-axis).
        return self.get_spatial_object().height

    def origin(self):
        #Responds a Coordinates of the top left origin of the raster in the spatial reference system of the source as a point object with x and y members.
        return self.get_spatial_object().origin

    def scale(self):
       #Responds a Pixel width and height used for georeferencing the raster, as a as a point object with x and y members.
        return self.get_spatial_object().scale

    def skew(self):
        #Responds the Skew coefficients used to georeference the raster, as a point object with x and y members. In case of north up images, these coefficients are both 0.
        return self.get_spatial_object().skew

    def transform(self, srid, driver=None, name=None, resampling='NearestNeighbour', max_error=0.0):
        #Returns a transformed version of this raster with the specified SRID.
        # This function transforms the current raster into a new spatial reference system that can be specified with an srid.
        return self.get_spatial_object().transform(srid, driver, name, resampling, max_error)

    def warp(self, ds_input, resampling='NearestNeighbour', max_error=0.0):
        #Responds a warped version of this raster.
        return self.get_spatial_object().warp(ds_input, resampling, max_error)

    def width(self):
        #responds the width of the source in pixels (X-axis).
        return self.get_spatial_object().width

    def vsi_buffer(self):
        return self.get_spatial_object().vsi_buffer

    def info(self):
        "Returns a string with a summary of the raster."
        return self.get_spatial_object().info

    def metadata(self):
        "Returns a string with a summary of the raster."
        return self.get_spatial_object().metadata

    def name(self):
        return self.get_spatial_object().name

class TiffModel(RasterModel):
    class Meta:
        abstract = True