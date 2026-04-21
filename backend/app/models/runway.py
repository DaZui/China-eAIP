from django.db import models

from . import common


# Create your models here.
class Runway(common.Common):
    aixm_designator: common.CharField = models.CharField()
    aixm_nominal_length: common.FloatOptional = models.FloatField(null=True)
    aixm_length_accuracy: common.FloatOptional = models.FloatField(null=True)
    aixm_nominal_width: common.FloatOptional = models.FloatField(null=True)
    aixm_width_accuracy: common.FloatOptional = models.FloatField(null=True)
    aixm_width_shoulder: common.FloatOptional = models.FloatField(null=True)
    aixm_annotations: common.CharField = models.CharField()
    aixm_associated_airport_heliport: common.CharField = models.CharField()
