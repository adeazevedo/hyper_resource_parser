from __future__ import unicode_literals
from hyper_resource.models import FeatureModel, FeatureModel, BusinessModel
# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.

import datetime
from django.contrib.gis.db import models
from django.utils.translation import ugettext_lazy as _

from hyper_resource.models import FeatureModel, FeatureModel

class EntryPoint(BusinessModel):
    unidades_federativas = models.CharField(max_length=200)
    municipios = models.CharField(max_length=200)
    outros_limites_oficiais = models.CharField(max_length=200)
    paises = models.CharField(max_length=200)
    terras_indigenas = models.CharField(max_length=200)
    unidades_de_conservacao_nao_snuc = models.CharField(max_length=200)
    unidades_de_protecao_integral = models.CharField(max_length=200)
    unidades_de_uso_sustentavel = models.CharField(max_length=200)
    aglomerados_rurais_de_extensao_urbana = models.CharField(max_length=200)
    aglomerados_rurais_isolado = models.CharField(max_length=200)
    aldeias_indigenas = models.CharField(max_length=200)
    areas_edificadas = models.CharField(max_length=200)
    capitais = models.CharField(max_length=200)
    cidades = models.CharField(max_length=200)
    vilas = models.CharField(max_length=200)
    curvas_batimetricas = models.CharField(max_length=200)
    curvas_de_nivel = models.CharField(max_length=200)
    dunas = models.CharField(max_length=200)
    elementos_fisiografico_natural = models.CharField(max_length=200)
    picos = models.CharField(max_length=200)
    pontos_cotados_altimetricos = models.CharField(max_length=200)
    pontos_cotados_batimetricos = models.CharField(max_length=200)
    eclusas = models.CharField(max_length=200)
    edificacoes_de_construcao_portuaria = models.CharField(max_length=200)
    edificacoes_de_construcao_aeroportuaria = models.CharField(max_length=200)
    edificacoes_de_metro_ferroviaria = models.CharField(max_length=200)
    fundeadouros = models.CharField(max_length=200)
    pistas_de_ponto_pouso = models.CharField(max_length=200)
    pontes = models.CharField(max_length=200)
    sinalizacoes = models.CharField(max_length=200)
    travessias = models.CharField(max_length=200)
    trechos_dutos = models.CharField(max_length=200)
    trechos_ferroviarios = models.CharField(max_length=200)
    trechos_hidroviarios = models.CharField(max_length=200)
    trechos_rodoviarios = models.CharField(max_length=200)
    tuneis = models.CharField(max_length=200)
    brejos_e_pantanos = models.CharField(max_length=200)
    mangues = models.CharField(max_length=200)
    vegetacoes_de_restinga = models.CharField(max_length=200)
    edificacoes_publica_militar = models.CharField(max_length=200)
    postos_fiscais = models.CharField(max_length=200)
    edificacoes_agropecuarias_de_extracao_vegetal_e_pesca = models.CharField(max_length=200)
    edificacoes_industrial = models.CharField(max_length=200)
    extracoes_minerais = models.CharField(max_length=200)
    edificacoes_religiosa = models.CharField(max_length=200)
    estacoes_geradoras_de_energia_eletrica = models.CharField(max_length=200)
    hidreletricas = models.CharField(max_length=200)
    termeletricas = models.CharField(max_length=200)
    torres_de_energia = models.CharField(max_length=200)
    bancos_de_areia = models.CharField(max_length=200)
    barragens = models.CharField(max_length=200)
    corredeiras = models.CharField(max_length=200)
    fozes_maritima = models.CharField(max_length=200)
    ilhas = models.CharField(max_length=200)
    massas_dagua = models.CharField(max_length=200)
    quedas_dagua = models.CharField(max_length=200)
    recifes = models.CharField(max_length=200)
    rochas_em_agua = models.CharField(max_length=200)
    sumidouros_vertedouros = models.CharField(max_length=200)
    terrenos_sujeito_a_inundacao = models.CharField(max_length=200)
    trechos_de_drenagem = models.CharField(max_length=200)
    trechos_de_massa_dagua = models.CharField(max_length=200)
    areas_de_desenvolvimento_de_controle = models.CharField(max_length=200)
    marcos_de_limite = models.CharField(max_length=200)


class EdifPubMilitar(FeatureModel):
    id_objeto = models.IntegerField(primary_key=True)
    nome = models.CharField(max_length=100, blank=True, null=True)
    nomeabrev = models.CharField(max_length=50, blank=True, null=True)
    geometriaaproximada = models.CharField(max_length=3, blank=True, null=True)
    tipoedifmil = models.CharField(max_length=26, blank=True, null=True)
    tipousoedif = models.CharField(max_length=21, blank=True, null=True)
    situacaofisica = models.TextField(blank=True, null=True)
    operacional = models.CharField(max_length=12, blank=True, null=True)
    matconstr = models.CharField(max_length=18, blank=True, null=True)
    geom = models.GeometryField(blank=True, null=True)


    iri_metadata = models.CharField(max_length=1000, blank=True, null=True)
    iri_style = models.CharField(max_length=1000, blank=True, null=True)
    contextclassname = 'edificacoes-publica-militar'
    class Meta:
        managed = False
        db_table = 'adm_edif_pub_militar_p'


class PostoFiscal(FeatureModel):
    id_objeto = models.IntegerField(primary_key=True)
    nome = models.CharField(max_length=100, blank=True, null=True)
    nomeabrev = models.CharField(max_length=50, blank=True, null=True)
    geometriaaproximada = models.CharField(max_length=3, blank=True, null=True)
    operacional = models.CharField(max_length=12, blank=True, null=True)
    situacaofisica = models.TextField(blank=True, null=True)
    tipopostofisc = models.CharField(max_length=22, blank=True, null=True)
    geom = models.GeometryField(blank=True, null=True)

    iri_metadata = models.CharField(max_length=1000, blank=True, null=True)
    iri_style = models.CharField(max_length=1000, blank=True, null=True)
    class Meta:
        managed = False
        db_table = 'adm_posto_fiscal_p'






class EdifAgropecExtVegetalPesca(FeatureModel):
    id_objeto = models.IntegerField(primary_key=True)
    nome = models.CharField(max_length=100, blank=True, null=True)
    nomeabrev = models.CharField(max_length=50, blank=True, null=True)
    geometriaaproximada = models.CharField(max_length=3, blank=True, null=True)
    operacional = models.CharField(max_length=12, blank=True, null=True)
    situacaofisica = models.TextField(blank=True, null=True)
    tipoedifagropec = models.CharField(max_length=50, blank=True, null=True)
    matconstr = models.CharField(max_length=18, blank=True, null=True)
    geom = models.GeometryField(blank=True, null=True)

    iri_metadata = models.CharField(max_length=1000, blank=True, null=True)
    iri_style = models.CharField(max_length=1000, blank=True, null=True)
    class Meta:
        managed = False
        db_table = 'eco_edif_agropec_ext_vegetal_pesca_p'


class EdifIndustrial(FeatureModel):
    id_objeto = models.IntegerField(primary_key=True)
    nome = models.CharField(max_length=100, blank=True, null=True)
    nomeabrev = models.CharField(max_length=50, blank=True, null=True)
    geometriaaproximada = models.CharField(max_length=3, blank=True, null=True)
    chamine = models.CharField(max_length=3, blank=True, null=True)
    operacional = models.CharField(max_length=12, blank=True, null=True)
    situacaofisica = models.TextField(blank=True, null=True)
    matconstr = models.CharField(max_length=18, blank=True, null=True)
    tipodivisaocnae = models.CharField(max_length=180, blank=True, null=True)
    geom = models.GeometryField(blank=True, null=True)

    iri_metadata = models.CharField(max_length=1000, blank=True, null=True)
    iri_style = models.CharField(max_length=1000, blank=True, null=True)
    class Meta:
        managed = False
        db_table = 'eco_edif_industrial_p'


class ExtMineral_A(FeatureModel):
    id_objeto = models.IntegerField(primary_key=True)
    nome = models.CharField(max_length=100, blank=True, null=True)
    nomeabrev = models.CharField(max_length=50, blank=True, null=True)
    geometriaaproximada = models.CharField(max_length=3, blank=True, null=True)
    tiposecaocnae = models.CharField(max_length=50, blank=True, null=True)
    operacional = models.CharField(max_length=12, blank=True, null=True)
    situacaofisica = models.TextField(blank=True, null=True)
    tipoextmin = models.CharField(max_length=20, blank=True, null=True)
    tipoprodutoresiduo = models.CharField(max_length=40, blank=True, null=True)
    tipopocomina = models.CharField(max_length=15, blank=True, null=True)
    procextracao = models.CharField(max_length=12, blank=True, null=True)
    formaextracao = models.CharField(max_length=12, blank=True, null=True)
    atividade = models.CharField(max_length=12, blank=True, null=True)
    geom = models.GeometryField(blank=True, null=True)

    iri_metadata = models.CharField(max_length=1000, blank=True, null=True)
    iri_style = models.CharField(max_length=1000, blank=True, null=True)
    class Meta:
        managed = False
        db_table = 'eco_ext_mineral_a'


