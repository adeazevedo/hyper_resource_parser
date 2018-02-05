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
    dic = {}

    dic[BooleanField] = 'http://schema.org/Boolean'
    dic[bool] = 'http://schema.org/Boolean'
    dic[True] = 'http://schema.org/Boolean'
    dic[False] = 'http://schema.org/Boolean'
    dic[FloatField] = 'http://schema.org/Float'
    dic[float] = 'http://schema.org/Float'
    dic[ForeignKey] = 'http://schema.org/Integer'
    dic[IntegerField] = 'http://schema.org/Integer'
    dic[AutoField]= 'http://schema.org/Integer'
    dic[int] = 'http://schema.org/Integer'
    dic[CharField] = 'http://schema.org/Text'
    dic[TextField] = 'http://schema.org/Text'
    dic[str] = 'http://schema.org/Text'
    dic[DateField] = 'http://schema.org/Date'
    dic[date] = 'http://schema.org/Date'
    dic[DateTimeField] = 'http://schema.org/DateTime'
    dic[datetime] = 'http://schema.org/DateTime'
    dic[TimeField] = 'http://schema.org/Time'
    dic[Model] = 'http://geojson.org/geojson-ld/vocab.html#Feature'
    dic[tuple]= 'http://schema.org/ListItem'

    dic[Q] = 'http://extension.schema.org/expression'
    dic[object] = 'http://schema.org/Thing'

    dic['nome'] = 'http://schema.org/name'
    dic['name'] = 'http://schema.org/name'
    dic['nomeAbrev'] = 'https://schema.org/alternateName'
    dic['responsible'] = 'http://schema.org/accountablePerson'
    dic['usuario'] = 'http://schema.org/Person'
    dic['user'] = 'http://schema.org/Person'

    dic['FeatureCollection'] = 'http://geojson.org/geojson-ld/vocab.html#FeatureCollection'
    dic[GeometryField] = 'http://geojson.org/geojson-ld/vocab.html#geometry'
    dic[PointField] = 'http://geojson.org/geojson-ld/vocab.html#Point'
    dic[LineStringField] = 'http://geojson.org/geojson-ld/vocab.html#LineString'
    dic[PolygonField] = 'http://geojson.org/geojson-ld/vocab.html#Polygon'
    dic[MultiPolygonField] = 'http://geojson.org/geojson-ld/vocab.html#MultiPolygon'
    dic[MultiLineStringField] = 'http://geojson.org/geojson-ld/vocab.html#MultiLineString'
    dic[MultiPointField] = 'http://geojson.org/geojson-ld/vocab.html#MultiPoint'

    dic[MultiPolygon] = 'http://geojson.org/geojson-ld/vocab.html#MultiPolygon'
    dic[Polygon] = 'http://geojson.org/geojson-ld/vocab.html#Polygon'
    dic[LineString] = 'http://geojson.org/geojson-ld/vocab.html#LineString'
    dic[Point] = 'http://geojson.org/geojson-ld/vocab.html#Point'
    dic[GEOSGeometry] = 'http://geojson.org/geojson-ld/vocab.html#geometry'
    dic[OGRGeometry] = 'http://geojson.org/geojson-ld/vocab.html#geometry'
    dic[MultiLineString] = 'http://geojson.org/geojson-ld/vocab.html#MultiLineString'
    dic[MultiPoint] = 'http://geojson.org/geojson-ld/vocab.html#MultiPoint'
    dic[GeometryCollection] = 'http://geojson.org/geojson-ld/vocab.html#GeometryCollection'
    dic[SpatialReference] = 'http://geojson.org/geojson-ld/vocab.html#SpatialReference'



    #collection
    dic['filter'] = 'http://opengis.org/operations/filter'
    dic['map'] = 'http://opengis.org/operations/map'
    dic['annotate'] = 'http://opengis.org/operations/annotate'

    dic['area'] = 'http://opengis.org/operations/area'
    dic['boundary'] = 'http://opengis.org/operations/boundary'
    dic['buffer'] = 'http://opengis.org/operations/buffer'
    dic['centroid'] = 'http://opengis.org/operations/centroid'
    dic['contains'] = 'http://opengis.org/operations/contains'
    dic['convex_hull'] = 'http://opengis.org/operations/convex_hull'
    dic['coord_seq'] = 'http://opengis.org/operations/coord_seq'
    dic['coords'] = 'http://opengis.org/operations/coords'
    dic['count'] = 'http://opengis.org/operations/count'
    dic['crosses'] = 'http://opengis.org/operations/crosses'
    dic['crs'] = 'http://opengis.org/operations/crs'
    dic['difference'] = 'http://opengis.org/operations/difference'
    dic['dims'] = 'http://opengis.org/operations/dims'
    dic['disjoint'] = 'http://opengis.org/operations/disjoint'
    dic['distance'] = 'http://opengis.org/operations/distance'
    dic['empty'] = 'http://opengis.org/operations/empty'
    dic['envelope'] = 'http://opengis.org/operations/envelope'
    dic['equals'] = 'http://opengis.org/operations/equals'
    dic['equals_exact'] = 'http://opengis.org/operations/equals_exact'
    dic['ewkb'] = 'http://opengis.org/operations/ewkb'
    dic['ewkt'] = 'http://opengis.org/operations/ewkt'
    dic['extend'] = 'http://opengis.org/operations/extend'
    dic['extent'] = 'http://opengis.org/operations/extent'
    dic['geojson'] = 'http://opengis.org/operations/geojson'
    dic['geom_type'] = 'http://opengis.org/operations/geom_type'
    dic['geom_typeid'] = 'http://opengis.org/operations/geom_typeid'
    dic['get_coords'] = 'http://opengis.org/operations/get_coords'
    dic['get_srid'] = 'http://opengis.org/operations/get_srid'
    dic['get_x'] = 'http://opengis.org/operations/get_x'
    dic['get_y'] = 'http://opengis.org/operations/get_y'
    dic['get_z'] = 'http://opengis.org/operations/get_z'
    dic['has_cs'] = 'http://opengis.org/operations/has_cs'
    dic['hasz'] = 'http://opengis.org/operations/hasz'
    dic['hex'] = 'http://opengis.org/operations/hex'
    dic['hexewkb'] = 'http://opengis.org/operations/hexewkb'
    dic['index'] = 'http://opengis.org/operations/index'
    dic['intersection'] = 'http://opengis.org/operations/intersection'
    dic['intersects'] = 'http://opengis.org/operations/intersects'
    dic['interpolate'] = 'http://opengis.org/operations/interpolate'
    dic['json'] = 'http://opengis.org/operations/json'
    dic['kml'] = 'http://opengis.org/operations/kml'
    dic['length'] = 'http://opengis.org/operations/length'
    dic['normalize'] = 'http://opengis.org/operations/normalize'
    dic['num_coords'] = 'http://opengis.org/operations/num_coords'
    dic['num_geom'] = 'http://opengis.org/operations/num_geom'
    dic['num_s'] = 'http://opengis.org/operations/num_s'
    dic['num_points']  = 'http://opengis.org/operations/num_points'
    dic['point_on_surface'] = 'http://opengis.org/operations/point_on_surface'
    dic['ogr'] = 'http://opengis.org/operations/ogr'
    dic['overlaps'] = 'http://opengis.org/operations/overlaps'
    dic['_on_surface'] = 'http://opengis.org/operations/_on_surface'
    dic['pop'] = 'http://opengis.org/operations/pop'
    dic['prepared'] = 'http://opengis.org/operations/prepared'
    dic['relate'] = 'http://opengis.org/operations/relate'
    dic['relate_pattern'] = 'http://opengis.org/operations/relate_pattern'
    dic['ring'] = 'http://opengis.org/operations/ring'
    dic['set_coords'] = 'http://opengis.org/operations/set_coords'
    dic['set_srid'] = 'http://opengis.org/operations/set_srid'
    dic['set_x'] = 'http://opengis.org/operations/set_x'
    dic['set_y'] = 'http://opengis.org/operations/set_y'
    dic['set_z'] = 'http://opengis.org/operations/set_z'
    dic['simple'] = 'http://opengis.org/operations/simple'
    dic['simplify'] = 'http://opengis.org/operations/simplify'
    dic['srid'] = 'http://opengis.org/operations/srid'
    dic['srs'] = 'http://opengis.org/operations/srs'
    dic['sym_difference'] = 'http://opengis.org/operations/sym_difference'
    dic['touches'] = 'http://opengis.org/operations/touches'
    dic['transform'] = 'http://opengis.org/operations/transform'
    dic['tuple'] = 'http://opengis.org/operations/tuple'
    dic['union'] = 'http://opengis.org/operations/union'
    dic['valid'] = 'http://opengis.org/operations/valid'
    dic['valid_reason'] = 'http://opengis.org/operations/valid_reason'
    dic['within'] = 'http://opengis.org/operations/within'
    dic['wkb'] = 'http://opengis.org/operations/wkb'
    dic['wkt'] = 'http://opengis.org/operations/wkt'
    dic['x'] = 'http://opengis.org/operations/x'
    dic['y'] = 'http://opengis.org/operations/y'
    dic['z'] = 'http://opengis.org/operations/z'

    return dic

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
    oc = OperationController()
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
        a_type = type(object_type) if object_type is not None else type(object)
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
            rets = (vocabulary(v_typed_called.return_type) if v_typed_called.return_type in vocabularyDict()  else ("NOT FOUND"))
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
        self.dict_context["hydra:iriTemplate"] = self.iriTemplates()

        return self.dict_context

    def context(self):
        if self.dict_context is None:
            self.initalize_context()
        return self.dict_context

    def set_context_(self, dictionary):
        self.dict_context = dictionary

class FeatureContext(ContextResource):


    def iri_template_contextualized_dict(self):
        pass



class FeatureCollectionContext(FeatureContext):
    pass