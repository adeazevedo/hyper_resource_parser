from collections import OrderedDict
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.views import APIView
from rest_framework import permissions
from rest_framework import generics
from rest_framework import status

from bcim.contexts import *
from .serializers import *
from hyper_resource.contexts import EntryPointResourceContext
from hyper_resource.resources.EntryPointResource import FeatureEntryPointResource
from hyper_resource.resources.FeatureCollectionResource import FeatureCollectionResource
from hyper_resource.resources.FeatureResource import FeatureResource

class APIRoot(FeatureEntryPointResource):
    serializer_class = EntryPointSerializer
    
    def get_root_response(self, request, format=None, *args, **kwargs):
        root_links = {
            'unidades federativas': reverse('bcim_v1:uf_list', request=request, format=format),
            'municipios': reverse('bcim_v1:municipio_list', request=request, format=format),
            #'outras unidades protegidas': reverse('bcim_v1:outras_unid_protegidas_list', request=request, format=format),
            'outros limites oficiais': reverse('bcim_v1:outros_limites_oficiais_list', request=request, format=format),
            'paises': reverse('bcim_v1:pais_list', request=request, format=format),
            'terras indigenas': reverse('bcim_v1:terra_indigena_list', request=request, format=format),
            'unidades de conservacao nao snuc': reverse('bcim_v1:unidade_conservacao_nao_snuc_list', request=request, format=format),
            'unidades de protecao integral': reverse('bcim_v1:unidade_protecao_integral_list', request=request, format=format),
            'unidades de uso sustentavel': reverse('bcim_v1:unidade_uso_sustentavel_list', request=request, format=format),
            'aglomerados rurais de extensao urbana': reverse('bcim_v1:aglomerado_rural_de_extensao_urbana_list', request=request, format=format),
            'aglomerados rurais isolado': reverse('bcim_v1:aglomerado_rural_isolado_list', request=request, format=format),
            'aldeias indigenas': reverse('bcim_v1:aldeia_indigena_list', request=request, format=format),
            'areas edificadas': reverse('bcim_v1:area_edificada_list', request=request, format=format),
            'capitais': reverse('bcim_v1:capital_list', request=request, format=format),
            'cidades': reverse('bcim_v1:cidade_list', request=request, format=format),
            'vilas': reverse('bcim_v1:vila_list', request=request, format=format),
            'curvas batimetricas': reverse('bcim_v1:curva_batimetrica_list', request=request, format=format),
            #'curvas de nivel': reverse('bcim_v1:curva_nivel_list', request=request, format=format),
            'curvas de nivel': reverse('bcim_v1:curva_nivel_list', request=request, format=format),
            'dunas': reverse('bcim_v1:duna_list', request=request, format=format),
            'elementos fisiografico natural': reverse('bcim_v1:elemento_fisiografico_natural_list', request=request, format=format),
            'picos': reverse('bcim_v1:pico_list', request=request, format=format),
            'pontos cotados altimetricos': reverse('bcim_v1:ponto_cotado_altimetrico_list', request=request, format=format),
            'pontos cotados batimetricos': reverse('bcim_v1:ponto_cotado_batimetrico_list', request=request, format=format),
            'eclusas': reverse('bcim_v1:eclusa_list', request=request, format=format),
            'edificacoes de construcao portuaria': reverse('bcim_v1:edif_const_portuaria_list', request=request, format=format),
            'edificacoes de construcao aeroportuaria': reverse('bcim_v1:edif_const_aeroportuaria_list', request=request, format=format),
            'edificacoes de metro ferroviaria': reverse('bcim_v1:edif_metro_ferroviaria_list', request=request, format=format),
            'fundeadouros': reverse('bcim_v1:fundeadouro_list', request=request, format=format),
            'pistas de ponto pouso': reverse('bcim_v1:pista_ponto_pouso_list', request=request, format=format),
            'pontes': reverse('bcim_v1:ponte_list', request=request, format=format),
            'sinalizacoes': reverse('bcim_v1:sinalizacao_list', request=request, format=format),
            'travessias': reverse('bcim_v1:travessia_list', request=request, format=format),
            'trechos dutos': reverse('bcim_v1:trecho_duto_list', request=request, format=format),
            'trechos ferroviarios': reverse('bcim_v1:trecho_ferroviario_list', request=request, format=format),
            'trechos hidroviarios': reverse('bcim_v1:trecho_hidroviario_list', request=request, format=format),
            #'trechos rodoviarios': reverse('bcim_v1:trecho_rodoviario_list', request=request, format=format),
            'trechos rodoviarios': reverse('bcim_v1:trecho_rodoviario_list', request=request, format=format),
            'tuneis': reverse('bcim_v1:tunel_list', request=request, format=format),
            'brejos e pantanos': reverse('bcim_v1:brejo_pantano_list', request=request, format=format),
            'mangues': reverse('bcim_v1:mangue_list', request=request, format=format),
            'vegetacoes de restinga': reverse('bcim_v1:veg_restinga_list', request=request, format=format),
            'edificacoes publica militar': reverse('bcim_v1:edif_pub_militar_list', request=request, format=format),
            'postos fiscais': reverse('bcim_v1:posto_fiscal_list', request=request, format=format),
            'edificacoes agropecuarias de extracao vegetal e pesca': reverse('bcim_v1:edif_agropec_ext_vegetal_pesca_list', request=request, format=format),
            'edificacoes industrial': reverse('bcim_v1:edif_industrial_list', request=request, format=format),
            'extracoes minerais': reverse('bcim_v1:ext_mineral_list', request=request, format=format),
            'edificacoes religiosa': reverse('bcim_v1:edif_religiosa_list', request=request, format=format),
            'estacoes geradoras de energia eletrica': reverse('bcim_v1:est_gerad_energia_eletrica_list', request=request, format=format),
            'hidreletricas': reverse('bcim_v1:hidreletrica_list', request=request, format=format),
            'termeletricas': reverse('bcim_v1:termeletrica_list', request=request, format=format),
            'torres de energia': reverse('bcim_v1:torre_energia_list', request=request, format=format),
            'bancos de areia': reverse('bcim_v1:banco_areia_list', request=request, format=format),
            'barragens': reverse('bcim_v1:barragem_list', request=request, format=format),
            'corredeiras': reverse('bcim_v1:corredeira_list', request=request, format=format),
            'fozes maritima': reverse('bcim_v1:foz_maritima_list', request=request, format=format),
            'ilhas': reverse('bcim_v1:ilha_list', request=request, format=format),
            'massas dagua': reverse('bcim_v1:massa_dagua_list', request=request, format=format),
            'quedas dagua': reverse('bcim_v1:queda_dagua_list', request=request, format=format),
            'recifes': reverse('bcim_v1:recife_list', request=request, format=format),
            'rochas em agua': reverse('bcim_v1:rocha_em_agua_list', request=request, format=format),
            'sumidouros vertedouros': reverse('bcim_v1:sumidouro_vertedouro_list', request=request, format=format),
            'terrenos sujeito a inundacao': reverse('bcim_v1:terreno_sujeito_inundacao_list', request=request, format=format),
            'trechos de drenagem': reverse('bcim_v1:trecho_drenagem_list', request=request, format=format),
            'trechos de massa dagua': reverse('bcim_v1:trecho_massa_dagua_list', request=request, format=format),
            'areas de desenvolvimento de controle': reverse('bcim_v1:area_desenvolvimento_controle_list', request=request, format=format),
            'marcos de limite': reverse('bcim_v1:marco_de_limite_list', request=request, format=format),
            #'pontos geodesicos': reverse('bcim_v1:ponto_exibicao_wgs84_list', request=request, format=format),
        }

        ordered_dict_of_link = OrderedDict(sorted(root_links.items(), key=lambda t: t[0]))
        return ordered_dict_of_link

