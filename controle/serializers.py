from controle.models import *
from rest_framework_gis.serializers import GeoFeatureModelSerializer

from rest_framework.serializers import ModelSerializer, HyperlinkedRelatedField

class GastoSerializer(ModelSerializer):
    tipo_gasto = HyperlinkedRelatedField(view_name='controle_v1:TipoGasto_detail', many=False, read_only=True)
    usuario = HyperlinkedRelatedField(view_name='controle_v1:Usuario_detail', many=False, read_only=True)
    class Meta:
        model = Gasto
        fields = ['id','data','tipo_gasto','usuario','valor']
        identifier = 'id'
        identifiers = ['id', 'pk']

    def create(self, validated_data):
        um_tipo_gasto = self.initial_data['tipo_gasto']
        um_usuario = self.initial_data['usuario']
        validated_data['tipo_gasto_id'] = um_tipo_gasto
        validated_data['usuario_id'] = um_usuario
        instance = super(GastoSerializer, self).create(validated_data)
        instance.tipo_gasto_id = um_tipo_gasto
        instance.usuario_id = um_usuario
        return instance

class TipoGastoSerializer(ModelSerializer):
    class Meta:
        model = TipoGasto
        fields = ['id','nome']
        identifier = 'id'
        identifiers = ['id', 'pk']


class UsuarioSerializer(ModelSerializer):
    gastos = HyperlinkedRelatedField(view_name='gastos_detail', many=True, read_only=True)
    class Meta:
        model = Usuario
        fields = ['gastos','id','nome','data_nascimento','email','senha']
        identifier = 'id'
        identifiers = ['id', 'pk']




serializers_dict = {}