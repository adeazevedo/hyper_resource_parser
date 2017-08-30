import os
import sys, inspect
import django

app_name = sys.argv[1]
model_name = sys.argv[2]

os.environ.setdefault("DJANGO_SETTINGS_MODULE", app_name+".settings")
django.setup()

from django.contrib.gis.db.models.fields import GeometryField
models = __import__(model_name+".models", fromlist=["*"])

def write_class(file_objet, model_class):
    sr = file_objet
    sr.write('class '+model_class[0]+'Serializer(GeoFeatureModelSerializer):\n')
    sr.write((' '*4)+'class Meta:\n')
    sr.write((' '*8)+'model = '+model_class[0]+'\n')
    identifier = None
    geom = None
    fields = model_class[1]._meta.get_fields()
    sr.write((' '*8)+'fields = [')
    for i,field in enumerate(fields):
        sr.write("'"+field.name+"'")
        if i < len(fields)-1:
            sr.write(',')
        else:
            sr.write(']\n')
        if field.primary_key:
            identifier = field.name
        if isinstance(field, GeometryField):
            geom = field.name
    if geom is not None:
        sr.write((' '*8)+"geo_field = '"+geom+"'\n")
    sr.write((' '*8)+"identifier = '"+identifier+"'\n\n\n")

classes_from = inspect.getmembers(sys.modules[model_name+'.models'], inspect.isclass)
with open('serializers.py', 'w+') as sr:
    sr.write("from "+model_name+".models import *\n")
    sr.write("from rest_framework_gis.serializers import GeoFeatureModelSerializer\n\n")
    for model_class in classes_from:
        write_class(sr, model_class)
    sr.close()