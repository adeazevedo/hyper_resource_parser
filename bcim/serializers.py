from rest_framework import serializers
from rest_framework.serializers import ModelSerializer, HyperlinkedModelSerializer

from rest_framework.reverse import reverse
from hyper_resource.serializers import BusinessSerializer, GeoBusinessSerializer
from hyper_resource_py.urls import basic_path, protocol, host_name
from .models import *

class EntryPointSerializer(BusinessSerializer):
    class Meta:
        model = EntryPoint
        fields = ["unidades-federativas", "municipios", "outros-limites-oficiais",
             "paises", "terras-indigenas", "unidades-de-conservacao-nao-snuc", "unidades-de-protecao-integral",
             "unidades-de-uso-sustentavel", "aglomerados-rurais-de-extensao-urbana", "aglomerados-rurais-isolado",
             "aldeias-indigenas", "areas-edificadas", "capitais", "cidades", "vilas", "curvas-batimetricas",
             "curvas-de-nivel", "curvas-de-nivel", "dunas", "elementos-fisiografico-natural", "picos",
             "pontos-cotados-altimetricos", "pontos-cotados-batimetricos", "eclusas", "edificacoes-de-construcao-portuaria",
             "edificacoes_de_construcao_aeroportuaria", "edificacoes_de_metro_ferroviaria", "fundeadouros", "pistas-de-ponto-pouso",
             "pontes", "sinalizacoes", "travessias", "trechos-dutos", "trechos-ferroviarios", "trechos-hidroviarios",
             "trechos-rodoviarios", "tuneis", "brejos-e-pantanos", "mangues", "vegetacoes-de-restinga", "edificacoes-publica-militar",
             "postos-fiscais", "edificacoes-agropecuarias-de-extracao-vegetal-e-pesca", "edificacoes-industrial",
             "extracoes-minerais", "edificacoes-religiosa", "estacoes-geradoras-de-energia-eletrica", "hidreletricas",
             "termeletricas", "torres-de-energia", "bancos-de-areia", "barragens", "corredeiras", "fozes-maritima",
             "ilhas", "massas-dagua", "quedas-dagua", "recifes", "rochas-em-agua", "sumidouros-vertedouros",
             "terrenos-sujeito-a-inundacao", "trechos-de-drenagem", "trechos-de-massa-dagua",
             "areas-de-desenvolvimento-de-controle", "marcos-de-limite"]
        identifier = None
        identifiers = []


class UnidadeFederacaoSerializer(GeoBusinessSerializer):
    class Meta:
        model = UnidadeFederacao
        geo_field = 'geom'
        fields = ['id_objeto', 'nome', 'nomeabrev', 'sigla', 'geocodigo', 'geometriaaproximada']
        identifiers = ['id_objeto', 'sigla', 'geocodigo']
        identifier = 'id_objeto'


class MunicipioSerializer(GeoBusinessSerializer):
    class Meta:
        model = Municipio
        geo_field = 'geom'
        fields = ['id_objeto', 'nome', 'nomeabrev',  'geocodigo', 'anodereferencia','geometriaaproximada']
        identifiers = ['id_objeto', 'geocodigo']
        identifier = 'id_objeto'

class OutrasUnidProtegidasSerializer(GeoBusinessSerializer):
    class Meta:
        model = OutrasUnidProtegidas
        geo_field = 'geom'
        fields = ['id_objeto', 'nome', 'nomeabrev',  'geometriaaproximada', 'sigla', 'areaoficial','administracao', 'tipooutunidprot', 'historicomodificacao']
        identifiers = ['id_objeto']
        identifier = 'id_objeto'

class OutrosLimitesOficiaisSerializer(GeoBusinessSerializer):
    class Meta:
        model = OutrosLimitesOficiais
        geo_field = 'geom'
        fields = ['id_objeto', 'nome', 'nomeabrev', 'geometriaaproximada', 'coincidecomdentrode', 'obssituacao', 'tipooutlimofic']
        # 'extensao'

        identifiers = ['id_objeto']
        identifier = 'id_objeto'

