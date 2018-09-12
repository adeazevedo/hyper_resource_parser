
from abc import abstractmethod

from hyper_resource.HyperResource import HyperResource


class ContextInterpreter:

    @abstractmethod
    def build(self, description):
        pass


class DjangoContextInterpreter(ContextInterpreter):

    def build(self, description):
        resource_class = HyperResource.query(description['entry_point'], description['resource'])

        resource = resource_class()

        resource.context

        return self.resource