class ExtMineral(FeatureModel):
    id_objeto = models.IntegerField(primary_key=True)
    nome = models.CharField(max_length=100, blank=True, null=True)
    nomeabrev = models.CharField(max_length=50, blank=True, null=True)
    geometriaaproximada = models.CharField(max_length=3, blank=True, null=True)
    tiposecaocnae = models.CharField(max_length=50, blank=True, null=True)
    operacional = models.CharField(max_length=12, blank=True, null=True)
    situacaofisica = models.TextField(blank=True, null=True)
    tipoextmin = models.CharField(max_length=20, blank=True, null=True)
    tipoprodutoresiduo = models.CharField(max_length=40, blank=True, null=True)
    tipopocomina = models.CharField(max_length=15, blank=True, null=True)
    procextracao = models.CharField(max_length=12, blank=True, null=True)
    formaextracao = models.CharField(max_length=12, blank=True, null=True)
    atividade = models.CharField(max_length=12, blank=True, null=True)
    geom = models.GeometryField(blank=True, null=True)

    iri_metadata = models.CharField(max_length=1000, blank=True, null=True)
    iri_style = models.CharField(max_length=1000, blank=True, null=True)
    class Meta:
        managed = False
        db_table = 'eco_ext_mineral_p'


class EdifReligiosa(FeatureModel):
    id_objeto = models.IntegerField(primary_key=True)
    nome = models.CharField(max_length=100, blank=True, null=True)
    nomeabrev = models.CharField(max_length=50, blank=True, null=True)
    geometriaaproximada = models.CharField(max_length=3, blank=True, null=True)
    religiao = models.CharField(max_length=100, blank=True, null=True)
    tipoedifrelig = models.CharField(max_length=12, blank=True, null=True)
    ensino = models.CharField(max_length=12, blank=True, null=True)
    operacional = models.CharField(max_length=12, blank=True, null=True)
    situacaofisica = models.TextField(blank=True, null=True)
    matconstr = models.CharField(max_length=18, blank=True, null=True)
    geom = models.GeometryField(blank=True, null=True)

    iri_metadata = models.CharField(max_length=1000, blank=True, null=True)
    iri_style = models.CharField(max_length=1000, blank=True, null=True)
    class Meta:
        managed = False
        db_table = 'edu_edif_religiosa_p'




class Employee(FeatureModel):
    employee_id = models.IntegerField(blank=True, null=True)
    name = models.CharField(max_length=30, blank=True, null=True)
    hire_date = models.DateField(blank=True, null=True)

    iri_metadata = models.CharField(max_length=1000, blank=True, null=True)
    iri_style = models.CharField(max_length=1000, blank=True, null=True)
    class Meta:
        managed = False
        db_table = 'employee'



class EstGeradEnergiaEletrica(FeatureModel):
    id_objeto = models.IntegerField(primary_key=True)
    nome = models.CharField(max_length=100, blank=True, null=True)
    nomeabrev = models.CharField(max_length=50, blank=True, null=True)
    geometriaaproximada = models.CharField(max_length=3, blank=True, null=True)
    codigoestacao = models.CharField(max_length=30, blank=True, null=True)
    potenciaoutorgada = models.IntegerField(blank=True, null=True)
    potenciafiscalizada = models.IntegerField(blank=True, null=True)
    operacional = models.CharField(max_length=12, blank=True, null=True)
    situacaofisica = models.TextField(blank=True, null=True)
    tipoestgerad = models.CharField(max_length=15, blank=True, null=True)
    destenergelet = models.CharField(max_length=56, blank=True, null=True)
    geom = models.GeometryField(blank=True, null=True)

    iri_metadata = models.CharField(max_length=1000, blank=True, null=True)
    iri_style = models.CharField(max_length=1000, blank=True, null=True)
    class Meta:
        managed = False
        db_table = 'enc_est_gerad_energia_eletrica_p'


class Hidreletrica(FeatureModel):
    id_objeto = models.IntegerField(primary_key=True)
    nome = models.CharField(max_length=100, blank=True, null=True)
    nomeabrev = models.CharField(max_length=50, blank=True, null=True)
    geometriaaproximada = models.CharField(max_length=3, blank=True, null=True)
    potenciaoutorgada = models.IntegerField(blank=True, null=True)
    potenciafiscalizada = models.IntegerField(blank=True, null=True)
    codigohidreletrica = models.CharField(max_length=30, blank=True, null=True)
    operacional = models.CharField(max_length=12, blank=True, null=True)
    situacaofisica = models.TextField(blank=True, null=True)
    geom = models.GeometryField(blank=True, null=True)

    iri_metadata = models.CharField(max_length=1000, blank=True, null=True)
    iri_style = models.CharField(max_length=1000, blank=True, null=True)
    class Meta:
        managed = False
        db_table = 'enc_hidreletrica_p'


class Termeletrica(FeatureModel):
    id_objeto = models.IntegerField(primary_key=True)
    nome = models.CharField(max_length=100, blank=True, null=True)
    nomeabrev = models.CharField(max_length=50, blank=True, null=True)
    geometriaaproximada = models.CharField(max_length=3, blank=True, null=True)
    potenciaoutorgada = models.IntegerField(blank=True, null=True)
    potenciafiscalizada = models.IntegerField(blank=True, null=True)
    combrenovavel = models.CharField(max_length=3, blank=True, null=True)
    tipomaqtermica = models.CharField(max_length=33, blank=True, null=True)
    geracao = models.CharField(max_length=20, blank=True, null=True)
    tipocombustivel = models.CharField(max_length=17, blank=True, null=True)
    operacional = models.CharField(max_length=12, blank=True, null=True)
    situacaofisica = models.TextField(blank=True, null=True)
    geom = models.GeometryField(blank=True, null=True)

    iri_metadata = models.CharField(max_length=1000, blank=True, null=True)
    iri_style = models.CharField(max_length=1000, blank=True, null=True)
    class Meta:
        managed = False
        db_table = 'enc_termeletrica_p'


class TorreEnergia(FeatureModel):
    id_objeto = models.IntegerField(primary_key=True)
    nome = models.CharField(max_length=100, blank=True, null=True)
    nomeabrev = models.CharField(max_length=50, blank=True, null=True)
    geometriaaproximada = models.CharField(max_length=3, blank=True, null=True)
    alturaestimada = models.FloatField(blank=True, null=True)
    arranjofases = models.CharField(max_length=50, blank=True, null=True)
    ovgd = models.CharField(max_length=12, blank=True, null=True)
    operacional = models.CharField(max_length=12, blank=True, null=True)
    situacaofisica = models.TextField(blank=True, null=True)
    tipotorre = models.CharField(max_length=12, blank=True, null=True)
    geom = models.GeometryField(blank=True, null=True)

    iri_metadata = models.CharField(max_length=1000, blank=True, null=True)
    iri_style = models.CharField(max_length=1000, blank=True, null=True)
    class Meta:
        managed = False
        db_table = 'enc_torre_energia_p'



class BancoAreia(FeatureModel):
    id_objeto = models.IntegerField(primary_key=True)
    nome = models.CharField(max_length=100, blank=True, null=True)
    nomeabrev = models.CharField(max_length=50, blank=True, null=True)
    geometriaaproximada = models.CharField(max_length=3, blank=True, null=True)
    tipobanco = models.CharField(max_length=14, blank=True, null=True)
    situacaoemagua = models.CharField(max_length=17, blank=True, null=True)
    materialpredominante = models.CharField(max_length=27, blank=True, null=True)
    geom = models.GeometryField(blank=True, null=True)

    iri_metadata = models.CharField(max_length=1000, blank=True, null=True)
    iri_style = models.CharField(max_length=1000, blank=True, null=True)
    class Meta:
        managed = False
        db_table = 'hid_banco_areia_a'


class Barragem(FeatureModel):
    id_objeto = models.IntegerField(primary_key=True)
    nome = models.CharField(max_length=100, blank=True, null=True)
    nomeabrev = models.CharField(max_length=50, blank=True, null=True)
    geometriaaproximada = models.CharField(max_length=3, blank=True, null=True)
    matconstr = models.CharField(max_length=18, blank=True, null=True)
    usoprincipal = models.CharField(max_length=15, blank=True, null=True)
    operacional = models.CharField(max_length=12, blank=True, null=True)
    situacaofisica = models.TextField(blank=True, null=True)
    geom = models.GeometryField(blank=True, null=True)

    iri_metadata = models.CharField(max_length=1000, blank=True, null=True)
    iri_style = models.CharField(max_length=1000, blank=True, null=True)
    class Meta:
        managed = False
        db_table = 'hid_barragem_l'


class Corredeira(FeatureModel):
    id_objeto = models.IntegerField(primary_key=True)
    nome = models.CharField(max_length=100, blank=True, null=True)
    nomeabrev = models.CharField(max_length=50, blank=True, null=True)
    geometriaaproximada = models.CharField(max_length=3, blank=True, null=True)
    geom = models.GeometryField(blank=True, null=True)

    iri_metadata = models.CharField(max_length=1000, blank=True, null=True)
    iri_style = models.CharField(max_length=1000, blank=True, null=True)
    class Meta:
        managed = False
        db_table = 'hid_corredeira_l'


class Corredeira_P(FeatureModel):
    id_objeto = models.IntegerField(primary_key=True)
    nome = models.CharField(max_length=100, blank=True, null=True)
    nomeabrev = models.CharField(max_length=50, blank=True, null=True)
    geometriaaproximada = models.CharField(max_length=3, blank=True, null=True)
    geom = models.GeometryField(blank=True, null=True)

    iri_metadata = models.CharField(max_length=1000, blank=True, null=True)
    iri_style = models.CharField(max_length=1000, blank=True, null=True)
    class Meta:
        managed = False
        db_table = 'hid_corredeira_p'