class UnidadeFederacaoDetail(FeatureResource):

    serializer_class = UnidadeFederacaoSerializer
    contextclassname = 'unidades-federativas'

    def initialize_context(self):
        self.context_resource = UnidadeFederacaoDetailContext()
        self.context_resource.resource= self

    def get(self, request, format=None, *args, **kwargs):
        if kwargs.get('sigla') is not None:
            kwargs['sigla'] = kwargs.get('sigla').upper()
            self.kwargs['sigla'] = kwargs.get('sigla').upper()
        return super(UnidadeFederacaoDetail, self).get(request, *args, **self.kwargs)

    def options(self, request, *args, **kwargs):
        if kwargs.get('sigla') is not None:
            kwargs['sigla'] = kwargs.get('sigla').upper()
            self.kwargs['sigla'] = kwargs.get('sigla').upper()
        return super(UnidadeFederacaoDetail, self).options(request, *args, **self.kwargs)


class UnidadeFederacaoList(FeatureCollectionResource):

    #queryset = UnidadeFederacao.objects.all()
    serializer_class = UnidadeFederacaoSerializer
    contextclassname = UnidadeFederacao.contextclassname

    def __init__(self):
        super(UnidadeFederacaoList, self).__init__()
        self.iri_metadata = 'http://www.metadados.geo.ibge.gov.br/geonetwork_ibge/srv/por/csw?request=GetRecordById&service=CSW&version=2.0.2&elementSetName=full&id=ff2d4215-9843-4137-bad9-c15f2a8caa9e'
        self.iri_style = 'http://styles.idehco4.tk/styles/unidade_federacao.sld'

    def get_queryset_old(self):

        geocodigo_uf = self.kwargs.get("geocodigo")
        if geocodigo_uf is not None:
            return self.queryset.filter(geocodigo=geocodigo_uf)

        sigla_uf = self.kwargs.get("sigla")
        if sigla_uf is not None:
            return self.queryset.filter(sigla=sigla_uf.upper())

        siglas = self.kwargs.get("siglas")
        if siglas is not None:
            return self.queryset.filter(sigla__in=siglas.split(","))

        return super(UnidadeFederacaoList, self).get_queryset()

    def initialize_context(self):
        self.context_resource = UnidadeFederacaoListContext()
        self.context_resource.resource = self


class MunicipioList(FeatureCollectionResource):

    queryset = Municipio.objects.all()
    serializer_class = MunicipioSerializer
    contextclassname = 'municipios'
    iri_metadata = 'http://www.metadados.geo.ibge.gov.br/geonetwork_ibge/srv/por/csw?request=GetRecordById&service=CSW&version=2.0.2&elementSetName=full&id=3cd8176c-2f59-4eab-8232-3da978d0ecf3'
    iri_style = 'http://styles.idehco4.tk/styles/municipio.sld'

    class Meta:
        managed = False
        db_table = 'lim_municipio_a'

    def initialize_context(self):
        self.context_resource = MunicipioListContext()
        self.context_resource.resource = self

class MunicipioDetail(FeatureResource):

    queryset = Municipio.objects.all()
    serializer_class = MunicipioSerializer
    contextclassname = 'municipios'
    lookup_field = "geocodigo"

    def initialize_context(self):
        self.context_resource = MunicipioDetailContext()
        self.context_resource.resource = self

class BrejoPantanoList(FeatureCollectionResource):

    queryset = BrejoPantano.objects.all()
    serializer_class = BrejoPantanoSerializer
    contextclassname = 'brejos-e-pantanos'

    def initialize_context(self):
        self.context_resource = BrejoPantanoListContext()
        self.context_resource.resource= self

class BrejoPantanoDetail(FeatureResource):

    serializer_class = BrejoPantanoSerializer
    contextclassname = 'brejos-e-pantanos'

    def initialize_context(self):
        self.context_resource = BrejoPantanoListContext()
        self.context_resource.resource= self


class OutrasUnidProtegidasList(FeatureCollectionResource):

    queryset = OutrasUnidProtegidas.objects.all()
    serializer_class = OutrasUnidProtegidasSerializer
    contextclassname = 'outras-unidades-protegidas'

    def initialize_context(self):
        self.context_resource = OutrasUnidProtegidasContext()
        self.context_resource.resource= self

class OutrasUnidProtegidasDetail(FeatureResource):

    serializer_class = OutrasUnidProtegidasSerializer
    contextclassname = 'outras-unidades-protegidas'

    def initialize_context(self):
        self.context_resource = OutrasUnidProtegidasContext()
        self.context_resource.resource= self


