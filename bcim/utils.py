import json

import ast
import re
import requests
import random
from django.contrib.gis.gdal.geometries import Point, Polygon, OGRGeometry
from django.contrib.gis.gdal import SpatialReference
from django.contrib.gis.geos.prepared import PreparedGeometry
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from requests.exceptions import HTTPError, ConnectionError
from rest_framework import permissions

from rest_framework.negotiation import BaseContentNegotiation

from django.contrib.gis.geos import GeometryCollection, GEOSGeometry

from context_api.views import *

#from image_generator.img_generator import BuilderPNG

from .serializers import  serializers_dict

class IgnoreClientContentNegotiation(BaseContentNegotiation):
    def select_parser(self, request, parsers):
        """
        Select the first parser in the `.parser_classes` list.
        """
        return parsers[0]

    def select_renderer(self, request, renderers, format_suffix):
        """
        Select the first renderer in the `.renderer_classes` list.
        """
        return (renderers[0], renderers[0].media_type)

class JSONResponse(HttpResponse):
    """
    An HttpResponse that renders its content into JSON.
    """
    def __init__(self, data, **kwargs):
        kwargs['content_type'] = 'application/json'
        super(JSONResponse, self).__init__(data, **kwargs)

class DefaultsMixin(object):
    permission_classes = (
        permissions.IsAuthenticatedOrReadOnly,
    )

    # paginate_by = 250
    #
    # Default settings for view authentication, permissions, filtering and pagination.

    # authentication_classes = (
    #     authentication.BasicAuthentication,
    #     authentication.TokenAuthentication,
    # )

class Type_Called():
    def __init__(self, a_name, params, answer):
        self.name = a_name
        self.parameters = params
        self.return_type = answer

    def description(self):
        param = self.parameters or []
        return "operation name:" + self.name + " " + "parameters:" + ",".join(param) + " " + "returned value:" + self.return_type

