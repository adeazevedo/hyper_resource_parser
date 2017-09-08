from __future__ import unicode_literals
from hyper_resource.models import FeatureModel, BusinessModel

from hyper_resource.models import  BusinessModel
# -*- coding: utf-8 -*-

from django.db import models

# Create your models here.
class Usuario(BusinessModel):
    id= models.AutoField(primary_key=True)
    nome = models.CharField(max_length=100)
    data_nascimento = models.DateField(null=True)
    email = models.CharField(null=True, max_length=100)
    senha = models.CharField(max_length=50)

class TipoGasto(BusinessModel):
    id= models.AutoField(primary_key=True)
    nome = models.CharField(max_length=100)
    tipo_gasto_generico = models.ForeignKey('self', db_column='id_tipogasto_generico', null=True)

class Gasto(BusinessModel):
    id= models.AutoField(primary_key=True)
    data = models.DateField(null=True)
    tipo_gasto = models.ForeignKey(TipoGasto, db_column='tipo_gasto_id')
    usuario = models.ForeignKey(Usuario, related_name='gastos')
    valor = models.FloatField()
    detalhe = models.CharField(max_length=100, null=True)

