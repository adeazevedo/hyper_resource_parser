from __future__ import unicode_literals
from hyper_resource.models import FeatureModel, BusinessModel
from hyper_resource.models import FeatureModel, BusinessModel
from hyper_resource.models import FeatureModel, BusinessModel
from hyper_resource.models import FeatureModel, BusinessModel
from hyper_resource.models import FeatureModel, BusinessModel
from hyper_resource.models import FeatureModel, BusinessModel
from hyper_resource.models import FeatureModel, BusinessModel
from hyper_resource.models import FeatureModel, BusinessModel
from hyper_resource.models import FeatureModel, BusinessModel
# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.

from django.contrib.gis.db import models


class Ator(BusinessModel):
    nome = models.CharField(max_length=500)
    status_adesao = models.CharField(max_length=30)
    documento_solicitacao = models.TextField(blank=True, null=True)
    capacitacao = models.CharField(max_length=20, blank=True, null=True)
    modalidade = models.CharField(max_length=20, blank=True, null=True)
    observacao = models.TextField(blank=True, null=True)
    id_ator = models.AutoField(primary_key=True)

    class Meta:
        managed = True
        db_table = 'Ator'


class Publicacaoinformacaogeoespacial(BusinessModel):
    tem_metadados = models.CharField(max_length=20, blank=True, null=True)
    tem_geoservicos = models.CharField(max_length=20, blank=True, null=True)
    tem_download = models.CharField(max_length=20, blank=True, null=True)
    tem_vinde = models.CharField(max_length=20, blank=True, null=True)
    id_publicacao_informacao_geoespacial = models.AutoField(primary_key=True)
    ator = models.ForeignKey(Ator,  db_column='id_ator', on_delete=models.PROTECT)

    class Meta:
        managed = True
        db_table = 'PublicacaoInformacaoGeoespacial'


class Representante(BusinessModel):
    id_representante = models.AutoField(primary_key=True)
    nome = models.CharField(max_length=150)
    e_mail = models.CharField(max_length=70, blank=True, null=True)
    funcao_cargo = models.CharField(max_length=100, blank=True, null=True)
    area_setor = models.CharField(max_length=150, blank=True, null=True)
    telefone1 = models.CharField(max_length=25, blank=True, null=True)
    telefone2 = models.CharField(max_length=25, blank=True, null=True)
    celular_telefone3 = models.CharField(max_length=25, blank=True, null=True)
    ator = models.ForeignKey(Ator, db_column='id_ator', on_delete=models.PROTECT, related_name="representantes")

    class Meta:
        managed = True
        db_table = 'Representante'
