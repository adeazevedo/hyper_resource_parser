# -*- coding: utf-8 -*-
from django.contrib.gis.db import models
from django.contrib.gis.db.models import GeometryField
from django.contrib.gis.db.models import LineStringField
from django.contrib.gis.db.models import MultiLineStringField
from django.contrib.gis.db.models import MultiPointField
from django.contrib.gis.db.models import MultiPolygonField
from django.contrib.gis.db.models import PointField
from django.contrib.gis.db.models import PolygonField
from django.contrib.gis.gdal import OGRGeometry
from django.contrib.gis.gdal import SpatialReference
from django.contrib.gis.geos import GEOSGeometry, Point, Polygon, MultiPolygon,LineString, MultiLineString, MultiPoint, GeometryCollection
from datetime import date, datetime
from time import *

from django.contrib.gis.geos.prepared import PreparedGeometry
from django.db.models import *

from hyper_resource.models import *


class Reflection:

    def superclass(a_class):
        """
        Retorna apenas uma das heranças de
        'a_class'. Se houver uma herança
        multipla, as demais classes serão
        ignoradas
        :return:
        """
        return a_class.__base__

    def supeclasses(a_class):
        """
        Retorna a(s) classe(s) de que
        'a_class' herda em forma do tupla
        :return:
        """
        return a_class.__bases__

    def operation_names(a_class):
        """
        Retorna uma lista de métodos públicos
        de 'a_class'
        :return:
        """
        # - dir() retona uma lista com todos os membros de 'a_class'
        # - se o valor do membro 'method' de 'a_class' for um chamável,
        # ou seja, se o valor de 'method' for uma função, e além disso,
        # se esta função não for privada, adicionamos ela na lista
        return [method for method in dir ( a_class ) if
                callable ( getattr ( a_class, method ) ) and a_class.is_not_private ( method )]



class FeatureCollection(object):
    pass