class FozMaritima(FeatureModel):
    id_objeto = models.IntegerField(primary_key=True)
    nome = models.CharField(max_length=100, blank=True, null=True)
    nomeabrev = models.CharField(max_length=50, blank=True, null=True)
    geometriaaproximada = models.CharField(max_length=3, blank=True, null=True)
    geom = models.GeometryField(blank=True, null=True)

    iri_metadata = models.CharField(max_length=1000, blank=True, null=True)
    iri_style = models.CharField(max_length=1000, blank=True, null=True)
    class Meta:
        managed = False
        db_table = 'hid_foz_maritima_l'


class Ilha(FeatureModel):
    id_objeto = models.IntegerField(primary_key=True)
    nome = models.CharField(max_length=100, blank=True, null=True)
    nomeabrev = models.CharField(max_length=50, blank=True, null=True)
    geometriaaproximada = models.CharField(max_length=3, blank=True, null=True)
    tipoilha = models.CharField(max_length=8, blank=True, null=True)
    geom = models.GeometryField(blank=True, null=True)

    iri_metadata = models.CharField(max_length=1000, blank=True, null=True)
    iri_style = models.CharField(max_length=1000, blank=True, null=True)
    class Meta:
        managed = False
        db_table = 'hid_ilha_a'


class MassaDagua(FeatureModel):
    id_objeto = models.IntegerField(primary_key=True)
    nome = models.CharField(max_length=100, blank=True, null=True)
    nomeabrev = models.CharField(max_length=50, blank=True, null=True)
    geometriaaproximada = models.CharField(max_length=3, blank=True, null=True)
    tipomassadagua = models.CharField(max_length=18, blank=True, null=True)
    salinidade = models.CharField(max_length=16, blank=True, null=True)
    regime = models.CharField(max_length=31, blank=True, null=True)
    geom = models.GeometryField(blank=True, null=True)

    iri_metadata = models.CharField(max_length=1000, blank=True, null=True)
    iri_style = models.CharField(max_length=1000, blank=True, null=True)
    class Meta:
        managed = False
        db_table = 'hid_massa_dagua_a'


class QuedaDagua(FeatureModel):
    id_objeto = models.IntegerField(primary_key=True)
    nome = models.CharField(max_length=100, blank=True, null=True)
    nomeabrev = models.CharField(max_length=50, blank=True, null=True)
    geometriaaproximada = models.CharField(max_length=3, blank=True, null=True)
    altura = models.FloatField(blank=True, null=True)
    tipoqueda = models.CharField(max_length=15, blank=True, null=True)
    geom = models.GeometryField(blank=True, null=True)

    iri_metadata = models.CharField(max_length=1000, blank=True, null=True)
    iri_style = models.CharField(max_length=1000, blank=True, null=True)
    class Meta:
        managed = False
        db_table = 'hid_queda_dagua_l'


class QuedaDagua_P(FeatureModel):
    id_objeto = models.IntegerField(primary_key=True)
    nome = models.CharField(max_length=100, blank=True, null=True)
    nomeabrev = models.CharField(max_length=50, blank=True, null=True)
    geometriaaproximada = models.CharField(max_length=3, blank=True, null=True)
    altura = models.FloatField(blank=True, null=True)
    tipoqueda = models.CharField(max_length=15, blank=True, null=True)
    geom = models.GeometryField(blank=True, null=True)

    iri_metadata = models.CharField(max_length=1000, blank=True, null=True)
    iri_style = models.CharField(max_length=1000, blank=True, null=True)
    class Meta:
        managed = False
        db_table = 'hid_queda_dagua_p'


class Recife(FeatureModel):
    id_objeto = models.IntegerField(primary_key=True)
    nome = models.CharField(max_length=100, blank=True, null=True)
    nomeabrev = models.CharField(max_length=50, blank=True, null=True)
    geometriaaproximada = models.CharField(max_length=3, blank=True, null=True)
    tiporecife = models.CharField(max_length=16, blank=True, null=True)
    situamare = models.CharField(max_length=35, blank=True, null=True)
    situacaocosta = models.CharField(max_length=12, blank=True, null=True)
    geom = models.GeometryField(blank=True, null=True)

    iri_metadata = models.CharField(max_length=1000, blank=True, null=True)
    iri_style = models.CharField(max_length=1000, blank=True, null=True)
    class Meta:
        managed = False
        db_table = 'hid_recife_a'


class Recife_P(FeatureModel):
    id_objeto = models.IntegerField(primary_key=True)
    nome = models.CharField(max_length=100, blank=True, null=True)
    nomeabrev = models.CharField(max_length=50, blank=True, null=True)
    geometriaaproximada = models.CharField(max_length=3, blank=True, null=True)
    tiporecife = models.CharField(max_length=16, blank=True, null=True)
    situamare = models.CharField(max_length=35, blank=True, null=True)
    situacaocosta = models.CharField(max_length=12, blank=True, null=True)
    geom = models.GeometryField(blank=True, null=True)

    iri_metadata = models.CharField(max_length=1000, blank=True, null=True)
    iri_style = models.CharField(max_length=1000, blank=True, null=True)
    class Meta:
        managed = False
        db_table = 'hid_recife_p'


class RochaEmAgua(FeatureModel):
    id_objeto = models.IntegerField(primary_key=True)
    nome = models.CharField(max_length=100, blank=True, null=True)
    nomeabrev = models.CharField(max_length=50, blank=True, null=True)
    geometriaaproximada = models.CharField(max_length=3, blank=True, null=True)
    alturalamina = models.FloatField(blank=True, null=True)
    situacaoemagua = models.CharField(max_length=17, blank=True, null=True)
    geom = models.GeometryField(blank=True, null=True)

    iri_metadata = models.CharField(max_length=1000, blank=True, null=True)
    iri_style = models.CharField(max_length=1000, blank=True, null=True)
    class Meta:
        managed = False
        db_table = 'hid_rocha_em_agua_a'


class RochaEmAgua_P(FeatureModel):
    id_objeto = models.IntegerField(primary_key=True)
    nome = models.CharField(max_length=100, blank=True, null=True)
    nomeabrev = models.CharField(max_length=50, blank=True, null=True)
    geometriaaproximada = models.CharField(max_length=3, blank=True, null=True)
    alturalamina = models.FloatField(blank=True, null=True)
    situacaoemagua = models.CharField(max_length=17, blank=True, null=True)
    geom = models.GeometryField(blank=True, null=True)

    iri_metadata = models.CharField(max_length=1000, blank=True, null=True)
    iri_style = models.CharField(max_length=1000, blank=True, null=True)
    class Meta:
        managed = False
        db_table = 'hid_rocha_em_agua_p'


class SumidouroVertedouro(FeatureModel):
    id_objeto = models.IntegerField(primary_key=True)
    nome = models.CharField(max_length=100, blank=True, null=True)
    nomeabrev = models.CharField(max_length=50, blank=True, null=True)
    geometriaaproximada = models.CharField(max_length=3, blank=True, null=True)
    causa = models.CharField(max_length=25, blank=True, null=True)
    tiposumvert = models.CharField(max_length=12, blank=True, null=True)
    geom = models.GeometryField(blank=True, null=True)

    iri_metadata = models.CharField(max_length=1000, blank=True, null=True)
    iri_style = models.CharField(max_length=1000, blank=True, null=True)
    class Meta:
        managed = False
        db_table = 'hid_sumidouro_vertedouro_p'


class TerrenoSujeitoInundacao(FeatureModel):
    id_objeto = models.IntegerField(primary_key=True)
    nome = models.CharField(max_length=100, blank=True, null=True)
    nomeabrev = models.CharField(max_length=50, blank=True, null=True)
    geometriaaproximada = models.CharField(max_length=3, blank=True, null=True)
    periodicidadeinunda = models.CharField(max_length=20, blank=True, null=True)
    geom = models.GeometryField(blank=True, null=True)

    iri_metadata = models.CharField(max_length=1000, blank=True, null=True)
    iri_style = models.CharField(max_length=1000, blank=True, null=True)
    class Meta:
        managed = False
        db_table = 'hid_terreno_sujeito_inundacao_a'


class TrechoDrenagem(FeatureModel):
    id_objeto = models.IntegerField(primary_key=True)
    nome = models.CharField(max_length=100, blank=True, null=True)
    nomeabrev = models.CharField(max_length=50, blank=True, null=True)
    geometriaaproximada = models.CharField(max_length=3, blank=True, null=True)
    dentrodepoligono = models.CharField(max_length=3, blank=True, null=True)
    compartilhado = models.CharField(max_length=3, blank=True, null=True)
    eixoprincipal = models.CharField(max_length=3, blank=True, null=True)
    caladomax = models.FloatField(blank=True, null=True)
    larguramedia = models.FloatField(blank=True, null=True)
    velocidademedcorrente = models.FloatField(blank=True, null=True)
    profundidademedia = models.FloatField(blank=True, null=True)
    coincidecomdentrode = models.CharField(max_length=35, blank=True, null=True)
    navegabilidade = models.CharField(max_length=16, blank=True, null=True)
    regime = models.CharField(max_length=31, blank=True, null=True)
    geom = models.GeometryField(blank=True, null=True)

    iri_metadata = models.CharField(max_length=1000, blank=True, null=True)
    iri_style = models.CharField(max_length=1000, blank=True, null=True)
    class Meta:
        managed = False
        db_table = 'hid_trecho_drenagem_l'