class OutrosLimitesOficiaisList(FeatureCollectionResource):

    queryset = OutrosLimitesOficiais.objects.all()
    serializer_class = OutrosLimitesOficiaisSerializer
    contextclassname = 'outros-limites-oficiais'

    def initialize_context(self):
        self.context_resource = OutrosLimitesOficiaisContext()
        self.context_resource.resource= self

class OutrosLimitesOficiaisDetail(FeatureResource):

    serializer_class = OutrosLimitesOficiaisSerializer
    contextclassname = 'outros-limites-oficiais'

    def initialize_context(self):
        self.context_resource = OutrosLimitesOficiaisContext()
        self.context_resource.resource= self

class PaisList(FeatureCollectionResource):

    queryset = Pais.objects.all()
    serializer_class = PaisSerializer
    contextclassname = 'paises'
    def initialize_context(self):
        self.context_resource = PaisListContext()
        self.context_resource.resource= self

class PaisDetail(FeatureResource):

    serializer_class = PaisSerializer
    contextclassname = 'paises'
    def initialize_context(self):
        self.context_resource = PaisListContext()
        self.context_resource.resource= self

class TerraIndigenaList(FeatureCollectionResource):

    queryset = TerraIndigena.objects.all()
    serializer_class = TerraIndigenaSerializer
    contextclassname = 'terras-indigenas'
    def initialize_context(self):
        self.context_resource = TerraIndigenaListContext()
        self.context_resource.resource= self

class TerraIndigenaDetail(FeatureResource):
    serializer_class = TerraIndigenaSerializer
    contextclassname = 'terras-indigenas'
    def initialize_context(self):
        self.context_resource = TerraIndigenaListContext()
        self.context_resource.resource= self

class UnidadeConservacaoNaoSnucList(FeatureCollectionResource):

    queryset = UnidadeConservacaoNaoSnuc.objects.all()
    serializer_class = UnidadeConservacaoNaoSnucSerializer
    contextclassname = 'unidades-de-conservacao-nao-snuc'
    def initialize_context(self):
        self.context_resource = UnidadeConservacaoNaoSnucListContext()
        self.context_resource.resource= self

class UnidadeConservacaoNaoSnucDetail(FeatureResource):

    serializer_class = UnidadeConservacaoNaoSnucSerializer
    contextclassname = 'unidades-de-conservacao-nao-snuc'
    def initialize_context(self):
        self.context_resource = UnidadeConservacaoNaoSnucListContext()
        self.context_resource.resource= self

class UnidadeProtecaoIntegralList(FeatureCollectionResource):

    queryset = UnidadeProtecaoIntegral.objects.all()
    serializer_class = UnidadeProtecaoIntegralSerializer
    contextclassname = 'unidades-de-protecao-integral'
    def initialize_context(self):
        self.context_resource = UnidadeProtecaoIntegralListContext()
        self.context_resource.resource= self

class UnidadeProtecaoIntegralDetail(FeatureResource):

    serializer_class = UnidadeProtecaoIntegralSerializer
    contextclassname = 'unidades-de-protecao-integral'
    def initialize_context(self):
        self.context_resource = UnidadeProtecaoIntegralListContext()
        self.context_resource.resource= self

class UnidadeUsoSustentavelList(FeatureCollectionResource):

    queryset = UnidadeUsoSustentavel.objects.all()
    serializer_class = UnidadeUsoSustentavelSerializer
    contextclassname = 'unidades-de-uso-sustentavel'
    def initialize_context(self):
        self.context_resource = UnidadeUsoSustentavelListContext()
        self.context_resource.resource= self

class UnidadeUsoSustentavelDetail(FeatureResource):

    serializer_class = UnidadeUsoSustentavelSerializer
    contextclassname = 'unidades-de-uso-sustentavel'
    def initialize_context(self):
        self.context_resource = UnidadeUsoSustentavelListContext()
        self.context_resource.resource= self

class AglomeradoRuralDeExtensaoUrbanaList(FeatureCollectionResource):

    queryset = AglomeradoRuralDeExtensaoUrbana.objects.all()
    serializer_class = AglomeradoRuralDeExtensaoUrbanaSerializer
    contextclassname = 'aglomerados-rurais-de-extensao-urbana'

    def initialize_context(self):
        self.context_resource = AglomeradoRuralDeExtensaoUrbanaContext()
        self.context_resource.resource= self

class AglomeradoRuralDeExtensaoUrbanaDetail(FeatureResource):

    serializer_class = AglomeradoRuralDeExtensaoUrbanaSerializer
    contextclassname = 'aglomerados-rurais-de-extensao-urbana'

    def initialize_context(self):
        self.context_resource = AglomeradoRuralDeExtensaoUrbanaContext()
        self.context_resource.resource= self

class AglomeradoRuralIsoladoList(FeatureCollectionResource):

    queryset = AglomeradoRuralIsolado.objects.all()
    serializer_class = AglomeradoRuralIsoladoSerializer
    contextclassname = 'aglomerados-rurais-isolado'

    def initialize_context(self):
        self.context_resource = AglomeradoRuralIsoladoContext()
        self.context_resource.resource= self

class AglomeradoRuralIsoladoDetail(FeatureResource):

    serializer_class = AglomeradoRuralIsoladoSerializer
    contextclassname = 'aglomerados-rurais-isolado'
    def initialize_context(self):
        self.context_resource = AglomeradoRuralIsoladoContext()
        self.context_resource.resource= self
class AldeiaIndigenaList(FeatureCollectionResource):

    queryset = AldeiaIndigena.objects.all()
    serializer_class = AldeiaIndigenaSerializer
    contextclassname = 'aldeias-indigenas'
    def initialize_context(self):
        self.context_resource = AldeiaIndigenaListContext()
        self.context_resource.resource = self

class AldeiaIndigenaListFiltered(FeatureCollectionResource):

    queryset = AldeiaIndigena.objects.all()
    serializer_class = AldeiaIndigenaSerializer
    contextclassname = 'aldeias-indigenas'

class AldeiaIndigenaListFilteredByQueryParameters(FeatureCollectionResource):

    serializer_class = AldeiaIndigenaSerializer
    contextclassname = 'aldeias-indigenas'

