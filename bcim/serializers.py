from rest_framework import serializers
from rest_framework.serializers import ModelSerializer, HyperlinkedModelSerializer
from rest_framework_gis.serializers import GeoFeatureModelSerializer
from rest_framework.reverse import reverse

from hyper_resource_py.urls import basic_path, protocol, host_name
from .models import *

class UnidadeFederacaoSerializer(GeoFeatureModelSerializer):
    class Meta:
        model = UnidadeFederacao
        geo_field = 'geom'
        fields = ['id_objeto', 'nome', 'nomeabrev', 'sigla', 'geocodigo']
        identifiers = ['id_objeto', 'sigla', 'geocodigo']
        identifier = 'id_objeto'


class MunicipioSerializer(GeoFeatureModelSerializer):
    class Meta:
        model = Municipio
        geo_field = 'geom'
        fields = ['id_objeto', 'nome', 'nomeabrev',  'geocodigo', 'anodereferencia','geometriaaproximada']
        identifiers = ['id_objeto', 'geocodigo']
        identifier = 'id_objeto'

class OutrasUnidProtegidasSerializer(GeoFeatureModelSerializer):
    class Meta:
        model = OutrasUnidProtegidas
        geo_field = 'geom'
        fields = ['id_objeto', 'nome', 'nomeabrev',  'geometriaaproximada', 'sigla', 'areaoficial','administracao', 'tipooutunidprot', 'historicomodificacao']
        identifiers = ['id_objeto']
        identifier = 'id_objeto'

class OutrosLimitesOficiaisSerializer(GeoFeatureModelSerializer):
    class Meta:
        model = OutrosLimitesOficiais
        geo_field = 'geom'
        fields = ['id_objeto', 'nome', 'nomeabrev', 'geometriaaproximada', 'coincidecomdentrode', 'obssituacao', 'tipooutlimofic']
        # 'extensao'

        identifiers = ['id_objeto']
        identifier = 'id_objeto'

class PaisSerializer(GeoFeatureModelSerializer):
    class Meta:
        model = Pais
        geo_field = 'geom'
        fields = ['id_objeto', 'nome', 'nomeabrev', 'sigla', 'geometriaaproximada', 'codiso3166' ]

        identifiers = ['id_objeto']
        identifier = 'id_objeto'

class TerraIndigenaSerializer(GeoFeatureModelSerializer):
    class Meta:
        model = TerraIndigena
        geo_field = 'geom'
        fields = ['id_objeto', 'nome', 'nomeabrev', 'geometriaaproximada', 'grupoetnico', 'datasituacaojuridica', 'situacaojuridica', 'nometi', 'codigofunai']
        # 'perimetrooficial', 'areaoficialha'

        identifiers = ['id_objeto']
        identifier = 'id_objeto'

class UnidadeConservacaoNaoSnucSerializer(GeoFeatureModelSerializer):
    class Meta:
        model = UnidadeConservacaoNaoSnuc
        geo_field = 'geom'
        fields = ['id_objeto', 'nome', 'nomeabrev', 'geometriaaproximada', 'sigla', 'areaoficial', 'administracao', 'classificacao', 'atolegal']
        # 'anocriacao'

        identifiers = ['id_objeto']
        identifier = 'id_objeto'

class UnidadeProtecaoIntegralSerializer(GeoFeatureModelSerializer):
    class Meta:
        model = UnidadeProtecaoIntegral
        geo_field = 'geom'
        fields = ['id_objeto', 'nome', 'nomeabrev', 'geometriaaproximada','anocriacao', 'sigla', 'areaoficial', 'administracao','atolegal', 'tipounidprotinteg', 'geom']
        # 'anocriacao'

        identifiers = ['id_objeto']
        identifier = 'id_objeto'

class UnidadeUsoSustentavelSerializer(GeoFeatureModelSerializer):
    class Meta:
        model = UnidadeUsoSustentavel
        geo_field = 'geom'
        fields = ['id_objeto', 'nome', 'nomeabrev', 'geometriaaproximada', 'sigla', 'areaoficial', 'administracao', 'tipounidusosust', 'atolegal']
        # 'anocriacao'

        identifiers = ['id_objeto']
        identifier = 'id_objeto'