class TrechoMassaDagua(FeatureModel):
    id_objeto = models.IntegerField(primary_key=True)
    nome = models.CharField(max_length=100, blank=True, null=True)
    nomeabrev = models.CharField(max_length=50, blank=True, null=True)
    geometriaaproximada = models.CharField(max_length=3, blank=True, null=True)
    tipotrechomassa = models.CharField(max_length=13, blank=True, null=True)
    salinidade = models.CharField(max_length=16, blank=True, null=True)
    regime = models.CharField(max_length=31, blank=True, null=True)
    geom = models.GeometryField(blank=True, null=True)

    iri_metadata = models.CharField(max_length=1000, blank=True, null=True)
    iri_style = models.CharField(max_length=1000, blank=True, null=True)
    class Meta:
        managed = False
        db_table = 'hid_trecho_massa_dagua_a'



class AreaDesenvolvimentoControle(FeatureModel):
    id_objeto = models.IntegerField(primary_key=True)
    nome = models.CharField(max_length=100, blank=True, null=True)
    nomeabrev = models.CharField(max_length=50, blank=True, null=True)
    geometriaaproximada = models.CharField(max_length=3, blank=True, null=True)
    classificacao = models.CharField(max_length=100, blank=True, null=True)
    geom = models.GeometryField(blank=True, null=True)

    iri_metadata = models.CharField(max_length=1000, blank=True, null=True)
    iri_style = models.CharField(max_length=1000, blank=True, null=True)
    class Meta:
        managed = False
        db_table = 'lim_area_desenvolvimento_controle_a'


class MarcoDeLimite(FeatureModel):
    id_objeto = models.IntegerField(primary_key=True)
    nome = models.CharField(max_length=100, blank=True, null=True)
    nomeabrev = models.CharField(max_length=50, blank=True, null=True)
    geometriaaproximada = models.CharField(max_length=3, blank=True, null=True)
    tipomarcolim = models.CharField(max_length=13, blank=True, null=True)
    latitude = models.CharField(max_length=20, blank=True, null=True)
    longitude = models.CharField(max_length=20, blank=True, null=True)
    altitudeortometrica = models.FloatField(blank=True, null=True)
    orgresp = models.CharField(max_length=10, blank=True, null=True)
    sistemageodesico = models.CharField(max_length=16, blank=True, null=True)
    outrarefplan = models.CharField(max_length=20, blank=True, null=True)
    outrarefalt = models.CharField(max_length=20, blank=True, null=True)
    referencialaltim = models.CharField(max_length=16, blank=True, null=True)
    geom = models.GeometryField(blank=True, null=True)

    iri_metadata = models.CharField(max_length=1000, blank=True, null=True)
    iri_style = models.CharField(max_length=1000, blank=True, null=True)
    class Meta:
        managed = False
        db_table = 'lim_marco_de_limite_p'


class Municipio(FeatureModel):
    id_objeto = models.IntegerField(primary_key=True)
    nome = models.CharField(max_length=100, blank=True, null=True)
    nomeabrev = models.CharField(max_length=50, blank=True, null=True)
    geometriaaproximada = models.CharField(max_length=3, blank=True, null=True)
    geocodigo = models.CharField(max_length=15, blank=True, null=True)
    anodereferencia = models.FloatField(blank=True, null=True)
    geom = models.GeometryField(blank=True, null=True)

    iri_metadata = models.CharField(max_length=1000, blank=True, null=True)
    iri_style = models.CharField(max_length=1000, blank=True, null=True)
    class Meta:
        managed = False
        db_table = 'lim_municipio_a'


class OutrasUnidProtegidas(FeatureModel):
    gid = models.AutoField(primary_key=True)
    nome = models.CharField(max_length=100, blank=True, null=True)
    nomeabrev = models.CharField(max_length=50, blank=True, null=True)
    geometriaa = models.CharField(max_length=3, blank=True, null=True)
    anocriacao = models.FloatField(blank=True, null=True)
    sigla = models.CharField(max_length=6, blank=True, null=True)
    areaoficia = models.CharField(max_length=15, blank=True, null=True)
    administra = models.CharField(max_length=18, blank=True, null=True)
    tipooutuni = models.CharField(max_length=30, blank=True, null=True)
    historicom = models.CharField(max_length=254, blank=True, null=True)
    geom = models.MultiPolygonField(srid=4326, dim=4, blank=True, null=True)

    iri_metadata = models.CharField(max_length=1000, blank=True, null=True)
    iri_style = models.CharField(max_length=1000, blank=True, null=True)
    class Meta:
        managed = False
        db_table = 'lim_outras_unid_protegidas_a'


class OutrosLimitesOficiais(FeatureModel):
    id_objeto = models.IntegerField(primary_key=True)
    nome = models.CharField(max_length=100, blank=True, null=True)
    nomeabrev = models.CharField(max_length=50, blank=True, null=True)
    geometriaaproximada = models.CharField(max_length=3, blank=True, null=True)
    coincidecomdentrode = models.CharField(max_length=50, blank=True, null=True)
    extensao = models.FloatField(blank=True, null=True)
    obssituacao = models.CharField(max_length=100, blank=True, null=True)
    tipooutlimofic = models.CharField(max_length=50, blank=True, null=True)
    geom = models.GeometryField(blank=True, null=True)

    iri_metadata = models.CharField(max_length=1000, blank=True, null=True)
    iri_style = models.CharField(max_length=1000, blank=True, null=True)
    class Meta:
        managed = False
        db_table = 'lim_outros_limites_oficiais_l'


class Pais(FeatureModel):
    id_objeto = models.IntegerField(primary_key=True)
    nome = models.CharField(max_length=100, blank=True, null=True)
    nomeabrev = models.CharField(max_length=50, blank=True, null=True)
    geometriaaproximada = models.CharField(max_length=3, blank=True, null=True)
    sigla = models.CharField(max_length=3, blank=True, null=True)
    codiso3166 = models.CharField(max_length=3, blank=True, null=True)
    geom = models.GeometryField(blank=True, null=True)

    iri_metadata = models.CharField(max_length=1000, blank=True, null=True)
    iri_style = models.CharField(max_length=1000, blank=True, null=True)
    class Meta:
        managed = False
        db_table = 'lim_pais_a'


class TerraIndigena(FeatureModel):
    id_objeto = models.IntegerField(primary_key=True)
    nome = models.CharField(max_length=100, blank=True, null=True)
    nomeabrev = models.CharField(max_length=50, blank=True, null=True)
    geometriaaproximada = models.CharField(max_length=3, blank=True, null=True)
    perimetrooficial = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    areaoficialha = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    grupoetnico = models.CharField(max_length=100, blank=True, null=True)
    datasituacaojuridica = models.CharField(max_length=20, blank=True, null=True)
    situacaojuridica = models.CharField(max_length=23, blank=True, null=True)
    nometi = models.CharField(max_length=100, blank=True, null=True)
    geom = models.GeometryField(blank=True, null=True)
    codigofunai = models.CharField(max_length=100, blank=True, null=True)

    iri_metadata = models.CharField(max_length=1000, blank=True, null=True)
    iri_style = models.CharField(max_length=1000, blank=True, null=True)
    class Meta:
        managed = False
        db_table = 'lim_terra_indigena_a'


class LimTerraIndigenaP(FeatureModel):
    id_objeto = models.IntegerField(primary_key=True)
    nome = models.CharField(max_length=100, blank=True, null=True)
    nomeabrev = models.CharField(max_length=50, blank=True, null=True)
    geometriaaproximada = models.CharField(max_length=3, blank=True, null=True)
    perimetrooficial = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    areaoficialha = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    grupoetnico = models.CharField(max_length=100, blank=True, null=True)
    datasituacaojuridica = models.CharField(max_length=20, blank=True, null=True)
    situacaojuridica = models.CharField(max_length=23, blank=True, null=True)
    nometi = models.CharField(max_length=100, blank=True, null=True)
    geom = models.PointField(srid=4326, dim=4, blank=True, null=True)

    iri_metadata = models.CharField(max_length=1000, blank=True, null=True)
    iri_style = models.CharField(max_length=1000, blank=True, null=True)
    class Meta:
        managed = False
        db_table = 'lim_terra_indigena_p'


class UnidadeConservacaoNaoSnuc(FeatureModel):
    id_objeto = models.IntegerField(primary_key=True)
    nome = models.CharField(max_length=100, blank=True, null=True)
    nomeabrev = models.CharField(max_length=50, blank=True, null=True)
    geometriaaproximada = models.CharField(max_length=3, blank=True, null=True)
    anocriacao = models.FloatField(blank=True, null=True)
    sigla = models.CharField(max_length=6, blank=True, null=True)
    areaoficial = models.CharField(max_length=15, blank=True, null=True)
    administracao = models.CharField(max_length=18, blank=True, null=True)
    classificacao = models.CharField(max_length=100, blank=True, null=True)
    atolegal = models.CharField(max_length=100, blank=True, null=True)
    geom = models.GeometryField(blank=True, null=True)

    iri_metadata = models.CharField(max_length=1000, blank=True, null=True)
    iri_style = models.CharField(max_length=1000, blank=True, null=True)
    class Meta:
        managed = False
        db_table = 'lim_unidade_conservacao_nao_snuc_a'