class FeatureModel(models.Model):

    def __init__(self, a_hyperlink):
        self.hyperlink = a_hyperlink
        self.dic = {}

    def centroid(self):
       return self.geom.centroid

    def ring(self):
        return self.geom.ring

    def crs(self):
        return self.geom.crs

    def wkt(self):
        return self.geom.wkt

    def srs(self):
        return self.geom.srs

    def hexewkb(self):
        return self.geom.hexewkb

    def equals_exact(self, other_GEOSGeometry, tolerance=0):
        return self.geom.equals_exact(other_GEOSGeometry, tolerance)

    def set_srid(self, a_srid):
        return self.geom.set_srid(a_srid)

    def hex(self):
        return self.geom.hex

    def has_cs(self):
        return self.geom.has_cs

    def area(self):
        return self.geom.area

    def extend(self):
        return self.geom.extend

    def wkb(self):
        return self.geom.wkb

    def geojson(self):
        return self.geom.geojson

    def relate(self, other_GEOSGeometry, pattern):
        return self.geom.relate(other_GEOSGeometry, pattern)

    def set_coords(self, coords):
        return self.geom.set_coords(coords)

    def simple(self):
        return self.geom.simple

    def geom_type(self):
        return self.geom.geom_type

    def set_y(self, y):
        return self.geom.set_y(y)

    def normalize(self):
        return self.geom.normalize

    def sym_difference(self, other_GEOSGeometry):
        return self.geom.sym_difference(other_GEOSGeometry)

    def valid_reason(self):
        return self.geom.valid_reason

    def geom_typeid(self):
        return self.geom.geom_typeid

    def valid(self):
        return self.geom.valid

    def ogr(self):
        return self.geom.ogr

    def coords(self):
        return self.geom.coords

    def num_coords(self):
        return self.geom.num_coords

    def get_srid(self):
        return self.geom.get_srid

    def distance(self, other_GEOSGeometry):
        return self.geom.distance(other_GEOSGeometry)

    def json(self):
        return self.geom.json

    def pop(self):
        return self.geom.pop

    def ewkb(self):
        return self.geom.ewkb

    def x(self):
        return self.geom.x

    def simplify(self, tolerance=0.0, preserve_topology=False):
        return self.geom.simplify(tolerance=0.0, preserve_topology=False)

    def set_z(self):
        return self.geom.set_z

    def buffer(self, width, quadsegs=8):
        return self.geom.buffer(width, quadsegs)

    def relate_pattern(self, other_GEOSGeometry, pattern):
        return self.geom.relate_pattern(other_GEOSGeometry, pattern)

    def z(self):
        return self.geom.z

    def num_geom(self):
        return self.geom.num_geom

    def coord_seq(self):
        return self.geom.coord_seq

    def dims(self):
        return self.geom.dims

    def get_y(self):
        return self.geom.get_y

    def tuple(self):
        return self.geom.tuple

    def y(self):
        return self.geom.y

    def convex_hull(self):
        return self.geom.convex_hull

    def get_x(self):
        return self.geom.get_x

    def index(self):
        return self.geom.index

    def boundary(self):
        return self.geom.boundary

    def kml(self):
        return self.geom.kml

    def touches(self, other_GEOSGeometry):
        return self.geom.touches(other_GEOSGeometry)

    def empty(self):
        return self.geom.empty

    def srid(self):
        return self.geom.srid

    def get_z(self):
        return self.geom.get_z

    def extent(self):
        return self.geom.extent

    def union(self, other_GEOSGeometry):
        return self.geom.union(other_GEOSGeometry)

    def intersects(self, other_GEOSGeometry):
        return self.geom.intersect(other_GEOSGeometry)

    def contains(self, other_GEOSGeometry):
        return self.geom.contains(other_GEOSGeometry)

    def hasz(self):
        return self.geom.hasz

    def crosses(self, other_GEOSGeometry):
        return self.geom.crosses(other_GEOSGeometry)

    def count(self):
        return self.geom.count

    def num_points(self):
        return self.geom.num_points

    def within(self, other_GEOSGeometry):
        return self.geom.within(other_GEOSGeometry)

    def intersection(self, other_GEOSGeometry):
        return self.geom.intersection(other_GEOSGeometry)

    def overlaps(self, other_GEOSGeometry):
        return self.geom.overlaps(other_GEOSGeometry)

    def equals(self, other_GeosGeometry ):
        return self.geom.equals( other_GeosGeometry)

    def point_on_surface(self):
        return self.geom.point_on_surface

    def difference(self, other_GEOSGeometry):
        return self.geom.difference(other_GEOSGeometry)

    def transform(self,srid, clone=True ):
        return self.geom.transform(srid, clone=True)

    def set_x(self, x):
        return self.geom.set_x(x)

    def get_coords(self):
        return self.geom.get_coords

    def envelope(self):
        return self.geom.envelope

    def prepared(self):
        return self.geom.prepared

    def ewkt(self):
        return self.geom.ewkt

    def length(self):
        return self.geom.length

    def disjoint(self, other_GEOSGeometry):
        return self.geom.disjoint(other_GEOSGeometry)

    def geometry_with_parameters_type(self):
        #self.dic = [   '', '', 'intersects', 'json', 'kml', 'length', 'normalize', 'num_coords', 'num_geom', 'num_points', 'ogr', 'overlaps', 'point_on_surface', 'pop', 'prepared', 'ptr', 'ptr_type', 'relate', 'relate_pattern', 'remove', 'reverse', 'ring', 'set_coords', 'set_srid', 'set_x', 'set_y', 'set_z', 'simple', 'simplify', 'sort', 'srid', 'srs', 'sym_difference', 'touches', 'transform', 'tuple', 'union', 'valid', 'valid_reason', 'within', 'wkb', 'wkt', 'x', 'y', 'z']

        if len(self.dic) == 0:
            self.dic['area'] = Type_Called('area', None, float)
            self.dic['boundary'] = Type_Called('boundary', None, GEOSGeometry)
            self.dic['buffer'] = Type_Called('buffer', [float], GEOSGeometry)
            self.dic['centroid'] = Type_Called('centroid', None, Point)
            self.dic['contains'] = Type_Called('contains', [GEOSGeometry], bool)
            self.dic['convex_hull'] = Type_Called('convex_hull', None, Polygon)
            self.dic['coord_seq'] = Type_Called('coord_seq', None, tuple)
            self.dic['coords'] = Type_Called('coords', None, tuple)
            self.dic['count'] = Type_Called('count', None, int)
            self.dic['crosses'] = Type_Called('crosses', [GEOSGeometry], bool)
            self.dic['crs'] = Type_Called('crs', None, SpatialReference)
            self.dic['difference'] = Type_Called('difference', [GEOSGeometry], GEOSGeometry)
            self.dic['dims'] = Type_Called('dims', None, int)
            self.dic['disjoint'] = Type_Called('disjoint',[GEOSGeometry], bool)
            self.dic['distance'] = Type_Called('distance',[GEOSGeometry], float)
            self.dic['empty'] = Type_Called('empty',None, bool)
            self.dic['envelope'] = Type_Called('envelope',None, GEOSGeometry)
            self.dic['equals'] = Type_Called('equals',[GEOSGeometry], bool)
            self.dic['equals_exact'] = Type_Called('equals_exact',[GEOSGeometry, float], bool)
            self.dic['ewkb'] = Type_Called('ewkb',None, str)
            self.dic['ewkt'] = Type_Called('ewkt',None, str)
            self.dic['extend'] = Type_Called('extend',None, tuple)
            self.dic['extent'] = Type_Called('extent',None, tuple)
            self.dic['geojson'] = Type_Called('geojson',None, str)
            self.dic['geom_type'] = Type_Called('geom_type',None, str)
            self.dic['geom_typeid'] = Type_Called('geom_typeid',None, int)
            self.dic['get_coords'] = Type_Called('get_coords', None, tuple)
            self.dic['get_srid'] = Type_Called('get_srid', None, str)
            self.dic['get_x'] = Type_Called('get_x', None, str)
            self.dic['get_y'] = Type_Called('get_y', None, str)
            self.dic['get_z'] = Type_Called('get_z', None, str)
            self.dic['has_cs'] = Type_Called('has_cs',None, bool)
            self.dic['hasz'] = Type_Called('hasz',None, bool)
            self.dic['hex'] = Type_Called('hex',None, str)
            self.dic['hexewkb'] = Type_Called('hexewkb',None, str)
            self.dic['index'] = Type_Called('index',None, int)
            self.dic['intersection'] = Type_Called('intersection',[GEOSGeometry], GEOSGeometry)
            self.dic['intersects'] = Type_Called('intersects',[GEOSGeometry], bool)
            self.dic['interpolate'] = Type_Called('interpolate',[float], Point)
            self.dic['json'] = Type_Called('json',None, str)
            self.dic['kml'] = Type_Called('kml',None, str)
            self.dic['length'] = Type_Called('length',None, float)
            self.dic['normalize'] = Type_Called('normalize',[float], Point)
            self.dic['num_coords'] = Type_Called('num_coords',None, int)
            self.dic['num_geom'] = Type_Called('num_geom',None, int)
            self.dic['num_points'] = Type_Called('num_points',None, int)
            self.dic['ogr'] = Type_Called('ogr',None,  OGRGeometry)
            self.dic['overlaps'] = Type_Called('overlaps',[GEOSGeometry],  bool)
            self.dic['point_on_surface'] = Type_Called('point_on_surface',None,  Point)
            self.dic['pop'] = Type_Called('pop',None,  tuple)
            #self.dic['prepared'] = Type_Called('prepared',None,  PreparedGeometry)
            self.dic['relate'] = Type_Called('relate',[GEOSGeometry],  str)
            self.dic['relate_pattern'] = Type_Called('relate_pattern',[GEOSGeometry, str],  str)
            self.dic['ring'] = Type_Called('ring',None,  bool)
            self.dic['set_coords'] = Type_Called('set_coords',[tuple],  None)
            self.dic['set_srid'] = Type_Called('set_srid',[str],  None)
            self.dic['set_x'] = Type_Called('set_x',[float],  None)
            self.dic['set_y'] = Type_Called('set_y',[float],  None)
            self.dic['set_z'] = Type_Called('set_z',[float],  None)
            self.dic['simple'] = Type_Called('simple',None,  bool)
            self.dic['simplify'] = Type_Called('simplify', [float, bool],  GEOSGeometry)
            self.dic['srid'] = Type_Called('srid', None,  int)
            self.dic['srs'] = Type_Called('srs', None,  SpatialReference)
            self.dic['sym_difference'] = Type_Called('sym_difference', [GEOSGeometry],  GEOSGeometry)
            self.dic['touches'] = Type_Called('touches', [GEOSGeometry],  bool)
            self.dic['transform'] = Type_Called('transform', [int, bool],  GEOSGeometry)
            self.dic['tuple'] = Type_Called('tuple', None,  tuple)
            self.dic['union'] = Type_Called('union', [GEOSGeometry],  GEOSGeometry)
            self.dic['valid'] = Type_Called('valid', [GEOSGeometry],  bool)
            self.dic['valid_reason'] = Type_Called('valid_reason', [GEOSGeometry],  str)
            self.dic['within'] = Type_Called('within', [GEOSGeometry],  bool)
            self.dic['wkb'] = Type_Called('wkb', None,  str)
            self.dic['wkt'] = Type_Called('wkt', None,  str)
            self.dic['x'] = Type_Called('x', None,  float)
            self.dic['y'] = Type_Called('y', None,  float)
            self.dic['z'] = Type_Called('z', None,  float)
        return self.dic