class AglomeradoRuralDeExtensaoUrbanaSerializer(GeoFeatureModelSerializer):
    class Meta:
        model = AglomeradoRuralDeExtensaoUrbana
        geo_field = 'geom'
        fields = ['id_objeto', 'nome', 'nomeabrev', 'geometriaaproximada']

        identifiers = ['id_objeto']
        identifier = 'id_objeto'

class AglomeradoRuralIsoladoSerializer(GeoFeatureModelSerializer):
    class Meta:
        model = AglomeradoRuralIsolado
        geo_field = 'geom'
        fields = ['id_objeto', 'nome', 'nomeabrev', 'geometriaaproximada', 'tipoaglomrurisol']

        identifiers = ['id_objeto']
        identifier = 'id_objeto'

class AldeiaIndigenaSerializer(GeoFeatureModelSerializer):
    class Meta:
        model = AldeiaIndigena
        geo_field = 'geom'
        fields = ['id_objeto', 'nome', 'nomeabrev', 'geometriaaproximada', 'codigofunai', 'terraindigena', 'etnia']

        identifiers = ['id_objeto']
        identifier = 'id_objeto'

class AreaEdificadaSerializer(GeoFeatureModelSerializer):
    class Meta:
        model = AreaEdificada
        geo_field = 'geom'
        fields = ['id_objeto', 'nome', 'nomeabrev', 'geometriaaproximada', 'geocodigo']

        identifiers = ['id_objeto']
        identifier = 'id_objeto'

class CapitalSerializer(GeoFeatureModelSerializer):
    class Meta:
        model = Capital
        geo_field = 'geom'
        fields = ['id_objeto', 'nome', 'nomeabrev', 'geometriaaproximada', 'tipocapital']

        identifiers = ['id_objeto']
        identifier = 'id_objeto'

class CidadeSerializer(GeoFeatureModelSerializer):
    class Meta:
        model = Cidade
        geo_field = 'geom'
        fields = ['id_objeto', 'nome', 'nomeabrev', 'geometriaaproximada']

        identifiers = ['id_objeto']
        identifier = 'id_objeto'

class VilaSerializer(GeoFeatureModelSerializer):
    class Meta:
        model = Vila
        geo_field = 'geom'
        fields = ['id_objeto', 'nome', 'nomeabrev', 'geometriaaproximada']

        identifiers = ['id_objeto']
        identifier = 'id_objeto'

class CurvaBatimetricaSerializer(GeoFeatureModelSerializer):
    class Meta:
        model = CurvaBatimetrica
        geo_field = 'geom'
        fields = ['id_objeto', 'profundidade']

        identifiers = ['id_objeto']
        identifier = 'id_objeto'

class CurvaNivelSerializer(GeoFeatureModelSerializer):
    class Meta:
        model = CurvaNivel
        geo_field = 'geom'
        fields = ['id_objeto', 'cota', 'depressao', 'geometriaaproximada', 'indice']

        identifiers = ['id_objeto']
        identifier = 'id_objeto'

class DunaSerializer(GeoFeatureModelSerializer):
    class Meta:
        model = Duna
        geo_field = 'geom'
        fields = ['id_objeto', 'nome', 'nomeabrev', 'geometriaaproximada', 'fixa']

        identifiers = ['id_objeto']
        identifier = 'id_objeto'

class ElementoFisiograficoNaturalSerializer(GeoFeatureModelSerializer):
    class Meta:
        model = ElementoFisiograficoNatural
        geo_field = 'geom'
        fields = ['id_objeto', 'nome', 'nomeabrev', 'geometriaaproximada', 'tipoelemnat']

        identifiers = ['id_objeto']
        identifier = 'id_objeto'

class PicoSerializer(GeoFeatureModelSerializer):
    class Meta:
        model = Pico
        geo_field = 'geom'
        fields = ['id_objeto', 'nome', 'nomeabrev', 'geometriaaproximada']

        identifiers = ['id_objeto']
        identifier = 'id_objeto'

