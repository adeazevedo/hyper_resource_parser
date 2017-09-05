from __future__ import unicode_literals
from hyper_resource.models import FeatureModel, BusinessModel
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

from hyper_resource.models import FeatureModel, BusinessModel


class EdifPubMilitar(BusinessModel):
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


class PostoFiscal(BusinessModel):
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






class EdifAgropecExtVegetalPesca(BusinessModel):
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


class EdifIndustrial(BusinessModel):
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


class ExtMineral_A(BusinessModel):
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


class ExtMineral(BusinessModel):
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


class EdifReligiosa(BusinessModel):
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




class Employee(BusinessModel):
    employee_id = models.IntegerField(blank=True, null=True)
    name = models.CharField(max_length=30, blank=True, null=True)
    hire_date = models.DateField(blank=True, null=True)

    iri_metadata = models.CharField(max_length=1000, blank=True, null=True)
    iri_style = models.CharField(max_length=1000, blank=True, null=True)
    class Meta:
        managed = False
        db_table = 'employee'



class EstGeradEnergiaEletrica(BusinessModel):
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


class Hidreletrica(BusinessModel):
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


class Termeletrica(BusinessModel):
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


class TorreEnergia(BusinessModel):
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



class BancoAreia(BusinessModel):
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


class Barragem(BusinessModel):
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


class Corredeira(BusinessModel):
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


class Corredeira_P(BusinessModel):
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


class FozMaritima(BusinessModel):
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


class Ilha(BusinessModel):
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


class MassaDagua(BusinessModel):
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


class QuedaDagua(BusinessModel):
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


class QuedaDagua_P(BusinessModel):
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


class Recife(BusinessModel):
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


class Recife_P(BusinessModel):
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


class RochaEmAgua(BusinessModel):
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


class RochaEmAgua_P(BusinessModel):
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


class SumidouroVertedouro(BusinessModel):
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


class TerrenoSujeitoInundacao(BusinessModel):
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


class TrechoDrenagem(BusinessModel):
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


class TrechoMassaDagua(BusinessModel):
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



class AreaDesenvolvimentoControle(BusinessModel):
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


class MarcoDeLimite(BusinessModel):
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


class OutrasUnidProtegidas(BusinessModel):
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
    geom = models.MultiPolygonField(srid=4674, dim=4, blank=True, null=True)

    iri_metadata = models.CharField(max_length=1000, blank=True, null=True)
    iri_style = models.CharField(max_length=1000, blank=True, null=True)
    class Meta:
        managed = False
        db_table = 'lim_outras_unid_protegidas_a'


class OutrosLimitesOficiais(BusinessModel):
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


class Pais(BusinessModel):
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


class TerraIndigena(BusinessModel):
    gid = models.AutoField(primary_key=True)
    nome = models.CharField(max_length=100, blank=True, null=True)
    nomeabrev = models.CharField(max_length=50, blank=True, null=True)
    geometriaa = models.CharField(max_length=3, blank=True, null=True)
    perimetroo = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    areaoficia = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    grupoetnic = models.CharField(max_length=100, blank=True, null=True)
    datasituac = models.CharField(max_length=20, blank=True, null=True)
    situacaoju = models.CharField(max_length=23, blank=True, null=True)
    nometi = models.CharField(max_length=100, blank=True, null=True)
    geom = models.MultiPolygonField(srid=4674, dim=4, blank=True, null=True)

    iri_metadata = models.CharField(max_length=1000, blank=True, null=True)
    iri_style = models.CharField(max_length=1000, blank=True, null=True)
    class Meta:
        managed = False
        db_table = 'lim_terra_indigena_a'


class LimTerraIndigenaP(BusinessModel):
    gid = models.AutoField(primary_key=True)
    nome = models.CharField(max_length=100, blank=True, null=True)
    nomeabrev = models.CharField(max_length=50, blank=True, null=True)
    geometriaa = models.CharField(max_length=3, blank=True, null=True)
    perimetroo = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    areaoficia = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    grupoetnic = models.CharField(max_length=100, blank=True, null=True)
    datasituac = models.CharField(max_length=20, blank=True, null=True)
    situacaoju = models.CharField(max_length=23, blank=True, null=True)
    nometi = models.CharField(max_length=100, blank=True, null=True)
    geom = models.PointField(srid=4674, dim=4, blank=True, null=True)

    iri_metadata = models.CharField(max_length=1000, blank=True, null=True)
    iri_style = models.CharField(max_length=1000, blank=True, null=True)
    class Meta:
        managed = False
        db_table = 'lim_terra_indigena_p'