def geometry_with_parameters_type():

    dic = {}

    dic['area'] = []
    dic['boundary'] = []
    dic['buffer'] = [float]
    dic['centroid'] = []
    dic['contains'] = [GEOSGeometry]
    dic['convex_hull'] = []
    dic['coord_seq'] = []
    dic['coords'] = []
    dic['coord_seq'] = []
    dic['count'] = [float]
    dic['crosses'] = [GEOSGeometry]
    dic['crs'] = []
    dic['difference'] = [GEOSGeometry]
    dic['dims'] = []
    dic['disjoint'] = [GEOSGeometry]
    dic['distance'] = [GEOSGeometry]
    dic['empty'] = []
    dic['envelope'] = []
    dic['equals'] = [GEOSGeometry]
    dic['equals_exact'] = [GEOSGeometry]
    dic['ewkb'] = []
    dic['ewkt'] = []
    dic['extend'] = []
    dic['extent'] = [tuple]
    dic['geojson'] = []
    dic['geom_type'] = []
    dic['geom_typeid'] = []
    dic['get_coords'] = []
    dic['get_srid'] = []
    dic['get_x'] = []
    dic['get_y'] = []
    dic['get_z'] = []
    dic['has_cs'] = []
    dic['hasz'] = []
    dic['hex'] = []
    dic['hexewkb'] = []
    dic['index'] = []
    dic['intersection'] = [GEOSGeometry]
    dic['intersects'] = [GEOSGeometry]
    dic['json'] = []
    dic['kml'] = []
    dic['length'] = []
    dic['normalize'] = []
    dic['num_coords'] = []
    dic['num_geom'] = []
    dic['num_points'] = []
    dic['ogr'] = []
    dic['overlaps'] = [GEOSGeometry]
    dic['point_on_surface'] = []
    dic['pop'] = []
    #dic['prepared'] = []
    dic['ptr'] = []
    dic['ptr_type'] = []
    dic['relate'] = [GEOSGeometry]
    dic['relate_pattern'] = [GEOSGeometry, str]
    dic['remove'] = [str]
    dic['reverse'] = []
    dic['ring'] = []
    dic['set_coords'] = [tuple]
    dic['set_srid'] = [int]
    dic['set_x'] = [float]
    dic['set_y'] = [float]
    dic['set_z'] = []
    dic['simple'] = []
    dic['simplify'] = [float, bool]
    dic['srid'] = []
    dic['srs'] = []
    dic['sym_difference'] = [GEOSGeometry]
    dic['touches'] = [GEOSGeometry]
    dic['transform'] = [int, bool]
    dic['tuple'] = []
    dic['union'] = [GEOSGeometry]
    dic['valid'] = []
    dic['valid_reason'] = [GEOSGeometry]
    dic['within'] = []
    dic['wkb'] = []
    dic['wkt'] = []
    dic['x'] = []
    dic['y'] = []
    dic['z'] = []
    return dic

