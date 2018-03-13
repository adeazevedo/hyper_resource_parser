from collections import OrderedDict
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.views import APIView
from rest_framework import permissions
from rest_framework import generics
from rest_framework import status

from bcim.contexts import *
from .serializers import *
from hyper_resource.views import *


def get_root_response(request):
    format = None
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

class APIRoot(APIView):

    def __init__(self):
        super(APIRoot, self).__init__()
        self.base_context = BaseContext('api-root')

    def add_url_in_header(self, url, response, rel):
        link = ' <'+url+'>; rel=\"'+rel+'\" '
        if "Link" not in response:
            response['Link'] = link
        else:
            response['Link'] += "," + link
        return response

    def options(self, request, *args, **kwargs):
        context = self.base_context.getContextData(request)
        root_links = get_root_response(request)
        context.update(root_links)
        response = Response(context, status=status.HTTP_200_OK, content_type="application/ld+json")
        entry_pointURL = reverse('bcim_v1:api_root', request=request)
        response = self.add_url_in_header(entry_pointURL, response, 'http://schema.org/EntryPoint')
        response = self.base_context.addContext(request, response)
        return response

    def get(self, request, *args, **kwargs):
        root_links = get_root_response(request)
        response = Response(root_links)
        entry_pointURL = reverse('bcim_v1:api_root', request=request)
        response = self.add_url_in_header(entry_pointURL, response, 'http://schema.org/EntryPoint')
        return self.base_context.addContext(request, response)


class UnidadeFederacaoDetail(FeatureResource):

    serializer_class = UnidadeFederacaoSerializer
    contextclassname = 'unidades-federativas'

    def initialize_context(self):
        self.context_resource = UnidadeFederacaoContext()
        self.context_resource.resource= self

    def get(self, request, *args, **kwargs):
        if kwargs.get('sigla') is not None:
            kwargs['sigla'] = kwargs.get('sigla').upper()
        return super(UnidadeFederacaoDetail, self).get(request, *args, **kwargs)

    def options(self, request, *args, **kwargs):
        if kwargs.get('sigla') is not None:
            kwargs['sigla'] = kwargs.get('sigla').upper()
        return super(UnidadeFederacaoDetail, self).options(request, *args, **kwargs)


class UnidadeFederacaoList(FeatureCollectionResource):

    #queryset = UnidadeFederacao.objects.all()
    serializer_class = UnidadeFederacaoSerializer
    contextclassname = UnidadeFederacao.contextclassname
    iri_metadata = 'http://www.metadados.geo.ibge.gov.br/geonetwork_ibge/srv/por/csw?request=GetRecordById&service=CSW&version=2.0.2&elementSetName=full&id=ff2d4215-9843-4137-bad9-c15f2a8caa9e'
    iri_style = 'http://styles.idehco4.tk/styles/unidade_federacao.sld'

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


class OutrosLimitesOficiaisContext(object):
    pass


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

class PaisDetail(FeatureResource):

    serializer_class = PaisSerializer
    contextclassname = 'paises'

class TerraIndigenaList(FeatureCollectionResource):

    queryset = TerraIndigena.objects.all()
    serializer_class = TerraIndigenaSerializer
    contextclassname = 'terras-indigenas'

class TerraIndigenaDetail(FeatureResource):
    serializer_class = TerraIndigenaSerializer
    contextclassname = 'terras-indigenas'

class UnidadeConservacaoNaoSnucList(FeatureCollectionResource):

    queryset = UnidadeConservacaoNaoSnuc.objects.all()
    serializer_class = UnidadeConservacaoNaoSnucSerializer
    contextclassname = 'unidades-de-conservacao-nao-snuc'

class UnidadeConservacaoNaoSnucDetail(FeatureResource):

    serializer_class = UnidadeConservacaoNaoSnucSerializer
    contextclassname = 'unidades-de-conservacao-nao-snuc'

class UnidadeProtecaoIntegralList(FeatureCollectionResource):

    queryset = UnidadeProtecaoIntegral.objects.all()
    serializer_class = UnidadeProtecaoIntegralSerializer
    contextclassname = 'unidades-de-protecao-integral'

class UnidadeProtecaoIntegralDetail(FeatureResource):

    serializer_class = UnidadeProtecaoIntegralSerializer
    contextclassname = 'unidades-de-protecao-integral'

class UnidadeUsoSustentavelList(FeatureCollectionResource):

    queryset = UnidadeUsoSustentavel.objects.all()
    serializer_class = UnidadeUsoSustentavelSerializer
    contextclassname = 'unidades-de-uso-sustentavel'