class PontoCotadoAltimetricoSerializer(GeoFeatureModelSerializer):
    class Meta:
        model = PontoCotadoAltimetrico
        geo_field = 'geom'
        fields = ['id_objeto', 'geometriaaproximada', 'cota', 'cotacomprovada']

        identifiers = ['id_objeto']
        identifier = 'id_objeto'

class PontoCotadoBatimetricoSerializer(GeoFeatureModelSerializer):
    class Meta:
        model = PontoCotadoBatimetrico
        geo_field = 'geom'
        fields = ['id_objeto', 'profundidade']

        identifiers = ['id_objeto']
        identifier = 'id_objeto'

class EclusaSerializer(GeoFeatureModelSerializer):
    class Meta:
        model = Eclusa
        geo_field = 'geom'
        fields = ['id_objeto', 'nome', 'nomeabrev', 'geometriaaproximada', 'desnivel', 'matconstr', 'operacional', 'situacaofisica', 'extensao', 'largura']
        # 'calado'

        identifiers = ['id_objeto']
        identifier = 'id_objeto'

class EdifConstPortuariaSerializer(GeoFeatureModelSerializer):
    class Meta:
        model = EdifConstPortuaria
        geo_field = 'geom'
        fields = ['id_objeto', 'nome', 'nomeabrev', 'geometriaaproximada', 'tipoedifport', 'administracao', 'matconstr', 'operacional', 'situacaofisica']

        identifiers = ['id_objeto']
        identifier = 'id_objeto'

class EdifConstrAeroportuariaSerializer(GeoFeatureModelSerializer):
    class Meta:
        model = EdifConstrAeroportuaria
        geo_field = 'geom'
        fields = ['id_objeto', 'nome', 'nomeabrev', 'geometriaaproximada', 'operacional', 'situacaofisica', 'administracao', 'matconstr', 'tipoedifaero']

        identifiers = ['id_objeto']
        identifier = 'id_objeto'

class EdifMetroFerroviariaSerializer(GeoFeatureModelSerializer):
    class Meta:
        model = EdifMetroFerroviaria
        geo_field = 'geom'
        fields = ['id_objeto', 'nome', 'nomeabrev', 'geometriaaproximada', 'multimodal', 'funcaoedifmetroferrov', 'operacional', 'situacaofisica', 'administracao', 'matconstr']

        identifiers = ['id_objeto']
        identifier = 'id_objeto'

class FundeadouroSerializer(GeoFeatureModelSerializer):
    class Meta:
        model = Fundeadouro
        geo_field = 'geom'
        fields = ['id_objeto', 'nome', 'nomeabrev', 'geometriaaproximada', 'administracao', 'destinacaofundeadouro']

        identifiers = ['id_objeto']
        identifier = 'id_objeto'

class PistaPontoPousoSerializer(GeoFeatureModelSerializer):
    class Meta:
        model = PistaPontoPouso
        geo_field = 'geom'
        fields = ['id_objeto', 'nome', 'nomeabrev', 'geometriaaproximada', 'operacional', 'situacaofisica', 'homologacao', 'tipopista', 'usopista', 'revestimento']
        # 'extensao', 'largura'

        identifiers = ['id_objeto']
        identifier = 'id_objeto'

class PonteSerializer(GeoFeatureModelSerializer):
    class Meta:
        model = Ponte
        geo_field = 'geom'
        fields = ['id_objeto', 'nome', 'nomeabrev', 'geometriaaproximada', 'modaluso', 'tipoponte', 'situacaofisica', 'operacional', 'matconstr', 'posicaopista']
        # 'extensao', 'largura', 'vaolivrehoriz', 'vaovertical', 'cargasuportmaxima', 'nrpistas', 'nrfaixas'

        identifiers = ['id_objeto']
        identifier = 'id_objeto'