class AldeiaIndigenaDetail(FeatureResource):

    serializer_class = AldeiaIndigenaSerializer
    contextclassname = 'aldeias-indigenas'
    def initialize_context(self):
        self.context_resource = AldeiaIndigenaDetailContext()
        self.context_resource.resource = self


class AreaEdificadaList(FeatureCollectionResource):

    queryset = AreaEdificada.objects.all()
    serializer_class = AreaEdificadaSerializer
    contextclassname = 'areas-edificadas'

    def initialize_context(self):
        self.context_resource = AreaEdificadaListContext()
        self.context_resource.resource = self

class AreaEdificadaDetail(FeatureResource):

    serializer_class = AreaEdificadaSerializer
    contextclassname = 'areas-edificadas'

    def initialize_context(self):
        self.context_resource = AreaEdificadaDetailContext()
        self.context_resource.resource = self

class CapitalList(FeatureCollectionResource):

    queryset = Capital.objects.all()
    serializer_class = CapitalSerializer
    contextclassname = 'capitais'
    def initialize_context(self):
        self.context_resource = CapitalListContext()
        self.context_resource.resource = self


class CapitalDetail(FeatureResource):

    queryset = Capital.objects.all()
    serializer_class = CapitalSerializer
    contextclassname = 'capitais'

    def initialize_context(self):
        self.context_resource = CapitalListContext()
        self.context_resource.resource = self

class CidadeList(FeatureCollectionResource):

    queryset = Cidade.objects.all()
    serializer_class = CidadeSerializer
    contextclassname = 'cidades'

    def initialize_context(self):
        self.context_resource = CidadeListContext()
        self.context_resource.resource = self

class CidadeDetail(FeatureResource):

    serializer_class = CidadeSerializer
    contextclassname = 'cidades'
    def initialize_context(self):
        self.context_resource = CidadeListContext()
        self.context_resource.resource = self

class VilaList(FeatureCollectionResource):

    queryset = Vila.objects.all()
    serializer_class = VilaSerializer
    contextclassname = 'vilas'
    def initialize_context(self):
        self.context_resource = VilaListContext()
        self.context_resource.resource = self

class VilaDetail(FeatureResource):

    serializer_class = VilaSerializer
    contextclassname = 'vilas'
    def initialize_context(self):
        self.context_resource = VilaListContext()
        self.context_resource.resource = self

class CurvaBatimetricaList(FeatureCollectionResource):

    queryset = CurvaBatimetrica.objects.all()
    serializer_class = CurvaBatimetricaSerializer
    contextclassname = 'curvas-batimetricas'
    def initialize_context(self):
        self.context_resource = CurvaBatimetricaListContext()
        self.context_resource.resource = self

class CurvaBatimetricaDetail(FeatureResource):

    serializer_class = CurvaBatimetricaSerializer
    contextclassname = 'curvas-batimetricas'
    def initialize_context(self):
        self.context_resource = CurvaBatimetricaListContext()
        self.context_resource.resource = self

class CurvaNivelList(FeatureCollectionResource):

    queryset = CurvaNivel.objects.all()
    serializer_class = CurvaNivelSerializer
    contextclassname ='curvas-de-nivel'
    def initialize_context(self):
        self.context_resource = CurvaNivelListContext()
        self.context_resource.resource = self

class CurvaNivelDetail(FeatureResource):

    serializer_class = CurvaNivelSerializer
    contextclassname = 'curvas-de-nivel'
    def initialize_context(self):
        self.context_resource = CurvaNivelListContext()
        self.context_resource.resource = self

class DunaList(FeatureCollectionResource):

    queryset = Duna.objects.all()
    serializer_class = DunaSerializer
    contextclassname = 'dunas'
    def initialize_context(self):
        self.context_resource = DunaListContext()
        self.context_resource.resource = self


class DunaDetail(FeatureResource):

    serializer_class = DunaSerializer
    contextclassname = 'dunas'
    def initialize_context(self):
        self.context_resource = DunaListContext()
        self.context_resource.resource = self

class ElementoFisiograficoNaturalList(FeatureCollectionResource):

    queryset = ElementoFisiograficoNatural.objects.all()
    serializer_class = ElementoFisiograficoNaturalSerializer
    contextclassname = 'elementos-fisiografico-natural'
    def initialize_context(self):
        self.context_resource = ElementoFisiograficoNaturalListContext()
        self.context_resource.resource = self

class ElementoFisiograficoNaturalDetail(FeatureResource):

    serializer_class = ElementoFisiograficoNaturalSerializer
    contextclassname = 'elementos-fisiografico-natural'
    def initialize_context(self):
        self.context_resource = ElementoFisiograficoNaturalListContext()
        self.context_resource.resource = self

class PicoList(FeatureCollectionResource):

    queryset = Pico.objects.all()
    serializer_class = PicoSerializer
    contextclassname = 'picos'
    def initialize_context(self):
        self.context_resource = PicoListContext()
        self.context_resource.resource = self

class PicoDetail(FeatureResource):

    serializer_class = PicoSerializer
    contextclassname = 'picos'
    def initialize_context(self):
        self.context_resource = PicoListContext()
        self.context_resource.resource = self

class PontoCotadoAltimetricoList(FeatureCollectionResource):

    queryset = PontoCotadoAltimetrico.objects.all()
    serializer_class = PontoCotadoAltimetricoSerializer
    contextclassname = 'pontos-cotados-altimetricos'
    def initialize_context(self):
        self.context_resource = PontoCotadoAltimetricoListContext()
        self.context_resource.resource = self

class PontoCotadoAltimetricoDetail(FeatureResource):

    serializer_class = PontoCotadoAltimetricoSerializer
    contextclassname = 'pontos-cotados-altimetricos'
    def initialize_context(self):
        self.context_resource = PontoCotadoAltimetricoListContext()
        self.context_resource.resource = self

class PontoCotadoBatimetricoList(FeatureCollectionResource):

    queryset = PontoCotadoBatimetrico.objects.all()
    serializer_class = PontoCotadoBatimetricoSerializer
    contextclassname = 'pontos-cotados-batimetricos'
    def initialize_context(self):
        self.context_resource = PontoCotadoBatimetricoListContext()
        self.context_resource.resource = self

