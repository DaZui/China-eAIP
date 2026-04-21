from django.db import models

from . import common


# Create your models here.
class RunwayDirection(common.Common):
    aixm_designator: common.CharField = models.CharField()
    aixm_true_bearing: common.FloatOptional = models.FloatField(null=True)
    aixm_true_bearing_accuracy: common.FloatOptional = models.FloatField(null=True)
    aixm_used_runway: common.CharField = models.CharField()