class PaisSerializer(GeoBusinessSerializer):
    class Meta:
        model = Pais
        geo_field = 'geom'
        fields = ['id_objeto', 'nome', 'nomeabrev', 'sigla', 'geometriaaproximada', 'codiso3166' ]

        identifiers = ['id_objeto']
        identifier = 'id_objeto'

class TerraIndigenaSerializer(GeoBusinessSerializer):
    class Meta:
        model = TerraIndigena
        geo_field = 'geom'
        fields = ['id_objeto', 'nome', 'nomeabrev', 'geometriaaproximada', 'grupoetnico', 'datasituacaojuridica', 'situacaojuridica', 'nometi', 'codigofunai']
        # 'perimetrooficial', 'areaoficialha'

        identifiers = ['id_objeto']
        identifier = 'id_objeto'

class UnidadeConservacaoNaoSnucSerializer(GeoBusinessSerializer):
    class Meta:
        model = UnidadeConservacaoNaoSnuc
        geo_field = 'geom'
        fields = ['id_objeto', 'nome', 'nomeabrev', 'geometriaaproximada', 'sigla', 'areaoficial', 'administracao', 'classificacao', 'atolegal']
        # 'anocriacao'

        identifiers = ['id_objeto']
        identifier = 'id_objeto'

class UnidadeProtecaoIntegralSerializer(GeoBusinessSerializer):
    class Meta:
        model = UnidadeProtecaoIntegral
        geo_field = 'geom'
        fields = ['id_objeto', 'nome', 'nomeabrev', 'geometriaaproximada','anocriacao', 'sigla', 'areaoficial', 'administracao','atolegal', 'tipounidprotinteg', 'geom']
        # 'anocriacao'

        identifiers = ['id_objeto']
        identifier = 'id_objeto'

class UnidadeUsoSustentavelSerializer(GeoBusinessSerializer):
    class Meta:
        model = UnidadeUsoSustentavel
        geo_field = 'geom'
        fields = ['id_objeto', 'nome', 'nomeabrev', 'geometriaaproximada', 'sigla', 'areaoficial', 'administracao', 'tipounidusosust', 'atolegal']
        # 'anocriacao'

        identifiers = ['id_objeto']
        identifier = 'id_objeto'

class AglomeradoRuralDeExtensaoUrbanaSerializer(GeoBusinessSerializer):
    class Meta:
        model = AglomeradoRuralDeExtensaoUrbana
        geo_field = 'geom'
        fields = ['id_objeto', 'nome', 'nomeabrev', 'geometriaaproximada']

        identifiers = ['id_objeto']
        identifier = 'id_objeto'

class AglomeradoRuralIsoladoSerializer(GeoBusinessSerializer):
    class Meta:
        model = AglomeradoRuralIsolado
        geo_field = 'geom'
        fields = ['id_objeto', 'nome', 'nomeabrev', 'geometriaaproximada', 'tipoaglomrurisol']

        identifiers = ['id_objeto']
        identifier = 'id_objeto'

class AldeiaIndigenaSerializer(GeoBusinessSerializer):
    class Meta:
        model = AldeiaIndigena
        geo_field = 'geom'
        fields = ['id_objeto', 'nome', 'nomeabrev', 'geometriaaproximada', 'codigofunai', 'terraindigena', 'etnia']

        identifiers = ['id_objeto']
        identifier = 'id_objeto'

class AreaEdificadaSerializer(GeoBusinessSerializer):
    class Meta:
        model = AreaEdificada
        geo_field = 'geom'
        fields = ['id_objeto', 'nome', 'nomeabrev', 'geometriaaproximada', 'geocodigo']

        identifiers = ['id_objeto']
        identifier = 'id_objeto'

class CapitalSerializer(GeoBusinessSerializer):
    class Meta:
        model = Capital
        geo_field = 'geom'
        fields = ['id_objeto', 'nome', 'nomeabrev', 'geometriaaproximada', 'tipocapital']

        identifiers = ['id_objeto']
        identifier = 'id_objeto'

class CidadeSerializer(GeoBusinessSerializer):
    class Meta:
        model = Cidade
        geo_field = 'geom'
        fields = ['id_objeto', 'nome', 'nomeabrev', 'geometriaaproximada']

        identifiers = ['id_objeto']
        identifier = 'id_objeto'