class UnidadeFederacao(FeatureModel):
    contextclassname = 'unidades-federativas'
    id_objeto = models.IntegerField(primary_key=True)
    nome = models.CharField(max_length=100, blank=True, null=True)
    nomeabrev = models.CharField(max_length=50, blank=True, null=True)
    geometriaaproximada = models.CharField(max_length=3, blank=True, null=True)
    sigla = models.CharField(max_length=3, blank=True, null=True)
    geocodigo = models.CharField(max_length=15, blank=True, null=True)
    geom = models.GeometryField(blank=True, null=True)

    
    iri_metadata = models.CharField(max_length=1000, blank=True, null=True)
    iri_style = models.CharField(max_length=1000, blank=True, null=True)
    class Meta:
        managed = False
        db_table = 'lim_unidade_federacao_a'

class UnidadeProtecaoIntegral(FeatureModel):
    id_objeto = models.IntegerField(primary_key=True)
    nome = models.CharField(max_length=100, blank=True, null=True)
    nomeabrev = models.CharField(max_length=50, blank=True, null=True)
    geometriaaproximada = models.CharField(max_length=3, blank=True, null=True)
    anocriacao = models.FloatField(blank=True, null=True)
    sigla = models.CharField(max_length=6, blank=True, null=True)
    areaoficial = models.CharField(max_length=15, blank=True, null=True)
    administracao = models.CharField(max_length=18, blank=True, null=True)
    atolegal = models.CharField(max_length=100, blank=True, null=True)
    tipounidprotinteg = models.CharField(max_length=100, blank=True, null=True)
    geom = models.GeometryField(blank=True, null=True)

    iri_metadata = models.CharField(max_length=1000, blank=True, null=True)
    iri_style = models.CharField(max_length=1000, blank=True, null=True)
    class Meta:
        managed = False
        db_table = 'lim_unidade_protecao_integral_a'


class UnidadeUsoSustentavel(FeatureModel):
    id_objeto = models.AutoField(primary_key=True)
    nome = models.CharField(max_length=100, blank=True, null=True)
    nomeabrev = models.CharField(max_length=50, blank=True, null=True)
    geometriaaproximada = models.CharField(max_length=3, blank=True, null=True)
    anocriacao = models.FloatField(blank=True, null=True)
    sigla = models.CharField(max_length=6, blank=True, null=True)
    areaoficial = models.CharField(max_length=15, blank=True, null=True)
    administracao = models.CharField(max_length=18, blank=True, null=True)
    atolegal = models.CharField(max_length=100, blank=True, null=True)
    tipounidusosust = models.CharField(max_length=100, blank=True, null=True)
    geom = models.GeometryField(blank=True, null=True)

    iri_metadata = models.CharField(max_length=1000, blank=True, null=True)
    iri_style = models.CharField(max_length=1000, blank=True, null=True)
    class Meta:
        managed = False
        db_table = 'lim_unidade_uso_sustentavel_a'


class AglomeradoRuralDeExtensaoUrbana(FeatureModel):
    id_objeto = models.IntegerField(primary_key=True)
    nome = models.CharField(max_length=100, blank=True, null=True)
    nomeabrev = models.CharField(max_length=50, blank=True, null=True)
    geometriaaproximada = models.CharField(max_length=3, blank=True, null=True)
    geom = models.GeometryField(blank=True, null=True)

    iri_metadata = models.CharField(max_length=1000, blank=True, null=True)
    iri_style = models.CharField(max_length=1000, blank=True, null=True)
    class Meta:
        managed = False
        db_table = 'loc_aglomerado_rural_de_extensao_urbana_p'


class AglomeradoRuralIsolado(FeatureModel):
    id_objeto = models.IntegerField(primary_key=True)
    nome = models.CharField(max_length=100, blank=True, null=True)
    nomeabrev = models.CharField(max_length=50, blank=True, null=True)
    geometriaaproximada = models.CharField(max_length=3, blank=True, null=True)
    tipoaglomrurisol = models.CharField(max_length=35, blank=True, null=True)
    geom = models.PointField(srid=4326, dim=4, blank=True, null=True)

    iri_metadata = models.CharField(max_length=1000, blank=True, null=True)
    iri_style = models.CharField(max_length=1000, blank=True, null=True)
    class Meta:
        managed = False
        db_table = 'loc_aglomerado_rural_isolado_p'


class AldeiaIndigena(FeatureModel):
    id_objeto = models.AutoField(primary_key=True)
    nome = models.CharField(max_length=100, blank=True, null=True)
    nomeabrev = models.CharField(max_length=50, blank=True, null=True)
    geometriaaproximada = models.CharField(max_length=3, blank=True, null=True)
    codigofunai = models.CharField(max_length=15, blank=True, null=True)
    terraindigena = models.CharField(max_length=100, blank=True, null=True)
    etnia = models.CharField(max_length=100, blank=True, null=True)
    geom = models.PointField(blank=True, null=True)

    iri_metadata = models.CharField(max_length=1000, blank=True, null=True)
    iri_style = models.CharField(max_length=1000, blank=True, null=True)
    class Meta:
        managed = False
        db_table = 'loc_aldeia_indigena_p'


class AreaEdificada(FeatureModel):
    id_objeto = models.IntegerField(primary_key=True, db_column='id_objeto')
    nome = models.CharField(max_length=100, blank=True, null=True)
    nomeabrev = models.CharField(max_length=50, blank=True, null=True)
    geometriaaproximada = models.CharField(max_length=3, blank=True, null=True)
    geocodigo = models.CharField(max_length=15, blank=True, null=True)
    geom = models.GeometryField(blank=True, null=True)

    iri_metadata = models.CharField(max_length=1000, blank=True, null=True)
    iri_style = models.CharField(max_length=1000, blank=True, null=True)
    class Meta:
        managed = False
        db_table = 'loc_area_edificada_a'


class Capital(FeatureModel):
    id_objeto = models.IntegerField(primary_key=True, db_column='id_objeto')
    nome = models.CharField(max_length=100, blank=True, null=True)
    nomeabrev = models.CharField(max_length=50, blank=True, null=True)
    geometriaaproximada = models.CharField(max_length=3, blank=True, null=True)
    tipocapital = models.CharField(max_length=20, blank=True, null=True)
    geom = models.GeometryField(blank=True, null=True)

    iri_metadata = models.CharField(max_length=1000, blank=True, null=True)
    iri_style = models.CharField(max_length=1000, blank=True, null=True)
    class Meta:
        managed = False
        db_table = 'loc_capital_p'


class Cidade(FeatureModel):
    id_objeto = models.IntegerField(primary_key=True, db_column='id_objeto')
    nome = models.CharField(max_length=100, blank=True, null=True)
    nomeabrev = models.CharField(max_length=50, blank=True, null=True)
    geometriaaproximada = models.CharField(max_length=3, blank=True, null=True)
    geom = models.GeometryField(blank=True, null=True)

    iri_metadata = models.CharField(max_length=1000, blank=True, null=True)
    iri_style = models.CharField(max_length=1000, blank=True, null=True)
    class Meta:
        managed = False
        db_table = 'loc_cidade_p'


class Vila(FeatureModel):
    id_objeto = models.IntegerField(primary_key=True, db_column='id_objeto')
    nome = models.CharField(max_length=100, blank=True, null=True)
    nomeabrev = models.CharField(max_length=50, blank=True, null=True)
    geometriaaproximada = models.CharField(max_length=3, blank=True, null=True)
    geom = models.GeometryField(blank=True, null=True)

    iri_metadata = models.CharField(max_length=1000, blank=True, null=True)
    iri_style = models.CharField(max_length=1000, blank=True, null=True)
    class Meta:
        managed = False
        db_table = 'loc_vila_p'




class Orderpart(FeatureModel):
    order_id = models.IntegerField(blank=True, null=True)
    part_id = models.IntegerField(blank=True, null=True)
    quantity = models.IntegerField(blank=True, null=True)

    iri_metadata = models.CharField(max_length=1000, blank=True, null=True)
    iri_style = models.CharField(max_length=1000, blank=True, null=True)
    class Meta:
        managed = False
        db_table = 'orderpart'


class Part(FeatureModel):
    part_id = models.IntegerField(blank=True, null=True)
    name = models.CharField(max_length=30, blank=True, null=True)
    cost = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)
    weight = models.FloatField(blank=True, null=True)
    employee_id = models.IntegerField(blank=True, null=True)

    iri_metadata = models.CharField(max_length=1000, blank=True, null=True)
    iri_style = models.CharField(max_length=1000, blank=True, null=True)
    class Meta:
        managed = False
        db_table = 'part'



class CurvaBatimetrica(FeatureModel):
    id_objeto = models.IntegerField(primary_key=True)
    profundidade = models.IntegerField(blank=True, null=True)
    geom = models.GeometryField(blank=True, null=True)

    iri_metadata = models.CharField(max_length=1000, blank=True, null=True)
    iri_style = models.CharField(max_length=1000, blank=True, null=True)
    class Meta:
        managed = False
        db_table = 'rel_curva_batimetrica_l'


class CurvaNivel(FeatureModel):
    id_objeto = models.IntegerField(primary_key=True)
    cota = models.IntegerField(blank=True, null=True)
    depressao = models.CharField(max_length=3, blank=True, null=True)
    geometriaaproximada = models.CharField(max_length=3, blank=True, null=True)
    indice = models.CharField(max_length=16, blank=True, null=True)
    geom = models.GeometryField(blank=True, null=True)

    iri_metadata = models.CharField(max_length=1000, blank=True, null=True)
    iri_style = models.CharField(max_length=1000, blank=True, null=True)
    class Meta:
        managed = False
        db_table = 'rel_curva_nivel_l'