# In developing.
class HandleFunctionsList(generics.ListCreateAPIView):

    content_negotiation_class = IgnoreClientContentNegotiation

    def __init__(self):
        super(HandleFunctionsList, self).__init__()
        if hasattr(self, 'contextclassname'):
            self.base_context = BaseContext(self.contextclassname)
        if not hasattr(self, 'iri_metadata'):
            self.iri_metadata = None
        if not hasattr(self, 'iri_style'):
            self.iri_style = None


    def setSerializer(self, kwargs):
        keyModel = 'model_class'
        if keyModel in kwargs and kwargs.get(keyModel) in serializers_dict:
            self.serializer_class = serializers_dict.get(kwargs.get(keyModel)).get('serializer')
            self.contextclassname = kwargs.get(keyModel)
            self.base_context = BaseContext(self.contextclassname)

    def options(self, request, *args, **kwargs):
        self.setSerializer(kwargs)
        parent_url = self.get_parent_url(request, kwargs)
        response = self.base_context.options(request)
        response = self.add_url_in_header(parent_url, response, "up")
        if self.iri_metadata is not None:
            response = self.add_url_in_header(self.iri_metadata, response, "metadata")
        if self.iri_style is not None:
            response = self.add_url_in_header(self.iri_style, response, "stylesheet")
        return response

    def generate_tmp_file(self, suffix='', length_name=10):
        return ''.join([random.choice('0123456789ABCDEF') for i in range(length_name)]) + suffix

    def get_style_file(self, request):
        if 'HTTP_LAYERSTYLE' in request.META:
            layer_style_url = request.META['HTTP_LAYERSTYLE']
            response = requests.get(layer_style_url)
            if response.status_code == 200:
                file_name = self.generate_tmp_file(suffix="_tmp_style.xml")
                with open(file_name, "w+") as st:
                    st.write(response.text.encode('UTF-8'))
                    st.close()
                return file_name
        return None

    def get_png(self, queryset, request):
        style = self.get_style_file(request)
        wkt = "GEOMETRYCOLLECTION("
        for i,e in enumerate(queryset):
            wkt += e.geom.wkt #it is need to fix the case that the attribute is not called by geom
            if i != len(queryset)-1:
                wkt += ","
            else:
                wkt += ")"
        geom_type = queryset[0].geom.geom_type

        config = {'wkt': wkt, 'type': geom_type}
        if style is not None:
            config["style"] = style
            config["deleteStyle"] = True
        builder_png = BuilderPNG(config)
        return builder_png.generate()

    def get_queryset(self):
        stFunction = self.kwargs.get("attributes_functions", None)
        modelClass = self.serializer_class.Meta.model

        if stFunction is None: # to get query parameters
            queryset = modelClass.objects.all()
            query_parameters = self.request.query_params
            dict = self.get_dict_with_spatialfunction_or_same_dict(query_parameters.dict())
            self.queryset = queryset.filter(**dict)

        else: # to get query from url
            geom_str_or_url = self.kwargs.get('geom')
            aKey = self.serializer_class.Meta.geo_field + '__' + stFunction
            aGeom = self.geos_geometry(geom_str_or_url)

            if stFunction is not None:
                self.queryset = modelClass.objects.filter(**({aKey: aGeom}))

        return self.queryset

    def get_parent_url(self, request, kwargs):
        url = request._request.path
        parts = url.split("/")
        index = -1
        if kwargs.get("attributes_functions", None) is not None:
            index = -2

        if parts[-1] == "":
            parent_url = "/".join(parts[:index-1])
        else:
            parent_url = "/".join(parts[:index])

        if "http" not in parent_url:
            parent_url += "/"
            host = request.get_host()
            parent_url = "http://" + host + parent_url

        return parent_url

    def add_url_in_header(self, url, response, rel):
        link = ' <'+url+'>; rel=\"'+rel+'\" '
        if "Link" not in response:
            response['Link'] = link
        else:
            response['Link'] += "," + link
        return response

    def get(self, request, *args, **kwargs):
        if kwargs.get('format') == 'jsonld':
            return self.options(request, *args, **kwargs)

        self.setSerializer(kwargs)
        parent_url = self.get_parent_url(request, kwargs)
        response = super(HandleFunctionsList, self).get(request, *args, **kwargs)
        accept = request.META['HTTP_ACCEPT']

        if accept.lower() == "image/png" or kwargs.get('format', None) == 'png':
            image = self.get_png(self.queryset, request)
            response = HttpResponse(image, content_type="image/png")

        response = self.add_url_in_header(parent_url, response, "up")
        if self.iri_metadata is not None:
            response = self.add_url_in_header(self.iri_metadata, response, "metadata")
        if self.iri_style is not None:
            response = self.add_url_in_header(self.iri_style, response, "stylesheet")
        return self.base_context.addContext(request, response)

    def make_geometrycollection_from_featurecollection(self, feature_collection):
        geoms = []
        features = ast.literal_eval(feature_collection)
        for feature in features['features']:
            feature_geom = feature['geometry']
            geoms.append(GEOSGeometry(feature_geom))
        return GeometryCollection(tuple(geoms))

    def geos_geometry(self, geom_str_or_url):
        a_geom = geom_str_or_url
        geom_str_or_url = re.sub(r':/+', '://', geom_str_or_url) #this is just because one slash disappears when the code gets here. This is a magic problem.
        str1 = (geom_str_or_url[0:5]).lower()
        https = ['http:', 'https']
        if (str1 in https):
            resp = requests.get(geom_str_or_url)
            j = resp.json()

            if j["type"].lower() == 'feature':
               return GEOSGeometry(json.dumps(j["geometry"]))

            if j["type"].lower() == 'featurecollection':
                return self.make_geometrycollection_from_featurecollection(resp.text)

            a_geom = json.dumps(j)

        return GEOSGeometry(a_geom)

    def json_geometrycollection_from_featurecollection(self, feature_collection):
        geometry_collection = {
            "type": "GeometryCollection",
            "geometries": []
        }

        for feature in feature_collection['features']:
            geometry_collection['geometries'].append(feature['geometry'])

        return json.dumps(geometry_collection)

    def get_dict_with_spatialfunction_or_same_dict(self, dict):
        for key, value in dict.items():
            if key.startswith('*'):
                new_key = self.serializer_class.Meta.geo_field + '__' + key[1:]
                dict.pop(key)
                str1 = (value[0:5]).lower()
                https = ['http:', 'https']
                if (str1 in https):
                    resp = requests.get(value)
                    j = resp.json()

                    if j["type"].lower() == 'feature':
                        value = json.dumps(j["geometry"])
                    elif j["type"].lower() == 'featurecollection':
                        value = self.json_geometrycollection_from_featurecollection(resp.json())
                    else:
                        value = json.dumps(j)

                #a_value = value
                #a_geom = GEOSGeometry(a_value, 4326)
                dict[new_key] = value
        return dict