class PontoCotadoBatimetricoDetail(FeatureResource):

    serializer_class = PontoCotadoBatimetricoSerializer
    contextclassname = 'pontos-cotados-batimetricos'
    def initialize_context(self):
        self.context_resource = PontoCotadoBatimetricoListContext()
        self.context_resource.resource = self

class EclusaList(FeatureCollectionResource):

    queryset = Eclusa.objects.all()
    serializer_class = EclusaSerializer
    contextclassname = 'eclusas'
    def initialize_context(self):
        self.context_resource = EclusaListContext()
        self.context_resource.resource = self

class EclusaDetail(FeatureResource):

    serializer_class = EclusaSerializer
    contextclassname = 'eclusas'
    def initialize_context(self):
        self.context_resource = EclusaListContext()
        self.context_resource.resource = self

class EdifConstPortuariaList(FeatureCollectionResource):

    queryset = EdifConstPortuaria.objects.all()
    serializer_class = EdifConstPortuariaSerializer
    contextclassname = 'edificacoes-de-construcao-portuaria'
    def initialize_context(self):
        self.context_resource = EdifConstPortuariaListContext()
        self.context_resource.resource = self

class EdifConstPortuariaDetail(FeatureResource):

    serializer_class = EdifConstPortuariaSerializer
    contextclassname = 'edificacoes-de-construcao-portuaria'
    def initialize_context(self):
        self.context_resource = EdifConstPortuariaListContext()
        self.context_resource.resource = self

class EdifConstrAeroportuariaList(FeatureCollectionResource):

    queryset = EdifConstrAeroportuaria.objects.all()
    serializer_class = EdifConstrAeroportuariaSerializer
    contextclassname = 'edificacoes-de-construcao-aeroportuaria'
    def initialize_context(self):
        self.context_resource = EdifConstrAeroportuariaListContext()
        self.context_resource.resource = self

class EdifConstrAeroportuariaDetail(FeatureResource):

    serializer_class = EdifConstrAeroportuariaSerializer
    contextclassname = 'edificacoes-de-construcao-aeroportuaria'
    def initialize_context(self):
        self.context_resource = EdifConstrAeroportuariaListContext()
        self.context_resource.resource = self

class EdifMetroFerroviariaList(FeatureCollectionResource):

    queryset = EdifMetroFerroviaria.objects.all()
    serializer_class = EdifMetroFerroviariaSerializer
    contextclassname = 'edificacoes-metro-ferroviaria'
    def initialize_context(self):
        self.context_resource = EdifMetroFerroviariaListContext()
        self.context_resource.resource = self

class EdifMetroFerroviariaDetail(FeatureResource):

    serializer_class = EdifMetroFerroviariaSerializer
    contextclassname = 'edificacoes-metro-ferroviaria'
    def initialize_context(self):
        self.context_resource = EdifMetroFerroviariaListContext()
        self.context_resource.resource = self


class FundeadouroList(FeatureCollectionResource):

    queryset = Fundeadouro.objects.all()
    serializer_class = FundeadouroSerializer
    contextclassname = 'fundeadouros'
    def initialize_context(self):
        self.context_resource = FundeadouroListContext()
        self.context_resource.resource = self


class FundeadouroDetail(FeatureResource):

    serializer_class = FundeadouroSerializer
    contextclassname = 'fundeadouros'
    def initialize_context(self):
        self.context_resource = FundeadouroListContext()
        self.context_resource.resource = self

class PistaPontoPousoList(FeatureCollectionResource):

    queryset = PistaPontoPouso.objects.all()
    serializer_class = PistaPontoPousoSerializer
    contextclassname = 'pistas-de-ponto-pouso'
    def initialize_context(self):
        self.context_resource = PistaPontoPousoListContext()
        self.context_resource.resource = self

class PistaPontoPousoDetail(FeatureResource):

    serializer_class = PistaPontoPousoSerializer
    contextclassname = 'pistas-de-ponto-pouso'
    def initialize_context(self):
        self.context_resource = PistaPontoPousoListContext()
        self.context_resource.resource = self

class PonteList(FeatureCollectionResource):

    queryset = Ponte.objects.all()
    serializer_class = PonteSerializer
    contextclassname = 'pontes'
    def initialize_context(self):
        self.context_resource = PonteListContext()
        self.context_resource.resource = self

class PonteDetail(FeatureResource):

    serializer_class = PonteSerializer
    contextclassname = 'pontes'
    def initialize_context(self):
        self.context_resource = PonteListContext()
        self.context_resource.resource = self

class SinalizacaoList(FeatureCollectionResource):

    queryset = Sinalizacao.objects.all()
    serializer_class = SinalizacaoSerializer
    contextclassname = 'sinalizacaoes'
    def initialize_context(self):
        self.context_resource = SinalizacaoListContext()
        self.context_resource.resource = self

class SinalizacaoDetail(FeatureResource):

    serializer_class = SinalizacaoSerializer
    contextclassname = 'sinalizacaoes'
    def initialize_context(self):
        self.context_resource = SinalizacaoListContext()
        self.context_resource.resource = self

class TravessiaList(FeatureCollectionResource):

    queryset = Travessia.objects.all()
    serializer_class = TravessiaSerializer
    contextclassname = 'travessias'
    def initialize_context(self):
        self.context_resource = TravessiaListContext()
        self.context_resource.resource = self

class TravessiaDetail(FeatureResource):

    serializer_class = TravessiaSerializer
    contextclassname = 'travessias'
    def initialize_context(self):
        self.context_resource = TravessiaListContext()
        self.context_resource.resource = self

class TrechoDutoList(FeatureCollectionResource):

    queryset = TrechoDuto.objects.all()
    serializer_class = TrechoDutoSerializer
    contextclassname = 'trechos-dutos'
    def initialize_context(self):
        self.context_resource = TrechoDutoListContext()
        self.context_resource.resource = self

class TrechoDutoDetail(FeatureResource):

    serializer_class = TrechoDutoSerializer
    contextclassname = 'trechos-dutos'
    def initialize_context(self):
        self.context_resource = TrechoDutoListContext()
        self.context_resource.resource = self

