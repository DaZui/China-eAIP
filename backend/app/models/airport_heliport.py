from django.db import models

from . import common


# Create your models here.
class AirportHeliport(common.Common):
    aixm_designator: common.CharField = models.CharField()
    aixm_name: common.CharField = models.CharField()
    aixm_location_indicator_icao: common.CharField = models.CharField()
    aixm_designator_iata: common.CharField = models.CharField()
    aixm_type: common.CharField = models.CharField()
    aixm_certified_icao: common.BooleanOptional = models.BooleanField(null=True)
    aixm_control_type: common.CharField = models.CharField()
    aixm_field_elevation: common.FloatOptional = models.FloatField(null=True)
    aixm_field_elevation_accuracy: common.FloatOptional = models.FloatField(null=True)
    aixm_magnetic_variation: common.FloatOptional = models.FloatField(null=True)
    aixm_magnetic_variation_accuracy: common.FloatOptional = models.FloatField(
        null=True
    )
    aixm_date_magnetic_variation: common.IntegerOptional = models.IntegerField(
        null=True
    )
    aixm_magnetic_variation_change: common.FloatOptional = models.FloatField(null=True)
    aixm_reference_temperature: common.FloatOptional = models.FloatField(null=True)
    aixm_certification_date: common.DateOptional = models.DateField(null=True)
    aixm_certification_expiration_date: common.DateOptional = models.DateField(
        null=True
    )
    aixm_served_city: common.CharField = models.CharField()
    aixm_latitude: common.FloatField = models.FloatField()
    aixm_longitude: common.FloatField = models.FloatField()
    aixm_annotations: common.CharField = models.CharField()
    aixm_availability: common.CharField = models.CharField()
