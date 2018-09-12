
import re
from bcim import serializers


class AbstractResource:
    def __init__(self):
        self.entry_point = {}
        self.model = None
        self.serializer_class = None

        self._result_set = None

        self.identifier_patterns = {}

    def set_filter(self, query_set=None):
        self._result_set = self.model.objects.filter(query_set)

        return self

    def result_set(self):
        if not self._result_set:
            self._result_set = self.model.objects.all()

        return self._result_set

    def serialize(self, **kwargs):
        obj = self.serializer_class(self.result_set(), many=True, context={'request': kwargs['request']})

        return obj.data

    def find_implicit_field(self, data):
        for pattern, action in self.identifier_patterns.items():
            if action(data):
                return pattern

        return None  # raise error


class UnidadeFederacaoResource(AbstractResource):
    def __init__(self):
        super().__init__()

        self.serializer_class = serializers.UnidadeFederacaoSerializer
        self.model = self.serializer_class.Meta.model

        self.identifier_patterns = {
            'id_objeto': lambda s: re.match(r'^[0-9]{3,}$', s),
            'geocodigo': lambda s: re.match(r'^[0-9]{2}$', s),
            'sigla': lambda s: re.match(r'^[A-Za-z]{2}$', s),
        }

