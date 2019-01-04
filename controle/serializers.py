from controle.models import *
from rest_framework_gis.serializers import GeoFeatureModelSerializer

from rest_framework.serializers import ModelSerializer, HyperlinkedRelatedField

from hyper_resource.serializers import BusinessSerializer


class EntryPointSerializer(BusinessSerializer):
    class Meta:
        model = EntryPoint
        fields = ["gasto-list", "tipo-gasto-list", "usuario-list"]
        identifier = None
        identifiers = []

class GastoSerializer(ModelSerializer):
    tipo_gasto = HyperlinkedRelatedField(view_name='controle_v1:TipoGasto_detail', many=False, read_only=True)
    usuario = HyperlinkedRelatedField(view_name='controle_v1:Usuario_detail', many=False, read_only=True)
    class Meta:
        model = Gasto
        fields = ['id','data','tipo_gasto','usuario','valor']
        identifier = 'id'
        identifiers = ['id', 'pk']




class TipoGastoSerializer(ModelSerializer):
    tipo_gasto_generico = HyperlinkedRelatedField(view_name='controle_v1:TipoGasto_detail', many=False, read_only=True)
    class Meta:
        model = TipoGasto
        fields = ['id','nome', 'tipo_gasto_generico']
        identifier = 'id'
        identifiers = ['id', 'pk']

    def updateOrCreate(self,validated_data, type):
        pass
    def create(self, validated_data):
        um_tipo_gasto = self.initial_data['tipo_gasto_generico']
        if um_tipo_gasto != None and um_tipo_gasto != '':
            arr = um_tipo_gasto.split('/')
            um_tipo_gasto = arr[-1] if arr[-1] != '' else arr[-2]
        validated_data['tipo_gasto_generico_id'] = um_tipo_gasto
        instance = super(TipoGastoSerializer, self).create(validated_data)
        instance.tipo_gasto_id = um_tipo_gasto
        return instance
    def update(self, instance, validated_data):
        um_tipo_gasto = self.initial_data['tipo_gasto_generico']
        if um_tipo_gasto != None and um_tipo_gasto != '':
            arr = um_tipo_gasto.split('/')
            um_tipo_gasto = arr[-1] if arr[-1] != '' else arr[-2]
        validated_data['tipo_gasto_generico_id'] = um_tipo_gasto
        instance = super(TipoGastoSerializer, self).update(instance, validated_data)
        instance.tipo_gasto_id = um_tipo_gasto
        return instance

class UsuarioSerializer(ModelSerializer):
    gastos = HyperlinkedRelatedField(view_name='controle_v1:TipoGasto_detail', many=True, read_only=True)
    class Meta:
        model = Usuario
        fields = ['gastos','id','nome','nome_usuario','data_nascimento','email','senha']
        identifier = 'id'
        identifiers = ['id', 'pk']




serializers_dict = {}