class VilaSerializer(GeoBusinessSerializer):
    class Meta:
        model = Vila
        geo_field = 'geom'
        fields = ['id_objeto', 'nome', 'nomeabrev', 'geometriaaproximada']

        identifiers = ['id_objeto']
        identifier = 'id_objeto'

class CurvaBatimetricaSerializer(GeoBusinessSerializer):
    class Meta:
        model = CurvaBatimetrica
        geo_field = 'geom'
        fields = ['id_objeto', 'profundidade']

        identifiers = ['id_objeto']
        identifier = 'id_objeto'

class CurvaNivelSerializer(GeoBusinessSerializer):
    class Meta:
        model = CurvaNivel
        geo_field = 'geom'
        fields = ['id_objeto', 'cota', 'depressao', 'geometriaaproximada', 'indice']

        identifiers = ['id_objeto']
        identifier = 'id_objeto'

class DunaSerializer(GeoBusinessSerializer):
    class Meta:
        model = Duna
        geo_field = 'geom'
        fields = ['id_objeto', 'nome', 'nomeabrev', 'geometriaaproximada', 'fixa']

        identifiers = ['id_objeto']
        identifier = 'id_objeto'

class ElementoFisiograficoNaturalSerializer(GeoBusinessSerializer):
    class Meta:
        model = ElementoFisiograficoNatural
        geo_field = 'geom'
        fields = ['id_objeto', 'nome', 'nomeabrev', 'geometriaaproximada', 'tipoelemnat']

        identifiers = ['id_objeto']
        identifier = 'id_objeto'

class PicoSerializer(GeoBusinessSerializer):
    class Meta:
        model = Pico
        geo_field = 'geom'
        fields = ['id_objeto', 'nome', 'nomeabrev', 'geometriaaproximada']

        identifiers = ['id_objeto']
        identifier = 'id_objeto'

class PontoCotadoAltimetricoSerializer(GeoBusinessSerializer):
    class Meta:
        model = PontoCotadoAltimetrico
        geo_field = 'geom'
        fields = ['id_objeto', 'geometriaaproximada', 'cota', 'cotacomprovada']

        identifiers = ['id_objeto']
        identifier = 'id_objeto'

class PontoCotadoBatimetricoSerializer(GeoBusinessSerializer):
    class Meta:
        model = PontoCotadoBatimetrico
        geo_field = 'geom'
        fields = ['id_objeto', 'profundidade']

        identifiers = ['id_objeto']
        identifier = 'id_objeto'

class EclusaSerializer(GeoBusinessSerializer):
    class Meta:
        model = Eclusa
        geo_field = 'geom'
        fields = ['id_objeto', 'nome', 'nomeabrev', 'geometriaaproximada', 'desnivel', 'matconstr', 'operacional', 'situacaofisica', 'extensao', 'largura']
        # 'calado'

        identifiers = ['id_objeto']
        identifier = 'id_objeto'

class EdifConstPortuariaSerializer(GeoBusinessSerializer):
    class Meta:
        model = EdifConstPortuaria
        geo_field = 'geom'
        fields = ['id_objeto', 'nome', 'nomeabrev', 'geometriaaproximada', 'tipoedifport', 'administracao', 'matconstr', 'operacional', 'situacaofisica']

        identifiers = ['id_objeto']
        identifier = 'id_objeto'

class EdifConstrAeroportuariaSerializer(GeoBusinessSerializer):
    class Meta:
        model = EdifConstrAeroportuaria
        geo_field = 'geom'
        fields = ['id_objeto', 'nome', 'nomeabrev', 'geometriaaproximada', 'operacional', 'situacaofisica', 'administracao', 'matconstr', 'tipoedifaero']

        identifiers = ['id_objeto']
        identifier = 'id_objeto'

class EdifMetroFerroviariaSerializer(GeoBusinessSerializer):
    class Meta:
        model = EdifMetroFerroviaria
        geo_field = 'geom'
        fields = ['id_objeto', 'nome', 'nomeabrev', 'geometriaaproximada', 'multimodal', 'funcaoedifmetroferrov', 'operacional', 'situacaofisica', 'administracao', 'matconstr']

        identifiers = ['id_objeto']
        identifier = 'id_objeto'

