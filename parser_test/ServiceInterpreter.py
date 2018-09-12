
from abc import abstractmethod


class ServiceInterpreter:
    @abstractmethod
    def build(self, description):
        pass