class Duna(FeatureModel):
    id_objeto = models.IntegerField(primary_key=True)
    nome = models.CharField(max_length=100, blank=True, null=True)
    nomeabrev = models.CharField(max_length=50, blank=True, null=True)
    geometriaaproximada = models.CharField(max_length=3, blank=True, null=True)
    fixa = models.CharField(max_length=3, blank=True, null=True)
    geom = models.GeometryField(blank=True, null=True)

    iri_metadata = models.CharField(max_length=1000, blank=True, null=True)
    iri_style = models.CharField(max_length=1000, blank=True, null=True)
    class Meta:
        managed = False
        db_table = 'rel_duna_a'


class ElementoFisiograficoNatural(FeatureModel):
    id_objeto = models.IntegerField(primary_key=True)
    nome = models.CharField(max_length=100, blank=True, null=True)
    nomeabrev = models.CharField(max_length=50, blank=True, null=True)
    geometriaaproximada = models.CharField(max_length=3, blank=True, null=True)
    tipoelemnat = models.CharField(max_length=12, blank=True, null=True)
    geom = models.GeometryField(blank=True, null=True)

    iri_metadata = models.CharField(max_length=1000, blank=True, null=True)
    iri_style = models.CharField(max_length=1000, blank=True, null=True)
    class Meta:
        managed = False
        db_table = 'rel_elemento_fisiografico_natural_l'


class ElementoFisiograficoNatural_P(FeatureModel):
    id_objeto = models.IntegerField(primary_key=True)
    nome = models.CharField(max_length=100, blank=True, null=True)
    nomeabrev = models.CharField(max_length=50, blank=True, null=True)
    geometriaaproximada = models.CharField(max_length=3, blank=True, null=True)
    tipoelemnat = models.CharField(max_length=12, blank=True, null=True)
    geom = models.GeometryField(blank=True, null=True)

    iri_metadata = models.CharField(max_length=1000, blank=True, null=True)
    iri_style = models.CharField(max_length=1000, blank=True, null=True)
    class Meta:
        managed = False
        db_table = 'rel_elemento_fisiografico_natural_p'


class Pico(FeatureModel):
    id_objeto = models.IntegerField(primary_key=True)
    nome = models.CharField(max_length=100, blank=True, null=True)
    nomeabrev = models.CharField(max_length=50, blank=True, null=True)
    geometriaaproximada = models.CharField(max_length=3, blank=True, null=True)
    geom = models.GeometryField(blank=True, null=True)

    iri_metadata = models.CharField(max_length=1000, blank=True, null=True)
    iri_style = models.CharField(max_length=1000, blank=True, null=True)
    class Meta:
        managed = False
        db_table = 'rel_pico_p'


class PontoCotadoAltimetrico(FeatureModel):
    id_objeto = models.IntegerField(primary_key=True)
    geometriaaproximada = models.CharField(max_length=3, blank=True, null=True)
    cota = models.FloatField(blank=True, null=True)
    cotacomprovada = models.CharField(max_length=3, blank=True, null=True)
    geom = models.GeometryField(blank=True, null=True)

    iri_metadata = models.CharField(max_length=1000, blank=True, null=True)
    iri_style = models.CharField(max_length=1000, blank=True, null=True)
    class Meta:
        managed = False
        db_table = 'rel_ponto_cotado_altimetrico_p'


class PontoCotadoBatimetrico(FeatureModel):
    id_objeto = models.IntegerField(primary_key=True)
    profundidade = models.FloatField(blank=True, null=True)
    geom = models.GeometryField(blank=True, null=True)

    iri_metadata = models.CharField(max_length=1000, blank=True, null=True)
    iri_style = models.CharField(max_length=1000, blank=True, null=True)
    class Meta:
        managed = False
        db_table = 'rel_ponto_cotado_batimetrico_p'




class Salesorder(FeatureModel):
    order_id = models.IntegerField(blank=True, null=True)
    customer_id = models.IntegerField(blank=True, null=True)
    employee_id = models.IntegerField(blank=True, null=True)
    order_date = models.DateField(blank=True, null=True)
    ship_date = models.DateField(blank=True, null=True)
    payment = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)

    iri_metadata = models.CharField(max_length=1000, blank=True, null=True)
    iri_style = models.CharField(max_length=1000, blank=True, null=True)
    class Meta:
        managed = False
        db_table = 'salesorder'


class Salesorder1(FeatureModel):
    order_id = models.IntegerField(blank=True, null=True)
    customer_oid = models.TextField(blank=True, null=True)  # This field type is a guess.
    employee_oid = models.TextField(blank=True, null=True)  # This field type is a guess.
    part_oid = models.TextField(blank=True, null=True)  # This field type is a guess.

    iri_metadata = models.CharField(max_length=1000, blank=True, null=True)
    iri_style = models.CharField(max_length=1000, blank=True, null=True)
    class Meta:
        managed = False
        db_table = 'salesorder1'


class TLogradouro(FeatureModel):
    cod_setor = models.BigIntegerField(blank=True, null=True)
    cod_situacao_setor = models.CharField(max_length=2, blank=True, null=True)
    cod_tipo_setor = models.CharField(max_length=2, blank=True, null=True)
    cod_especie = models.CharField(max_length=2, blank=True, null=True)
    nom_tipo_seglogr = models.CharField(max_length=20, blank=True, null=True)
    nom_titulo_seglogr = models.CharField(max_length=30, blank=True, null=True)
    nom_seglogr = models.CharField(max_length=60, blank=True, null=True)
    num_endereco = models.IntegerField(blank=True, null=True)
    dsc_modificador = models.CharField(max_length=7, blank=True, null=True)
    nom_comp_elem1 = models.CharField(max_length=20, blank=True, null=True)
    val_comp_elem1 = models.CharField(max_length=10, blank=True, null=True)
    nom_comp_elem2 = models.CharField(max_length=20, blank=True, null=True)
    val_comp_elem2 = models.CharField(max_length=10, blank=True, null=True)
    nom_comp_elem3 = models.CharField(max_length=20, blank=True, null=True)
    val_comp_elem3 = models.CharField(max_length=10, blank=True, null=True)
    nom_comp_elem4 = models.CharField(max_length=20, blank=True, null=True)
    val_comp_elem4 = models.CharField(max_length=10, blank=True, null=True)
    nom_comp_elem5 = models.CharField(max_length=20, blank=True, null=True)
    val_comp_elem5 = models.CharField(max_length=10, blank=True, null=True)
    nom_comp_elem6 = models.CharField(max_length=20, blank=True, null=True)
    val_comp_elem6 = models.CharField(max_length=10, blank=True, null=True)
    dsc_ponto_referencia = models.CharField(max_length=60, blank=True, null=True)
    dsc_localidade = models.CharField(max_length=60, blank=True, null=True)
    cep_face = models.CharField(max_length=8, blank=True, null=True)
    val_latitude_padrao = models.CharField(max_length=15, blank=True, null=True)
    val_longitude_padrao = models.CharField(max_length=15, blank=True, null=True)
    dsc_estabelecimento = models.CharField(max_length=40, blank=True, null=True)
    cod_indicador_estab_endereco = models.CharField(max_length=1, blank=True, null=True)
    cod_indicador_const_endereco = models.CharField(max_length=1, blank=True, null=True)
    cod_indicador_finalidade_const = models.CharField(max_length=1, blank=True, null=True)
    cod_indicador_const_endereco2 = models.CharField(max_length=1, blank=True, null=True)

    iri_metadata = models.CharField(max_length=1000, blank=True, null=True)
    iri_style = models.CharField(max_length=1000, blank=True, null=True)
    class Meta:
        managed = False
        db_table = 't_logradouro'



class Eclusa(FeatureModel):
    id_objeto = models.IntegerField(primary_key=True)
    nome = models.CharField(max_length=100, blank=True, null=True)
    nomeabrev = models.CharField(max_length=50, blank=True, null=True)
    geometriaaproximada = models.CharField(max_length=3, blank=True, null=True)
    desnivel = models.FloatField(blank=True, null=True)
    largura = models.FloatField(blank=True, null=True)
    extensao = models.FloatField(blank=True, null=True)
    calado = models.FloatField(blank=True, null=True)
    matconstr = models.CharField(max_length=18, blank=True, null=True)
    operacional = models.CharField(max_length=12, blank=True, null=True)
    situacaofisica = models.TextField(blank=True, null=True)
    geom = models.GeometryField(blank=True, null=True)

    iri_metadata = models.CharField(max_length=1000, blank=True, null=True)
    iri_style = models.CharField(max_length=1000, blank=True, null=True)
    class Meta:
        managed = False
        db_table = 'tra_eclusa_l'


class EdifConstPortuaria(FeatureModel):
    id_objeto = models.IntegerField(primary_key=True)
    nome = models.CharField(max_length=100, blank=True, null=True)
    nomeabrev = models.CharField(max_length=50, blank=True, null=True)
    geometriaaproximada = models.CharField(max_length=3, blank=True, null=True)
    tipoedifport = models.CharField(max_length=23, blank=True, null=True)
    administracao = models.TextField(blank=True, null=True)
    matconstr = models.CharField(max_length=18, blank=True, null=True)
    operacional = models.CharField(max_length=12, blank=True, null=True)
    situacaofisica = models.TextField(blank=True, null=True)
    geom = models.GeometryField(blank=True, null=True)

    iri_metadata = models.CharField(max_length=1000, blank=True, null=True)
    iri_style = models.CharField(max_length=1000, blank=True, null=True)
    class Meta:
        managed = False
        db_table = 'tra_edif_const_portuaria_p'