class SinalizacaoSerializer(GeoFeatureModelSerializer):
    class Meta:
        model = Sinalizacao
        geo_field = 'geom'
        fields = ['id_objeto', 'nome', 'nomeabrev', 'geometriaaproximada', 'situacaofisica', 'operacional', 'tiposinal']

        identifiers = ['id_objeto']
        identifier = 'id_objeto'

class TravessiaSerializer(GeoFeatureModelSerializer):
    class Meta:
        model = Travessia
        geo_field = 'geom'
        fields = ['id_objeto', 'nome', 'nomeabrev', 'geometriaaproximada', 'tipotravessia']

        identifiers = ['id_objeto']
        identifier = 'id_objeto'

class TrechoDutoSerializer(GeoFeatureModelSerializer):
    class Meta:
        model = TrechoDuto
        geo_field = 'geom'
        fields = ['id_objeto', 'nome', 'nomeabrev', 'geometriaaproximada', 'situacaofisica', 'operacional', 'matconstr', 'tipotrechoduto', 'mattransp', 'setor', 'posicaorelativa', 'situacaoespacial']
        # 'nrdutos'

        identifiers = ['id_objeto']
        identifier = 'id_objeto'

class TrechoFerroviarioSerializer(GeoFeatureModelSerializer):
    class Meta:
        model = TrechoFerroviario
        geo_field = 'geom'
        fields = ['id_objeto', 'nome', 'nomeabrev', 'geometriaaproximada', 'situacaofisica', 'operacional', 'codtrechoferrov', 'posicaorelativa', 'tipotrechoferrov', 'bitola', 'eletrificada', 'emarruamento', 'jurisdicao', 'administracao', 'concessionaria', 'nrlinhas']
        # 'cargasuportmaxima'

        identifiers = ['id_objeto']
        identifier = 'id_objeto'

class TrechoHidroviarioSerializer(GeoFeatureModelSerializer):
    class Meta:
        model = TrechoHidroviario
        geo_field = 'geom'
        fields = ['id_objeto', 'nome', 'nomeabrev', 'geometriaaproximada', 'situacaofisica', 'operacional', 'regime']
        # 'caladomaxseca', 'extensaotrecho'

        identifiers = ['id_objeto']
        identifier = 'id_objeto'

class TrechoRodoviarioSerializer(GeoFeatureModelSerializer):
    class Meta:
        model = TrechoRodoviario
        geo_field = 'geom'
        fields = ['id_objeto', 'codtrechorodov', 'tipotrechorod', 'jurisdicao', 'administracao','concessionaria', 'revestimento', 'operacional', 'situacaofisica', 'nrpistas', 'nrfaixas', 'trafego', 'canteirodivisorio', 'capaccarga']

        identifiers = ['id_objeto']
        identifier = 'id_objeto'

class TunelSerializer(GeoFeatureModelSerializer):
    class Meta:
        model = Tunel
        geo_field = 'geom'
        fields = ['id_objeto', 'nome', 'nomeabrev', 'geometriaaproximada', 'modaluso', 'situacaofisica', 'operacional', 'posicaopista', 'matconstr', 'tipotunel']
        # 'extensao', 'largura', 'altura', 'nrpistas', 'nrfaixas'

        identifiers = ['id_objeto']
        identifier = 'id_objeto'

class BrejoPantanoSerializer(GeoFeatureModelSerializer):
    class Meta:
        model = BrejoPantano
        geo_field = 'geom'
        fields = ['id_objeto', 'nome', 'nomeabrev', 'geometriaaproximada', 'antropizada', 'denso', 'tipobrejopantano', 'classificacaoporte']
        # 'alturamediaindividuos'

        identifiers = ['id_objeto']
        identifier = 'id_objeto'

class MangueSerializer(GeoFeatureModelSerializer):
    class Meta:
        model = Mangue
        geo_field = 'geom'
        fields = ['id_objeto', 'nome', 'nomeabrev', 'geometriaaproximada', 'antropizada', 'denso', 'classificacaoporte']
        # 'alturamediaindividuos'

        identifiers = ['id_objeto']
        identifier = 'id_objeto'