class UnidadeConservacaoNaoSnuc(BusinessModel):
    gid = models.AutoField(primary_key=True)
    nome = models.CharField(max_length=100, blank=True, null=True)
    nomeabrev = models.CharField(max_length=50, blank=True, null=True)
    geometriaa = models.CharField(max_length=3, blank=True, null=True)
    anocriacao = models.FloatField(blank=True, null=True)
    sigla = models.CharField(max_length=6, blank=True, null=True)
    areaoficia = models.CharField(max_length=15, blank=True, null=True)
    administra = models.CharField(max_length=18, blank=True, null=True)
    classifica = models.CharField(max_length=100, blank=True, null=True)
    atolegal = models.CharField(max_length=100, blank=True, null=True)
    geom = models.MultiPolygonField(srid=4674, dim=4, blank=True, null=True)

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

class UnidadeProtecaoIntegral(BusinessModel):
    gid = models.AutoField(primary_key=True)
    nome = models.CharField(max_length=100, blank=True, null=True)
    nomeabrev = models.CharField(max_length=50, blank=True, null=True)
    geometriaa = models.CharField(max_length=3, blank=True, null=True)
    anocriacao = models.FloatField(blank=True, null=True)
    sigla = models.CharField(max_length=6, blank=True, null=True)
    areaoficia = models.CharField(max_length=15, blank=True, null=True)
    administra = models.CharField(max_length=18, blank=True, null=True)
    atolegal = models.CharField(max_length=100, blank=True, null=True)
    tipounidpr = models.CharField(max_length=100, blank=True, null=True)
    geom = models.MultiPolygonField(srid=4674, dim=4, blank=True, null=True)

    iri_metadata = models.CharField(max_length=1000, blank=True, null=True)
    iri_style = models.CharField(max_length=1000, blank=True, null=True)
    class Meta:
        managed = False
        db_table = 'lim_unidade_protecao_integral_a'


class UnidadeUsoSustentavel(BusinessModel):
    gid = models.AutoField(primary_key=True)
    nome = models.CharField(max_length=100, blank=True, null=True)
    nomeabrev = models.CharField(max_length=50, blank=True, null=True)
    geometriaa = models.CharField(max_length=3, blank=True, null=True)
    anocriacao = models.FloatField(blank=True, null=True)
    sigla = models.CharField(max_length=6, blank=True, null=True)
    areaoficia = models.CharField(max_length=15, blank=True, null=True)
    administra = models.CharField(max_length=18, blank=True, null=True)
    atolegal = models.CharField(max_length=100, blank=True, null=True)
    tipounidus = models.CharField(max_length=100, blank=True, null=True)
    geom = models.MultiPolygonField(srid=4674, dim=4, blank=True, null=True)

    iri_metadata = models.CharField(max_length=1000, blank=True, null=True)
    iri_style = models.CharField(max_length=1000, blank=True, null=True)
    class Meta:
        managed = False
        db_table = 'lim_unidade_uso_sustentavel_a'


class AglomeradoRuralDeExtensaoUrbana(BusinessModel):
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


class AglomeradoRuralIsolado(BusinessModel):
    gid = models.AutoField(primary_key=True, db_column='id_objeto')
    nome = models.CharField(max_length=100, blank=True, null=True)
    nomeabrev = models.CharField(max_length=50, blank=True, null=True)
    geometriaa = models.CharField(max_length=3, blank=True, null=True)
    tipoaglomr = models.CharField(max_length=35, blank=True, null=True)
    geom = models.PointField(srid=4674, dim=4, blank=True, null=True)

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


class AreaEdificada(BusinessModel):
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


