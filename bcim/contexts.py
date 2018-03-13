from hyper_resource.contexts import ContextResource, FeatureResouceContext, FeatureCollectionResourceContext

class UnidadeFederacaoContext(FeatureResouceContext):

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
    def representation_name(self):
        return "sigla"

    #def  supportedProperties(self):
    #dic = {"hydra:supportedProperties": [
    #    {
    #        "hydra:writeable": true, "hydra:property": "nome", "hydra:readable": true, "isIdentifier": false, "hydra:required": true, "isExternal": false, "@type": "SupportedProperty",  "isUnique": false
    #    }
    #]}
    #return dic

class TrechoDrenagemListContext(FeatureResouceContext):
    pass
class UnidadeFederacaoListContext(FeatureResouceContext):
    pass

class MunicipioListContext(FeatureResouceContext):
    pass

class MunicipioDetailContext(FeatureResouceContext):
    pass

class AldeiaIndigenaDetailContext(FeatureResouceContext):
    pass

class AldeiaIndigenaListContext(FeatureResouceContext):
    pass

class OutrasUnidProtegidasContext(FeatureResouceContext):
    pass
class AglomeradoRuralDeExtensaoUrbanaContext(FeatureResouceContext):
    pass
class AglomeradoRuralIsoladoContext(FeatureResouceContext):
    pass

class TrechoFerroviarioListContext(FeatureCollectionResourceContext):
    pass

class TrechoFerroviarioDetailContext(FeatureResouceContext):
    pass