class BasicAPIViewHypermedia(APIView):

    def model_class(self):
        return self.serializer_class.Meta.model

    def geometry_field_name(self):
        return self.serializer_class.Meta.geo_field

    def get_geometry_object(self, object_model):
        return getattr(object_model, self.geometry_field_name(), None)

    def key_is_identifier(self, key):
        return key in self.serializer_class.Meta.identifiers

    def dic_with_only_identitier_field(self, dict_params):
        dic = dict_params.copy()
        a_dict = {}
        for key, value in dic.items():
            if self.key_is_identifier(key):
                a_dict[key] = value

        return a_dict

    def is_spatial_operation(self, attribute_or_method_name):
        return (attribute_or_method_name in geometry_with_parameters_type().keys())

    def is_spatial_attribute(self, attribute_or_method_name):
        return self.geometry_field_name() == attribute_or_method_name

    def is_spatial_and_has_parameters(self, attribute_or_method_name):
        dic = geometry_with_parameters_type()
        return (attribute_or_method_name in dic) and len(dic[attribute_or_method_name])

class APIViewHypermedia(BasicAPIViewHypermedia):

    content_negotiation_class = IgnoreClientContentNegotiation

    def get_object(self, a_dict):
        queryset = self.model_class().objects.all()
        obj = get_object_or_404(queryset, **a_dict)
        self.check_object_permissions(self.request, obj)
        return obj

    def attributes_functions_name_template(self):
        return 'attributes_functions'

    def _has_method(self, object, method_name):
        return hasattr(object, method_name) and callable(getattr(object, method_name))

    def has_only_attribute(self, object, attributes_functions_name):
        attrs_functs = attributes_functions_name.split('/')
        if len(attrs_functs) > 1:
            return False
        if '&' in attrs_functs[0]:
            return True

        if self._has_method(object, attrs_functs[0]):
            return False
        return hasattr(object, attrs_functs[0])


    def parametersConverted(self, params_as_array):
        paramsConveted = []

        for value in params_as_array:
            if value.lower() == 'true':
                paramsConveted.append(True)
                continue
            elif value.lower() == 'false':
                paramsConveted.append(False)
                continue

            try:
                paramsConveted.append(int( value ) )
                continue
            except ValueError:
                pass
            try:
               paramsConveted.append( float( value ) )
               continue
            except ValueError:
                pass
            try:
               paramsConveted.append( GEOSGeometry( value ) )
               continue
            except ValueError:
                pass
            try:
                http_str = (value[0:4]).lower()
                if (http_str == 'http'):
                    resp = requests.get(value)
                    if 400 <= resp.status_code <= 599:
                        raise HTTPError({resp.status_code: resp.reason})
                    js = resp.json()

                    if (js.get("type") and js["type"].lower() in ['feature', 'featurecollection']):
                        a_geom = js["geometry"]
                    else:
                        a_geom = js
                    paramsConveted.append(GEOSGeometry((json.dumps(a_geom))))
            except (ConnectionError,  HTTPError) as err:
                print('Error: '.format(err))
                #paramsConveted.append (value)

        return paramsConveted

    def make_geometrycollection_from_featurecollection(self, feature_collection):
        geoms = []
        features = ast.literal_eval(feature_collection)
        for feature in features['features']:
            feature_geom = feature['geometry']
            geoms.append(GEOSGeometry(feature_geom))
        return GeometryCollection(tuple(geoms))

    def all_parameters_converted(self, attribute_or_function_name, parameters):
        parameters_converted = []
        if self.is_spatial_and_has_parameters(attribute_or_function_name):
            parameters_type = geometry_with_parameters_type()[attribute_or_function_name]
            for i in range(0, len(parameters)):
                if GEOSGeometry == parameters_type[i]:
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

    def _value_from_object(self, object, attribute_or_function_name, parameters):
        obj = getattr(object, attribute_or_function_name)

        if len(parameters):
            params = self.all_parameters_converted(attribute_or_function_name, parameters)
            return obj(*params)

        if callable(obj):
            return obj()

        return obj

    def response_resquest_with_attributes(self, object_model, attributes_functions_name):
        a_dict ={}
        attributes = attributes_functions_name.split('&')
        for attr_name in attributes:
           obj = self._value_from_object(object_model, attr_name, [])
           if isinstance(obj, GEOSGeometry):
               geom = obj
               obj = json.loads(obj.geojson)
               if len(attributes) == 1:
                   return (obj, 'application/vnd.geo+json', geom)

           a_dict[attr_name] = obj

        return (a_dict, 'application/json')

    def attributes_functions_str_has_url(self, attributes_functions_str_url):
        return (attributes_functions_str_url.find('http:') > -1) or (attributes_functions_str_url.find('https:') > -1)\
               or (attributes_functions_str_url.find('www.') > -1)

    def attributes_functions_splitted_by_url(self, attributes_functions_str_url):
        res = attributes_functions_str_url.lower().find('http:')
        if res == -1:
            res = attributes_functions_str_url.lower().find('https:')
            if res == -1:
                res = attributes_functions_str_url.lower().find('www.')
                if res == -1:
                    return [attributes_functions_str_url]

        return [attributes_functions_str_url[0:res], attributes_functions_str_url[res:]]

    def _execute_attribute_or_method(self, object, attribute_or_method_name, array_of_attribute_or_method_name):
        dic = {}
        parameters = []
        arr_attrib_method_name = array_of_attribute_or_method_name
        att_or_method_name = attribute_or_method_name

        if self.is_spatial_and_has_parameters(att_or_method_name):
            parameters = arr_attrib_method_name[0].split('&')
            arr_attrib_method_name = arr_attrib_method_name[1:]

        obj = self._value_from_object(object, att_or_method_name, parameters)

        if len(arr_attrib_method_name) == 0:
            return obj

        return self._execute_attribute_or_method(obj, arr_attrib_method_name[0], arr_attrib_method_name[1:])

    def function_name(self, attributes_functions_str):
        functions_dic = geometry_with_parameters_type()
        if str(attributes_functions_str[-1]) in functions_dic:
            return str(attributes_functions_str[-1])
        return str(attributes_functions_str[-2])

    def response_of_request(self, object, attributes_functions_str):
        att_funcs = attributes_functions_str.split('/')

        obj = self.get_geometry_object(object)
        if not self.is_spatial_operation(att_funcs[0]) and self.is_spatial_attribute(att_funcs[0]):
            att_funcs = att_funcs[1:]

        a_value = self._execute_attribute_or_method(obj, att_funcs[0], att_funcs[1:])

        if isinstance(a_value, GEOSGeometry) or isinstance(a_value, OGRGeometry):
            geom = a_value
            a_value = json.loads(a_value.geojson)
            return (a_value, 'application/vnd.geo+json', geom, {'status_code': '200'})
        elif isinstance(a_value, SpatialReference):
            a_value = {
                self.function_name(att_funcs): a_value.wkt
            }
        else:
            a_value = {
                self.function_name(att_funcs): a_value
            }

        return (a_value, 'application/json')

    def generate_tmp_file(self, suffix='', length_name=10):
        return ''.join([random.choice('0123456789ABCDEF') for i in range(length_name)]) + suffix

    def get_style_file(self, request):
        if 'HTTP_LAYERSTYLE' in request.META:
            layer_style_url = request.META['HTTP_LAYERSTYLE']
            response = requests.get(layer_style_url)
            if response.status_code == 200:
                file_name = self.generate_tmp_file(suffix="_tmp_style.xml")
                with open(file_name, "w+") as st:
                    st.write(response.text.encode('UTF-8'))
                    st.close()
                return file_name
        return None

    def get_png(self, queryset, request):
        style = self.get_style_file(request)

        if isinstance(queryset, GEOSGeometry):
            wkt = queryset.wkt
            geom_type = queryset.geom_type
        else:
            wkt = queryset.geom.wkt
            geom_type = queryset.geom.geom_type

        config = {'wkt': wkt, 'type': geom_type}
        if style is not None:
            config["style"] = style
            config["deleteStyle"] = True
        builder_png = BuilderPNG(config)
        return builder_png.generate()

    def get(self, request, *args, **kwargs):
        object_model = self.get_object(self.dic_with_only_identitier_field(kwargs))
        attributes_functions_str = kwargs.get(self.attributes_functions_name_template())

        if attributes_functions_str is None:
            serializer = self.serializer_class(object_model)
            output = (serializer.data, 'application/vnd.geo+json', object_model)

        elif self.has_only_attribute(object_model, attributes_functions_str):
            output = self.response_resquest_with_attributes(object_model, attributes_functions_str)

        elif self.attributes_functions_str_has_url(attributes_functions_str.lower()):
            attributes_functions_str = re.sub(r':/+', '://', attributes_functions_str)
            arr_of_two_url = self.attributes_functions_splitted_by_url(attributes_functions_str)
            resp = requests.get(arr_of_two_url[1])
            if resp.status_code == 404:
                return Response({'Erro:' + str(resp.status_code)}, status=status.HTTP_404_NOT_FOUND)
            j = resp.text
            attributes_functions_str = arr_of_two_url[0] + j
            output = self.response_of_request(object_model, attributes_functions_str)
        else:
            output = self.response_of_request(object_model, attributes_functions_str)


        response = Response(data=output[0], content_type=output[1])

        accept = request.META['HTTP_ACCEPT']
        if accept.lower() == "image/png" or kwargs.get('format', None) == 'png':
            if len(output) == 3:
                queryset = output[2]
                image = self.get_png(queryset, request)
                #headers = response._headers
                response = HttpResponse(image, content_type="image/png")
                #headers.update(response._headers)
                #response._headers = headers
            else:
                return Response({'Erro': 'The server can generate an image only from a geometry data'}, status=status.HTTP_404_NOT_FOUND)

        return response

