
import lark

from rest_framework.views import APIView
from rest_framework.response import Response

from parser_test.Interpreter import Interpreter

from parser_test.DjangoServiceAdapter import DjangoServiceAdapter


ACCESS_CONTROL_ALLOW_METHODS = ['GET', 'OPTIONS', 'HEAD']

CORS_ALLOW_HEADERS = [
    'accept',
    'accept-encoding',
    'authorization',
    'content-type',
    'content-location',
    'dnt',
    'origin',
    'user-agent',
    'x-csrftoken',
    'x-requested-with',
    'link',
]

CORS_EXPOSE_HEADERS = [
    'accept',
    'accept-encoding',
    'authorization',
    'content-type',
    'content-location',
    'dnt',
    'origin',
    'user-agent',
    'x-csrftoken',
    'x-requested-with',
    'x-access-token',
    'access-control-allow-origin',
    'link',
]


class HyperView(APIView):
    def __init__(self):
        super(HyperView, self).__init__()

    def parser(self, url):
        parser = lark.Lark(open('grammar.lark'))
        url = url.strip('/')

        tree = parser.parse(url)
        print(tree.pretty())

        return tree

    def add_cors_headers(self, response):
        response['access-control-allow-origin'] = '*',
        response['access-control-allow-methods'] = ', '.join(ACCESS_CONTROL_ALLOW_METHODS),
        response['access-control-allow-headers'] = ', '.join(CORS_ALLOW_HEADERS),
        response['access-control-expose-headers'] = ', '.join(CORS_EXPOSE_HEADERS)

        return response

    def get(self, request, *args, **kwargs):
        tree = self.parser(request.path)

        django_interp = DjangoServiceAdapter()
        interpreter = Interpreter(django_interp)
        #interpreter = ServiceInterpreter()

        resource = interpreter.interpret(tree)

        response = Response(resource.serialize(request=request))
        self.add_cors_headers(response)

        return response

    # def options(self, request, *args, **kwargs):
    #     tree = self.parser(request.path)
    #
    #     django_interp = DjangoContextInterpreter()
    #     interpreter = Interpreter(django_interp)
    #
    #     resource = interpreter.interpret(tree)
    #
    #     response = Response(resource.serialize(request=request))
    #     self.add_cors_headers(response)
    #
    #     return response
