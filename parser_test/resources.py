
# coding: utf-8

import re
from bcim import serializers
from abc import ABC, abstractmethod


class AbstractResource(ABC):
    @abstractmethod
    def serialize(self, **kwargs):
        pass

    def context(self):
        pass


# Toda coleção é iterável então implemetar __len__, __getitem__, __setitem__, __delitem__, __iter__
class AbstractCollectionResource(AbstractResource):
    @abstractmethod
    def filter(self, conditions=None):
        pass

    @abstractmethod
    def projection(self, *fields):
        pass


class CollectionResource(AbstractCollectionResource):
    def __init__(self, data_set=None):
        super().__init__()
        self.data_set = data_set

    def serialize(self, **kwargs):
        return list(self.data_set)

    def filter(self, conditions=None):
        pass

    def projection(self, *fields):
        pass


class SpatialResource(AbstractResource):
    def serialize(self, **kwargs):
        pass


class FeatureResource(SpatialResource):
    def serialize(self, **kwargs):
        pass

    def projection(self, *fields):
        pass


class FeatureCollectionResource(AbstractCollectionResource):
    def serialize(self, **kwargs):
        from django.core import serializers
        return serializers.serialize('geojson', self._result_set, geometry_field='geom')

    def find_implicit_field(self, data):
        for pattern, action in self.identifier_patterns.items():
            if action(data):
                return pattern

        return None  # raise error

    def filter(self, conditions=None):
        pass

    def projection(self, *fields):
        pass


class ContextResource(AbstractResource):
    pass




class UnidadeFederacaoResource(FeatureCollectionResource):
    def __init__(self):
        super().__init__()

        self.serializer_class = serializers.UnidadeFederacaoSerializer
        self.model = self.serializer_class.Meta.model
        self._result_set = self.model.objects.all()
        self._projected_fields = []

        self.identifier_patterns = {
            'id_objeto': lambda s: re.match(r'^[0-9]{3,}$', s),
            'geocodigo': lambda s: re.match(r'^[0-9]{2}$', s),
            'sigla': lambda s: re.match(r'^[A-Za-z]{2}$', s),
        }

    def result_set(self):
        if self._result_set is None:
            self._result_set = self.model.objects.all()

        return self._result_set

    def serialize(self, **kwargs):
        fields=('id_objeto', *self._projected_fields) if self._projected_fields else None

        obj = self.serializer_class(self.result_set(), fields=fields, many=True, context={'request': kwargs['request']})

        return obj.data

    def projection(self, *fields):
        if 'geom' in fields:
            #self._result_set = self._result_set.values('id_objeto', *fields)
            self._projected_fields = fields
            return self

        projected = self._result_set.values(*fields)

        return CollectionResource(projected)

    def filter(self, conditions=None):
        if conditions:
            self._result_set = self._result_set.filter(conditions)

        return self


class ProxyResource:
    def __init__(self, resource):
        super().__init__()
        self._resource = resource

    # Aqui eu intercepto a chamada de método para o recurso
    # e substituo a referencia quando o método chamado retorna
    # um objeto que é subclasse de AbstractResource
    def __getattr__(self, name):
        def wrapper(*args, **kwargs):
            ref = getattr(self._resource, name)

            if callable(ref):
                obj = ref(*args, **kwargs)
                if issubclass(type(obj), AbstractResource):
                    self._resource = obj

                return obj

            return ref

        return wrapper

    def serialize(self, **kwargs):
        return self._resource.serialize(**kwargs)