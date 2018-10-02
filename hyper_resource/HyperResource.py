
from bcim import serializers

from parser_test import resources
from parser_test.resources import ProxyResource

entry_points = {
    'bcim': {
        'unidades-federativas': resources.UnidadeFederacaoResource,
        'municipios': serializers.MunicipioSerializer,
        'outros-limites-oficiais': serializers.OutrosLimitesOficiaisSerializer,
        'paises': serializers.PaisSerializer,
        'terras-indigenas': serializers.TerraIndigenaSerializer,
        'unidades-de-conservacao-nao-snuc': serializers.UnidadeConservacaoNaoSnucSerializer,
        'unidades-de-protecao-integral': serializers.UnidadeProtecaoIntegralSerializer,
        'unidades-de-uso-sustentavel': serializers.UnidadeUsoSustentavelSerializer,
        'aglomerados-rurais-de-extensao-urbana': serializers.AglomeradoRuralDeExtensaoUrbanaSerializer,
        'aglomerados-rurais-isolado': serializers.AglomeradoRuralIsoladoSerializer,
        'aldeias-indigenas': serializers.AldeiaIndigenaSerializer,
        'areas-edificadas': serializers.AreaEdificadaSerializer,
        'capitais': serializers.CapitalSerializer,
        'cidades': serializers.CidadeSerializer,
        'vilas': serializers.VilaSerializer,
        'curvas-batimetricas': serializers.CurvaBatimetricaSerializer,
        'curvas-de-nivel': serializers.CurvaNivelSerializer,
        'dunas': serializers.DunaSerializer,
        'elementos-fisiografico-natural': serializers.ElementoFisiograficoNaturalSerializer,
        'picos': serializers.PicoSerializer,
        'pontos-cotados-altimetricos': serializers.PontoCotadoAltimetricoSerializer,
        'pontos-cotados-batimetricos': serializers.PontoCotadoBatimetricoSerializer,
        'eclusas': serializers.EclusaSerializer,
        'edificacoes-de-construcao-portuaria': serializers.EdifConstPortuariaSerializer,
        'edificacoes-de-construcao-aeroportuaria': serializers.EdifConstrAeroportuariaSerializer,
        'edificacoes-de-metro-ferroviaria': serializers.EdifMetroFerroviariaSerializer,
        'fundeadouros': serializers.FundeadouroSerializer,
        'pistas-de-ponto-pouso': serializers.PistaPontoPousoSerializer,
        'pontes': serializers.PonteSerializer,
        'sinalizacoes': serializers.SinalizacaoSerializer,
        'travessias': serializers.TravessiaSerializer,
        'trechos-dutos': serializers.TrechoDutoSerializer,
        'trechos-ferroviarios': serializers.TrechoFerroviarioSerializer,
        'trechos-hidroviarios': serializers.TrechoHidroviarioSerializer,
        'trechos-rodoviarios': serializers.TrechoRodoviarioSerializer,
        'tuneis': serializers.TunelSerializer,
        'brejos-e-pantanos': serializers.BrejoPantanoSerializer,
        'mangues': serializers.MangueSerializer,
        'vegetacoes-de-restinga': serializers.VegRestingaSerializer,
        'edificacoes-publica-militar': serializers.EdifPubMilitarSerializer,
        'postos-fiscais': serializers.PostoFiscalSerializer,
        'edificacoes-agropecuarias-de-extracao-vegetal-e-pesca': serializers.EdifAgropecExtVegetalPescaSerializer,
        'edificacoes-industrial': serializers.EdifIndustrialSerializer,
        'extracoes-minerais': serializers.ExtMineralSerializer,
        'edificacoes-religiosa': serializers.EdifReligiosaSerializer,
        'estacoes-geradoras-de-energia-eletrica': serializers.EstGeradEnergiaEletricaSerializer,
        'hidreletricas': serializers.HidreletricaSerializer,
        'termeletricas': serializers.TermeletricaSerializer,
        'torres-de-energia': serializers.TorreEnergiaSerializer,
        'bancos-de-areia': serializers.BancoAreiaSerializer,
        'barragens': serializers.BarragemSerializer,
        'corredeiras': serializers.CorredeiraSerializer,
        'fozes-maritima': serializers.FozMaritimaSerializer,
        'ilhas': serializers.IlhaSerializer,
        'massas-dagua': serializers.MassaDaguaSerializer,
        'quedas-dagua': serializers.QuedaDaguaSerializer,
        'recifes': serializers.RecifeSerializer,
        'rochas-em-agua': serializers.RochaEmAguaSerializer,
        'sumidouros-vertedouros': serializers.SumidouroVertedouroSerializer,
        'terrenos-sujeito-a-inundacao': serializers.TerrenoSujeitoInundacaoSerializer,
        'trechos-de-drenagem': serializers.TrechoDrenagemSerializer,
        'trechos-de-massa-dagua': serializers.TrechoMassaDaguaSerializer,
        'areas-de-desenvolvimento-de-controle': serializers.AreaDesenvolvimentoControleSerializer,
        'marcos-de-limite': serializers.MarcoDeLimiteSerializer,
    }
}


class HyperResource:
    @staticmethod
    def get(entry_point, resource_name):
        abs_resource = entry_points.get(entry_point).get(resource_name)
        return lambda: ProxyResource(abs_resource())
