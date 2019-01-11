from hyper_resource.contexts import ContextResource, FeatureResourceContext, FeatureCollectionResourceContext

class UnidadeFederacaoListContext(FeatureCollectionResourceContext):

    '''
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
    '''
    def representation_name(self):
        return "sigla"

    def get_default_resource_id_vocabulary(self):
        return "https://schema.org/State"

    #def  supportedProperties(self):
    #dic = {"hydra:supportedProperties": [
    #    {
    #        "hydra:writeable": true, "hydra:property": "nome", "hydra:readable": true, "isIdentifier": false, "hydra:required": true, "isExternal": false, "@type": "SupportedProperty",  "isUnique": false
    #    }
    #]}
    #return dic

class UnidadeFederacaoDetailContext(FeatureResourceContext):

    '''
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
    '''
    def get_default_resource_id_vocabulary(self):
        return "https://schema.org/State"

    def representation_name(self):
        return "sigla"

class TrechoDrenagemListContext(FeatureResourceContext):
    pass

class MunicipioListContext(FeatureResourceContext):
    pass

class MunicipioDetailContext(FeatureResourceContext):
    pass

class AldeiaIndigenaDetailContext(FeatureResourceContext):
    pass

class AldeiaIndigenaListContext(FeatureCollectionResourceContext):
    pass

    # todo: can be defined programaticaly by checking model geometric attribute type
    #def get_default_resource_id_vocabulary(self):
    #    return "http://geojson.org/geojson-ld/vocab.html#Point"

class OutrasUnidProtegidasContext(FeatureResourceContext):
    pass
class AglomeradoRuralDeExtensaoUrbanaContext(FeatureResourceContext):
    pass
class AglomeradoRuralIsoladoContext(FeatureResourceContext):
    pass

class TrechoFerroviarioListContext(FeatureCollectionResourceContext):
    pass

class TrechoFerroviarioDetailContext(FeatureResourceContext):
    pass

class AreaDesenvolvimentoControleListContext(FeatureResourceContext):
    pass
class AreaEdificadaListContext(FeatureResourceContext):
    pass
class AreaEdificadaDetailContext(FeatureResourceContext):
    pass

class BancoAreiaListContext(FeatureCollectionResourceContext):
    pass

class BancoAreiaDetailContext(FeatureResourceContext):
    pass
class BarragemListContext(FeatureCollectionResourceContext):
    pass
class BrejoPantanoListContext(FeatureCollectionResourceContext):
    pass
class CapitalListContext(FeatureCollectionResourceContext):
    pass
class CidadeListContext(FeatureCollectionResourceContext):
    pass
class CorredeiraListContext(FeatureCollectionResourceContext):
    pass

class CurvaBatimetricaListContext(FeatureCollectionResourceContext):
    pass
class CurvaNivelListContext(FeatureCollectionResourceContext):
    pass
class DunaListContext(FeatureCollectionResourceContext):
    pass
class EclusaListContext(FeatureCollectionResourceContext):
    pass
class EdifAgropecExtVegetalPescaListContext(FeatureCollectionResourceContext):
    pass
class EdifConstrAeroportuariaListContext(FeatureCollectionResourceContext):
    pass
class EdifConstPortuariaListContext(FeatureCollectionResourceContext):
    pass
class EdifMetroFerroviariaListContext(FeatureCollectionResourceContext):
    pass
class EdifIndustrialListContext(FeatureCollectionResourceContext):
    pass
class EdifPubMilitarListContext(FeatureCollectionResourceContext):
    pass
class EdifReligiosaListContext(FeatureCollectionResourceContext):
    pass
class ElementoFisiograficoNaturalListContext(FeatureCollectionResourceContext):
    pass
class PicoListContext(FeatureCollectionResourceContext):
    pass
class EstGeradEnergiaEletricaListContext(FeatureCollectionResourceContext):
    pass
class ExtMineralListContext(FeatureCollectionResourceContext):
    pass
class FozMaritimaListContext(FeatureCollectionResourceContext):
    pass
class FundeadouroListContext(FeatureCollectionResourceContext):
    pass
class HidreletricaListContext(FeatureCollectionResourceContext):
    pass
class IlhaListContext(FeatureCollectionResourceContext):
    pass
class MangueListContext(FeatureCollectionResourceContext):
    pass
class MarcoDeLimiteListContext(FeatureCollectionResourceContext):
    pass
class MassaDaguaListContext(FeatureCollectionResourceContext):
    pass
class PaisListContext(FeatureCollectionResourceContext):
    pass
class PistaPontoPousoListContext(FeatureCollectionResourceContext):
    pass
class PonteListContext(FeatureCollectionResourceContext):
    pass
class PontoCotadoAltimetricoListContext(FeatureCollectionResourceContext):
    pass
class PontoCotadoBatimetricoListContext(FeatureCollectionResourceContext):
    pass
class PostoFiscalListContext(FeatureCollectionResourceContext):
    pass
class QuedaDaguaListContext(FeatureCollectionResourceContext):
    pass
class RecifeListContext(FeatureCollectionResourceContext):
    pass
class RochaEmAguaListContext(FeatureCollectionResourceContext):
    pass
class SinalizacaoListContext(FeatureCollectionResourceContext):
    pass
class SumidouroVertedouroListContext(FeatureCollectionResourceContext):
    pass
class TermeletricaListContext(FeatureCollectionResourceContext):
    pass
class TerraIndigenaListContext(FeatureCollectionResourceContext):
    pass
class TerrenoSujeitoInundacaoListContext(FeatureCollectionResourceContext):
    pass
class TorreEnergiaListContext(FeatureCollectionResourceContext):
    pass
class TravessiaListContext(FeatureCollectionResourceContext):
    pass
class TrechoMassaDaguaListContext(FeatureCollectionResourceContext):
    pass
class TrechoDutoListContext(FeatureCollectionResourceContext):
    pass
class TrechoHidroviarioListContext(FeatureCollectionResourceContext):
    pass
class TrechoRodoviarioListContext(FeatureCollectionResourceContext):
    pass
class TunelListContext(FeatureCollectionResourceContext):
    pass
class UnidadeConservacaoNaoSnucListContext(FeatureCollectionResourceContext):
    pass
class UnidadeProtecaoIntegralListContext(FeatureCollectionResourceContext):
    pass
class UnidadeUsoSustentavelListContext(FeatureCollectionResourceContext):
    pass
class VegRestingaListContext(FeatureCollectionResourceContext):
    pass
class VilaListContext(FeatureCollectionResourceContext):
    pass
class OutrosLimitesOficiaisContext(FeatureCollectionResourceContext):
    pass