
from django.conf.urls import include,  url
from rest_framework.urlpatterns import format_suffix_patterns
from bcim import views


app_name = "bcim"
urlpatterns = (
    url(r'^(?P<attributes_functions>count-resource.*$|projection.*$|filter.*$|collect.*$|offset-limit.*$)/?$', views.APIRoot.as_view(), name='api_root_af'), # HARCODED
    url(r'^$', views.APIRoot.as_view(), name='api_root'),

    #unidades federativas

    url(r'^' + views.UnidadeFederacaoDetail.contextclassname + '/(?P<geocodigo>[0-9]{2})/(?P<attributes_functions>.*)/?$', views.UnidadeFederacaoDetail.as_view(), name='uf_detail_geocodigo'),
    url(r'^' + views.UnidadeFederacaoDetail.contextclassname + '/(?P<geocodigo>[0-9]{2})/?$', views.UnidadeFederacaoDetail.as_view(), name='uf_detail_geocodigo'),
    url(r'^' + views.UnidadeFederacaoDetail.contextclassname + '/(?P<id_objeto>[0-9]+)/(?P<attributes_functions>.*)/?$', views.UnidadeFederacaoDetail.as_view(), name='uf_detail_id_objeto'),
    url(r'^' + views.UnidadeFederacaoDetail.contextclassname + '/(?P<id_objeto>[0-9]+)/?$', views.UnidadeFederacaoDetail.as_view(), name='uf_detail_id_objeto'),
    url(r'^' + views.UnidadeFederacaoDetail.contextclassname + '/(?P<sigla>[A-Za-z]{2})/?$', views.UnidadeFederacaoDetail.as_view(), name='uf_detail_sigla'),
    url(r'^' + views.UnidadeFederacaoDetail.contextclassname + '/(?P<sigla>[A-Za-z]{2})/(?P<attributes_functions>.*)/?$', views.UnidadeFederacaoDetail.as_view(), name='uf_detail_si'),
    url(r'^unidades-federativas/?$', views.UnidadeFederacaoList.as_view(), name='uf_list'),
    url(r'^unidades-federativas/(?P<attributes_functions>.*)/?$', views.UnidadeFederacaoList.as_view(), name='uf_list_sigla_filtered'),

    #municipios
    url(r'^' + views.MunicipioDetail.contextclassname + '/(?P<geocodigo>[0-9]{7})/(?P<attributes_functions>.*)/?$', views.MunicipioDetail.as_view(), name='mun_detail_geocodigo'),
    url(r'^' + views.MunicipioDetail.contextclassname + '/(?P<geocodigo>[0-9]{7})/?$', views.MunicipioDetail.as_view(), name='mun_detail_geocodigo'),
    #collection
    url(r'^municipios/?$', views.MunicipioList.as_view(), name='municipio_list'),
    url(r'^municipios/(?P<attributes_functions>.*)/?$', views.MunicipioList.as_view(), name='municipio_list_functions'),

    #aldeias indigenas
    url(r'^aldeias-indigenas/(?P<id_objeto>[0-9]+)/?$', views.AldeiaIndigenaDetail.as_view(), name='uf_detail_aldeia'),
    url(r'^aldeias-indigenas/(?P<id_objeto>[0-9]+)/(?P<attributes_functions>.*)/?$', views.AldeiaIndigenaDetail.as_view(), name='uf_detail_si'),

    #collection
    url(r'^aldeias-indigenas/?$', views.AldeiaIndigenaList.as_view(), name='aldeia_indigena_list'),
    url(r'^aldeias-indigenas/(?P<attributes_functions>.*)/?$', views.AldeiaIndigenaList.as_view(), name='aldeia_indigena_list_filtered'),

    url(r'^capitais/?$', views.CapitalList.as_view(), name='capital_list'),
    url(r'^capitais/(?P<attributes_functions>.*)/?$', views.CapitalList.as_view(), name='capital_list_fn'),
    url(r'^capitais/(?P<id_objeto>[0-9]+)/?$', views.CapitalDetail.as_view(), name='capital_detail_id_objeto'),
    url(r'^capitais/(?P<id_objeto>[0-9]+)/(?P<attributes_functions>.*)/?$', views.CapitalDetail.as_view(), name='capital_detail_si'),


    url(r'^cidades/(?P<id_objeto>[0-9]+)/?$', views.CidadeDetail.as_view(), name='cidade_detail_id_objeto'),
    url(r'^cidades/(?P<id_objeto>[0-9]+)/(?P<attributes_functions>.*)/?$', views.CidadeDetail.as_view(), name='cidade_detail_si'),
    url(r'^cidades/?$', views.CidadeList.as_view(), name = 'cidade_list'),
    url(r'^cidades/(?P<attributes_functions>.*)/?$', views.CidadeList.as_view(), name='cidade_list_fn'),


    #Trecho_ferroviario
    url(r'^trechos-ferroviarios/(?P<id_objeto>[0-9]+)/?$', views.TrechoFerroviarioDetail.as_view(), name='tf_detail_id_objeto'),
    url(r'^trechos-ferroviarios/(?P<id_objeto>[0-9]+)/(?P<attributes_functions>.*)/?$', views.TrechoFerroviarioDetail.as_view(), name='tf_detail_si'),
    url(r'^trechos-ferroviarios/?$', views.TrechoFerroviarioList.as_view(), name='trecho_ferroviario_list'),
    url(r'^trechos-ferroviarios/(?P<attributes_functions>.*)/?$', views.TrechoFerroviarioList.as_view(), name='trecho_ferroviario_list_fn'),

    url(r'^trechos-hidroviarios/(?P<id_objeto>[0-9]+)/?$', views.TrechoHidroviarioDetail.as_view(), name='th_detail_id_objeto'),
    url(r'^trechos-hidroviarios/(?P<id_objeto>[0-9]+)/(?P<attributes_functions>.*)/?$', views.TrechoHidroviarioDetail.as_view(), name='th_detail_si'),
    url(r'^trechos-hidroviarios/?$', views.TrechoHidroviarioList.as_view(), name='trecho_hidroviario_list'),
    url(r'^trechos-hidroviarios/(?P<attributes_functions>.*)/?$', views.TrechoHidroviarioList.as_view(), name='trecho_hidroviario_list_fn'),

    #url(r'^trechos-rodoviarios/?$', views.TrechoRodoviarioList.as_view(), name='trecho_rodoviario_list'),
    url(r'^trechos-rodoviarios/(?P<id_objeto>[0-9]+)/?$', views.TrechoRodoviarioDetail.as_view(), name='trecho_rodoviario_detail_id_objeto'),
    url(r'^trechos-rodoviarios/(?P<id_objeto>[0-9]+)/(?P<attributes_functions>.*)/?$', views.TrechoRodoviarioDetail.as_view(), name='trecho_rodoviario_detail_si'),
    url(r'^trechos-rodoviarios/?$', views.TrechoRodoviarioList.as_view(), name='trecho_rodoviario_list'),
    url(r'^trechos-rodoviarios/(?P<attributes_functions>.*)/?$', views.TrechoRodoviarioList.as_view(), name='trecho_rodoviario_list_fn'),


    url(r'^outras-unidades-protegidas/(?P<id_objeto>[0-9]+)/?$', views.OutrasUnidProtegidasDetail.as_view(), name='outras_unid_protegidas_detail'),
    url(r'^outras-unidades-protegidas/(?P<id_objeto>[0-9]+)/(?P<attributes_functions>.*)/?$', views.OutrasUnidProtegidasDetail.as_view(), name='outras_unid_protegidas_si'),
    url(r'^outras-unidades-protegidas/?$', views.OutrasUnidProtegidasList.as_view(), name='outras_unid_protegidas_list'),
    url(r'^outras-unidades-protegidas/(?P<attributes_functions>.*)/?$', views.OutrasUnidProtegidasList.as_view(), name='outras_unid_protegidas_list_fn'),


    url(r'^outros-limites-oficiais/(?P<id_objeto>[0-9]+)/?$', views.OutrosLimitesOficiaisDetail.as_view(), name='outros_limites_oficiais_detail_id_objeto'),
    url(r'^outros-limites-oficiais/(?P<id_objeto>[0-9]+)/(?P<attributes_functions>.*)/?$', views.OutrosLimitesOficiaisDetail.as_view(), name='outros_limites_oficiais_detail_si'),
    url(r'^outros-limites-oficiais/?$', views.OutrosLimitesOficiaisList.as_view(), name='outros_limites_oficiais_list'),
    url(r'^outros-limites-oficiais/(?P<attributes_functions>.*)/?$', views.OutrosLimitesOficiaisList.as_view(), name='outros_limites_oficiais_list_fn'),


    url(r'^paises/(?P<id_objeto>[0-9]+)/?$', views.PaisDetail.as_view(), name='pais_detail_id_objeto'),
    url(r'^paises/(?P<id_objeto>[0-9]+)/(?P<attributes_functions>.*)/?$', views.PaisDetail.as_view(), name='pais_detail_si'),
    url(r'^paises/?$', views.PaisList.as_view(), name='pais_list'),
    url(r'^paises/(?P<attributes_functions>.*)/?$', views.PaisList.as_view(), name='pais_list_fn'),


    url(r'^terras-indigenas/(?P<id_objeto>[0-9]+)/(?P<attributes_functions>.*)/?$', views.TerraIndigenaDetail.as_view(), name='terra_indigena_detail_id_objeto'),
    url(r'^terras-indigenas/(?P<id_objeto>[0-9]+)/?$', views.TerraIndigenaDetail.as_view(), name='terra_indigena_detail_id_objeto'),
    url(r'^terras-indigenas/?$', views.TerraIndigenaList.as_view(), name='terra_indigena_list'),
    url(r'^terras-indigenas/(?P<attributes_functions>.*)/?$', views.TerraIndigenaList.as_view(), name='terra_indigena_list_fn'),


    url(r'^unidades-de-conservacao-nao-snuc/(?P<id_objeto>[0-9]+)/?$', views.UnidadeConservacaoNaoSnucDetail.as_view(), name='unidade_conservacao_nao_snuc_detail_id_objeto'),
    url(r'^unidades-de-conservacao-nao-snuc/(?P<id_objeto>[0-9]+)/(?P<attributes_functions>.*)/?$', views.UnidadeConservacaoNaoSnucDetail.as_view(), name='unidade_conservacao_nao_snuc_detail_si'),
    url(r'^unidades-de-conservacao-nao-snuc/?$', views.UnidadeConservacaoNaoSnucList.as_view(), name='unidade_conservacao_nao_snuc_list'),
    url(r'^unidades-de-conservacao-nao-snuc/(?P<attributes_functions>.*)/?$', views.UnidadeConservacaoNaoSnucList.as_view(), name='unidade_conservacao_nao_snuc_list'),

    url(r'^unidades-de-protecao-integral/(?P<id_objeto>[0-9]+)/?$', views.UnidadeProtecaoIntegralDetail.as_view(), name='unidade_protecao_integral_detail_id_objeto'),
    url(r'^unidades-de-protecao-integral/(?P<id_objeto>[0-9]+)/(?P<attributes_functions>.*)/?$', views.UnidadeProtecaoIntegralDetail.as_view(), name='unidade_protecao_integral_detail_si'),
    url(r'^unidades-de-protecao-integral/?$', views.UnidadeProtecaoIntegralList.as_view(), name='unidade_protecao_integral_list'),
    url(r'^unidades-de-protecao-integral/(?P<attributes_functions>.*)/?$', views.UnidadeProtecaoIntegralList.as_view(), name='unidade_protecao_integral_list'),

    url(r'^unidades-de-uso-sustentavel/(?P<id_objeto>[0-9]+)/?$', views.UnidadeUsoSustentavelDetail.as_view(), name='unidade_uso_sustentavel_detail_id_objeto'),
    url(r'^unidades-de-uso-sustentavel/(?P<id_objeto>[0-9]+)/(?P<attributes_functions>.*)/?$', views.UnidadeUsoSustentavelDetail.as_view(), name='unidade_uso_sustentavel_detail_id_objeto'),
    url(r'^unidades-de-uso-sustentavel/?$', views.UnidadeUsoSustentavelList.as_view(), name='unidade_uso_sustentavel_list'),
    url(r'^unidades-de-uso-sustentavel/(?P<attributes_functions>.*)/?$', views.UnidadeUsoSustentavelList.as_view(), name='unidade_uso_sustentavel_list'),

    url(r'^aglomerados-rurais-de-extensao-urbana/(?P<id_objeto>[0-9]+)/?$', views.AglomeradoRuralDeExtensaoUrbanaDetail.as_view(), name='aglomerado_rural_de_extensao_urbana_detail_id_objeto'),
    url(r'^aglomerados-rurais-de-extensao-urbana/(?P<id_objeto>[0-9]+)/(?P<attributes_functions>.*)/?$', views.AglomeradoRuralDeExtensaoUrbanaDetail.as_view(), name='aglomerado_rural_de_extensao_urbana_detail_id_objeto'),
    url(r'^aglomerados-rurais-de-extensao-urbana/?$', views.AglomeradoRuralDeExtensaoUrbanaList.as_view(), name='aglomerado_rural_de_extensao_urbana_list'),
    url(r'^aglomerados-rurais-de-extensao-urbana/(?P<attributes_functions>.*)/?$', views.AglomeradoRuralDeExtensaoUrbanaList.as_view(), name='aglomerado_rural_de_extensao_urbana_list'),


    url(r'^aglomerados-rurais-isolado/(?P<id_objeto>[0-9]+)/?$', views.AglomeradoRuralIsoladoDetail.as_view(), name='aglomerado_rural_isolado_detail_id_objeto'),
    url(r'^aglomerados-rurais-isolado/(?P<id_objeto>[0-9]+)/(?P<attributes_functions>.*)/?$', views.AglomeradoRuralIsoladoDetail.as_view(), name='aglomerado_rural_isolado_detail_si'),
    url(r'^aglomerados-rurais-isolado/?$', views.AglomeradoRuralIsoladoList.as_view(), name='aglomerado_rural_isolado_list'),
    url(r'^aglomerados-rurais-isolado/(?P<attributes_functions>.*)/?$', views.AglomeradoRuralIsoladoList.as_view(), name='aglomerado_rural_isolado_list'),

    url(r'^areas-edificadas/(?P<id_objeto>[0-9]+)/?$', views.AreaEdificadaDetail.as_view(), name='area_edificada_detail_id_objeto'),
    url(r'^areas-edificadas/(?P<id_objeto>[0-9]+)/(?P<attributes_functions>.*)/?$', views.AreaEdificadaDetail.as_view(), name='area_edificada_detail_af'),
    url(r'^areas-edificadas/?$', views.AreaEdificadaList.as_view(), name='area_edificada_list'),
    url(r'^areas-edificadas/(?P<attributes_functions>.*)/?$', views.AreaEdificadaList.as_view(), name='area_edificada_list'),

    url(r'^vilas/(?P<id_objeto>[0-9]+)/?$', views.VilaDetail.as_view(), name='vila_detail_id_objeto'),
    url(r'^vilas/(?P<id_objeto>[0-9]+)/(?P<attributes_functions>.*)/?$', views.VilaDetail.as_view(), name='vila_detail_af'),

    url(r'^vilas/?$', views.VilaList.as_view(), name='vila_list'),
    url(r'^vilas/(?P<attributes_functions>.*)/?$', views.VilaList.as_view(), name='vila_list'),

    url(r'^curvas-batimetricas/(?P<id_objeto>[0-9]+)/?$', views.CurvaBatimetricaDetail.as_view(), name='curva_batimetrica_detail_id_objeto'),
    url(r'^curvas-batimetricas/(?P<id_objeto>[0-9]+)/(?P<attributes_functions>.*)/?$', views.CurvaBatimetricaDetail.as_view(), name='curva_batimetrica_detail_af'),
    url(r'^curvas-batimetricas/?$', views.CurvaBatimetricaList.as_view(), name='curva_batimetrica_list'),
    url(r'^curvas-batimetricas/(?P<attributes_functions>.*)/?$', views.CurvaBatimetricaList.as_view(), name='curva_batimetrica_list'),


    #url(r'^curvas-de-nivel/?$', views.CurvaNivelList.as_view(), name='curva_nivel_list'), # nao carrega (muita informacao)
    url(r'^curvas-de-nivel/(?P<id_objeto>[0-9]+)/?$', views.CurvaNivelDetail.as_view(), name='curva_nivel_id_objeto'),
    url(r'^curvas-de-nivel/(?P<id_objeto>[0-9]+)/(?P<attributes_functions>.*)/?$', views.CurvaNivelDetail.as_view(), name='curva_nivel_detail_si'),
    url(r'^curvas-de-nivel/?$', views.CurvaNivelList.as_view(), name = 'curva_nivel_list'),
    url(r'^curvas-de-nivel/(?P<attributes_functions>.*)/?$', views.CurvaNivelList.as_view(), name='curva_nivel_list_fn'),



    url(r'^dunas/(?P<id_objeto>[0-9]+)/?$', views.DunaDetail.as_view(), name='duna_detail_id_objeto'),
    url(r'^dunas/(?P<id_objeto>[0-9]+)/(?P<attributes_functions>.*)/?$', views.DunaDetail.as_view(), name='duna_detail_af'),
    url(r'^dunas/?$', views.DunaList.as_view(), name='duna_list'),
    url(r'^dunas/(?P<attributes_functions>.*)/?$', views.DunaList.as_view(), name='duna_list'),
    

    url(r'^elementos-fisiografico-natural/(?P<id_objeto>[0-9]+)/?$', views.ElementoFisiograficoNaturalDetail.as_view(), name='elemento_fisiografico_natural_detail_id_objeto'),
    url(r'^elementos-fisiografico-natural/(?P<id_objeto>[0-9]+)/(?P<attributes_functions>.*)/?$', views.ElementoFisiograficoNaturalDetail.as_view(), name='elemento_fisiografico_natural_detail_id_objeto'),
    url(r'^elementos-fisiografico-natural/?$', views.ElementoFisiograficoNaturalList.as_view(), name='elemento_fisiografico_natural_list'),
    url(r'^elementos-fisiografico-natural/(?P<attributes_functions>.*)/?$', views.ElementoFisiograficoNaturalList.as_view(), name='elemento_fisiografico_natural_list'),


    url(r'^picos/(?P<id_objeto>[0-9]+)/?$', views.PicoDetail.as_view(), name='pico_detail_id_objeto'),
    url(r'^picos/(?P<id_objeto>[0-9]+)/(?P<attributes_functions>.*)/?$', views.PicoDetail.as_view(), name='pico_detail_af'),
    url(r'^picos/?$', views.PicoList.as_view(), name='pico_list'),
    url(r'^picos/(?P<attributes_functions>.*)/?$', views.PicoList.as_view(), name='pico_list'),


    url(r'^pontos-cotados-altimetricos/(?P<id_objeto>[0-9]+)/?$', views.PontoCotadoAltimetricoDetail.as_view(), name='ponto_cotado_altimetrico_detail_id_objeto'),
    url(r'^pontos-cotados-altimetricos/(?P<id_objeto>[0-9]+)/(?P<attributes_functions>.*)/?$', views.PontoCotadoAltimetricoDetail.as_view(), name='ponto_cotado_altimetrico_detail_af'),
    url(r'^pontos-cotados-altimetricos/?$', views.PontoCotadoAltimetricoList.as_view(), name='ponto_cotado_altimetrico_list'),
    url(r'^pontos-cotados-altimetricos/(?P<attributes_functions>.*)/?$', views.PontoCotadoAltimetricoList.as_view(), name='ponto_cotado_altimetrico_list'),

    url(r'^pontos-cotados-batimetricos/(?P<id_objeto>[0-9]+)/?$', views.PontoCotadoBatimetricoDetail.as_view(), name='ponto_cotado_batimetrico_detail_id_objeto'),
    url(r'^pontos-cotados-batimetricos/(?P<id_objeto>[0-9]+)/(?P<attributes_functions>.*)/?$', views.PontoCotadoBatimetricoDetail.as_view(), name='ponto_cotado_batimetrico_detail_af'),
    url(r'^pontos-cotados-batimetricos/?$', views.PontoCotadoBatimetricoList.as_view(), name='ponto_cotado_batimetrico_list'),
    url(r'^pontos-cotados-batimetricos/(?P<attributes_functions>.*)/?$', views.PontoCotadoBatimetricoList.as_view(), name='ponto_cotado_batimetrico_list'),

    url(r'^eclusas/(?P<id_objeto>[0-9]+)/?$', views.EclusaDetail.as_view(), name='eclusa_detail_id_objeto'),
    url(r'^eclusas/(?P<id_objeto>[0-9]+)/(?P<attributes_functions>.*)/?$', views.EclusaDetail.as_view(), name='eclusa_detail_af'),
    url(r'^eclusas/?$', views.EclusaList.as_view(), name='eclusa_list'),
    url(r'^eclusas/(?P<attributes_functions>.*)/?$', views.EclusaList.as_view(), name='eclusa_list'),


    url(r'^edificacoes-de-construcao-portuaria/(?P<id_objeto>[0-9]+)/?$', views.EdifConstPortuariaDetail.as_view(), name='edif_const_portuaria_detail_id_objeto'),
    url(r'^edificacoes-de-construcao-portuaria/(?P<id_objeto>[0-9]+)/(?P<attributes_functions>.*)/?$', views.EdifConstPortuariaDetail.as_view(), name='edif_const_portuaria_detail_af'),
    url(r'^edificacoes-de-construcao-portuaria/?$', views.EdifConstPortuariaList.as_view(), name='edif_const_portuaria_list'),
    url(r'^edificacoes-de-construcao-portuaria/(?P<attributes_functions>.*)/?$', views.EdifConstPortuariaList.as_view(), name='edif_const_portuaria_list'),


    url(r'^edificacoes-de-construcao-aeroportuaria/(?P<id_objeto>[0-9]+)/?$', views.EdifConstrAeroportuariaDetail.as_view(), name='edif_const_aeroportuaria_detail_id_objeto'),
    url(r'^edificacoes-de-construcao-aeroportuaria/(?P<id_objeto>[0-9]+)/(?P<attributes_functions>.*)/?$', views.EdifConstrAeroportuariaDetail.as_view(), name='edif_const_aeroportuaria_detail_af'),
    url(r'^edificacoes-de-construcao-aeroportuaria/?$', views.EdifConstrAeroportuariaList.as_view(), name='edif_const_aeroportuaria_list'),
    url(r'^edificacoes-de-construcao-aeroportuaria/(?P<attributes_functions>.*)/?$', views.EdifConstrAeroportuariaList.as_view(), name='edif_const_aeroportuaria_list'),


    url(r'^edificacoes-metro-ferroviaria/(?P<id_objeto>[0-9]+)/?$', views.EdifMetroFerroviariaDetail.as_view(), name='edif_metro_ferroviaria_detail_id_objeto'),
    url(r'^edificacoes-metro-ferroviaria/(?P<id_objeto>[0-9]+)/(?P<attributes_functions>.*)/?$', views.EdifMetroFerroviariaDetail.as_view(), name='edif_metro_ferroviaria_detail_af'),
    url(r'^edificacoes-metro-ferroviaria/?$', views.EdifMetroFerroviariaList.as_view(), name='edif_metro_ferroviaria_list'),
    url(r'^edificacoes-metro-ferroviaria/(?P<attributes_functions>.*)/?$', views.EdifMetroFerroviariaList.as_view(), name='edif_metro_ferroviaria_list'),

    url(r'^fundeadouros/(?P<id_objeto>[0-9]+)/?$', views.FundeadouroDetail.as_view(), name='fundeadouro_detail_id_objeto'),
    url(r'^fundeadouros/(?P<id_objeto>[0-9]+)/(?P<attributes_functions>.*)/?$', views.FundeadouroDetail.as_view(), name='fundeadouro_detail_af'),
    url(r'^fundeadouros/?$', views.FundeadouroList.as_view(), name='fundeadouro_list'),
    url(r'^fundeadouros/(?P<attributes_functions>.*)/?$', views.FundeadouroList.as_view(), name='fundeadouro_list'),


    url(r'^pistas-de-ponto-pouso/(?P<id_objeto>[0-9]+)/?$', views.PistaPontoPousoDetail.as_view(), name='pista_ponto_pouso_detail_id_objeto'),
    url(r'^pistas-de-ponto-pouso/(?P<id_objeto>[0-9]+)/(?P<attributes_functions>.*)/?$', views.PistaPontoPousoDetail.as_view(), name='pista_ponto_pouso_af'),
    url(r'^pistas-de-ponto-pouso/?$', views.PistaPontoPousoList.as_view(), name='pista_ponto_pouso_list'),
    url(r'^pistas-de-ponto-pouso/(?P<attributes_functions>.*)/?$', views.PistaPontoPousoList.as_view(), name='pista_ponto_pouso_list'),


    url(r'^pontes/(?P<id_objeto>[0-9]+)/?$', views.PonteDetail.as_view(), name='ponte_detail_id_objeto'),
    url(r'^pontes/(?P<id_objeto>[0-9]+)/(?P<attributes_functions>.*)/?$', views.PonteDetail.as_view(), name='ponte_detail_af'),
    url(r'^pontes/?$', views.PonteList.as_view(), name='ponte_list'),
    url(r'^pontes/(?P<attributes_functions>.*)/?$', views.PonteList.as_view(), name='ponte_list'),


    url(r'^sinalizacaoes/(?P<id_objeto>[0-9]+)/?$', views.SinalizacaoDetail.as_view(), name='sinalizacao_detail_id_objeto'),
    url(r'^sinalizacaoes/(?P<id_objeto>[0-9]+)/(?P<attributes_functions>.*)/?$', views.SinalizacaoDetail.as_view(), name='sinalizacao_detail_af'),
    url(r'^sinalizacaoes/?$', views.SinalizacaoList.as_view(), name='sinalizacao_list'),
    url(r'^sinalizacaoes/(?P<attributes_functions>.*)/?$', views.SinalizacaoList.as_view(), name='sinalizacao_list'),


    url(r'^travessias/(?P<id_objeto>[0-9]+)/?$', views.TravessiaDetail.as_view(), name='travessia_detail_id_objeto'),
    url(r'^travessias/(?P<id_objeto>[0-9]+)/(?P<attributes_functions>.*)/?$', views.TravessiaDetail.as_view(), name='travessia_detail_id_objeto_detail_af'),
    url(r'^travessias/?$', views.TravessiaList.as_view(), name='travessia_list'),
    url(r'^travessias/(?P<attributes_functions>.*)/?$', views.TravessiaList.as_view(), name='travessia_list'),

    url(r'^trechos-dutos/(?P<id_objeto>[0-9]+)/?$', views.TrechoDutoDetail.as_view(), name='trecho_duto_detail_id_objeto'),
    url(r'^trechos-dutos/(?P<id_objeto>[0-9]+)/(?P<attributes_functions>.*)/?$', views.TrechoDutoDetail.as_view(), name='trecho_duto_detail_af'),
    url(r'^trechos-dutos/?$', views.TrechoDutoList.as_view(), name='trecho_duto_list'),
    url(r'^trechos-dutos/(?P<attributes_functions>.*)/?$', views.TrechoDutoList.as_view(), name='trecho_duto_list'),

    url(r'^tuneis/(?P<id_objeto>[0-9]+)/?$', views.TunelDetail.as_view(), name='tunel_detail_id_objeto'),
    url(r'^tuneis/(?P<id_objeto>[0-9]+)/(?P<attributes_functions>.*)/?$', views.TunelDetail.as_view(), name='tunel_detail_af'),

    url(r'^tuneis/?$', views.TunelList.as_view(), name='tunel_list'),
    url(r'^tuneis/(?P<attributes_functions>.*)/?$', views.TunelList.as_view(), name='tunel_list'),

    url(r'^brejos-e-pantanos/(?P<id_objeto>[0-9]+)/?$', views.BrejoPantanoDetail.as_view(), name='brejo_pantano_detail_id_objeto'),
    url(r'^brejos-e-pantanos/(?P<id_objeto>[0-9]+)/(?P<attributes_functions>.*)/?$', views.BrejoPantanoDetail.as_view(), name='brejo_pantano_detail_af'),
    url(r'^brejos-e-pantanos/?$', views.BrejoPantanoList.as_view(), name='brejo_pantano_list'),
    url(r'^brejos-e-pantanos/(?P<attributes_functions>.*)/?$', views.BrejoPantanoList.as_view(), name='brejo_pantano_list'),


    url(r'^mangues/(?P<id_objeto>[0-9]+)/?$', views.MangueDetail.as_view(), name='mangue_detail_id_objeto'),
    url(r'^mangues/(?P<id_objeto>[0-9]+)/(?P<attributes_functions>.*)/?$', views.MangueDetail.as_view(), name='mangue_detail_af'),
    url(r'^mangues/?$', views.MangueList.as_view(), name='mangue_list'),
    url(r'^mangues/(?P<attributes_functions>.*)/?$', views.MangueList.as_view(), name='mangue_list'),

    url(r'^vegetacoes-de-restinga/(?P<id_objeto>[0-9]+)/?$', views.VegRestingaDetail.as_view(), name='veg_restinga_detail_id_objeto'),
    url(r'^vegetacoes-de-restinga/(?P<id_objeto>[0-9]+)/(?P<attributes_functions>.*)/?$', views.VegRestingaDetail.as_view(), name='veg_restinga_detail_af'),
    url(r'^vegetacoes-de-restinga/?$', views.VegRestingaList.as_view(), name='veg_restinga_list'),
    url(r'^vegetacoes-de-restinga/(?P<attributes_functions>.*)/?$', views.VegRestingaList.as_view(), name='veg_restinga_list'),


    url(r'^edificacoes-publica-militar/(?P<id_objeto>[0-9]+)/?$', views.EdifPubMilitarDetail.as_view(), name='edif_pub_militar_detail_id_objeto'),
    url(r'^edificacoes-publica-militar/(?P<id_objeto>[0-9]+)/(?P<attributes_functions>.*)/?$', views.EdifPubMilitarDetail.as_view(), name='edif_pub_militar_detail_af'),
    url(r'^edificacoes-publica-militar/?$', views.EdifPubMilitarList.as_view(), name='edif_pub_militar_list'),
    url(r'^edificacoes-publica-militar/(?P<attributes_functions>.*)/?$', views.EdifPubMilitarList.as_view(), name='edif_pub_militar_list'),

    url(r'^postos-fiscais/(?P<id_objeto>[0-9]+)/?$', views.PostoFiscalDetail.as_view(), name='posto_fiscal_detail_id_objeto'),
    url(r'^postos-fiscais/(?P<id_objeto>[0-9]+)/(?P<attributes_functions>.*)/?$', views.PostoFiscalDetail.as_view(), name='posto_fiscal_detail_af'),
    url(r'^postos-fiscais/?$', views.PostoFiscalList.as_view(), name='posto_fiscal_list'),
    url(r'^postos-fiscais/(?P<attributes_functions>.*)/?$', views.PostoFiscalList.as_view(), name='posto_fiscal_list'),


    url(r'^edificacoes-agropecuarias-de-extracao-vegetal-e-pesca/(?P<id_objeto>[0-9]+)/?$', views.EdifAgropecExtVegetalPescaDetail.as_view(), name='edif_agropec_ext_vegetal_detail_id_objeto'),
    url(r'^edificacoes-agropecuarias-de-extracao-vegetal-e-pesca/(?P<id_objeto>[0-9]+)/(?P<attributes_functions>.*)/?$', views.EdifAgropecExtVegetalPescaDetail.as_view(), name='edif_agropec_ext_vegetal_detail_af'),
    url(r'^edificacoes-agropecuarias-de-extracao-vegetal-e-pesca/?$', views.EdifAgropecExtVegetalPescaList.as_view(), name='edif_agropec_ext_vegetal_pesca_list'),
    url(r'^edificacoes-agropecuarias-de-extracao-vegetal-e-pesca/(?P<attributes_functions>.*)/?$', views.EdifAgropecExtVegetalPescaList.as_view(), name='edif_agropec_ext_vegetal_pesca_list'),


    url(r'^edificacoes-industrial/(?P<id_objeto>[0-9]+)/?$', views.EdifIndustrialDetail.as_view(), name='edif_industrial_detail_id_objeto'),
    url(r'^edificacoes-industrial/(?P<id_objeto>[0-9]+)/(?P<attributes_functions>.*)/?$', views.EdifIndustrialDetail.as_view(), name='edif_industrial_detail_af'),
    url(r'^edificacoes-industrial/?$', views.EdifIndustrialList.as_view(), name='edif_industrial_list'),
    url(r'^edificacoes-industrial/(?P<attributes_functions>.*)/?$', views.EdifIndustrialList.as_view(), name='edif_industrial_list'),

    url(r'^extracoes-minerais/(?P<id_objeto>[0-9]+)/?$', views.ExtMineralDetail.as_view(), name='ext_mineral_detail_id_objeto'),
    url(r'^extracoes-minerais/(?P<id_objeto>[0-9]+)/(?P<attributes_functions>.*)/?$', views.ExtMineralDetail.as_view(), name='ext_mineral_detail_af'),
    url(r'^extracoes-minerais/?$', views.ExtMineralList.as_view(), name='ext_mineral_list'),
    url(r'^extracoes-minerais/(?P<attributes_functions>.*)/?$', views.ExtMineralList.as_view(), name='ext_mineral_list'),

    url(r'^edificacoes-religiosa/(?P<id_objeto>[0-9]+)/?$', views.EdifReligiosaDetail.as_view(), name='edif_religiosa_detail_id_objeto'),
    url(r'^edificacoes-religiosa/(?P<id_objeto>[0-9]+)/(?P<attributes_functions>.*)/?$', views.EdifReligiosaDetail.as_view(), name='edif_religiosa_detail_af'),
    url(r'^edificacoes-religiosa/?$', views.EdifReligiosaList.as_view(), name='edif_religiosa_list'),
    url(r'^edificacoes-religiosa/(?P<attributes_functions>.*)/?$', views.EdifReligiosaList.as_view(), name='edif_religiosa_list'),

    url(r'^estacoes-geradoras-de-energia-eletrica/(?P<id_objeto>[0-9]+)/?$', views.EstGeradEnergiaEletricaDetail.as_view(), name='est_gerad_energia_eletrica_detail_id_objeto'),
    url(r'^estacoes-geradoras-de-energia-eletrica/(?P<id_objeto>[0-9]+)/(?P<attributes_functions>.*)/?$', views.EstGeradEnergiaEletricaDetail.as_view(), name='est_gerad_energia_eletrica_detail_af'),
    url(r'^estacoes-geradoras-de-energia-eletrica/?$', views.EstGeradEnergiaEletricaList.as_view(), name='est_gerad_energia_eletrica_list'),
    url(r'^estacoes-geradoras-de-energia-eletrica/(?P<attributes_functions>.*)/?$', views.EstGeradEnergiaEletricaList.as_view(), name='est_gerad_energia_eletrica_list'),


    url(r'^hidreletricas/(?P<id_objeto>[0-9]+)/?$', views.HidreletricaDetail.as_view(), name='hidreletrica_detail_id_objeto'),
    url(r'^hidreletricas/(?P<id_objeto>[0-9]+)/(?P<attributes_functions>.*)/?$', views.HidreletricaDetail.as_view(), name='hidreletrica_detail_af'),
    url(r'^hidreletricas/?$', views.HidreletricaList.as_view(), name='hidreletrica_list'),
    url(r'^hidreletricas/(?P<attributes_functions>.*)/?$', views.HidreletricaList.as_view(), name='hidreletrica_list'),

    url(r'^termeletricas/(?P<id_objeto>[0-9]+)/?$', views.TermeletricaDetail.as_view(), name='termeletrica_detail_id_objeto'),
    url(r'^termeletricas/(?P<id_objeto>[0-9]+)/(?P<attributes_functions>.*)/?$', views.TermeletricaDetail.as_view(), name='termeletrica_detail_af'),
    url(r'^termeletricas/?$', views.TermeletricaList.as_view(), name='termeletrica_list'),
    url(r'^termeletricas/(?P<attributes_functions>.*)/?$', views.TermeletricaList.as_view(), name='termeletrica_list'),


    url(r'^torres-de-energia/(?P<id_objeto>[0-9]+)/?$', views.TorreEnergiaDetail.as_view(), name='torre_energia_detail_id_objeto'),
    url(r'^torres-de-energia/(?P<id_objeto>[0-9]+)/(?P<attributes_functions>.*)/?$', views.TorreEnergiaDetail.as_view(), name='torre_energia_detail_af'),
    url(r'^torres-de-energia/?$', views.TorreEnergiaList.as_view(), name='torre_energia_list'),
    url(r'^torres-de-energia/(?P<attributes_functions>.*)/?$', views.TorreEnergiaList.as_view(), name='torre_energia_list'),


    url(r'^bancos-de-areia/(?P<id_objeto>[0-9]+)/?$', views.BancoAreiaDetail.as_view(), name='banco_areia_detail_id_objeto'),
    url(r'^bancos-de-areia/(?P<id_objeto>[0-9]+)/(?P<attributes_functions>.*)/?$', views.BancoAreiaDetail.as_view(), name='banco_areia_detail_af'),
    url(r'^bancos-de-areia/?$', views.BancoAreiaList.as_view(), name='banco_areia_list'),
    url(r'^bancos-de-areia/(?P<attributes_functions>.*)/?$', views.BancoAreiaList.as_view(), name='banco_areia_list'),

    url(r'^barragens/(?P<id_objeto>[0-9]+)/?$', views.BarragemDetail.as_view(), name='barragem_detail_id_objeto'),
    url(r'^barragens/(?P<id_objeto>[0-9]+)/(?P<attributes_functions>.*)/?$', views.BarragemDetail.as_view(), name='barragem_detail_af'),
    url(r'^barragens/?$', views.BarragemList.as_view(), name='barragem_list'),
    url(r'^barragens/(?P<attributes_functions>.*)/?$', views.BarragemList.as_view(), name='barragem_list'),


    url(r'^corredeiras/(?P<id_objeto>[0-9]+)/?$', views.CorredeiraDetail.as_view(), name='corredeira_detail_id_objeto'),
    url(r'^corredeiras/(?P<id_objeto>[0-9]+)/(?P<attributes_functions>.*)/?$', views.CorredeiraDetail.as_view(), name='corredeira_detail_af'),
    url(r'^corredeiras/?$', views.CorredeiraList.as_view(), name='corredeira_list'),
    url(r'^corredeiras/(?P<attributes_functions>.*)/?$', views.CorredeiraList.as_view(), name='corredeira_list'),


    url(r'^fozes-maritima/(?P<id_objeto>[0-9]+)/?$', views.FozMaritimaDetail.as_view(), name='foz_maritima_detail_id_objeto'),
    url(r'^fozes-maritima/(?P<id_objeto>[0-9]+)/(?P<attributes_functions>.*)/?$', views.FozMaritimaDetail.as_view(), name='foz_maritima_detail_af'),
    url(r'^fozes-maritima/?$', views.FozMaritimaList.as_view(), name='foz_maritima_list'),
    url(r'^fozes-maritima/(?P<attributes_functions>.*)/?$', views.FozMaritimaList.as_view(), name='foz_maritima_list'),


    url(r'^ilhas/(?P<id_objeto>[0-9]+)/?$', views.IlhaDetail.as_view(), name='ilha_detail_id_objeto'),
    url(r'^ilhas/(?P<id_objeto>[0-9]+)/(?P<attributes_functions>.*)/?$', views.IlhaDetail.as_view(), name='ilha_detail_af'),
    url(r'^ilhas/?$', views.IlhaList.as_view(), name='ilha_list'),
    url(r'^ilhas/(?P<attributes_functions>.*)/?$', views.IlhaList.as_view(), name='ilha_list'),


    url(r'^massas-dagua/(?P<id_objeto>[0-9]+)/?$', views.MassaDaguaDetail.as_view(), name='massa_dagua_detail_id_objeto'),
    url(r'^massas-dagua/(?P<id_objeto>[0-9]+)/(?P<attributes_functions>.*)/?$', views.MassaDaguaDetail.as_view(), name='massa_dagua_detail_af'),
    url(r'^massas-dagua/?$', views.MassaDaguaList.as_view(), name='massa_dagua_list'),
    url(r'^massas-dagua/(?P<attributes_functions>.*)/?$', views.MassaDaguaList.as_view(), name='massa_dagua_list'),

    url(r'^quedas-dagua/(?P<id_objeto>[0-9]+)/?$', views.QuedaDaguaDetail.as_view(), name='queda_dagua_detail_id_objeto'),
    url(r'^quedas-dagua/(?P<id_objeto>[0-9]+)/(?P<attributes_functions>.*)/?$', views.QuedaDaguaDetail.as_view(), name='queda_dagua_detail_af'),
    url(r'^quedas-dagua/?$', views.QuedaDaguaList.as_view(), name='queda_dagua_list'),
    url(r'^quedas-dagua/(?P<attributes_functions>.*)/?$', views.QuedaDaguaList.as_view(), name='queda_dagua_list'),


    url(r'^recifes/(?P<id_objeto>[0-9]+)/?$', views.RecifeDetail.as_view(), name='recife_detail_id_objeto'),
    url(r'^recifes/(?P<id_objeto>[0-9]+)/(?P<attributes_functions>.*)/?$', views.RecifeDetail.as_view(), name='recife_detail_af'),
    url(r'^recifes/?$', views.RecifeList.as_view(), name='recife_list'),
    url(r'^recifes/(?P<attributes_functions>.*)/?$', views.RecifeList.as_view(), name='recife_list'),


    url(r'^rochas-em-agua/(?P<id_objeto>[0-9]+)/?$', views.RochaEmAguaDetail.as_view(), name='rocha_em_agua_detail_id_objeto'),
    url(r'^rochas-em-agua/(?P<id_objeto>[0-9]+)/(?P<attributes_functions>.*)/?$', views.RochaEmAguaDetail.as_view(), name='rocha_em_agua_detail_af'),
    url(r'^rochas-em-agua/?$', views.RochaEmAguaList.as_view(), name='rocha_em_agua_list'),
    url(r'^rochas-em-agua/(?P<attributes_functions>.*)/?$', views.RochaEmAguaList.as_view(), name='rocha_em_agua_list'),

    url(r'^sumidouros-vertedouros/(?P<id_objeto>[0-9]+)/?$', views.SumidouroVertedouroDetail.as_view(), name='sumidouro_vertedouro_detail_id_objeto'),
    url(r'^sumidouros-vertedouros/(?P<id_objeto>[0-9]+)/(?P<attributes_functions>.*)/?$', views.SumidouroVertedouroDetail.as_view(), name='sumidouro_vertedouro_detail_af'),
    url(r'^sumidouros-vertedouros/?$', views.SumidouroVertedouroList.as_view(), name='sumidouro_vertedouro_list'),
    url(r'^sumidouros-vertedouros/(?P<attributes_functions>.*)/?$', views.SumidouroVertedouroList.as_view(), name='sumidouro_vertedouro_list'),

    url(r'^terrenos-sujeito-a-inundacao/(?P<id_objeto>[0-9]+)/?$', views.TerrenoSujeitoInundacaoDetail.as_view(), name='terreno_sujeito_inundacao_detail_id_objeto'),
    url(r'^terrenos-sujeito-a-inundacao/(?P<id_objeto>[0-9]+)/(?P<attributes_functions>.*)/?$', views.TerrenoSujeitoInundacaoDetail.as_view(), name='terreno_sujeito_inundacao_detail_id_objeto'),
    url(r'^terrenos-sujeito-a-inundacao/?$', views.TerrenoSujeitoInundacaoList.as_view(), name='terreno_sujeito_inundacao_list'),
    url(r'^terrenos-sujeito-a-inundacao/(?P<attributes_functions>.*)/?$', views.TerrenoSujeitoInundacaoList.as_view(), name='terreno_sujeito_inundacao_list'),

    url(r'^trechos-de-drenagem/(?P<id_objeto>[0-9]+)/?$', views.TrechoDrenagemDetail.as_view(), name='trecho_drenagem_detail_id_objeto'),
    url(r'^trechos-de-drenagem/(?P<id_objeto>[0-9]+)/(?P<attributes_functions>.*)/?$', views.TrechoDrenagemDetail.as_view(), name='trecho_drenagem_detail_af'),
    url(r'^trechos-de-drenagem/?$', views.TrechoDrenagemList.as_view(), name='trecho_drenagem_list'),
    url(r'^trechos-de-drenagem/(?P<attributes_functions>.*)/?$', views.TrechoDrenagemList.as_view(), name='trecho_drenagem_list'),

    url(r'^trechos-de-massa-dagua/(?P<id_objeto>[0-9]+)/?$', views.TrechoMassaDaguaDetail.as_view(), name='trecho_massa_dagua_id_objeto'),
    url(r'^trechos-de-massa-dagua/(?P<id_objeto>[0-9]+)/(?P<attributes_functions>.*)/?$', views.TrechoMassaDaguaDetail.as_view(), name='trecho_massa_dagua_detail_af'),
    url(r'^trechos-de-massa-dagua/?$', views.TrechoMassaDaguaList.as_view(), name='trecho_massa_dagua_list'),
    url(r'^trechos-de-massa-dagua/(?P<attributes_functions>.*)/?$', views.TrechoMassaDaguaList.as_view(), name='trecho_massa_dagua_list'),


    url(r'^areas-de-desenvolvimento-de-controle/(?P<id_objeto>[0-9]+)/?$', views.AreaDesenvolvimentoControleDetail.as_view(), name='area_desenvolvimento_controle_detail_id_objeto'),
    url(r'^areas-de-desenvolvimento-de-controle/(?P<id_objeto>[0-9]+)/(?P<attributes_functions>.*)/?$', views.AreaDesenvolvimentoControleDetail.as_view(), name='area_desenvolvimento_controle_detail_af'),
    url(r'^areas-de-desenvolvimento-de-controle/?$', views.AreaDesenvolvimentoControleList.as_view(), name='area_desenvolvimento_controle_list'),
    url(r'^areas-de-desenvolvimento-de-controle/(?P<attributes_functions>.*)/?$', views.AreaDesenvolvimentoControleList.as_view(), name='area_desenvolvimento_controle_list'),

    url(r'^marcos-de-limite/(?P<id_objeto>[0-9]+)/?$', views.MarcoDeLimiteDetail.as_view(), name='marco_de_limite_detail_id_objeto'),
    url(r'^marcos-de-limite/(?P<id_objeto>[0-9]+)/(?P<attributes_functions>.*)/?$', views.MarcoDeLimiteDetail.as_view(), name='marco_de_limite_detail_af'),
    url(r'^marcos-de-limite/?$', views.MarcoDeLimiteList.as_view(), name='marco_de_limite_list'),
    url(r'^marcos-de-limite/(?P<attributes_functions>.*)/?$', views.MarcoDeLimiteList.as_view(), name='marco_de_limite_list'),

    # urls generalized

)

urlpatterns = format_suffix_patterns(urlpatterns, allowed=['json', 'png', 'jsonld'])
