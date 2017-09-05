from django.db import models

# Create your models here.
from hyper_resource.models import FeatureModel, BusinessModel
from hyper_resource.views import StyleResource


class LineTest(FeatureModel):
    pass

class PolygonTest(FeatureModel):
    pass

class PointTest(FeatureModel):
    pass

class StyleTest(StyleResource):
    pass

class TodoTest(BusinessModel):
    pass

class PartTest(BusinessModel):
    pass

class RasterTest(BusinessModel):
    pass