class EdifConstrAeroportuaria(FeatureModel):
    id_objeto = models.IntegerField(primary_key=True)
    nome = models.CharField(max_length=100, blank=True, null=True)
    nomeabrev = models.CharField(max_length=50, blank=True, null=True)
    geometriaaproximada = models.CharField(max_length=3, blank=True, null=True)
    operacional = models.CharField(max_length=12, blank=True, null=True)
    situacaofisica = models.TextField(blank=True, null=True)
    administracao = models.TextField(blank=True, null=True)
    matconstr = models.CharField(max_length=18, blank=True, null=True)
    tipoedifaero = models.CharField(max_length=23, blank=True, null=True)
    geom = models.GeometryField(blank=True, null=True)

    iri_metadata = models.CharField(max_length=1000, blank=True, null=True)
    iri_style = models.CharField(max_length=1000, blank=True, null=True)
    class Meta:
        managed = False
        db_table = 'tra_edif_constr_aeroportuaria_p'


class EdifMetroFerroviaria(FeatureModel):
    id_objeto = models.IntegerField(primary_key=True)
    nome = models.CharField(max_length=100, blank=True, null=True)
    nomeabrev = models.CharField(max_length=50, blank=True, null=True)
    geometriaaproximada = models.CharField(max_length=3, blank=True, null=True)
    multimodal = models.CharField(max_length=12, blank=True, null=True)
    funcaoedifmetroferrov = models.CharField(max_length=44, blank=True, null=True)
    operacional = models.CharField(max_length=12, blank=True, null=True)
    situacaofisica = models.TextField(blank=True, null=True)
    administracao = models.TextField(blank=True, null=True)
    matconstr = models.CharField(max_length=18, blank=True, null=True)
    geom = models.GeometryField(blank=True, null=True)

    iri_metadata = models.CharField(max_length=1000, blank=True, null=True)
    iri_style = models.CharField(max_length=1000, blank=True, null=True)
    class Meta:
        managed = False
        db_table = 'tra_edif_metro_ferroviaria_p'


class Fundeadouro(FeatureModel):
    id_objeto = models.IntegerField(primary_key=True)
    nome = models.CharField(max_length=100, blank=True, null=True)
    nomeabrev = models.CharField(max_length=50, blank=True, null=True)
    geometriaaproximada = models.CharField(max_length=3, blank=True, null=True)
    administracao = models.TextField(blank=True, null=True)
    destinacaofundeadouro = models.CharField(max_length=43, blank=True, null=True)
    geom = models.GeometryField(blank=True, null=True)

    iri_metadata = models.CharField(max_length=1000, blank=True, null=True)
    iri_style = models.CharField(max_length=1000, blank=True, null=True)
    class Meta:
        managed = False
        db_table = 'tra_fundeadouro_p'


class PistaPontoPouso(FeatureModel):
    id_objeto = models.IntegerField(primary_key=True)
    nome = models.CharField(max_length=100, blank=True, null=True)
    geometriaaproximada = models.CharField(max_length=3, blank=True, null=True)
    nomeabrev = models.CharField(max_length=50, blank=True, null=True)
    largura = models.FloatField(blank=True, null=True)
    extensao = models.FloatField(blank=True, null=True)
    operacional = models.CharField(max_length=12, blank=True, null=True)
    situacaofisica = models.TextField(blank=True, null=True)
    homologacao = models.CharField(max_length=12, blank=True, null=True)
    tipopista = models.CharField(max_length=14, blank=True, null=True)
    usopista = models.CharField(max_length=15, blank=True, null=True)
    revestimento = models.TextField(blank=True, null=True)
    geom = models.GeometryField(blank=True, null=True)

    iri_metadata = models.CharField(max_length=1000, blank=True, null=True)
    iri_style = models.CharField(max_length=1000, blank=True, null=True)
    class Meta:
        managed = False
        db_table = 'tra_pista_ponto_pouso_p'


class Ponte(FeatureModel):
    id_objeto = models.IntegerField(primary_key=True)
    nome = models.CharField(max_length=100, blank=True, null=True)
    geometriaaproximada = models.CharField(max_length=3, blank=True, null=True)
    nomeabrev = models.CharField(max_length=50, blank=True, null=True)
    tipoponte = models.CharField(max_length=12, blank=True, null=True)
    modaluso = models.CharField(max_length=15, blank=True, null=True)
    situacaofisica = models.TextField(blank=True, null=True)
    operacional = models.CharField(max_length=12, blank=True, null=True)
    matconstr = models.CharField(max_length=18, blank=True, null=True)
    vaolivrehoriz = models.FloatField(blank=True, null=True)
    vaovertical = models.FloatField(blank=True, null=True)
    cargasuportmaxima = models.FloatField(blank=True, null=True)
    nrpistas = models.IntegerField(blank=True, null=True)
    nrfaixas = models.IntegerField(blank=True, null=True)
    extensao = models.FloatField(blank=True, null=True)
    largura = models.FloatField(blank=True, null=True)
    posicaopista = models.CharField(max_length=13, blank=True, null=True)
    geom = models.GeometryField(blank=True, null=True)

    iri_metadata = models.CharField(max_length=1000, blank=True, null=True)
    iri_style = models.CharField(max_length=1000, blank=True, null=True)
    class Meta:
        managed = False
        db_table = 'tra_ponte_l'


class Sinalizacao(FeatureModel):
    id_objeto = models.IntegerField(primary_key=True)
    nome = models.CharField(max_length=100, blank=True, null=True)
    nomeabrev = models.CharField(max_length=50, blank=True, null=True)
    geometriaaproximada = models.CharField(max_length=3, blank=True, null=True)
    operacional = models.CharField(max_length=12, blank=True, null=True)
    situacaofisica = models.TextField(blank=True, null=True)
    tiposinal = models.CharField(max_length=21, blank=True, null=True)
    geom = models.GeometryField(blank=True, null=True)

    iri_metadata = models.CharField(max_length=1000, blank=True, null=True)
    iri_style = models.CharField(max_length=1000, blank=True, null=True)
    class Meta:
        managed = False
        db_table = 'tra_sinalizacao_p'


class Travessia(FeatureModel):
    id_objeto = models.IntegerField(primary_key=True)
    nome = models.CharField(max_length=100, blank=True, null=True)
    geometriaaproximada = models.CharField(max_length=3, blank=True, null=True)
    nomeabrev = models.CharField(max_length=50, blank=True, null=True)
    tipotravessia = models.CharField(max_length=18, blank=True, null=True)
    geom = models.GeometryField(blank=True, null=True)

    iri_metadata = models.CharField(max_length=1000, blank=True, null=True)
    iri_style = models.CharField(max_length=1000, blank=True, null=True)
    class Meta:
        managed = False
        db_table = 'tra_travessia_l'


class Travessia_P(FeatureModel):
    id_objeto = models.IntegerField(primary_key=True)
    nome = models.CharField(max_length=100, blank=True, null=True)
    geometriaaproximada = models.CharField(max_length=3, blank=True, null=True)
    nomeabrev = models.CharField(max_length=50, blank=True, null=True)
    tipotravessia = models.CharField(max_length=18, blank=True, null=True)
    geom = models.GeometryField(blank=True, null=True)

    iri_metadata = models.CharField(max_length=1000, blank=True, null=True)
    iri_style = models.CharField(max_length=1000, blank=True, null=True)
    class Meta:
        managed = False
        db_table = 'tra_travessia_p'


class TrechoDuto(FeatureModel):
    id_objeto = models.IntegerField(primary_key=True)
    nome = models.CharField(max_length=100, blank=True, null=True)
    nomeabrev = models.CharField(max_length=50, blank=True, null=True)
    geometriaaproximada = models.CharField(max_length=3, blank=True, null=True)
    nrdutos = models.IntegerField(blank=True, null=True)
    tipotrechoduto = models.CharField(max_length=22, blank=True, null=True)
    mattransp = models.CharField(max_length=12, blank=True, null=True)
    setor = models.CharField(max_length=21, blank=True, null=True)
    posicaorelativa = models.CharField(max_length=15, blank=True, null=True)
    matconstr = models.CharField(max_length=18, blank=True, null=True)
    situacaoespacial = models.CharField(max_length=11, blank=True, null=True)
    operacional = models.CharField(max_length=12, blank=True, null=True)
    situacaofisica = models.TextField(blank=True, null=True)
    geom = models.GeometryField(blank=True, null=True)

    iri_metadata = models.CharField(max_length=1000, blank=True, null=True)
    iri_style = models.CharField(max_length=1000, blank=True, null=True)
    class Meta:
        managed = False
        db_table = 'tra_trecho_duto_l'


