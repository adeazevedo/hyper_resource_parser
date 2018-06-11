from __future__ import unicode_literals
from hyper_resource.models import FeatureModel, BusinessModel, RasterModel
# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.

from django.contrib.gis.db import models

class ImagemExemplo1(RasterModel):
    rid = models.AutoField(primary_key=True)
    rast = models.RasterField(blank=True, null=True)  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'imagem1'

class ImagemExemplo2(RasterModel):
    rid = models.AutoField(primary_key=True)
    rast = models.RasterField(blank=True, null=True)  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'imagem2'

class ImagemExemploTile1(RasterModel):
    rid = models.AutoField(primary_key=True)
    rast = models.RasterField(blank=True, null=True)  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'imagem1_tiles'

class ImagemExemploTile2(RasterModel):
    rid = models.AutoField(primary_key=True)
    rast = models.RasterField(blank=True, null=True)  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'imagem2_tiles'