def vocabularyDict():
    """
    Returns a dict whose each key is a type and his
    respective value is a string that points to a vocabulary
    that explains what this type is
    :return:
    """
    dict = {}

    dict[BooleanField] = 'http://schema.org/Boolean'
    dict[bool] = 'http://schema.org/Boolean'
    dict[True] = 'http://schema.org/Boolean'
    dict[False] = 'http://schema.org/Boolean'
    dict[FloatField] = 'http://schema.org/Float'
    dict[float] = 'http://schema.org/Float'
    dict[ForeignKey] = 'http://schema.org/Integer'
    dict[IntegerField] = 'http://schema.org/Integer'
    dict[AutoField]= 'http://schema.org/Integer'
    dict[int] = 'http://schema.org/Integer'
    dict[CharField] = 'http://schema.org/Text'
    dict[TextField] = 'http://schema.org/Text'
    dict[str] = 'http://schema.org/Text'
    dict[DateField] = 'http://schema.org/Date'
    dict[date] = 'http://schema.org/Date'
    dict[DateTimeField] = 'http://schema.org/DateTime'
    dict[datetime] = 'http://schema.org/DateTime'
    dict[TimeField] = 'http://schema.org/Time'
    dict[Model] = 'http://geojson.org/geojson-ld/vocab.html#Feature'
    dict[tuple]= 'http://schema.org/ItemList'
    dict[list]= 'http://schema.org/ItemList'


    dict[Q] = 'http://extension.schema.org/expression'
    dict[object] = 'http://schema.org/Thing'

    dict['nome'] = 'http://schema.org/name'
    dict['name'] = 'http://schema.org/name'
    dict['nomeAbrev'] = 'https://schema.org/alternateName'
    dict['responsible'] = 'http://schema.org/accountablePerson'
    dict['usuario'] = 'http://schema.org/Person'
    dict['user'] = 'http://schema.org/Person'

    dict['FeatureCollection'] = 'http://geojson.org/geojson-ld/vocab.html#FeatureCollection'
    dict[GeometryField] = 'http://geojson.org/geojson-ld/vocab.html#geometry'
    dict[PointField] = 'http://geojson.org/geojson-ld/vocab.html#Point'
    dict[LineStringField] = 'http://geojson.org/geojson-ld/vocab.html#LineString'
    dict[PolygonField] = 'http://geojson.org/geojson-ld/vocab.html#Polygon'
    dict[MultiPolygonField] = 'http://geojson.org/geojson-ld/vocab.html#MultiPolygon'
    dict[MultiLineStringField] = 'http://geojson.org/geojson-ld/vocab.html#MultiLineString'
    dict[MultiPointField] = 'http://geojson.org/geojson-ld/vocab.html#MultiPoint'

    dict[MultiPolygon] = 'http://geojson.org/geojson-ld/vocab.html#MultiPolygon'
    dict[Polygon] = 'http://geojson.org/geojson-ld/vocab.html#Polygon'
    dict[LineString] = 'http://geojson.org/geojson-ld/vocab.html#LineString'
    dict[Point] = 'http://geojson.org/geojson-ld/vocab.html#Point'
    dict[GEOSGeometry] = 'http://geojson.org/geojson-ld/vocab.html#geometry'
    dict[OGRGeometry] = 'http://geojson.org/geojson-ld/vocab.html#geometry'
    dict[MultiLineString] = 'http://geojson.org/geojson-ld/vocab.html#MultiLineString'
    dict[MultiPoint] = 'http://geojson.org/geojson-ld/vocab.html#MultiPoint'
    dict[GeometryCollection] = 'http://geojson.org/geojson-ld/vocab.html#GeometryCollection'
    dict[SpatialReference] = 'http://geojson.org/geojson-ld/vocab.html#SpatialReference'



    #collection
    dict['filter'] = 'http://opengis.org/operations/filter'
    dict['map'] = 'http://opengis.org/operations/map'
    dict['annotate'] = 'http://opengis.org/operations/annotate'
    dict['count_elements'] = 'http://opengis.org/operations/count_elements'
    dict['offset_limit'] = 'http://opengis.org/operations/offset_limit'
    dict['distance_lte'] = 'http://opengis.org/operations/distance_lte'
    dict['area'] = 'http://opengis.org/operations/area'
    dict['boundary'] = 'http://opengis.org/operations/boundary'
    dict['buffer'] = 'http://opengis.org/operations/buffer'
    dict['centroid'] = 'http://opengis.org/operations/centroid'
    dict['contains'] = 'http://opengis.org/operations/contains'
    dict['convex_hull'] = 'http://opengis.org/operations/convex_hull'
    dict['coord_seq'] = 'http://opengis.org/operations/coord_seq'
    dict['coords'] = 'http://opengis.org/operations/coords'
    dict['count'] = 'http://opengis.org/operations/count'
    dict['crosses'] = 'http://opengis.org/operations/crosses'
    dict['crs'] = 'http://opengis.org/operations/crs'
    dict['difference'] = 'http://opengis.org/operations/difference'
    dict['dims'] = 'http://opengis.org/operations/dims'
    dict['disjoint'] = 'http://opengis.org/operations/disjoint'
    dict['distance'] = 'http://opengis.org/operations/distance'
    dict['empty'] = 'http://opengis.org/operations/empty'
    dict['envelope'] = 'http://opengis.org/operations/envelope'
    dict['equals'] = 'http://opengis.org/operations/equals'
    dict['equals_exact'] = 'http://opengis.org/operations/equals_exact'
    dict['ewkb'] = 'http://opengis.org/operations/ewkb'
    dict['ewkt'] = 'http://opengis.org/operations/ewkt'
    dict['extend'] = 'http://opengis.org/operations/extend'
    dict['extent'] = 'http://opengis.org/operations/extent'
    dict['geojson'] = 'http://opengis.org/operations/geojson'
    dict['geom_type'] = 'http://opengis.org/operations/geom_type'
    dict['geom_typeid'] = 'http://opengis.org/operations/geom_typeid'
    dict['get_coords'] = 'http://opengis.org/operations/get_coords'
    dict['get_srid'] = 'http://opengis.org/operations/get_srid'
    dict['get_x'] = 'http://opengis.org/operations/get_x'
    dict['get_y'] = 'http://opengis.org/operations/get_y'
    dict['get_z'] = 'http://opengis.org/operations/get_z'
    dict['has_cs'] = 'http://opengis.org/operations/has_cs'
    dict['hasz'] = 'http://opengis.org/operations/hasz'
    dict['hex'] = 'http://opengis.org/operations/hex'
    dict['hexewkb'] = 'http://opengis.org/operations/hexewkb'
    dict['index'] = 'http://opengis.org/operations/index'
    dict['intersection'] = 'http://opengis.org/operations/intersection'
    dict['intersects'] = 'http://opengis.org/operations/intersects'
    dict['interpolate'] = 'http://opengis.org/operations/interpolate'
    dict['json'] = 'http://opengis.org/operations/json'
    dict['kml'] = 'http://opengis.org/operations/kml'
    dict['length'] = 'http://opengis.org/operations/length'
    dict['normalize'] = 'http://opengis.org/operations/normalize'
    dict['num_coords'] = 'http://opengis.org/operations/num_coords'
    dict['num_geom'] = 'http://opengis.org/operations/num_geom'
    dict['num_s'] = 'http://opengis.org/operations/num_s'
    dict['num_points']  = 'http://opengis.org/operations/num_points'
    dict['point_on_surface'] = 'http://opengis.org/operations/point_on_surface'
    dict['ogr'] = 'http://opengis.org/operations/ogr'
    dict['overlaps'] = 'http://opengis.org/operations/overlaps'
    dict['_on_surface'] = 'http://opengis.org/operations/_on_surface'
    dict['pop'] = 'http://opengis.org/operations/pop'
    dict['prepared'] = 'http://opengis.org/operations/prepared'
    dict['relate'] = 'http://opengis.org/operations/relate'
    dict['relate_pattern'] = 'http://opengis.org/operations/relate_pattern'
    dict['ring'] = 'http://opengis.org/operations/ring'
    dict['set_coords'] = 'http://opengis.org/operations/set_coords'
    dict['set_srid'] = 'http://opengis.org/operations/set_srid'
    dict['set_x'] = 'http://opengis.org/operations/set_x'
    dict['set_y'] = 'http://opengis.org/operations/set_y'
    dict['set_z'] = 'http://opengis.org/operations/set_z'
    dict['simple'] = 'http://opengis.org/operations/simple'
    dict['simplify'] = 'http://opengis.org/operations/simplify'
    dict['srid'] = 'http://opengis.org/operations/srid'
    dict['srs'] = 'http://opengis.org/operations/srs'
    dict['sym_difference'] = 'http://opengis.org/operations/sym_difference'
    dict['touches'] = 'http://opengis.org/operations/touches'
    dict['transform'] = 'http://opengis.org/operations/transform'
    dict['tuple'] = 'http://opengis.org/operations/tuple'
    dict['union'] = 'http://opengis.org/operations/union'
    dict['valid'] = 'http://opengis.org/operations/valid'
    dict['valid_reason'] = 'http://opengis.org/operations/valid_reason'
    dict['within'] = 'http://opengis.org/operations/within'
    dict['wkb'] = 'http://opengis.org/operations/wkb'
    dict['wkt'] = 'http://opengis.org/operations/wkt'
    dict['x'] = 'http://opengis.org/operations/x'
    dict['y'] = 'http://opengis.org/operations/y'
    dict['z'] = 'http://opengis.org/operations/z'

    dict['distance_gt'] = 'http://opengis.org/operations/distance_gt'
    dict['overlaps_right'] = 'http://opengis.org/operations/overlaps_right'
    dict['contained'] = 'http://opengis.org/operations/contained'
    dict['distance_lt'] = 'http://opengis.org/operations/distance_lt'
    dict['dwithin'] = 'http://opengis.org/operations/dwithin'
    dict['bboverlaps'] = 'http://opengis.org/operations/bboverlaps'
    dict['bbcontains'] = 'http://opengis.org/operations/bbcontains'
    dict['distance_gte'] = 'http://opengis.org/operations/distance_gte'
    dict['overlaps_below'] = 'http://opengis.org/operations/overlaps_below'
    dict['overlaps_above'] = 'http://opengis.org/operations/overlaps_above'
    dict['overlaps_left'] = 'http://opengis.org/operations/overlaps_left'
    dict['contains_properly'] = 'http://opengis.org/operations/contains_properly'
    dict['isvalid'] = 'http://opengis.org/operations/isvalid'
    dict['right'] = 'http://opengis.org/operations/right'
    dict['exact'] = 'http://opengis.org/operations/exact'
    dict['covers'] = 'http://opengis.org/operations/covers'
    dict['strictly_below'] = 'http://opengis.org/operations/strictly_below'
    dict['left'] = 'http://opengis.org/operations/left'
    dict['same_as'] = 'http://opengis.org/operations/same_as'
    dict['coveredby'] = 'http://opengis.org/operations/coveredby'
    dict['strictly_above'] = 'http://opengis.org/operations/strictly_above'



    return dict