class TrechoFerroviario(FeatureModel):
    id_objeto = models.IntegerField(primary_key=True)
    nome = models.CharField(max_length=100, blank=True, null=True)
    nomeabrev = models.CharField(max_length=50, blank=True, null=True)
    geometriaaproximada = models.CharField(max_length=3, blank=True, null=True)
    codtrechoferrov = models.CharField(max_length=25, blank=True, null=True)
    posicaorelativa = models.CharField(max_length=15, blank=True, null=True)
    tipotrechoferrov = models.CharField(max_length=12, blank=True, null=True)
    bitola = models.CharField(max_length=27, blank=True, null=True)
    eletrificada = models.CharField(max_length=12, blank=True, null=True)
    nrlinhas = models.CharField(max_length=12, blank=True, null=True)
    emarruamento = models.CharField(max_length=12, blank=True, null=True)
    jurisdicao = models.TextField(blank=True, null=True)
    administracao = models.TextField(blank=True, null=True)
    concessionaria = models.CharField(max_length=100, blank=True, null=True)
    operacional = models.CharField(max_length=12, blank=True, null=True)
    cargasuportmaxima = models.FloatField(blank=True, null=True)
    situacaofisica = models.TextField(blank=True, null=True)
    geom = models.GeometryField(blank=True, null=True)

    iri_metadata = models.CharField(max_length=1000, blank=True, null=True)
    iri_style = models.CharField(max_length=1000, blank=True, null=True)
    class Meta:
        managed = False
        db_table = 'tra_trecho_ferroviario_l'


class TrechoHidroviario(FeatureModel):
    id_objeto = models.IntegerField(primary_key=True)
    nome = models.CharField(max_length=100, blank=True, null=True)
    nomeabrev = models.CharField(max_length=50, blank=True, null=True)
    geometriaaproximada = models.CharField(max_length=3, blank=True, null=True)
    extensaotrecho = models.FloatField(blank=True, null=True)
    caladomaxseca = models.FloatField(blank=True, null=True)
    operacional = models.CharField(max_length=12, blank=True, null=True)
    situacaofisica = models.TextField(blank=True, null=True)
    regime = models.CharField(max_length=31, blank=True, null=True)
    geom = models.GeometryField(blank=True, null=True)

    iri_metadata = models.CharField(max_length=1000, blank=True, null=True)
    iri_style = models.CharField(max_length=1000, blank=True, null=True)
    class Meta:
        managed = False
        db_table = 'tra_trecho_hidroviario_l'


class TrechoRodoviario(FeatureModel):
    id_objeto = models.IntegerField(primary_key=True)
    codtrechorodov = models.CharField(max_length=25, blank=True, null=True)
    tipotrechorod = models.TextField(blank=True, null=True)
    jurisdicao = models.TextField(blank=True, null=True)
    administracao = models.TextField(blank=True, null=True)
    concessionaria = models.CharField(max_length=100, blank=True, null=True)
    revestimento = models.TextField(blank=True, null=True)
    operacional = models.CharField(max_length=12, blank=True, null=True)
    situacaofisica = models.TextField(blank=True, null=True)
    nrpistas = models.IntegerField(blank=True, null=True)
    nrfaixas = models.IntegerField(blank=True, null=True)
    trafego = models.TextField(blank=True, null=True)
    canteirodivisorio = models.CharField(max_length=4, blank=True, null=True)
    capaccarga = models.DecimalField(max_digits=19, decimal_places=6, blank=True, null=True)
    geom = models.GeometryField(blank=True, null=True)

    iri_metadata = models.CharField(max_length=1000, blank=True, null=True)
    iri_style = models.CharField(max_length=1000, blank=True, null=True)
    class Meta:
        managed = False
        db_table = 'tra_trecho_rodoviario_l'


class Tunel(FeatureModel):
    id_objeto = models.IntegerField(primary_key=True)
    nome = models.CharField(max_length=100, blank=True, null=True)
    geometriaaproximada = models.CharField(max_length=3, blank=True, null=True)
    nomeabrev = models.CharField(max_length=50, blank=True, null=True)
    modaluso = models.CharField(max_length=15, blank=True, null=True)
    nrpistas = models.IntegerField(blank=True, null=True)
    nrfaixas = models.IntegerField(blank=True, null=True)
    extensao = models.FloatField(blank=True, null=True)
    altura = models.FloatField(blank=True, null=True)
    largura = models.FloatField(blank=True, null=True)
    posicaopista = models.CharField(max_length=13, blank=True, null=True)
    situacaofisica = models.TextField(blank=True, null=True)
    operacional = models.CharField(max_length=12, blank=True, null=True)
    matconstr = models.CharField(max_length=18, blank=True, null=True)
    tipotunel = models.CharField(max_length=28, blank=True, null=True)
    geom = models.GeometryField(blank=True, null=True)

    iri_metadata = models.CharField(max_length=1000, blank=True, null=True)
    iri_style = models.CharField(max_length=1000, blank=True, null=True)
    class Meta:
        managed = False
        db_table = 'tra_tunel_l'



class BrejoPantano(FeatureModel):

    id_objeto = models.IntegerField(primary_key=True)
    nome = models.CharField(max_length=100, blank=True, null=True)
    nomeabrev = models.CharField(max_length=50, blank=True, null=True)
    geometriaaproximada = models.CharField(max_length=3, blank=True, null=True)
    alturamediaindividuos = models.FloatField(blank=True, null=True)
    classificacaoporte = models.CharField(max_length=12, blank=True, null=True)
    tipobrejopantano = models.CharField(max_length=27, blank=True, null=True)
    denso = models.CharField(max_length=12, blank=True, null=True)
    antropizada = models.CharField(max_length=23, blank=True, null=True)
    geom = models.GeometryField(blank=True, null=True)

    iri_metadata = models.CharField(max_length=1000, blank=True, null=True)
    iri_style = models.CharField(max_length=1000, blank=True, null=True)
    class Meta:
        managed = False
        db_table = 'veg_brejo_pantano_a'


class Mangue(FeatureModel):
    id_objeto = models.IntegerField(primary_key=True)
    nome = models.CharField(max_length=100, blank=True, null=True)
    nomeabrev = models.CharField(max_length=50, blank=True, null=True)
    geometriaaproximada = models.CharField(max_length=3, blank=True, null=True)
    alturamediaindividuos = models.FloatField(blank=True, null=True)
    classificacaoporte = models.CharField(max_length=12, blank=True, null=True)
    denso = models.CharField(max_length=12, blank=True, null=True)
    antropizada = models.CharField(max_length=23, blank=True, null=True)
    geom = models.GeometryField(blank=True, null=True)

    iri_metadata = models.CharField(max_length=1000, blank=True, null=True)
    iri_style = models.CharField(max_length=1000, blank=True, null=True)
    class Meta:
        managed = False
        db_table = 'veg_mangue_a'


class VegRestinga(FeatureModel):
    id_objeto = models.IntegerField(primary_key=True)
    nome = models.CharField(max_length=100, blank=True, null=True)
    nomeabrev = models.CharField(max_length=50, blank=True, null=True)
    geometriaaproximada = models.CharField(max_length=3, blank=True, null=True)
    alturamediaindividuos = models.FloatField(blank=True, null=True)
    classificacaoporte = models.CharField(max_length=12, blank=True, null=True)
    denso = models.CharField(max_length=12, blank=True, null=True)
    antropizada = models.CharField(max_length=23, blank=True, null=True)
    geom = models.GeometryField(blank=True, null=True)

    iri_metadata = models.CharField(max_length=1000, blank=True, null=True)
    iri_style = models.CharField(max_length=1000, blank=True, null=True)
    class Meta:
        managed = False
        db_table = 'veg_veg_restinga_a'




class Vegetable(FeatureModel):
    animal_id = models.IntegerField(blank=True, null=True)
    name = models.CharField(max_length=20, blank=True, null=True)

    iri_metadata = models.CharField(max_length=1000, blank=True, null=True)
    iri_style = models.CharField(max_length=1000, blank=True, null=True)
    class Meta:
        managed = False
        db_table = 'vegetable'


class PontosExibicaoWgs84(FeatureModel):
    id_gps = models.IntegerField(primary_key=True)
    long_decimal = models.FloatField(blank=True, null=True)
    lat_decimal = models.FloatField(blank=True, null=True)
    sistema_geodesico = models.TextField(blank=True, null=True)
    geom = models.PointField(blank=True, null=True)

    iri_metadata = models.CharField(max_length=1000, blank=True, null=True)
    iri_style = models.CharField(max_length=1000, blank=True, null=True)
    class Meta:
        managed = False
        db_table = 'pontos_exibicao_wgs84'

class BlocoR9(FeatureModel):
    gid = models.AutoField(primary_key=True)
    nomenclatu = models.CharField(max_length=50, blank=True, null=True)
    situacao_b = models.CharField(max_length=1, blank=True, null=True)
    indice_blo = models.IntegerField(blank=True, null=True)
    nome_bacia = models.CharField(max_length=50, blank=True, null=True)
    nome_setor = models.CharField(max_length=50, blank=True, null=True)
    id4 = models.IntegerField(blank=True, null=True)
    area_bloco = models.FloatField(blank=True, null=True)
    geom = models.MultiPolygonField(blank=True, null=True)

    iri_metadata = models.CharField(max_length=1000, blank=True, null=True)
    iri_style = models.CharField(max_length=1000, blank=True, null=True)
    class Meta:
        managed = False
        db_table = 'bloco_r9'

class ModeloTeste(FeatureModel):
    data = models.DateField(blank=True, null=True)
    sigla = models.CharField(max_length=2, blank=True, null=True)
    contador = models.IntegerField(blank=True, null=True)
    geom = models.GeometryField(srid=0, blank=True, null=True)
    id_modelo_teste = models.IntegerField(primary_key=True)
    tempo = models.TimeField(blank=True, null=True)
    data_hora = models.DateTimeField(blank=True, null=True)
    valor = models.FloatField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'modelo_teste'