class UnidadeUsoSustentavelDetail(FeatureResource):

    serializer_class = UnidadeUsoSustentavelSerializer
    contextclassname = 'unidades-de-uso-sustentavel'

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

class AreaEdificadaDetail(FeatureResource):

    serializer_class = AreaEdificadaSerializer
    contextclassname = 'areas-edificadas'

class CapitalList(FeatureCollectionResource):

    queryset = Capital.objects.all()
    serializer_class = CapitalSerializer
    contextclassname = 'capitais'


class CapitalDetail(FeatureResource):

    queryset = Capital.objects.all()
    serializer_class = CapitalSerializer
    contextclassname = 'capitais'

class CidadeList(FeatureCollectionResource):

    queryset = Cidade.objects.all()
    serializer_class = CidadeSerializer
    contextclassname = 'cidades'

class CidadeDetail(FeatureResource):

    serializer_class = CidadeSerializer
    contextclassname = 'cidades'

class VilaList(FeatureCollectionResource):

    queryset = Vila.objects.all()
    serializer_class = VilaSerializer
    contextclassname = 'vilas'

class VilaDetail(FeatureResource):

    serializer_class = VilaSerializer
    contextclassname = 'vilas'

class CurvaBatimetricaList(FeatureCollectionResource):

    queryset = CurvaBatimetrica.objects.all()
    serializer_class = CurvaBatimetricaSerializer
    contextclassname = 'curvas-batimetricas'

class CurvaBatimetricaDetail(FeatureResource):

    serializer_class = CurvaBatimetricaSerializer
    contextclassname = 'curvas-batimetricas'

class CurvaNivelList(FeatureCollectionResource):

    queryset = CurvaNivel.objects.all()
    serializer_class = CurvaNivelSerializer
    contextclassname ='curvas-de-nivel'

class CurvaNivelDetail(FeatureResource):

    serializer_class = CurvaNivelSerializer
    contextclassname = 'curvas-de-nivel'

class DunaList(FeatureCollectionResource):

    queryset = Duna.objects.all()
    serializer_class = DunaSerializer
    contextclassname = 'dunas'

class DunaDetail(FeatureResource):

    serializer_class = DunaSerializer
    contextclassname = 'dunas'

class ElementoFisiograficoNaturalList(FeatureCollectionResource):

    queryset = ElementoFisiograficoNatural.objects.all()
    serializer_class = ElementoFisiograficoNaturalSerializer
    contextclassname = 'elementos-fisiografico-natural'

class ElementoFisiograficoNaturalDetail(FeatureResource):

    serializer_class = ElementoFisiograficoNaturalSerializer
    contextclassname = 'elementos-fisiografico-natural'

class PicoList(FeatureCollectionResource):

    queryset = Pico.objects.all()
    serializer_class = PicoSerializer
    contextclassname = 'picos'

class PicoDetail(FeatureResource):

    serializer_class = PicoSerializer
    contextclassname = 'picos'

class PontoCotadoAltimetricoList(FeatureCollectionResource):

    queryset = PontoCotadoAltimetrico.objects.all()
    serializer_class = PontoCotadoAltimetricoSerializer
    contextclassname = 'pontos-cotados-altimetricos'

class PontoCotadoAltimetricoDetail(FeatureResource):

    serializer_class = PontoCotadoAltimetricoSerializer
    contextclassname = 'pontos-cotados-altimetricos'

class PontoCotadoBatimetricoList(FeatureCollectionResource):

    queryset = PontoCotadoBatimetrico.objects.all()
    serializer_class = PontoCotadoBatimetricoSerializer
    contextclassname = 'pontos-cotados-batimetricos'

class PontoCotadoBatimetricoDetail(FeatureResource):

    serializer_class = PontoCotadoBatimetricoSerializer
    contextclassname = 'pontos-cotados-batimetricos'

class EclusaList(FeatureCollectionResource):

    queryset = Eclusa.objects.all()
    serializer_class = EclusaSerializer
    contextclassname = 'eclusas'

class EclusaDetail(FeatureResource):

    serializer_class = EclusaSerializer
    contextclassname = 'eclusas'

class EdifConstPortuariaList(FeatureCollectionResource):

    queryset = EdifConstPortuaria.objects.all()
    serializer_class = EdifConstPortuariaSerializer
    contextclassname = 'edificacoes-de-construcao-portuaria'

class EdifConstPortuariaDetail(FeatureResource):

    serializer_class = EdifConstPortuariaSerializer
    contextclassname = 'edificacoes-de-construcao-portuaria'

