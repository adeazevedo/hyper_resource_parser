from hyper_resource.contexts import ContextResource, FeatureContext, FeatureCollectionContext

class UnidadeFederacaoContext(FeatureContext):

    def attributes_contextualized_dict(self):

        dic_context = {            "id_objeto":  "http://schema.org/identifier",
                                   "nome":  "http://schema.org/name",
                                   "nomeabrev":  "http://schema.org/alternateName",
                                   "sigla": "http://schema.org/alternateName",
                                   "geometriaaproximada": "http://schema.org/Boolean",
                                   "geocodigo": "http://schema.org/code",
                                   "geom": "http://geojson.org/geojson-ld/vocab.html#geometry"
                       }

        return dic_context

    #def  supportedProperties(self):
    #dic = {"hydra:supportedProperties": [
    #    {
    #        "hydra:writeable": true, "hydra:property": "nome", "hydra:readable": true, "isIdentifier": false, "hydra:required": true, "isExternal": false, "@type": "SupportedProperty",  "isUnique": false
    #    }
    #]}
    #return dic


class UnidadeFederacaoListContext(FeatureContext):
    pass

class MunicipioListContext(FeatureContext):
    pass

class MunicipioDetailContext(FeatureContext):
    pass

class AldeiaIndigenaDetailContext(FeatureContext):
    pass

class AldeiaIndigenaListContext(FeatureContext):
    pass

class SprintContext(ContextResource):
    pass
class TaskContext(ContextResource):
    pass

class SprintListContext(FeatureContext):
    pass
class SprintDetailContext(FeatureContext):
    pass
class TaskListContext(FeatureContext):
    pass
class TaskDetailContext(FeatureContext):
    pass

class OutrasUnidProtegidasContext(FeatureContext):
    pass
class AglomeradoRuralDeExtensaoUrbanaContext(FeatureContext):
    pass
class AglomeradoRuralIsoladoContext(FeatureContext):
    pass

class TrechoFerroviarioListContext(FeatureCollectionContext):
    pass

class TrechoFerroviarioDetailContext(FeatureContext):
    pass