class FundeadouroSerializer(GeoBusinessSerializer):
    class Meta:
        model = Fundeadouro
        geo_field = 'geom'
        fields = ['id_objeto', 'nome', 'nomeabrev', 'geometriaaproximada', 'administracao', 'destinacaofundeadouro']

        identifiers = ['id_objeto']
        identifier = 'id_objeto'

class PistaPontoPousoSerializer(GeoBusinessSerializer):
    class Meta:
        model = PistaPontoPouso
        geo_field = 'geom'
        fields = ['id_objeto', 'nome', 'nomeabrev', 'geometriaaproximada', 'operacional', 'situacaofisica', 'homologacao', 'tipopista', 'usopista', 'revestimento']
        # 'extensao', 'largura'

        identifiers = ['id_objeto']
        identifier = 'id_objeto'

class PonteSerializer(GeoBusinessSerializer):
    class Meta:
        model = Ponte
        geo_field = 'geom'
        fields = ['id_objeto', 'nome', 'nomeabrev', 'geometriaaproximada', 'modaluso', 'tipoponte', 'situacaofisica', 'operacional', 'matconstr', 'posicaopista']
        # 'extensao', 'largura', 'vaolivrehoriz', 'vaovertical', 'cargasuportmaxima', 'nrpistas', 'nrfaixas'

        identifiers = ['id_objeto']
        identifier = 'id_objeto'

class SinalizacaoSerializer(GeoBusinessSerializer):
    class Meta:
        model = Sinalizacao
        geo_field = 'geom'
        fields = ['id_objeto', 'nome', 'nomeabrev', 'geometriaaproximada', 'situacaofisica', 'operacional', 'tiposinal']

        identifiers = ['id_objeto']
        identifier = 'id_objeto'

class TravessiaSerializer(GeoBusinessSerializer):
    class Meta:
        model = Travessia
        geo_field = 'geom'
        fields = ['id_objeto', 'nome', 'nomeabrev', 'geometriaaproximada', 'tipotravessia']

        identifiers = ['id_objeto']
        identifier = 'id_objeto'

class TrechoDutoSerializer(GeoBusinessSerializer):
    class Meta:
        model = TrechoDuto
        geo_field = 'geom'
        fields = ['id_objeto', 'nome', 'nomeabrev', 'geometriaaproximada', 'situacaofisica', 'operacional', 'matconstr', 'tipotrechoduto', 'mattransp', 'setor', 'posicaorelativa', 'situacaoespacial']
        # 'nrdutos'

        identifiers = ['id_objeto']
        identifier = 'id_objeto'

class TrechoFerroviarioSerializer(GeoBusinessSerializer):
    class Meta:
        model = TrechoFerroviario
        geo_field = 'geom'
        fields = ['id_objeto', 'nome', 'nomeabrev', 'geometriaaproximada', 'situacaofisica', 'operacional', 'codtrechoferrov', 'posicaorelativa', 'tipotrechoferrov', 'bitola', 'eletrificada', 'emarruamento', 'jurisdicao', 'administracao', 'concessionaria', 'nrlinhas']
        # 'cargasuportmaxima'

        identifiers = ['id_objeto']
        identifier = 'id_objeto'

class TrechoHidroviarioSerializer(GeoBusinessSerializer):
    class Meta:
        model = TrechoHidroviario
        geo_field = 'geom'
        fields = ['id_objeto', 'nome', 'nomeabrev', 'geometriaaproximada', 'situacaofisica', 'operacional', 'regime']
        # 'caladomaxseca', 'extensaotrecho'

        identifiers = ['id_objeto']
        identifier = 'id_objeto'

class TrechoRodoviarioSerializer(GeoBusinessSerializer):
    class Meta:
        model = TrechoRodoviario
        geo_field = 'geom'
        fields = ['id_objeto', 'codtrechorodov', 'tipotrechorod', 'jurisdicao', 'administracao','concessionaria', 'revestimento', 'operacional', 'situacaofisica', 'nrpistas', 'nrfaixas', 'trafego', 'canteirodivisorio', 'capaccarga']

        identifiers = ['id_objeto']
        identifier = 'id_objeto'