class EdifConstrAeroportuariaList(FeatureCollectionResource):

    queryset = EdifConstrAeroportuaria.objects.all()
    serializer_class = EdifConstrAeroportuariaSerializer
    contextclassname = 'edificacoes-de-construcao-aeroportuaria'

class EdifConstrAeroportuariaDetail(FeatureResource):

    serializer_class = EdifConstPortuariaSerializer
    contextclassname = 'edificacoes-de-construcao-aeroportuaria'

class EdifMetroFerroviariaList(FeatureCollectionResource):

    queryset = EdifMetroFerroviaria.objects.all()
    serializer_class = EdifMetroFerroviariaSerializer
    contextclassname = 'edificacoes-metro-ferroviaria'

class EdifMetroFerroviariaDetail(FeatureResource):

    serializer_class = EdifMetroFerroviariaSerializer
    contextclassname = 'edificacoes-metro-ferroviaria'

class FundeadouroList(FeatureCollectionResource):

    queryset = Fundeadouro.objects.all()
    serializer_class = FundeadouroSerializer
    contextclassname = 'fundeadouros'

class FundeadouroDetail(FeatureResource):

    serializer_class = FundeadouroSerializer
    contextclassname = 'fundeadouros'

class PistaPontoPousoList(FeatureCollectionResource):

    queryset = PistaPontoPouso.objects.all()
    serializer_class = PistaPontoPousoSerializer
    contextclassname = 'pistas-de-ponto-pouso'

class PistaPontoPousoDetail(FeatureResource):

    serializer_class = PistaPontoPousoSerializer
    contextclassname = 'pistas-de-ponto-pouso'

class PonteList(FeatureCollectionResource):

    queryset = Ponte.objects.all()
    serializer_class = PonteSerializer
    contextclassname = 'pontes'

class PonteDetail(FeatureResource):

    serializer_class = PonteSerializer
    contextclassname = 'pontes'

class SinalizacaoList(FeatureCollectionResource):

    queryset = Sinalizacao.objects.all()
    serializer_class = SinalizacaoSerializer
    contextclassname = 'sinalizacaoes'

class SinalizacaoDetail(FeatureResource):

    serializer_class = SinalizacaoSerializer
    contextclassname = 'sinalizacaoes'

class TravessiaList(FeatureCollectionResource):

    queryset = Travessia.objects.all()
    serializer_class = TravessiaSerializer
    contextclassname = 'travessias'

class TravessiaDetail(FeatureResource):

    serializer_class = TravessiaSerializer
    contextclassname = 'travessias'

class TrechoDutoList(FeatureCollectionResource):

    queryset = TrechoDuto.objects.all()
    serializer_class = TrechoDutoSerializer
    contextclassname = 'trechos-dutos'

class TrechoDutoDetail(FeatureResource):

    serializer_class = TrechoDutoSerializer
    contextclassname = 'trechos-dutos'

class TrechoFerroviarioList(FeatureCollectionResource):

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

class TrechoHidroviarioDetail(FeatureResource):

    serializer_class = TrechoHidroviarioSerializer
    contextclassname = 'trechos-hidroviarios'

class TrechoRodoviarioList(FeatureCollectionResource):

    queryset = TrechoRodoviario.objects.all()
    serializer_class = TrechoRodoviarioSerializer
    contextclassname = 'trechos-rodoviarios'

class TrechoRodoviarioDetail(FeatureResource):

    serializer_class = TrechoRodoviarioSerializer
    contextclassname = 'trechos-rodoviarios'

class TunelList(FeatureCollectionResource):

    queryset = Tunel.objects.all()
    serializer_class = TunelSerializer
    contextclassname = 'tuneis'

class TunelDetail(FeatureResource):

    serializer_class = TunelSerializer
    contextclassname = 'tuneis'

class BrejoPantanoList(FeatureCollectionResource):

    queryset = BrejoPantano.objects.all()
    serializer_class = BrejoPantanoSerializer
    contextclassname = 'brejos-e-pantanos'

class BrejoPantanoDetail(FeatureResource):

    serializer_class = BrejoPantanoSerializer
    contextclassname = 'brejos-e-pantanos'

class MangueList(FeatureCollectionResource):

    queryset = Mangue.objects.all()
    serializer_class = MangueSerializer
    contextclassname = 'mangues'

class MangueDetail(FeatureResource):

    serializer_class = MangueSerializer
    contextclassname  = 'mangues'

class VegRestingaList(FeatureCollectionResource):

    queryset = VegRestinga.objects.all()
    serializer_class = VegRestingaSerializer
    contextclassname = 'vegetacoes-de-restinga'

class VegRestingaDetail(FeatureResource):

    serializer_class = VegRestingaSerializer
    contextclassname = 'vegetacoes-de-restinga'