class TrechoFerroviarioList(FeatureCollectionResource):

    def __init__(self):
        super(TrechoFerroviarioList, self).__init__()
        self.iri_metadata = "http://www.metadados.inde.gov.br/geonetwork/srv/por/csw?service=CSW&version=2.0.2&request=GetRecordById&id=556709aa-69bf-4b18-b8ce-515190e59d22&elementsetname=full"

    queryset = TrechoFerroviario.objects.all()
    serializer_class = TrechoFerroviarioSerializer
    contextclassname = 'trechos-ferroviarios'
    def initialize_context(self):
        self.context_resource = TrechoFerroviarioListContext()
        self.context_resource.resource= self

class TrechoFerroviarioDetail(FeatureResource):

    serializer_class = TrechoFerroviarioSerializer
    contextclassname = 'trechos-ferroviarios'
    def initialize_context(self):
        self.context_resource = TrechoFerroviarioDetailContext()
        self.context_resource.resource= self

class TrechoHidroviarioList(FeatureCollectionResource):

    queryset = TrechoHidroviario.objects.all()
    serializer_class = TrechoHidroviarioSerializer
    contextclassname = 'trechos-hidroviarios'
    def initialize_context(self):
        self.context_resource = TrechoHidroviarioListContext()
        self.context_resource.resource = self

class TrechoHidroviarioDetail(FeatureResource):

    serializer_class = TrechoHidroviarioSerializer
    contextclassname = 'trechos-hidroviarios'
    def initialize_context(self):
        self.context_resource = TrechoHidroviarioListContext()
        self.context_resource.resource = self

class TrechoRodoviarioList(FeatureCollectionResource):

    queryset = TrechoRodoviario.objects.all()
    serializer_class = TrechoRodoviarioSerializer
    contextclassname = 'trechos-rodoviarios'
    def initialize_context(self):
        self.context_resource = TrechoRodoviarioListContext()
        self.context_resource.resource = self

class TrechoRodoviarioDetail(FeatureResource):

    serializer_class = TrechoRodoviarioSerializer
    contextclassname = 'trechos-rodoviarios'
    def initialize_context(self):
        self.context_resource = TrechoRodoviarioListContext()
        self.context_resource.resource = self

class TunelList(FeatureCollectionResource):

    queryset = Tunel.objects.all()
    serializer_class = TunelSerializer
    contextclassname = 'tuneis'
    def initialize_context(self):
        self.context_resource = TunelListContext()
        self.context_resource.resource = self

class TunelDetail(FeatureResource):

    serializer_class = TunelSerializer
    contextclassname = 'tuneis'
    def initialize_context(self):
        self.context_resource = TunelListContext()
        self.context_resource.resource = self


class MangueList(FeatureCollectionResource):

    queryset = Mangue.objects.all()
    serializer_class = MangueSerializer
    contextclassname = 'mangues'

    def initialize_context(self):
        self.context_resource = MangueListContext()
        self.context_resource.resource= self

class MangueDetail(FeatureResource):

    serializer_class = MangueSerializer
    contextclassname  = 'mangues'
    def initialize_context(self):
        self.context_resource = MangueListContext()
        self.context_resource.resource= self

class VegRestingaList(FeatureCollectionResource):

    queryset = VegRestinga.objects.all()
    serializer_class = VegRestingaSerializer
    contextclassname = 'vegetacoes-de-restinga'
    def initialize_context(self):
        self.context_resource = VegRestingaListContext()
        self.context_resource.resource= self


class VegRestingaDetail(FeatureResource):

    serializer_class = VegRestingaSerializer
    contextclassname = 'vegetacoes-de-restinga'
    def initialize_context(self):
        self.context_resource = VegRestingaListContext()
        self.context_resource.resource= self

class EdifPubMilitarList(FeatureCollectionResource):

    queryset = EdifPubMilitar.objects.all()
    serializer_class = EdifPubMilitarSerializer
    contextclassname = 'edificacoes-publica-militar'
    def initialize_context(self):
        self.context_resource = EdifPubMilitarListContext()
        self.context_resource.resource= self

class EdifPubMilitarDetail(FeatureResource):

    serializer_class = EdifPubMilitarSerializer
    contextclassname = 'edificacoes-publica-militar'

    def initialize_context(self):
       self.context_resource = EdifPubMilitarListContext()
       self.context_resource.resource = self


class PostoFiscalList(FeatureCollectionResource):

    queryset = PostoFiscal.objects.all()
    serializer_class = PostoFiscalSerializer
    contextclassname = 'postos-fiscais'

    def initialize_context(self):
      self.context_resource = PostoFiscalListContext()
      self.context_resource.resource = self


class PostoFiscalDetail(FeatureResource):

    serializer_class = PostoFiscalSerializer
    contextclassname = 'postos-fiscais'

    def initialize_context(self):
        self.context_resource = PostoFiscalListContext()
        self.context_resource.resource = self

class EdifAgropecExtVegetalPescaList(FeatureCollectionResource):

    queryset = EdifAgropecExtVegetalPesca.objects.all()
    serializer_class = EdifAgropecExtVegetalPescaSerializer
    contextclassname = 'edificacoes-agropecuarias-de-extracao-vegetal-e-pesca'

    def initialize_context(self):
        self.context_resource = EdifAgropecExtVegetalPescaListContext()
        self.context_resource.resource = self

class EdifAgropecExtVegetalPescaDetail(FeatureResource):

    serializer_class = EdifAgropecExtVegetalPescaSerializer
    contextclassname = 'edificacoes-agropecuarias-de-extracao-vegetal-e-pesca'
    def initialize_context(self):
        self.context_resource = EdifAgropecExtVegetalPescaListContext()
        self.context_resource.resource = self

class EdifIndustrialList(FeatureCollectionResource):

    queryset = EdifIndustrial.objects.all()
    serializer_class = EdifIndustrialSerializer
    contextclassname = 'edificacoes-industrial'
    def initialize_context(self):
        self.context_resource = EdifIndustrialListContext()
        self.context_resource.resource = self

class EdifIndustrialDetail(FeatureResource):

    serializer_class = EdifIndustrialSerializer
    contextclassname = 'edificacoes-industrial'
    def initialize_context(self):
        self.context_resource = EdifIndustrialListContext()
        self.context_resource.resource = self

