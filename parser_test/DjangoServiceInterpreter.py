
from operator import or_, and_, invert
from functools import reduce
import pprint

from django.db.models import Q

from hyper_resource.HyperResource import HyperResource
from parser_test.ServiceInterpreter import ServiceInterpreter


class DjangoServiceInterpreter(ServiceInterpreter):
    def __init__(self):
        super().__init__()

        self.resource = None

    # Overridden
    # Method used by Interpreter obj
    def build(self, description):
        resource_class = HyperResource.query(description['entry_point'], description['resource'])

        self.resource = resource_class()

        if 'implicit_filter' in description:
            data = description['implicit_filter']
            field = self.resource.find_implicit_field(data)

            desc = (field, 'eq', data)

            self.resource.set_filter(Filter.to_q(desc))

        elif description['filter']:
            self.resource.set_filter(self.build_filter(description['filter']))

        return self.resource

    def build_filter(self, representation):
        if not representation:
            return Q()

        q_list = [Q()]
        # User can chain several filter in url, so transform all in Q Object and unite with and expr
        for expr in representation:
            q_list.append(self.process_logic(expr))

        q_objects_query = reduce(Filter.and_, q_list)

        return q_objects_query

    def process_logic(self, logic_tree):
        # If is a tuple, transform into Q Object
        if isinstance(logic_tree, tuple):
            return Filter.to_q(logic_tree)

        # Recursively transform non-tuples in Q Objects
        for i, expr in enumerate(logic_tree.children):
            if not isinstance(expr, tuple):
                logic_tree.children[i] = self.process_logic(expr)

        # Decide which execution to do based on expression type
        switch = {
            'or': lambda or_expr_list: reduce(Filter.or_, or_expr_list),
            'and': lambda and_expr_list: reduce(Filter.and_, and_expr_list),
            'not': lambda not_expr: Filter.not_(not_expr[0]),
            'default': lambda expr: Filter.to_q(expr[0])
        }

        callback = switch.get(logic_tree.operation) or switch['default']
        return callback(logic_tree.children)


class Filter:
    @staticmethod
    def to_q(tup):
        # tup is already Q instance then return itself
        if isinstance(tup, Q):
            return tup

        if tup is None:
            return Q()

        field = tup[0]
        operator = tup[1]
        values = tup[2] if len(tup) > 2 else ''

        # Case operator is 'not' or 'not/in' turn values into a list if it is not
        if operator in ['in', 'not/in']:
            values = [tup[2]] if not isinstance(tup[2], list) else []

        switch = {
            'eq': Q(**{field: values}),
            'neq': ~Q(**{field: values}),
            'gt': Q(**{field + '__gt': values}),
            'gte': Q(**{field + '__gte': values}),
            'lt': Q(**{field + '__lt': values}),
            'lte': Q(**{field + '__lte': values}),
            'like': Q(**{field + '__contains': values}),
            'in': Q(**{field + '__in': values}),
            'not/in': ~Q(**{field + '__in': values}),
            'between': Q(**{field + '__range': values}),
            'isnull': Q(**{field + '__isnull': True}),
            'isnotnull': Q(**{field + '__isnull': False})
        }
        q_object = switch.get(operator)
        return q_object

    @staticmethod
    def or_(a, b=Q()):
        return or_(Filter.to_q(a), Filter.to_q(b))

    @staticmethod
    def and_(a, b=Q()):
        return and_(Filter.to_q(a), Filter.to_q(b))

    @staticmethod
    def not_(other):
        return invert(Filter.to_q(other))



