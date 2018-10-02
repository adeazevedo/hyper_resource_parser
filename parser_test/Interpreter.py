
import lark


class Interpreter(lark.visitors.Interpreter):

    PRIORITY_ENTRY_POINT_COMMAND = 1
    PRIORITY_IMPLICIT_FILTER_COMMAND = 4
    PRIORITY_FILTER_COMMAND = 5
    PRIORITY_PROJECTION_COMMAND = 10

    def __init__(self, implementation):
        self._implementation = implementation

        self.queue = PriorityQueue()

    def interpret(self, syntatic_tree):
        return self.visit(syntatic_tree)

    def api_path(self, tree):
        api = tree.children.pop(0)

        entry_point_name = self.entry_point(tree.children.pop(0))
        resource_name = self.resource_locator(tree.children.pop(0))

        self.queue.add_task(('entry_point', lambda: self._implementation.build_resource(entry_point_name, resource_name)),
                            self.PRIORITY_ENTRY_POINT_COMMAND)

        # Expression chain interpretation
        for child in tree.children:
            self.visit(child)

        # implementation query the commands
        resource = self._implementation.build(self.queue)

        return resource

    def entry_point(self, tree):
        name = self.id(tree.children.pop(0))
        return name

    def resource_locator(self, tree):
        resource_name = self.id(tree.children.pop(0))

        if tree.children:
            implicit_id = self.implicit_expression(tree.children.pop(0))
            command = lambda: self._implementation.build_implicit_filter(implicit_id)
            self.queue.add_task(('implicit_filter', command), self.PRIORITY_IMPLICIT_FILTER_COMMAND)

        return resource_name

    def expression_chain(self, tree):
        filter_description = []

        for child in tree.children:
            if child.data == 'filter':
                filter_ = self.filter(child)
                filter_description.append(filter_)

            elif child.data == 'projection':
                projection = self.projection(child)

                command = lambda: self._implementation.exec_function('projection', *projection)
                self.queue.add_task(('projection', command), self.PRIORITY_PROJECTION_COMMAND)

        if filter_description:
            command = lambda: self._implementation.build_filter(filter_description)
            self.queue.add_task(('filter', command), self.PRIORITY_FILTER_COMMAND)

    def filter(self, tree):
        result = self.visit_children(tree)
        return result[0]

    def projection(self, tree):
        result = self.visit_children(tree)
        return result[0] if isinstance(result[0], list) else [result[0]]

    def logical_expression(self, tree):
        result = self.visit(tree.children.pop(0))
        return result

    def or_expression(self, tree):
        results = self.visit_children(tree)
        return OrFilter(results)

    def and_expression(self, tree):
        results = self.visit_children(tree)
        return AndFilter(results)

    def not_expression(self, tree):
        expr = self.visit(tree.children.pop(0))
        return NotFilter(expr)

    def simple_expression(self, tree):
        return SimpleExpr().transform(tree)

    def between_expression(self, tree):
        return BetweenExpr().transform(tree)

    def null_comparison(self, tree):
        return NullExpr().transform(tree)

    def implicit_expression(self, tree):
        id_or_number = self.visit(tree.children.pop(0))
        return id_or_number

    def id_list(self, tree):
        return self.visit_children(tree)

    def id(self, tree):
        return str(tree.children.pop(0))

    def number(self, tree):
        return str(tree.children.pop(0))

    def object_id(self, tree):
        return int(tree.children.pop(0))


class BaseTransformer(lark.visitors.InlineTransformer):
    id = lambda self, item: str(item)
    number = lambda self, item: str(item)
    id_list = lambda self, *items: list(items)
    number_list = lambda self, *items: list(items)

    operator = lambda self, *items: str(items[0])
    null_operator = lambda self, *items: str(items[0])


class SimpleExpr(BaseTransformer):
    def simple_expression(self, *items):
        return items


class BetweenExpr(BaseTransformer):
    def between_expression(self, *items):
        field = items[0]
        operator = items[1]
        values = items[2:]

        return field, operator, values


class NullExpr(BaseTransformer):
    def null_comparison(self, *items):
        field = items[0]
        operator = self.operator(items[1])

        return field, operator


# Filter class is a Composite pattern. And, Or and Not Filter classes apply this pattern
class Filter:
    def __init__(self):
        self.children = []

    def add(self, component):
        if component is None:
            return

        self.children.append(component)

    def remove(self, component):
        if component is None:
            return

        index = self.children.index(component)

        self.children.pop(index)

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return str(self.children)


class AndFilter(Filter):
    def __init__(self, list_expr):
        super().__init__()
        self.operation = 'and'

        for expr in list_expr:
            self.add(expr)

    def __str__(self):
        return '(' + ' AND '.join([str(child) for child in self.children]) + ')'


class OrFilter(Filter):
    def __init__(self, list_expr):
        super().__init__()
        self.operation = 'or'

        for expr in list_expr:
            self.add(expr)

    def __str__(self):
        return '(' + ' OR '.join([str(child) for child in self.children]) + ')'


class NotFilter(Filter):
    def __init__(self, expr):
        super().__init__()
        self.operation = 'not'

        self.add(expr)

    def __str__(self):
        return ' NOT ' + str(self.children[0])



import heapq, itertools

class PriorityQueue:
    def __init__(self):
        self.priority_queue = []
        self.entry_finder = {}  # mapping of tasks to entries
        self.REMOVED = '<removed-task>'  # placeholder for a removed task
        self.counter = itertools.count()  # unique sequence count

    def add_task(self, task, priority=0):
        #'Add a new task or update the priority of an existing task'
        if task in self.entry_finder:
            self.remove_task(task)

        count = next(self.counter)
        entry = [priority, count, task]
        self.entry_finder[task] = entry
        heapq.heappush(self.priority_queue, entry)

    def remove_task(self, task):
        #'Mark an existing task as REMOVED.  Raise KeyError if not found.'
        entry = self.entry_finder.pop(task)
        entry[-1] = self.REMOVED

    def pop_task(self):
        'Remove and return the lowest priority task. Raise KeyError if empty.'
        while self.priority_queue:
            priority, count, task = heapq.heappop(self.priority_queue)

            if task is not self.REMOVED:
                del self.entry_finder[task]
                return task

        return None