def vocabulary(a_key):
    """
    Returns a string with a url pointing to a vocabulary that explains
    what is 'a_key'. Exemple: if a_key is 'float' returns 'http://schema.org/Float'
    :param a_key:
    :return:
    """
    return vocabularyDict()[a_key] if a_key in vocabularyDict() else None

class SupportedProperty():
    """
    SupportedProperty é uma classe
    que implementa o vocabulário do Hydra,
    que define informações sobre cada atributo
    de cada classe de modelo na aplicação.
    Ela define, como podemos ver no construtor abaixo,
    se uma determinada propriedade é um identificador (ID),
    se é possível escrevê⁻la u se esta é somente leitura, etc
    """
    def __init__(self, property_name='', required=False, readable=True, writeable=True, is_unique=False, is_identifier=False, is_external=False ):
        self.property_name = property_name
        self.required = required
        self.readable = readable
        self.writeable = writeable
        self.is_unique = is_unique
        self.is_identifier = is_identifier
        self.is_external = is_external


    def context(self):
        """
        Retorna um dicionário que mostra informações de uma
        determinada propriedade suportada por uma determinada classe,
        como se esta é uma propriedade obrigatória (required) por exemplo
        :return:
        """

        return {
            "@type": "SupportedProperty",
            "hydra:property": self.property_name,
            "hydra:writeable": self.writeable,
            "hydra:readable": self.readable,
            "hydra:required": self.required,
            "isUnique": self.is_unique,
            "isIdentifier": self.is_identifier,
            "isExternal": self.is_external
        }

