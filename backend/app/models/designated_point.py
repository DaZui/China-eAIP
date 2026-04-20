from django.db import models

from . import common


# Create your models here.
class DesignatedPoint(common.Common):
    aixm_designator: common.CharField = models.CharField()
    aixm_name: common.CharField = models.CharField()
    aixm_latitude: common.FloatField = models.FloatField()
    aixm_longitude: common.FloatField = models.FloatField()
    aixm_horizontal_accuracy_in_meter: common.FloatOptional = models.FloatField(
        null=True
    )
    aixm_airport_heliport: common.CharField = models.CharField()
