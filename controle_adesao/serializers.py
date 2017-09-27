from controle_adesao.models import *
from rest_framework_gis.serializers import GeoFeatureModelSerializer

from rest_framework.serializers import ModelSerializer, HyperlinkedRelatedField

class AtorSerializer(ModelSerializer):
    representantes = HyperlinkedRelatedField(view_name='controle_adesao:Representante_detail', many=True, read_only=True)
    class Meta:
        model = Ator
        fields = ['representantes','nome','status_adesao','documento_solicitacao','capacitacao','modalidade','observacao','id_ator']
        identifier = 'id_ator'
        identifiers = ['pk', 'id_ator']


class PublicacaoinformacaogeoespacialSerializer(ModelSerializer):
    ator = HyperlinkedRelatedField(view_name='controle_adesao:Ator_detail', many=False, read_only=True)
    class Meta:
        model = Publicacaoinformacaogeoespacial
        fields = ['tem_metadados','tem_geoservicos','tem_download','tem_vinde','id_publicacao_informacao_geoespacial','ator']
        identifier = 'id_publicacao_informacao_geoespacial'
        identifiers = ['pk', 'id_publicacao_informacao_geoespacial']


class RepresentanteSerializer(ModelSerializer):
    ator = HyperlinkedRelatedField(view_name='controle_adesao:Ator_detail', many=False, read_only=True)
    class Meta:
        model = Representante
        fields = ['id_representante','nome','e_mail','funcao_cargo','area_setor','telefone1','telefone2','celular_telefone3','ator']
        identifier = 'id_representante'
        identifiers = ['pk', 'id_representante']




serializers_dict = {}