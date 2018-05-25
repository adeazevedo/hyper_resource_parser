from hyper_resource.contexts import ContextResource


class SubBooleanOperatorResourceContext(ContextResource):
    def attributes_contextualized_dict(self):

        dic_context = {
                                   "in":  "http:/interfaces/in",
                                   "*in":  "http:/interfaces/in",
                                   "isnull":  "http:/interfaces/isnull",
                                   "*isnull":  "http:/interfaces/isnull",
                                   "isnotnull":  "http:/interfaces/isnull",
                                   "*inotsnull":  "http:/interfaces/inotsnull",
                                   "between":  "http:/interfaces/in",
                                   "*between":  "http:/interfaces/in",
                                   "eq":  "http://schema.org/equal",
                                   "neq":  "http://schema.org/nonEqual",
                                   "*neq":  "http://schema.org/nonEqual",
                                   "*eq":  "http://schema.org/equal",
                                   "*noeq":  "http://schema.org/nonEqual",
                                    "lt":  "http://schema.org/lesser",
                                    "*lt":  "http://schema.org/lesser",
                                   "lte":  "http://schema.org/lesserOrEqual",
                                    "*lte":  "http://schema.org/lesserOrEqual",
                                   "gt":  "http://schema.org/greater",
                                    "*gt":  "http://schema.org/greater",
                                   "gte":  "http://schema.org/greaterOrEqual",
                                    "*gte":  "http://schema.org/greaterOrEqual",

                       }

        return dic_context