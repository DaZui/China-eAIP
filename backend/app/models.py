import datetime

from django.db import models

BooleanField = models.BooleanField[bool, bool]
BooleanOptional = models.BooleanField[bool | None, bool | None]
CharField = models.CharField[str, str]
DateField = models.DateField[datetime.date, datetime.date]
DateOptional = models.DateField[datetime.date | None, datetime.date | None]
DateTimeField = models.DateTimeField[datetime.datetime, datetime.datetime]
FloatField = models.FloatField[float, float]
FloatOptional = models.FloatField[float | None, float | None]
IntegerField = models.IntegerField[int, int]
IntegerOptional = models.IntegerField[int | None, int | None]


# Create your models here.
class AirportHeliport(models.Model):
    uuid: CharField = models.CharField()
    information_valid_since: DateTimeField = models.DateTimeField()
    information_valid_until: DateTimeField = models.DateTimeField()
    aixm_sequence_number: IntegerField = models.IntegerField()
    aixm_correction_number: IntegerField = models.IntegerField()
    aixm_designator: CharField = models.CharField()
    aixm_name: CharField = models.CharField()
    aixm_location_indicator_icao: CharField = models.CharField()
    aixm_designator_iata: CharField = models.CharField()
    aixm_type: CharField = models.CharField()
    aixm_certified_icao: BooleanOptional = models.BooleanField(null=True)
    aixm_control_type: CharField = models.CharField()
    aixm_field_elevation: FloatOptional = models.FloatField(null=True)
    aixm_field_elevation_accuracy: FloatOptional = models.FloatField(null=True)
    aixm_magnetic_variation: FloatOptional = models.FloatField(null=True)
    aixm_magnetic_variation_accuracy: FloatOptional = models.FloatField(null=True)
    aixm_date_magnetic_variation: IntegerOptional = models.IntegerField(null=True)
    aixm_magnetic_variation_change: FloatOptional = models.FloatField(null=True)
    aixm_reference_temperature: FloatOptional = models.FloatField(null=True)
    aixm_certification_date: DateOptional = models.DateField(null=True)
    aixm_certification_expiration_date: DateOptional = models.DateField(null=True)
    aixm_city: CharField = models.CharField()
    aixm_latitude: FloatField = models.FloatField()
    aixm_longitude: FloatField = models.FloatField()
