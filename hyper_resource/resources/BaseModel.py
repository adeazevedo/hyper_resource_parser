from django.contrib.gis.gdal import GDALRaster
from django.db import connection


class BaseModel(object):

    _instance = None
    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = object.__new__(cls, *args, **kwargs)
        return cls._instance

    def create_model_object_raster(self, view_resource, row):
        obj_model = view_resource.model_class()()
        setattr(obj_model,view_resource.pk_name(), row[0])
        rst = GDALRaster(row[1].tobytes())
        setattr(obj_model,view_resource.spatial_field_name(), rst)
        return obj_model

    def get_model_object_raster(self, view_resource, kwargs):
       pk_name = view_resource.pk_name()
       sql_string = "SELECT " + pk_name +  ", ST_AsGDALRaster(" + view_resource.spatial_field_name() +  ", 'GTiff') FROM " + view_resource.table_name() +  " WHERE " + pk_name + "  = " + kwargs['pk']
       with connection.cursor() as cursor:
            cursor.execute(sql_string)
            row = cursor.fetchone()
            return self.create_model_object_raster(view_resource, row)

    def get_model_objects_raster(self, view_resource, kwargs):
       pk_name = view_resource.pk_name()
       sql_string = "SELECT " + pk_name +  ", ST_AsGDALRaster(" + view_resource.spatial_field_name() +  ", 'GTiff') FROM " + view_resource.table_name()
       with connection.cursor() as cursor:
            cursor.execute(sql_string)
            rows = cursor.fetchall()
            model_raster_collection = []
            for row in rows:
                model_raster_collection.append(self.create_model_object_raster(view_resource, row))
            return model_raster_collection

    def get_iris_raster(self, view_resource, kwargs):
        pk_name = view_resource.pk_name()
        sql_string = "SELECT " + pk_name + " FROM " + view_resource.table_name()
        iri= view_resource.request.build_absolute_uri()
        with connection.cursor() as cursor:
            cursor.execute(sql_string)
            rows = cursor.fetchall()
            iri_raster_dic = {}
            name = view_resource.table_name()
            for row in rows:
                str_pk = str(row[0])
                iri_raster_dic[name+ '-' + str_pk ] = (iri + str_pk + '/')
            return iri_raster_dic