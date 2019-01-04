from __future__ import unicode_literals
import base64
import jwt

from hyper_resource.models import FeatureModel, BusinessModel

from hyper_resource.models import  BusinessModel
# -*- coding: utf-8 -*-

from django.db import models

# Create your models here.
from hyper_resource_py.settings import SECRET_KEY

class EntryPoint(BusinessModel):
    gasto_list = models.CharField(max_length=200)
    tipo_gasto_list = models.CharField(max_length=200)
    usuario_list = models.CharField(max_length=200)

class Usuario(BusinessModel):
    id= models.AutoField(primary_key=True)
    nome = models.CharField(max_length=100)
    nome_usuario = models.CharField(max_length=100)
    avatar = models.CharField(max_length=100)
    data_nascimento = models.DateField(null=True)
    email = models.CharField(null=True, max_length=100)
    senha = models.CharField(max_length=50)

    def col_of_gasto(self):
        return self.gastos.all()

    @classmethod
    def jwt_algorithm(cls):
        return 'HS256'

    @classmethod
    def getOneOrNone(cls, user_name, password):
        return Usuario.objects.filter(nome_usuario=user_name, senha=password).first()

    def getToken(self):
        encoded = jwt.encode({'id': self.id, 'nome_usuario': self.nome_usuario}, SECRET_KEY,
                             algorithm=Usuario.jwt_algorithm())
        return encoded

    @classmethod
    def login(cls, user_name, password):
        usuario = Usuario.getOneOrNone(user_name, password)
        if usuario is None:
            return None
        a_dict = {}
        a_dict['id'] = usuario.id
        a_dict['nome'] = usuario.nome
        a_dict['nome_usuario'] = usuario.nome_usuario
        a_dict['avatar'] = usuario.avatar
        a_dict['token'] = usuario.getToken()
        return a_dict

    @classmethod
    def token_is_ok(cls, a_token):
        try:
            payload = jwt.decode(a_token, SECRET_KEY, algorithm=Usuario.jwt_algorithm())
            return True
        except jwt.InvalidTokenError:
            return False

    def encodeField(self, a_field):
        return base64.b64encode(a_field.encode())

    def decodeField(self, a_field):
        return base64.b64decode(a_field.encode())

class TipoGasto(BusinessModel):
    id= models.AutoField(primary_key=True)
    nome = models.CharField(max_length=100)
    tipo_gasto_generico = models.ForeignKey('self', db_column='id_tipogasto_generico', on_delete=models.PROTECT, null=True)

class Gasto(BusinessModel):
    id= models.AutoField(primary_key=True)
    data = models.DateField(null=True)
    tipo_gasto = models.ForeignKey(TipoGasto, db_column='tipo_gasto_id', on_delete=models.PROTECT)
    usuario = models.ForeignKey(Usuario, related_name='gastos', on_delete=models.PROTECT)
    valor = models.FloatField()
    detalhe = models.CharField(max_length=100, null=True)
    #cod_municipio = models.CharField(max_length=7, null=True)

