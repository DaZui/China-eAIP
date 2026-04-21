import typing

from django.db import models

from . import common


# Create your models here.
class Runway(common.Common):
    aixm_designator: common.CharField = models.CharField()
    aixm_nominal_length: common.DecimalField = models.DecimalField(
        decimal_places=1, max_digits=5
    )
    aixm_nominal_width: common.DecimalField = models.DecimalField(
        decimal_places=1, max_digits=3
    )
    aixm_width_shoulder: common.DecimalOptional = models.DecimalField(
        null=True, decimal_places=1, max_digits=3
    )
    aixm_annotation: models.JSONField[typing.Any, typing.Any] = models.JSONField()
    aixm_associated_airport_heliport: common.CharField = models.CharField()