class VegRestingaSerializer(GeoFeatureModelSerializer):
    class Meta:
        model = VegRestinga
        geo_field = 'geom'
        fields = ['id_objeto', 'nome', 'nomeabrev', 'geometriaaproximada', 'antropizada', 'denso', 'classificacaoporte']
        # 'alturamediaindividuos'

        identifiers = ['id_objeto']
        identifier = 'id_objeto'

class EdifPubMilitarSerializer(GeoFeatureModelSerializer):
    class Meta:
        model = EdifPubMilitar
        geo_field = 'geom'
        fields = ['id_objeto', 'nome', 'nomeabrev', 'geometriaaproximada', 'tipoedifmil', 'tipousoedif', 'situacaofisica', 'operacional', 'matconstr']

        identifiers = ['id_objeto']
        identifier = 'id_objeto'

class PostoFiscalSerializer(GeoFeatureModelSerializer):
    class Meta:
        model = PostoFiscal
        geo_field = 'geom'
        fields = ['id_objeto', 'nome', 'nomeabrev', 'geometriaaproximada', 'tipopostofisc', 'situacaofisica', 'operacional']

        identifiers = ['id_objeto']
        identifier = 'id_objeto'

class EdifAgropecExtVegetalPescaSerializer(GeoFeatureModelSerializer):
    class Meta:
        model = EdifAgropecExtVegetalPesca
        geo_field = 'geom'
        fields = ['id_objeto', 'nome', 'nomeabrev', 'geometriaaproximada', 'tipoedifagropec', 'situacaofisica', 'operacional', 'matconstr']

        identifiers = ['id_objeto']
        identifier = 'id_objeto'

class EdifIndustrialSerializer(GeoFeatureModelSerializer):
    class Meta:
        model = EdifIndustrial
        geo_field = 'geom'
        fields = ['id_objeto', 'nome', 'nomeabrev', 'geometriaaproximada', 'tipodivisaocnae', 'situacaofisica', 'operacional', 'matconstr', 'chamine']

        identifiers = ['id_objeto']
        identifier = 'id_objeto'

class ExtMineralSerializer(GeoFeatureModelSerializer):
    class Meta:
        model = ExtMineral
        geo_field = 'geom'
        fields = ['id_objeto', 'nome', 'nomeabrev', 'geometriaaproximada', 'tiposecaocnae', 'situacaofisica', 'operacional', 'tipoextmin', 'tipoprodutoresiduo', 'tipopocomina', 'procextracao', 'formaextracao', 'atividade']

        identifiers = ['id_objeto']
        identifier = 'id_objeto'

class EdifReligiosaSerializer(GeoFeatureModelSerializer):
    class Meta:
        model = EdifReligiosa
        geo_field = 'geom'
        fields = ['id_objeto', 'nome', 'nomeabrev', 'geometriaaproximada', 'religiao', 'situacaofisica', 'operacional', 'tipoedifrelig', 'ensino', 'matconstr']

        identifiers = ['id_objeto']
        identifier = 'id_objeto'

class EstGeradEnergiaEletricaSerializer(GeoFeatureModelSerializer):
    class Meta:
        model = EstGeradEnergiaEletrica
        geo_field = 'geom'
        fields = ['id_objeto', 'nome', 'nomeabrev', 'geometriaaproximada', 'codigoestacao', 'situacaofisica', 'operacional', 'destenergelet', 'tipoestgerad']
        # 'potenciaoutorgada', 'potenciafiscalizada'

        identifiers = ['id_objeto']
        identifier = 'id_objeto'

class HidreletricaSerializer(GeoFeatureModelSerializer):
    class Meta:
        model = Hidreletrica
        geo_field = 'geom'
        fields = ['id_objeto', 'nome', 'nomeabrev', 'geometriaaproximada', 'codigohidreletrica', 'situacaofisica', 'operacional']
        # 'potenciaoutorgada', 'potenciafiscalizada'

        identifiers = ['id_objeto']
        identifier = 'id_objeto'