class TunelSerializer(GeoBusinessSerializer):
    class Meta:
        model = Tunel
        geo_field = 'geom'
        fields = ['id_objeto', 'nome', 'nomeabrev', 'geometriaaproximada', 'modaluso', 'situacaofisica', 'operacional', 'posicaopista', 'matconstr', 'tipotunel']
        # 'extensao', 'largura', 'altura', 'nrpistas', 'nrfaixas'

        identifiers = ['id_objeto']
        identifier = 'id_objeto'

class BrejoPantanoSerializer(GeoBusinessSerializer):
    class Meta:
        model = BrejoPantano
        geo_field = 'geom'
        fields = ['id_objeto', 'nome', 'nomeabrev', 'geometriaaproximada', 'antropizada', 'denso', 'tipobrejopantano', 'classificacaoporte']
        # 'alturamediaindividuos'

        identifiers = ['id_objeto']
        identifier = 'id_objeto'

class MangueSerializer(GeoBusinessSerializer):
    class Meta:
        model = Mangue
        geo_field = 'geom'
        fields = ['id_objeto', 'nome', 'nomeabrev', 'geometriaaproximada', 'antropizada', 'denso', 'classificacaoporte']
        # 'alturamediaindividuos'

        identifiers = ['id_objeto']
        identifier = 'id_objeto'

class VegRestingaSerializer(GeoBusinessSerializer):
    class Meta:
        model = VegRestinga
        geo_field = 'geom'
        fields = ['id_objeto', 'nome', 'nomeabrev', 'geometriaaproximada', 'antropizada', 'denso', 'classificacaoporte']
        # 'alturamediaindividuos'

        identifiers = ['id_objeto']
        identifier = 'id_objeto'

class EdifPubMilitarSerializer(GeoBusinessSerializer):
    class Meta:
        model = EdifPubMilitar
        geo_field = 'geom'
        fields = ['id_objeto', 'nome', 'nomeabrev', 'geometriaaproximada', 'tipoedifmil', 'tipousoedif', 'situacaofisica', 'operacional', 'matconstr']

        identifiers = ['id_objeto']
        identifier = 'id_objeto'

class PostoFiscalSerializer(GeoBusinessSerializer):
    class Meta:
        model = PostoFiscal
        geo_field = 'geom'
        fields = ['id_objeto', 'nome', 'nomeabrev', 'geometriaaproximada', 'tipopostofisc', 'situacaofisica', 'operacional']

        identifiers = ['id_objeto']
        identifier = 'id_objeto'

class EdifAgropecExtVegetalPescaSerializer(GeoBusinessSerializer):
    class Meta:
        model = EdifAgropecExtVegetalPesca
        geo_field = 'geom'
        fields = ['id_objeto', 'nome', 'nomeabrev', 'geometriaaproximada', 'tipoedifagropec', 'situacaofisica', 'operacional', 'matconstr']

        identifiers = ['id_objeto']
        identifier = 'id_objeto'

class EdifIndustrialSerializer(GeoBusinessSerializer):
    class Meta:
        model = EdifIndustrial
        geo_field = 'geom'
        fields = ['id_objeto', 'nome', 'nomeabrev', 'geometriaaproximada', 'tipodivisaocnae', 'situacaofisica', 'operacional', 'matconstr', 'chamine']

        identifiers = ['id_objeto']
        identifier = 'id_objeto'

class ExtMineralSerializer(GeoBusinessSerializer):
    class Meta:
        model = ExtMineral
        geo_field = 'geom'
        fields = ['id_objeto', 'nome', 'nomeabrev', 'geometriaaproximada', 'tiposecaocnae', 'situacaofisica', 'operacional', 'tipoextmin', 'tipoprodutoresiduo', 'tipopocomina', 'procextracao', 'formaextracao', 'atividade']

        identifiers = ['id_objeto']
        identifier = 'id_objeto'