class ExtMineralList(FeatureCollectionResource):

    queryset = ExtMineral.objects.all()
    serializer_class = ExtMineralSerializer
    contextclassname = 'extracoes-minerais'
    def initialize_context(self):
        self.context_resource = ExtMineralListContext()
        self.context_resource.resource = self

class ExtMineralDetail(FeatureResource):

    serializer_class = ExtMineralSerializer
    contextclassname = 'extracoes-minerais'
    def initialize_context(self):
        self.context_resource = ExtMineralListContext()
        self.context_resource.resource = self

class EdifReligiosaList(FeatureCollectionResource):

    queryset = EdifReligiosa.objects.all()
    serializer_class = EdifReligiosaSerializer
    contextclassname = 'edificacoes-religiosa'
    def initialize_context(self):
        self.context_resource = EdifReligiosaListContext()
        self.context_resource.resource = self

class EdifReligiosaDetail(FeatureResource):

    serializer_class = EdifReligiosaSerializer
    contextclassname = 'edificacoes-religiosa'
    def initialize_context(self):
        self.context_resource = EdifReligiosaListContext()
        self.context_resource.resource = self

class EstGeradEnergiaEletricaList(FeatureCollectionResource):

    queryset = EstGeradEnergiaEletrica.objects.all()
    serializer_class = EstGeradEnergiaEletricaSerializer
    contextclassname = 'estacoes-geradoras-de-energia-eletrica'
    def initialize_context(self):
        self.context_resource = EstGeradEnergiaEletricaListContext()
        self.context_resource.resource = self

class EstGeradEnergiaEletricaDetail(FeatureResource):

    serializer_class = EstGeradEnergiaEletricaSerializer
    contextclassname = 'estacoes-geradoras-de-energia-eletrica'
    def initialize_context(self):
        self.context_resource = EstGeradEnergiaEletricaListContext()
        self.context_resource.resource = self

class HidreletricaList(FeatureCollectionResource):

    queryset = Hidreletrica.objects.all()
    serializer_class = HidreletricaSerializer
    contextclassname = 'hidreletricas'
    def initialize_context(self):
        self.context_resource = HidreletricaListContext()
        self.context_resource.resource = self

class HidreletricaDetail(FeatureResource):

    serializer_class = HidreletricaSerializer
    contextclassname = 'hidreletricas'
    def initialize_context(self):
        self.context_resource = HidreletricaListContext()
        self.context_resource.resource = self

class TermeletricaList(FeatureCollectionResource):

    queryset = Termeletrica.objects.all()
    serializer_class = TermeletricaSerializer
    contextclassname = 'termeletricas'
    def initialize_context(self):
        self.context_resource = TermeletricaListContext()
        self.context_resource.resource = self

class TermeletricaDetail(FeatureResource):

    serializer_class = TermeletricaSerializer
    contextclassname = 'termeletricas'
    def initialize_context(self):
        self.context_resource = TermeletricaListContext()
        self.context_resource.resource = self

class TorreEnergiaList(FeatureCollectionResource):

    queryset = TorreEnergia.objects.all()
    serializer_class = TorreEnergiaSerializer
    contextclassname = 'torres-de-energia'
    def initialize_context(self):
        self.context_resource = TorreEnergiaListContext()
        self.context_resource.resource = self

class TorreEnergiaDetail(FeatureResource):

    serializer_class = TorreEnergiaSerializer
    contextclassname = 'torres-de-energia'
    def initialize_context(self):
        self.context_resource = TorreEnergiaListContext()
        self.context_resource.resource = self

class BancoAreiaList(FeatureCollectionResource):

    queryset = BancoAreia.objects.all()
    serializer_class = BancoAreiaSerializer
    contextclassname = 'bancos-de-areia'

    def initialize_context(self):
        self.context_resource = BancoAreiaListContext()
        self.context_resource.resource= self

class BancoAreiaDetail(FeatureResource):

    serializer_class = BancoAreiaSerializer
    contextclassname = 'bancos-de-areia'

    def initialize_context(self):
        self.context_resource = BancoAreiaDetailContext()
        self.context_resource.resource= self

class BarragemList(FeatureCollectionResource):

    queryset = Barragem.objects.all()
    serializer_class = BarragemSerializer
    contextclassname = 'barragens'

    def initialize_context(self):
        self.context_resource = BarragemListContext()
        self.context_resource.resource= self

class BarragemDetail(FeatureResource):

    serializer_class = BarragemSerializer
    contextclassname = 'barragens'

    def initialize_context(self):
        self.context_resource = BarragemListContext()
        self.context_resource.resource= self

class CorredeiraList(FeatureCollectionResource):

    queryset = Corredeira.objects.all()
    serializer_class = CorredeiraSerializer
    contextclassname = 'corredeiras'

    def initialize_context(self):
        self.context_resource = CorredeiraListContext()
        self.context_resource.resource = self

class CorredeiraDetail(FeatureResource):

    serializer_class = CorredeiraSerializer
    contextclassname = 'corredeiras'

    def initialize_context(self):
        self.context_resource = CorredeiraListContext()
        self.context_resource.resource = self

class FozMaritimaList(FeatureCollectionResource):

    queryset = FozMaritima.objects.all()
    serializer_class = FozMaritimaSerializer
    contextclassname = 'fozes-maritima'
    def initialize_context(self):
        self.context_resource = FozMaritimaListContext()
        self.context_resource.resource = self

class FozMaritimaDetail(FeatureResource):

    serializer_class = FozMaritimaSerializer
    contextclassname = 'fozes-maritima'
    def initialize_context(self):
        self.context_resource = FozMaritimaListContext()
        self.context_resource.resource = self

class IlhaList(FeatureCollectionResource):

    queryset = Ilha.objects.all()
    serializer_class = IlhaSerializer
    contextclassname = 'ilhas'
    def initialize_context(self):
        self.context_resource = IlhaListContext()
        self.context_resource.resource = self

class IlhaDetail(FeatureResource):

    serializer_class = IlhaSerializer
    contextclassname = 'ilhas'
    def initialize_context(self):
        self.context_resource = IlhaListContext()
        self.context_resource.resource = self