class SupportedOperation():
    def __init__(self, operation='', title='', method='', expects='', returns='', type='', link=''):
        self.method = method  # the method to start this operation (GET, POST, HEAD, etc)
        self.operation = operation  # the operation definition
        self.title = title  # the operation name
        self.expects = expects  # the expected parameters to this operation
        self.returns = returns  # what this operations returns (float, int, str, etc)
        self.type = type
        self.link = link # the link to the explanation of what this operation is

    def context(self):
        return {
                "hydra:method": self.method,
                "hydra:operation": self.operation,
                "hydra:expects": self.expects,
                "hydra:returns": self.returns,
                "hydra:statusCode": '',
                "@id": self.link
        }


def initialize_dict():
    """
    Returns a dict whose each index is a geometric type and
    his respective value is another dict with geometric operations
    corresponding to this type. A example is showned below:
    # dict
    # {
    #   GeometryField: {
    #       'area' : Type_Called( ... ),
    #       'boundary' : Type_Called( ... ),
    #       'buffer' : Type_Called( ... ),
    #   },
    #   GEOSGeometry { ... },
    #    ...
    # }
    :return:
    """
    dict = {}
    oc = BaseOperationController()
    dict[GeometryField] = oc.geometry_operations_dict()
    dict[GEOSGeometry] = oc.geometry_operations_dict()
    dict[Point] = oc.point_operations_dict()
    dict[Polygon] = oc.polygon_operations_dict()
    dict[LineString] = oc.line_operations_dict()
    dict[MultiPoint] = oc.point_operations_dict()
    dict[MultiPolygon] = oc.polygon_operations_dict()
    dict[MultiLineString] = oc.line_operations_dict()
    dict[GeometryCollection] = oc.geometry_operations_dict()
    return dict