class HandleFunctionDetail(APIViewHypermedia):

    def __init__(self):
        super(HandleFunctionDetail, self).__init__()
        self.iri_metadata = None
        self.iri_style = None
        if hasattr(self, 'contextclassname'):
            self.base_context = BaseContext(self.contextclassname, serializer_object=self.serializer_class)

    def getLinks(self, kwargs):
        object_model = self.get_object(self.dic_with_only_identitier_field(kwargs))
        self.iri_metadata = object_model.iri_metadata
        self.iri_style = object_model.iri_style

    def setSerializer(self, kwargs):
        keyModel = 'model_class'
        if keyModel in kwargs and kwargs.get(keyModel) in serializers_dict:
            self.serializer_class = serializers_dict.get(kwargs.get(keyModel)).get('serializer')
            kwargs[self.serializer_class.Meta.identifier] = kwargs['id_objeto']
            del kwargs['id_objeto']
            self.contextclassname = kwargs.get(keyModel)
            self.base_context = BaseContext(self.contextclassname)

    def get_parent_url(self, request, kwargs):
        url = request._request.path
        parts = url.split("/")
        index = -1
        attributes_functions = kwargs.get("attributes_functions", None)
        if attributes_functions is not None:
            funcs = attributes_functions.split("/")
            for i in xrange(-1, -(len(funcs)+1), -1):
                if self.is_spatial_operation(funcs[i]):
                    index = i
                    break

        if parts[-1] == "":
            parent_url = "/".join(parts[:index-1])
        else:
            parent_url = "/".join(parts[:index])

        if "http" not in parent_url:
            parent_url += "/"
            host = request.get_host()
            parent_url = "http://" + host + parent_url

        return parent_url

    def add_url_in_header(self, url, response, rel):
        link = ' <'+url+'>; rel=\"'+rel+'\" '
        if "Link" not in response:
            response['Link'] = link
        else:
            response['Link'] += "," + link
        return response

    def get(self, request, *args, **kwargs):
        if kwargs.get('format') == 'jsonld':
            return self.options(request, *args, **kwargs)

        self.setSerializer(kwargs)
        self.getLinks(kwargs)
        parent_url = self.get_parent_url(request, kwargs)
        res = super(HandleFunctionDetail, self).get(request, *args, **kwargs)
        res = self.add_url_in_header(parent_url, res, "up")
        if self.iri_metadata is not None:
            res = self.add_url_in_header(self.iri_metadata, res, "metadata")
        if self.iri_style is not None:
            res = self.add_url_in_header(self.iri_style, res, "stylesheet")
        return self.base_context.addContext(request, res)

    def options(self, request, *args, **kwargs):
        self.setSerializer(kwargs)
        self.getLinks(kwargs)
        parent_url = self.get_parent_url(request, kwargs)
        response = self.base_context.options(request)
        response = self.add_url_in_header(parent_url, response, "up")
        if self.iri_metadata is not None:
            response = self.add_url_in_header(self.iri_metadata, response, "metadata")
        if self.iri_style is not None:
            response = self.add_url_in_header(self.iri_style, response, "stylesheet")
        return response
