import datetime

from china_eaip_dataset import geojson
from china_eaip_dataset.aixm.data_types import CONVERT_TO_METER
from django.db import models

from . import schemas

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
    aixm_field_elevation_in_meter: FloatOptional = models.FloatField(null=True)
    aixm_field_elevation_accuracy_in_meter: FloatOptional = models.FloatField(null=True)
    aixm_magnetic_variation: FloatOptional = models.FloatField(null=True)
    aixm_magnetic_variation_accuracy: FloatOptional = models.FloatField(null=True)
    aixm_date_magnetic_variation: IntegerOptional = models.IntegerField(null=True)
    aixm_magnetic_variation_change: FloatOptional = models.FloatField(null=True)
    aixm_reference_temperature_in_celcius: FloatOptional = models.FloatField(null=True)
    aixm_certification_date: DateOptional = models.DateField(null=True)
    aixm_certification_expiration_date: DateOptional = models.DateField(null=True)
    aixm_served_city: CharField = models.CharField()
    aixm_latitude: FloatField = models.FloatField()
    aixm_longitude: FloatField = models.FloatField()
    aixm_annotations: CharField = models.CharField()
    aixm_availability: CharField = models.CharField()

    @property
    def feature(self) -> schemas.AirportHeliport:
        return schemas.AirportHeliport(
            geometry=geojson.Point(
                coordinates=(
                    self.aixm_longitude,
                    self.aixm_latitude,
                    self.aixm_field_elevation_in_meter or 0,
                )
            ),
            properties=schemas.Properties.model_validate(
                obj=self, from_attributes=True
            ),
            id=self.uuid,
        )

    @property
    def aixm_name_display(self) -> str:
        if self.aixm_served_city == self.aixm_name:
            return self.aixm_name.title()
        return f"{self.aixm_served_city} / {self.aixm_name}".title()

    @property
    def aixm_field_elevation_display(self) -> list[str]:
        if self.aixm_field_elevation_in_meter is None:
            return []

        elevation_in_m: float = self.aixm_field_elevation_in_meter
        elevation_in_ft: float = elevation_in_m / CONVERT_TO_METER["FT"]

        if self.aixm_field_elevation_accuracy_in_meter is None:
            return [f"{elevation_in_m:.1f} m", f"{elevation_in_ft:.1f} ft"]

        accuracy_in_m: float = self.aixm_field_elevation_accuracy_in_meter
        accuracy_in_ft: float = accuracy_in_m / CONVERT_TO_METER["FT"]

        return [
            f"{elevation_in_m:.1f} ± {accuracy_in_m:.1f} m",
            f"{elevation_in_ft:.1f} ± {accuracy_in_ft:.1f} ft",
        ]

    @property
    def aixm_reference_temperature_display(self) -> list[str]:
        if self.aixm_reference_temperature_in_celcius is None:
            return []

        in_c: float = self.aixm_reference_temperature_in_celcius
        in_f: float = in_c * 1.8 + 32

        return [f"{in_c:.1f} ℃", f"{in_f:.1f} ℉"]

    @property
    def aixm_magnetic_variation_display(self) -> list[str]:
        if self.aixm_magnetic_variation is None:
            return []

        rv: list[str] = [
            f"{self.aixm_magnetic_variation:.2f} ° ± {self.aixm_magnetic_variation_accuracy:.2f} °"
            if self.aixm_magnetic_variation_accuracy
            else f"{self.aixm_magnetic_variation:.2f} °"
        ]

        if self.aixm_date_magnetic_variation:
            rv.append(f"Last Measured in {self.aixm_date_magnetic_variation}")

        if self.aixm_magnetic_variation_change:
            rv.append(
                f"Changing at {self.aixm_magnetic_variation_change:.2f} ° per year"
            )

        return rv