class ContextResource:

    def __init__(self):
        self.basic_path = None
        self.complement_path = None
        self.host = None
        self.dict_context = None
        self.resource = None

    #def attribute_name_list(self):
    #    return ( field.attname for field in self.model_class._meta.fields[:])

    #def attribute_type_list(self):
    #    return ( type(field) for field in self.model_class._meta.fields[:])

    def get_context_for_object(an_object):

        if isinstance(AbstractResource, an_object):
            return an_object.context()
        if  isinstance(GEOSGeometry, an_object):
            return None
    def host_with_path(self):
        return self.host + self.basic_path + "/" + self.complement_path

    def operation_names(self):
        """
        Retorna todos o valores de todos os métodos
        do objeto ContextResource que não sejam privados
        :return:
        """
        return [method for method in dir(self) if callable(getattr(self, method)) and self.is_not_private(method)]

    def attribute_contextualized_dict_for(self, field):
        """
        Returns a dict that says what this attribute is (@id) and
        what is his type (@type)
        :param field:
        :return:
        """
        #Exemple: if field.name is 'name' returns 'http://schema.org/name'
        voc = vocabulary(field.name)
        #Example: if voc_type is str returns 'http://schema.org/Text'
        voc_type = vocabulary(type(field))
        # 'voc' will be the @id if this is not None, otherwise 'voc_type' will be the @id
        res_voc = voc if voc is not None else voc_type
        # if isn't possible to define what is field.name, we consider that field.name is a 'Thing'
        if res_voc is None:
            res_voc  = "http://schema.org/Thing"
        #return res_voc #{ "@id": res_voc, "@type": "@id"}
        return {'@id': res_voc, '@type':  voc_type }

    def attributes_contextualized_dict(self):
        """
        Return a dict whose each key is the name of the model field
        and his respective value is a another dict containing the @id and
        @type for each respective model field
        :return:
        """
        dic_field = {}

        # AbstractResouce.fields_to_web() returns a list of model fields
        fields = self.resource.fields_to_web()
        for field_model in fields:
            dic_field[field_model.name] = self.attribute_contextualized_dict_for(field_model)
        return dic_field

    def selectedAttributeContextualized_dict(self, attribute_name_array):
        """
        Receives a list of model attributes and return this data in a dict form
        whose each these attribute is the dict key and his respective value
        is another dict with the identification of this attribute (@id) and
        the type of this attribute (@type)
        :param attribute_name_array:
        :return:
        """
        # list(ContextResource.attributes_contextualized_dict().items()) gets a list whose
        # each element is a tuple with the model attribute and his respective value
        return {k: v for k, v in list(self.attributes_contextualized_dict().items()) if k in attribute_name_array}

    def supportedPropertyFor(self, field):
        voc = vocabulary(field.name)
        res_voc = voc if voc is not None else vocabulary(type(field))
        return { "@id": res_voc, "@type": "@id"}

    def identifier_field_or_None(self):
        fields = self.resource.fields_to_web()
        for field in fields:
             if field.primary_key is True:
                 return field
        return None

    def representationName(self):
        ide_field = self.identifier_field_or_None()
        if ide_field is not None:
            return  {"hydra:property":ide_field.name , "@type": "SupportedProperty"}
        return {}

    def supportedProperties(self):
        arr_dict = []
        if self.resource is None:
            return []
        fields = self.resource.fields_to_web()
        for field in fields:
            arr_dict.append(SupportedProperty(property_name=field.name, required=field.null, readable=True, writeable=True, is_unique=False, is_identifier=field.primary_key, is_external=False))
        return [supportedAttribute.context() for supportedAttribute in arr_dict]

    def supportedOperationsFor(self, object, object_type=None):
        """
        Returns a list of dicts. Each list element is a dict containing a vocabulary for a geometric operation
        This dict is result of all possible operations for the 'object_type'
        :param object:
        :param object_type:
        :return:
        """
        # initialize_dict() gets a dict with geometric types as keys and dict of geometric operations as values
        dict = initialize_dict()
        # 'a_type' is the type of the field ('object_type') or the type of his value (type(object))
        a_type = object_type if object_type is not None else type(object)
        # if 'a_type' correspond to a operations dict key, gets the dict correnponding to this key
        # remember: 'dict' is a dict of geometric operations dict
        dict_operations = dict[a_type] if a_type in dict else {}
        # dict_operations will be something like this:
        # GeometryField: {
        #    'area' : Type_Called( {
        #                            'name': 'area',
        #                            'parameters': [],
        #                            'return_type': float
        #                           } ),
        #    'boundary' : Type_Called( ... ),
        #    'buffer' : Type_Called( ... ),
        #    ...
        # }
        arr = []
        # basically, the for loop bellow will get the vocabulary to each element in the Type_Called
        # value that corresponds to the operation like 'area', 'boundary', etc.
        for k, v_typed_called in dict_operations.items():
            # 'exps' will be a empty list if 'Type_Called.parameters' is None or
            # a vocabulary list (one vocabulary per parameters item) otherwise
            # ex: if Type_Called.parrameters == ['name', 'user', 'responsible]
            # 'exps' will be ['http://schema.org/name', 'http://schema.org/Person', ''http://schema.org/accountablePerson']
            exps = [] if v_typed_called.parameters is None else [vocabulary(param) for param in v_typed_called.parameters]
            # if 'Type_Called.return_type' correspond to a vocabulary dict key,
            # gets the corresponding vocabulary to this return type, or "NOT FOUND" otherwise
            rets = (vocabulary(v_typed_called.return_type) if v_typed_called.return_type in vocabularyDict()  else ("NOT FOUND"))
            # gets the vocabulary to the Type_Called.name
            link_id = vocabulary(v_typed_called.name)
            # mounts a SupportedOperation object with the vocabularies above and adds to array
            arr.append( SupportedOperation(operation=v_typed_called.name, title=v_typed_called.name, method='GET', expects=exps, returns=rets, type='', link=link_id))

        # SupportedOperations.context() returns the vocabulary for a SupportedOperation object in a dict form
        return [supportedOperation.context() for supportedOperation in arr]

    def supportedOperations(self):

        arr = []
        if self.resource is None:
            return []
        for k, v_typed_called in self.resource.operations_with_parameters_type().items():
            exps = [] if v_typed_called.parameters is None else [vocabulary(param) for param in v_typed_called.parameters]
            if v_typed_called.return_type in vocabularyDict():
                rets = vocabulary(v_typed_called.return_type)
            else:
                rets = "NOT FOUND"
            link_id = vocabulary(v_typed_called.name)
            arr.append( SupportedOperation(operation=v_typed_called.name, title=v_typed_called.name, method='GET', expects=exps, returns=rets, type='', link=link_id))

        return [supportedOperation.context() for supportedOperation in arr]

    def iriTemplates(self):
        iri_templates = []
        dict = {}
        dict["@type"] = "IriTemplate"
        dict["template"] = self.host_with_path() + "{list*}"  # Ex.: http://host/unidades-federativas/nome,sigla,geom
        dict["mapping"] = [ {"@type": "iriTemplateMapping", "variable": "list*", "property": "hydra:property", "required": True}]

        iri_templates.append(dict)

        return {"iri_templates": iri_templates}

    def set_context_to_attributes(self, attributes_name):
        """
        Receives a list of model attribute names, gets a dict whose
        his keys is the name of each model attribute and his respective
        value is another dict containing the definition (@id) and the type (@type) of the
        attribute. This method store this dict as value of the "@context" key
        The resulting structure is then stored in the ContextResource.dic_context
        OBS: this dict, like the all Context can be accessed by the resource view
        The final dict is showned below:
        #{
        #    "@context": {
        #        "name" : {"@id": "http://schema.org/name", "@type": "http://schema.org/Text"},
        #        "nomeAbrev" : {"@id": "https://schema.org/alternateName", "@type": "http://schema.org/Text"},
        #        ...
        #    }
        #}
        :param attributes_name:
        :return:
        """
        self.dict_context = {}
        # ContextResource.selectedAttributeContextualized_dict() returns a dict like this:
        # {
        #   "name" : {"@id": "http://schema.org/name", "@type": "http://schema.org/Text"},
        #   "nomeAbrev" : {"@id": "https://schema.org/alternateName", "@type": "http://schema.org/Text"},
        #   ...
        # }
        self.dict_context["@context"] = self.selectedAttributeContextualized_dict(attributes_name)

    def set_context_to_only_one_attribute(self, object, attribute_name, attribute_type=None):
        """
        Receives a object model and a attribute for this, set the context for this attribute
        and, if this attribute (or his value) is a geometric type, also set a context explaining
        all the possible operetions for this attribute
        :param object - a object model:
        :param attribute_name - a name corresponding a object model attribute:
        :param attribute_type - the field of object model:
        :return:
        """
        # do the same process for multiple field but this time has only one
        self.set_context_to_attributes([attribute_name])

        # the entire code below has the objective to determinate if this field (or his value) is a geometric object,
        # if this is True we set a context explining all the possible operation for this field
        # 'obj' is the value of the model field representated by 'attribute_name' (possibly is another object)
        obj = getattr(object, attribute_name, None)
        # 'a_type' is the models field if this is not None or the type of the field value otherwise
        a_type = attribute_type if attribute_type is not None else type(obj)
        isGeometry = isinstance(obj, GEOSGeometry) or isinstance(attribute_type, GeometryField)

        # if the field value is a GEOSGeometry or if the field is a GeometryField
        # sets another index in ContextResource.dict_context
        if isGeometry:
            self.dict_context["hydra:supportedOperations"] = self.supportedOperationsFor(obj, a_type)

    def set_context_to_operation(self, object, operation_name):
        """
        Set a context to the object operation (defined in operation_name)
        in ContextResource.dict_context
        :param object:
        :param operation_name:
        :return:
        """
        self.dict_context = {}
        dict = {}

        # vocabulary() returns a string representing the definition of the operations named in 'operation_name'
        # If 'operation_name' is 'area', dict will be something like this:
        # {
        #   "@id": "http://opengis.org/operations/area",
        #   "@type": "@id"
        # }
        dict [operation_name] = { "@id": vocabulary(operation_name),"@type": "@id" }
        # dict will be the value of the key "@context" in ContextResource.dict_context
        self.dict_context["@context"] = dict
        isGeometry = isinstance(object, GEOSGeometry)
        if isGeometry:
            self.dict_context["hydra:supportedOperations"] = self.supportedOperationsFor(object, type(object))

    def set_context_to_object(self, object, attribute_name):
        self.dict_context = {}
        self.dict_context["@context"] = self.selectedAttributeContextualized_dict([attribute_name])
        if len(self.dict_context["@context"]) == 0:
            self.set_context_to_operation(object, attribute_name)
        else:
            self.dict_context["hydra:supportedOperations"] = self.supportedOperationsFor(object, type(object))

    def initalize_context(self):
        self.dict_context = {}
        self.dict_context["@context"] = self.attributes_contextualized_dict()
        self.dict_context["hydra:supportedProperties"] = self.supportedProperties()
        self.dict_context["hydra:supportedOperations"] = self.supportedOperations()
        self.dict_context["hydra:representationName"] = self.representationName()
        self.dict_context["hydra:iriTemplate"] = self.iriTemplates()

        return self.dict_context

    def context(self):
        if self.dict_context is None:
            self.initalize_context()
        return self.dict_context

    def set_context_(self, dictionary):
        self.dict_context = dictionary

class FeatureResouceContext(ContextResource):


    def iri_template_contextualized_dict(self):
        pass


class FeatureCollectionResourceContext(FeatureResouceContext):
    pass

class AbstractCollectionResourceContext(ContextResource):
    pass