class EdifReligiosaSerializer(GeoBusinessSerializer):
    class Meta:
        model = EdifReligiosa
        geo_field = 'geom'
        fields = ['id_objeto', 'nome', 'nomeabrev', 'geometriaaproximada', 'religiao', 'situacaofisica', 'operacional', 'tipoedifrelig', 'ensino', 'matconstr']

        identifiers = ['id_objeto']
        identifier = 'id_objeto'

class EstGeradEnergiaEletricaSerializer(GeoBusinessSerializer):
    class Meta:
        model = EstGeradEnergiaEletrica
        geo_field = 'geom'
        fields = ['id_objeto', 'nome', 'nomeabrev', 'geometriaaproximada', 'codigoestacao', 'situacaofisica', 'operacional', 'destenergelet', 'tipoestgerad']
        # 'potenciaoutorgada', 'potenciafiscalizada'

        identifiers = ['id_objeto']
        identifier = 'id_objeto'

class HidreletricaSerializer(GeoBusinessSerializer):
    class Meta:
        model = Hidreletrica
        geo_field = 'geom'
        fields = ['id_objeto', 'nome', 'nomeabrev', 'geometriaaproximada', 'codigohidreletrica', 'situacaofisica', 'operacional']
        # 'potenciaoutorgada', 'potenciafiscalizada'

        identifiers = ['id_objeto']
        identifier = 'id_objeto'

class TermeletricaSerializer(GeoBusinessSerializer):
    class Meta:
        model = Termeletrica
        geo_field = 'geom'
        fields = ['id_objeto', 'nome', 'nomeabrev', 'geometriaaproximada', 'combrenovavel', 'situacaofisica', 'operacional', 'tipomaqtermica', 'geracao', 'tipocombustivel']
        # 'potenciaoutorgada', 'potenciafiscalizada'

        identifiers = ['id_objeto']
        identifier = 'id_objeto'

class TorreEnergiaSerializer(GeoBusinessSerializer):
    class Meta:
        model = TorreEnergia
        geo_field = 'geom'
        fields = ['id_objeto', 'nome', 'nomeabrev', 'geometriaaproximada', 'situacaofisica', 'operacional', 'arranjofases', 'ovgd', 'tipotorre']
        # 'alturaestimada'

        identifiers = ['id_objeto']
        identifier = 'id_objeto'

class BancoAreiaSerializer(GeoBusinessSerializer):
    class Meta:
        model = BancoAreia
        geo_field = 'geom'
        fields = ['id_objeto', 'nome', 'nomeabrev', 'geometriaaproximada', 'tipobanco', 'situacaoemagua', 'materialpredominante']

        identifiers = ['id_objeto']
        identifier = 'id_objeto'

class BarragemSerializer(GeoBusinessSerializer):
    class Meta:
        model = Barragem
        geo_field = 'geom'
        fields = ['id_objeto', 'nome', 'nomeabrev', 'geometriaaproximada', 'usoprincipal', 'situacaofisica', 'operacional', 'matconstr']

        identifiers = ['id_objeto']
        identifier = 'id_objeto'

class CorredeiraSerializer(GeoBusinessSerializer):
    class Meta:
        model = Corredeira
        geo_field = 'geom'
        fields = ['id_objeto', 'nome', 'nomeabrev', 'geometriaaproximada']

        identifiers = ['id_objeto']
        identifier = 'id_objeto'

class FozMaritimaSerializer(GeoBusinessSerializer):
    class Meta:
        model = FozMaritima
        geo_field = 'geom'
        fields = ['id_objeto', 'nome', 'nomeabrev', 'geometriaaproximada']

        identifiers = ['id_objeto']
        identifier = 'id_objeto'

class IlhaSerializer(GeoBusinessSerializer):
    class Meta:
        model = Ilha
        geo_field = 'geom'
        fields = ['id_objeto', 'nome', 'nomeabrev', 'geometriaaproximada', 'tipoilha']

        identifiers = ['id_objeto']
        identifier = 'id_objeto'

class MassaDaguaSerializer(GeoBusinessSerializer):
    class Meta:
        model = MassaDagua
        geo_field = 'geom'
        fields = ['id_objeto', 'nome', 'nomeabrev', 'geometriaaproximada', 'tipomassadagua', 'salinidade', 'regime']

        identifiers = ['id_objeto']
        identifier = 'id_objeto'