class Capital(BusinessModel):
    gid = models.AutoField(primary_key=True)
    nome = models.CharField(max_length=100, blank=True, null=True)
    nomeabrev = models.CharField(max_length=50, blank=True, null=True)
    geometriaa = models.CharField(max_length=3, blank=True, null=True)
    tipocapita = models.CharField(max_length=20, blank=True, null=True)
    geom = models.GeometryField(blank=True, null=True)

    iri_metadata = models.CharField(max_length=1000, blank=True, null=True)
    iri_style = models.CharField(max_length=1000, blank=True, null=True)
    class Meta:
        managed = False
        db_table = 'loc_capital_p'


class Cidade(BusinessModel):
    gid = models.AutoField(primary_key=True)
    nome = models.CharField(max_length=100, blank=True, null=True)
    nomeabrev = models.CharField(max_length=50, blank=True, null=True)
    geometriaa = models.CharField(max_length=3, blank=True, null=True)
    geom = models.GeometryField(blank=True, null=True)

    iri_metadata = models.CharField(max_length=1000, blank=True, null=True)
    iri_style = models.CharField(max_length=1000, blank=True, null=True)
    class Meta:
        managed = False
        db_table = 'loc_cidade_p'


class Vila(BusinessModel):
    gid = models.AutoField(primary_key=True)
    nome = models.CharField(max_length=100, blank=True, null=True)
    nomeabrev = models.CharField(max_length=50, blank=True, null=True)
    geometriaa = models.CharField(max_length=3, blank=True, null=True)
    geom = models.GeometryField(blank=True, null=True)

    iri_metadata = models.CharField(max_length=1000, blank=True, null=True)
    iri_style = models.CharField(max_length=1000, blank=True, null=True)
    class Meta:
        managed = False
        db_table = 'loc_vila_p'




class Orderpart(BusinessModel):
    order_id = models.IntegerField(blank=True, null=True)
    part_id = models.IntegerField(blank=True, null=True)
    quantity = models.IntegerField(blank=True, null=True)

    iri_metadata = models.CharField(max_length=1000, blank=True, null=True)
    iri_style = models.CharField(max_length=1000, blank=True, null=True)
    class Meta:
        managed = False
        db_table = 'orderpart'


class Part(BusinessModel):
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



class CurvaBatimetrica(BusinessModel):
    id_objeto = models.IntegerField(primary_key=True)
    profundidade = models.IntegerField(blank=True, null=True)
    geom = models.GeometryField(blank=True, null=True)

    iri_metadata = models.CharField(max_length=1000, blank=True, null=True)
    iri_style = models.CharField(max_length=1000, blank=True, null=True)
    class Meta:
        managed = False
        db_table = 'rel_curva_batimetrica_l'


class CurvaNivel(BusinessModel):
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


class Duna(BusinessModel):
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


class ElementoFisiograficoNatural(BusinessModel):
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


class ElementoFisiograficoNatural_P(BusinessModel):
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


class Pico(BusinessModel):
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


class PontoCotadoAltimetrico(BusinessModel):
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


class PontoCotadoBatimetrico(BusinessModel):
    id_objeto = models.IntegerField(primary_key=True)
    profundidade = models.FloatField(blank=True, null=True)
    geom = models.GeometryField(blank=True, null=True)

    iri_metadata = models.CharField(max_length=1000, blank=True, null=True)
    iri_style = models.CharField(max_length=1000, blank=True, null=True)
    class Meta:
        managed = False
        db_table = 'rel_ponto_cotado_batimetrico_p'




class Salesorder(BusinessModel):
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


class Salesorder1(BusinessModel):
    order_id = models.IntegerField(blank=True, null=True)
    customer_oid = models.TextField(blank=True, null=True)  # This field type is a guess.
    employee_oid = models.TextField(blank=True, null=True)  # This field type is a guess.
    part_oid = models.TextField(blank=True, null=True)  # This field type is a guess.

    iri_metadata = models.CharField(max_length=1000, blank=True, null=True)
    iri_style = models.CharField(max_length=1000, blank=True, null=True)
    class Meta:
        managed = False
        db_table = 'salesorder1'


class TLogradouro(BusinessModel):
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



class Eclusa(BusinessModel):
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


class EdifConstPortuaria(BusinessModel):
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