class EdifPubMilitarList(FeatureCollectionResource):

    queryset = EdifPubMilitar.objects.all()
    serializer_class = EdifPubMilitarSerializer
    contextclassname = 'edificacoes-publica-militar'

class EdifPubMilitarDetail(FeatureResource):

    serializer_class = EdifPubMilitarSerializer
    contextclassname = 'edificacoes-publica-militar'

class PostoFiscalList(FeatureCollectionResource):

    queryset = PostoFiscal.objects.all()
    serializer_class = PostoFiscalSerializer
    contextclassname = 'postos-fiscais'


class PostoFiscalDetail(FeatureResource):

    serializer_class = PostoFiscalSerializer
    contextclassname = 'postos-fiscais'

class EdifAgropecExtVegetalPescaList(FeatureCollectionResource):

    queryset = EdifAgropecExtVegetalPesca.objects.all()
    serializer_class = EdifAgropecExtVegetalPescaSerializer
    contextclassname = 'edificacoes-agropecuarias-de-extracao-vegetal-e-pesca'

class EdifAgropecExtVegetalPescaDetail(FeatureResource):

    serializer_class = EdifAgropecExtVegetalPescaSerializer
    contextclassname = 'edificacoes-agropecuarias-de-extracao-vegetal-e-pesca'

class EdifIndustrialList(FeatureCollectionResource):

    queryset = EdifIndustrial.objects.all()
    serializer_class = EdifIndustrialSerializer
    contextclassname = 'edificacoes-industrial'

class EdifIndustrialDetail(FeatureResource):

    serializer_class = EdifIndustrialSerializer
    contextclassname = 'edificacoes-industrial'

class ExtMineralList(FeatureCollectionResource):

    queryset = ExtMineral.objects.all()
    serializer_class = ExtMineralSerializer
    contextclassname = 'extracoes-minerais'

class ExtMineralDetail(FeatureResource):

    serializer_class = ExtMineralSerializer
    contextclassname = 'extracoes-minerais'

class EdifReligiosaList(FeatureCollectionResource):

    queryset = EdifReligiosa.objects.all()
    serializer_class = EdifReligiosaSerializer
    contextclassname = 'edificacoes-religiosa'

class EdifReligiosaDetail(FeatureResource):

    serializer_class = EdifReligiosaSerializer
    contextclassname = 'edificacoes-religiosa'

class EstGeradEnergiaEletricaList(FeatureCollectionResource):

    queryset = EstGeradEnergiaEletrica.objects.all()
    serializer_class = EstGeradEnergiaEletricaSerializer
    contextclassname = 'estacoes-geradoras-de-energia-eletrica'

class EstGeradEnergiaEletricaDetail(FeatureResource):

    serializer_class = EstGeradEnergiaEletricaSerializer
    contextclassname = 'estacoes-geradoras-de-energia-eletrica'

class HidreletricaList(FeatureCollectionResource):

    queryset = Hidreletrica.objects.all()
    serializer_class = HidreletricaSerializer
    contextclassname = 'hidreletricas'

class HidreletricaDetail(FeatureResource):

    serializer_class = HidreletricaSerializer
    contextclassname = 'hidreletricas'

class TermeletricaList(FeatureCollectionResource):

    queryset = Termeletrica.objects.all()
    serializer_class = TermeletricaSerializer
    contextclassname = 'termeletricas'

class TermeletricaDetail(FeatureResource):

    serializer_class = TermeletricaSerializer
    contextclassname = 'termeletricas'

class TorreEnergiaList(FeatureCollectionResource):

    queryset = TorreEnergia.objects.all()
    serializer_class = TorreEnergiaSerializer
    contextclassname = 'torres-de-energia'

class TorreEnergiaDetail(FeatureResource):

    serializer_class = TorreEnergiaSerializer
    contextclassname = 'torres-de-energia'

class BancoAreiaList(FeatureCollectionResource):

    queryset = BancoAreia.objects.all()
    serializer_class = BancoAreiaSerializer
    contextclassname = 'bancos-de-areia'

class BancoAreiaDetail(FeatureResource):

    serializer_class = BancoAreiaSerializer
    contextclassname = 'bancos-de-areia'

class BarragemList(FeatureCollectionResource):

    queryset = Barragem.objects.all()
    serializer_class = BarragemSerializer
    contextclassname = 'barragens'

class BarragemDetail(FeatureResource):

    serializer_class = BarragemSerializer
    contextclassname = 'barragens'

class CorredeiraList(FeatureCollectionResource):

    queryset = Corredeira.objects.all()
    serializer_class = CorredeiraSerializer
    contextclassname = 'corredeiras'

