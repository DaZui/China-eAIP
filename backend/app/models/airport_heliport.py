import typing

from django.db import models

from . import base, common


# Create your models here.
class AirportHeliport(common.Common):
    aixm_designator: common.CharField = models.CharField()
    aixm_name: common.CharField = models.CharField()
    aixm_location_indicator_icao: common.CharField = models.CharField()
    aixm_designator_iata: common.CharField = models.CharField()
    aixm_type: common.CharField = models.CharField()
    aixm_certified_icao: common.BooleanOptional = models.BooleanField(null=True)
    aixm_control_type: common.CharField = models.CharField()
    aixm_field_elevation: common.DecimalOptional = models.DecimalField(
        null=True, decimal_places=1, max_digits=5
    )
    aixm_magnetic_variation: common.DecimalOptional = models.DecimalField(
        null=True, decimal_places=2, max_digits=4
    )
    aixm_date_magnetic_variation: common.DecimalOptional = models.DecimalField(
        null=True, decimal_places=0, max_digits=4
    )
    aixm_reference_temperature: common.DecimalOptional = models.DecimalField(
        null=True, decimal_places=1, max_digits=3
    )
    aixm_certification_date: common.DateOptional = models.DateField(null=True)
    aixm_certification_expiration_date: common.DateOptional = models.DateField(
        null=True
    )
    aixm_arp: models.ForeignKey[base.ElevatedPoint, base.ElevatedPoint] = (
        models.ForeignKey(base.ElevatedPoint, models.PROTECT)
    )
    aixm_served_city: common.CharField = models.CharField()
    aixm_annotations: models.JSONField[typing.Any, typing.Any] = models.JSONField()
    aixm_availability: models.JSONField[typing.Any, typing.Any] = models.JSONField()