class MassaDaguaList(FeatureCollectionResource):

    queryset = MassaDagua.objects.all()
    serializer_class = MassaDaguaSerializer
    contextclassname = 'massas-dagua'
    def initialize_context(self):
        self.context_resource = MassaDaguaListContext()
        self.context_resource.resource = self

class MassaDaguaDetail(FeatureResource):

    serializer_class = MassaDaguaSerializer
    contextclassname = 'massas-dagua'
    def initialize_context(self):
        self.context_resource = MassaDaguaListContext()
        self.context_resource.resource = self

class QuedaDaguaList(FeatureCollectionResource):

    queryset = QuedaDagua.objects.all()
    serializer_class = QuedaDaguaSerializer
    contextclassname = 'quedas-dagua'
    def initialize_context(self):
        self.context_resource = QuedaDaguaListContext()
        self.context_resource.resource = self

class QuedaDaguaDetail(FeatureResource):

    serializer_class = QuedaDaguaSerializer
    contextclassname = 'quedas-dagua'
    def initialize_context(self):
        self.context_resource = QuedaDaguaListContext()
        self.context_resource.resource = self

class RecifeList(FeatureCollectionResource):

    #queryset = Recife.objects.all()
    serializer_class = RecifeSerializer
    contextclassname = 'recifes'
    def initialize_context(self):
        self.context_resource = RecifeListContext()
        self.context_resource.resource = self

class RecifeDetail(FeatureResource):

    serializer_class = RecifeSerializer
    contextclassname = 'recifes'
    def initialize_context(self):
        self.context_resource = RecifeListContext()
        self.context_resource.resource = self

class RochaEmAguaList(FeatureCollectionResource):

    queryset = RochaEmAgua.objects.all()
    serializer_class = RochaEmAguaSerializer
    contextclassname = 'rochas-em-agua'
    def initialize_context(self):
        self.context_resource = RochaEmAguaListContext()
        self.context_resource.resource = self

class RochaEmAguaDetail(FeatureResource):

    serializer_class = RochaEmAguaSerializer
    contextclassname = 'rochas-em-agua'
    def initialize_context(self):
        self.context_resource = RochaEmAguaListContext()
        self.context_resource.resource = self

class SumidouroVertedouroList(FeatureCollectionResource):

    queryset = SumidouroVertedouro.objects.all()
    serializer_class = SumidouroVertedouroSerializer
    contextclassname = 'sumidouros-vertedouros'
    def initialize_context(self):
        self.context_resource = SumidouroVertedouroListContext()
        self.context_resource.resource = self

class SumidouroVertedouroDetail(FeatureResource):

    serializer_class = SumidouroVertedouroSerializer
    contextclassname = 'sumidouros-vertedouros'
    def initialize_context(self):
        self.context_resource = SumidouroVertedouroListContext()
        self.context_resource.resource = self

class TerrenoSujeitoInundacaoList(FeatureCollectionResource):

    queryset = TerrenoSujeitoInundacao.objects.all()
    serializer_class = TerrenoSujeitoInundacaoSerializer
    contextclassname = 'terrenos-sujeito-a-inundacao'
    def initialize_context(self):
        self.context_resource = TerrenoSujeitoInundacaoListContext()
        self.context_resource.resource = self

class TerrenoSujeitoInundacaoDetail(FeatureResource):

    serializer_class = TerrenoSujeitoInundacaoSerializer
    contextclassname = 'terrenos-sujeito-a-inundacao'
    def initialize_context(self):
        self.context_resource = TerrenoSujeitoInundacaoListContext()
        self.context_resource.resource = self

class TrechoDrenagemList(FeatureCollectionResource):

    queryset = TrechoDrenagem.objects.all()
    serializer_class = TrechoDrenagemSerializer
    contextclassname = 'trechos-de-drenagem'
    def initialize_context(self):
        self.context_resource = TrechoDrenagemListContext()
        self.context_resource.resource = self

class TrechoDrenagemDetail(FeatureResource):

    serializer_class = TrechoDrenagemSerializer
    contextclassname = 'trechos-de-drenagem'
    def initialize_context(self):
        self.context_resource = TrechoDrenagemListContext()
        self.context_resource.resource = self

class TrechoMassaDaguaList(FeatureCollectionResource):

    queryset = TrechoMassaDagua.objects.all()
    serializer_class = TrechoMassaDaguaSerializer
    contextclassname = 'trechos-de-massa-dagua'
    def initialize_context(self):
        self.context_resource = TrechoMassaDaguaListContext()
        self.context_resource.resource = self

class TrechoMassaDaguaDetail(FeatureResource):

    serializer_class = TrechoMassaDaguaSerializer
    contextclassname = 'trechos-de-massa-dagua'
    def initialize_context(self):
        self.context_resource = TrechoMassaDaguaListContext()
        self.context_resource.resource = self

class AreaDesenvolvimentoControleList(FeatureCollectionResource):

    queryset = AreaDesenvolvimentoControle.objects.all()
    serializer_class = AreaDesenvolvimentoControleSerializer
    contextclassname = 'areas-de-desenvolvimento-de-controle'
    def initialize_context(self):
        self.context_resource = AreaDesenvolvimentoControleListContext()
        self.context_resource.resource = self

class AreaDesenvolvimentoControleDetail(FeatureResource):

    serializer_class = AreaDesenvolvimentoControleSerializer
    contextclassname = 'areas-de-desenvolvimento-de-controle'
    def initialize_context(self):
        self.context_resource = AreaDesenvolvimentoControleListContext()
        self.context_resource.resource = self

class MarcoDeLimiteList(FeatureCollectionResource):

    queryset = MarcoDeLimite.objects.all()
    serializer_class = MarcoDeLimiteSerializer
    contextclassname = 'marcos-de-limite'
    def initialize_context(self):
        self.context_resource = MarcoDeLimiteListContext()
        self.context_resource.resource = self

class MarcoDeLimiteDetail(FeatureResource):

    serializer_class = MarcoDeLimiteSerializer
    contextclassname = 'marcos-de-limite'
    def initialize_context(self):
        self.context_resource = MarcoDeLimiteListContext()
        self.context_resource.resource = self