class CorredeiraDetail(FeatureResource):

    serializer_class = CorredeiraSerializer
    contextclassname = 'corredeiras'

class FozMaritimaList(FeatureCollectionResource):

    queryset = FozMaritima.objects.all()
    serializer_class = FozMaritimaSerializer
    contextclassname = 'fozes-maritima'

class FozMaritimaDetail(FeatureResource):

    serializer_class = FozMaritimaSerializer
    contextclassname = 'fozes-maritima'

class IlhaList(FeatureCollectionResource):

    queryset = Ilha.objects.all()
    serializer_class = IlhaSerializer
    contextclassname = 'ilhas'

class IlhaDetail(FeatureResource):

    serializer_class = IlhaSerializer
    contextclassname = 'ilhas'

class MassaDaguaList(FeatureCollectionResource):

    queryset = MassaDagua.objects.all()
    serializer_class = MassaDaguaSerializer
    contextclassname = 'massas-dagua'

class MassaDaguaDetail(FeatureResource):

    serializer_class = MassaDaguaSerializer
    contextclassname = 'massas-dagua'

class QuedaDaguaList(FeatureCollectionResource):

    queryset = QuedaDagua.objects.all()
    serializer_class = QuedaDaguaSerializer
    contextclassname = 'quedas-dagua'

class QuedaDaguaDetail(FeatureResource):

    serializer_class = QuedaDaguaSerializer
    contextclassname = 'quedas-dagua'

class RecifeList(FeatureCollectionResource):

    #queryset = Recife.objects.all()
    serializer_class = RecifeSerializer
    contextclassname = 'recifes'

class RecifeDetail(FeatureResource):

    serializer_class = RecifeSerializer
    contextclassname = 'recifes'

class RochaEmAguaList(FeatureCollectionResource):

    queryset = RochaEmAgua.objects.all()
    serializer_class = RochaEmAguaSerializer
    contextclassname = 'rochas-em-agua'

class RochaEmAguaDetail(FeatureResource):

    serializer_class = RochaEmAguaSerializer
    contextclassname = 'rochas-em-agua'

class SumidouroVertedouroList(FeatureCollectionResource):

    queryset = SumidouroVertedouro.objects.all()
    serializer_class = SumidouroVertedouroSerializer
    contextclassname = 'sumidouros-vertedouros'

class SumidouroVertedouroDetail(FeatureResource):

    serializer_class = SumidouroVertedouroSerializer
    contextclassname = 'sumidouros-vertedouros'

class TerrenoSujeitoInundacaoList(FeatureCollectionResource):

    queryset = TerrenoSujeitoInundacao.objects.all()
    serializer_class = TerrenoSujeitoInundacaoSerializer
    contextclassname = 'terrenos-sujeito-a-inundacao'

class TerrenoSujeitoInundacaoDetail(FeatureResource):

    serializer_class = TerrenoSujeitoInundacaoSerializer
    contextclassname = 'terrenos-sujeito-a-inundacao'

class TrechoDrenagemList(FeatureCollectionResource):

    queryset = TrechoDrenagem.objects.all()
    serializer_class = TrechoDrenagemSerializer
    contextclassname = 'trechos-de-drenagem'

class TrechoDrenagemDetail(FeatureResource):

    serializer_class = TrechoDrenagemSerializer
    contextclassname = 'trechos-de-drenagem'

class TrechoMassaDaguaList(FeatureCollectionResource):

    queryset = TrechoMassaDagua.objects.all()
    serializer_class = TrechoMassaDaguaSerializer
    contextclassname = 'trechos-de-drenagem'

class TrechoMassaDaguaDetail(FeatureResource):

    serializer_class = TrechoMassaDaguaSerializer
    contextclassname = 'trechos-de-massa-dagua'

class AreaDesenvolvimentoControleList(FeatureCollectionResource):

    queryset = AreaDesenvolvimentoControle.objects.all()
    serializer_class = AreaDesenvolvimentoControleSerializer
    contextclassname = 'areas-de-desenvolvimento-de-controle'

class AreaDesenvolvimentoControleDetail(FeatureResource):

    serializer_class = AreaDesenvolvimentoControleSerializer
    contextclassname = 'areas-de-desenvolvimento-de-controle'

class MarcoDeLimiteList(FeatureCollectionResource):

    queryset = MarcoDeLimite.objects.all()
    serializer_class = MarcoDeLimiteSerializer
    contextclassname = 'marcos-de-limite'

class MarcoDeLimiteDetail(FeatureResource):

    serializer_class = MarcoDeLimiteSerializer
    contextclassname = 'marcos-de-limite'