class TermeletricaSerializer(GeoFeatureModelSerializer):
    class Meta:
        model = Termeletrica
        geo_field = 'geom'
        fields = ['id_objeto', 'nome', 'nomeabrev', 'geometriaaproximada', 'combrenovavel', 'situacaofisica', 'operacional', 'tipomaqtermica', 'geracao', 'tipocombustivel']
        # 'potenciaoutorgada', 'potenciafiscalizada'

        identifiers = ['id_objeto']
        identifier = 'id_objeto'

class TorreEnergiaSerializer(GeoFeatureModelSerializer):
    class Meta:
        model = TorreEnergia
        geo_field = 'geom'
        fields = ['id_objeto', 'nome', 'nomeabrev', 'geometriaaproximada', 'situacaofisica', 'operacional', 'arranjofases', 'ovgd', 'tipotorre']
        # 'alturaestimada'

        identifiers = ['id_objeto']
        identifier = 'id_objeto'

class BancoAreiaSerializer(GeoFeatureModelSerializer):
    class Meta:
        model = BancoAreia
        geo_field = 'geom'
        fields = ['id_objeto', 'nome', 'nomeabrev', 'geometriaaproximada', 'tipobanco', 'situacaoemagua', 'materialpredominante']

        identifiers = ['id_objeto']
        identifier = 'id_objeto'

class BarragemSerializer(GeoFeatureModelSerializer):
    class Meta:
        model = Barragem
        geo_field = 'geom'
        fields = ['id_objeto', 'nome', 'nomeabrev', 'geometriaaproximada', 'usoprincipal', 'situacaofisica', 'operacional', 'matconstr']

        identifiers = ['id_objeto']
        identifier = 'id_objeto'

class CorredeiraSerializer(GeoFeatureModelSerializer):
    class Meta:
        model = Corredeira
        geo_field = 'geom'
        fields = ['id_objeto', 'nome', 'nomeabrev', 'geometriaaproximada']

        identifiers = ['id_objeto']
        identifier = 'id_objeto'

class FozMaritimaSerializer(GeoFeatureModelSerializer):
    class Meta:
        model = FozMaritima
        geo_field = 'geom'
        fields = ['id_objeto', 'nome', 'nomeabrev', 'geometriaaproximada']

        identifiers = ['id_objeto']
        identifier = 'id_objeto'

class IlhaSerializer(GeoFeatureModelSerializer):
    class Meta:
        model = Ilha
        geo_field = 'geom'
        fields = ['id_objeto', 'nome', 'nomeabrev', 'geometriaaproximada', 'tipoilha']

        identifiers = ['id_objeto']
        identifier = 'id_objeto'

class MassaDaguaSerializer(GeoFeatureModelSerializer):
    class Meta:
        model = MassaDagua
        geo_field = 'geom'
        fields = ['id_objeto', 'nome', 'nomeabrev', 'geometriaaproximada', 'tipomassadagua', 'salinidade', 'regime']

        identifiers = ['id_objeto']
        identifier = 'id_objeto'

class QuedaDaguaSerializer(GeoFeatureModelSerializer):
    class Meta:
        model = QuedaDagua
        geo_field = 'geom'
        fields = ['id_objeto', 'nome', 'nomeabrev', 'geometriaaproximada', 'tipoqueda']
        # 'altura'

        identifiers = ['id_objeto']
        identifier = 'id_objeto'

class RecifeSerializer(GeoFeatureModelSerializer):
    class Meta:
        model = Recife
        geo_field = 'geom'
        fields = ['id_objeto', 'nome', 'nomeabrev', 'geometriaaproximada', 'tiporecife', 'situamare', 'situacaocosta']

        identifiers = ['id_objeto']
        identifier = 'id_objeto'

class RochaEmAguaSerializer(GeoFeatureModelSerializer):
    class Meta:
        model = RochaEmAgua
        geo_field = 'geom'
        fields = ['id_objeto', 'nome', 'nomeabrev', 'geometriaaproximada', 'situacaoemagua']
        # 'alturalamina'

        identifiers = ['id_objeto']
        identifier = 'id_objeto'