class QuedaDaguaSerializer(GeoBusinessSerializer):
    class Meta:
        model = QuedaDagua
        geo_field = 'geom'
        fields = ['id_objeto', 'nome', 'nomeabrev', 'geometriaaproximada', 'tipoqueda']
        # 'altura'

        identifiers = ['id_objeto']
        identifier = 'id_objeto'

class RecifeSerializer(GeoBusinessSerializer):
    class Meta:
        model = Recife
        geo_field = 'geom'
        fields = ['id_objeto', 'nome', 'nomeabrev', 'geometriaaproximada', 'tiporecife', 'situamare', 'situacaocosta']

        identifiers = ['id_objeto']
        identifier = 'id_objeto'

class RochaEmAguaSerializer(GeoBusinessSerializer):
    class Meta:
        model = RochaEmAgua
        geo_field = 'geom'
        fields = ['id_objeto', 'nome', 'nomeabrev', 'geometriaaproximada', 'situacaoemagua']
        # 'alturalamina'

        identifiers = ['id_objeto']
        identifier = 'id_objeto'

class SumidouroVertedouroSerializer(GeoBusinessSerializer):
    class Meta:
        model = SumidouroVertedouro
        geo_field = 'geom'
        fields = ['id_objeto', 'nome', 'nomeabrev', 'geometriaaproximada', 'causa', 'tiposumvert']

        identifiers = ['id_objeto']
        identifier = 'id_objeto'

class TerrenoSujeitoInundacaoSerializer(GeoBusinessSerializer):
    class Meta:
        model = TerrenoSujeitoInundacao
        geo_field = 'geom'
        fields = ['id_objeto', 'nome', 'nomeabrev', 'geometriaaproximada', 'periodicidadeinunda']

        identifiers = ['id_objeto']
        identifier = 'id_objeto'

class TrechoDrenagemSerializer(GeoBusinessSerializer):
    class Meta:
        model = TrechoDrenagem
        geo_field = 'geom'
        fields = ['id_objeto', 'nome', 'nomeabrev', 'geometriaaproximada', 'profundidademedia', 'coincidecomdentrode', 'compartilhado', 'eixoprincipal', 'navegabilidade', 'regime', 'caladomax', 'larguramedia', 'velocidademedcorrente', 'dentrodepoligono']


        identifiers = ['id_objeto']
        identifier = 'id_objeto'

class TrechoMassaDaguaSerializer(GeoBusinessSerializer):
    class Meta:
        model = TrechoMassaDagua
        geo_field = 'geom'
        fields = ['id_objeto', 'nome', 'nomeabrev', 'geometriaaproximada', 'tipotrechomassa', 'salinidade', 'regime']

        identifiers = ['id_objeto']
        identifier = 'id_objeto'

class AreaDesenvolvimentoControleSerializer(GeoBusinessSerializer):
    class Meta:
        model = AreaDesenvolvimentoControle
        geo_field = 'geom'
        fields = ['id_objeto', 'nome', 'nomeabrev', 'geometriaaproximada', 'classificacao']

        identifiers = ['id_objeto']
        identifier = 'id_objeto'

class MarcoDeLimiteSerializer(GeoBusinessSerializer):
    class Meta:
        model = MarcoDeLimite
        geo_field = 'geom'
        fields = ['id_objeto', 'nome', 'nomeabrev', 'geometriaaproximada', 'tipomarcolim', 'latitude', 'longitude', 'orgresp', 'sistemageodesico', 'outrarefplan', 'outrarefalt', 'referencialaltim']
        # 'altitudeortometrica'


        identifiers = ['id_objeto']
        identifier = 'id_objeto'

serializers_dict = {
    'outras-unidades-protegidas': {
        'name': "outras unidades protegidas",
        'serializer': OutrasUnidProtegidasSerializer
    },
    'outros-limites-oficiais': {
        'name': "outros limites oficiais",
        'serializer': OutrosLimitesOficiaisSerializer
    },
}