class EdifConstrAeroportuaria(BusinessModel):
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


class EdifMetroFerroviaria(BusinessModel):
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


class Fundeadouro(BusinessModel):
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


class PistaPontoPouso(BusinessModel):
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


class Ponte(BusinessModel):
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


class Sinalizacao(BusinessModel):
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


class Travessia(BusinessModel):
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


class Travessia_P(BusinessModel):
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


class TrechoDuto(BusinessModel):
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


class TrechoFerroviario(BusinessModel):
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


class TrechoHidroviario(BusinessModel):
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


class TrechoRodoviario(BusinessModel):
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


class Tunel(BusinessModel):
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



class BrejoPantano(BusinessModel):

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


class Mangue(BusinessModel):
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


class VegRestinga(BusinessModel):
    id = models.IntegerField(primary_key=True, db_column='id_objeto')
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




class Vegetable(BusinessModel):
    animal_id = models.IntegerField(blank=True, null=True)
    name = models.CharField(max_length=20, blank=True, null=True)

    iri_metadata = models.CharField(max_length=1000, blank=True, null=True)
    iri_style = models.CharField(max_length=1000, blank=True, null=True)
    class Meta:
        managed = False
        db_table = 'vegetable'


class PontosExibicaoWgs84(BusinessModel):
    id_gps = models.IntegerField(primary_key=True)
    long_decimal = models.FloatField(blank=True, null=True)
    lat_decimal = models.FloatField(blank=True, null=True)
    sistema_geodesico = models.TextField(blank=True, null=True)
    geom = models.PointField(blank=True, null=True)
    objects = models.GeoManager()

    iri_metadata = models.CharField(max_length=1000, blank=True, null=True)
    iri_style = models.CharField(max_length=1000, blank=True, null=True)
    class Meta:
        managed = False
        db_table = 'pontos_exibicao_wgs84'

class BlocoR9(BusinessModel):
    gid = models.AutoField(primary_key=True)
    nomenclatu = models.CharField(max_length=50, blank=True, null=True)
    situacao_b = models.CharField(max_length=1, blank=True, null=True)
    indice_blo = models.IntegerField(blank=True, null=True)
    nome_bacia = models.CharField(max_length=50, blank=True, null=True)
    nome_setor = models.CharField(max_length=50, blank=True, null=True)
    id4 = models.IntegerField(blank=True, null=True)
    area_bloco = models.FloatField(blank=True, null=True)
    geom = models.MultiPolygonField(blank=True, null=True)
    objects = models.GeoManager()

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

class Sprint(BusinessModel):
    contextclassname = 'sprints'
    id = models.AutoField(primary_key=True, db_column='id_sprint')
    name = models.CharField(max_length=100, blank=True, default='')
    description = models.TextField(blank=True, default='')
    end = models.DateField(unique=True, blank=True,default=datetime.date.today)

    class Meta:
        managed = False
        db_table = 'sprint'

    def __str__(self):
        return self.name or _('Sprint ending %s') % self.end

class Task(BusinessModel):
    contextclassname = 'tasks'
    #Unit of work to be done for the sprint
    STATUS_TODO = 1
    STATUS_IN_PROGRESS = 2
    STATUS_TESTING = 3
    STATUS_DONE = 4
    STATUS_CHOICES = (
        (STATUS_TODO, _('Not Started')),
        (STATUS_IN_PROGRESS, _('In Progress')),
        (STATUS_TESTING, _('Testing')),
        (STATUS_DONE, _('Done')),
    )
    id= models.AutoField(primary_key=True, db_column='id_task' )
    name = models.CharField(max_length=300, blank=True, null=True)
    description = models.CharField(max_length=1000, blank=True, null=True)
    status = models.CharField(max_length=20, blank=True, null=True)
    order = models.IntegerField(blank=True, null=True)
    started = models.DateField(blank=True, null=True,)
    due = models.DateField(blank=True, null=True)
    completed = models.DateField(blank=True, null=True)
    sprint = models.ForeignKey(Sprint,  db_column='id_sprint',related_name='tasks' ,blank=True, null=True)


    class Meta:
        managed = False
        db_table = 'task'

    def __str__(self):
        return self.name