class SumidouroVertedouroSerializer(GeoFeatureModelSerializer):
    class Meta:
        model = SumidouroVertedouro
        geo_field = 'geom'
        fields = ['id_objeto', 'nome', 'nomeabrev', 'geometriaaproximada', 'causa', 'tiposumvert']

        identifiers = ['id_objeto']
        identifier = 'id_objeto'

class TerrenoSujeitoInundacaoSerializer(GeoFeatureModelSerializer):
    class Meta:
        model = TerrenoSujeitoInundacao
        geo_field = 'geom'
        fields = ['id_objeto', 'nome', 'nomeabrev', 'geometriaaproximada', 'periodicidadeinunda']

        identifiers = ['id_objeto']
        identifier = 'id_objeto'

class TrechoDrenagemSerializer(GeoFeatureModelSerializer):
    class Meta:
        model = TrechoDrenagem
        geo_field = 'geom'
        fields = ['id_objeto', 'nome', 'nomeabrev', 'geometriaaproximada', 'profundidademedia', 'coincidecomdentrode', 'compartilhado', 'eixoprincipal', 'navegabilidade', 'regime', 'caladomax', 'larguramedia', 'velocidademedcorrente', 'dentrodepoligono']


        identifiers = ['id_objeto']
        identifier = 'id_objeto'

class TrechoMassaDaguaSerializer(GeoFeatureModelSerializer):
    class Meta:
        model = TrechoMassaDagua
        geo_field = 'geom'
        fields = ['id_objeto', 'nome', 'nomeabrev', 'geometriaaproximada', 'tipotrechomassa', 'salinidade', 'regime']

        identifiers = ['id_objeto']
        identifier = 'id_objeto'

class AreaDesenvolvimentoControleSerializer(GeoFeatureModelSerializer):
    class Meta:
        model = AreaDesenvolvimentoControle
        geo_field = 'geom'
        fields = ['id_objeto', 'nome', 'nomeabrev', 'geometriaaproximada', 'classificacao']

        identifiers = ['id_objeto']
        identifier = 'id_objeto'

class MarcoDeLimiteSerializer(GeoFeatureModelSerializer):
    class Meta:
        model = MarcoDeLimite
        geo_field = 'geom'
        fields = ['id_objeto', 'nome', 'nomeabrev', 'geometriaaproximada', 'tipomarcolim', 'latitude', 'longitude', 'orgresp', 'sistemageodesico', 'outrarefplan', 'outrarefalt', 'referencialaltim']
        # 'altitudeortometrica'


        identifiers = ['id_objeto']
        identifier = 'id_objeto'


class SprintSerializer(ModelSerializer):
    tasks = serializers.HyperlinkedRelatedField(view_name='bcim_v1:task_detail', many=True, read_only=True)

    class Meta:
        model = Sprint
        fields = ['pk', 'name', 'description', 'end', 'tasks']
        identifiers = ['pk' ]
        identifier = 'pk'



class TaskSerializer(ModelSerializer):

    sprint = serializers.HyperlinkedRelatedField(view_name='bcim_v1:sprint_detail', many=False, read_only=True)
    #sprint = serializers.SerializerMethodField()
    class Meta:
        model = Task
        fields = ['id', 'name', 'description',  'sprint', 'status', 'order', 'started', 'due', 'completed']
        identifiers = ['pk']
        identifier = 'pk'


    '''
    def update(self, instance, validated_data):
        a_sprint = self.initial_data['sprint']
        instance.sprint_id = a_sprint
        super(TaskSerializer, self).update( instance, validated_data)
        return instance
    '''

    def create(self, validated_data):
        a_sprint = self.initial_data['sprint']
        validated_data['sprint_id'] = a_sprint
        instance = super(TaskSerializer, self).create(validated_data)
        instance.sprint_id = a_sprint
        return instance

    '''
    def get_sprint(self, a_task):
        if a_task.sprint is None:
            return None
        return  protocol + '://' + host_name + '/' + basic_path +  a_task.sprint.contextclassname + '/' + str(a_task.sprint.id)
    '''


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

