from china_eaip_dataset import geojson
from django.db import models

from .. import schemas
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
    aixm_field_elevation_in_meter: common.FloatOptional = models.FloatField(null=True)
    aixm_field_elevation_accuracy_in_meter: common.FloatOptional = models.FloatField(
        null=True
    )
    aixm_magnetic_variation: common.FloatOptional = models.FloatField(null=True)
    aixm_magnetic_variation_accuracy: common.FloatOptional = models.FloatField(
        null=True
    )
    aixm_date_magnetic_variation: common.IntegerOptional = models.IntegerField(
        null=True
    )
    aixm_magnetic_variation_change: common.FloatOptional = models.FloatField(null=True)
    aixm_reference_temperature_in_celcius: common.FloatOptional = models.FloatField(
        null=True
    )
    aixm_certification_date: common.DateOptional = models.DateField(null=True)
    aixm_certification_expiration_date: common.DateOptional = models.DateField(
        null=True
    )
    aixm_served_city: common.CharField = models.CharField()
    aixm_latitude: common.FloatField = models.FloatField()
    aixm_longitude: common.FloatField = models.FloatField()
    aixm_horizontal_accuracy_in_meter: common.FloatOptional = models.FloatField(
        null=True
    )
    aixm_annotations: common.CharField = models.CharField()
    aixm_availability: common.CharField = models.CharField()

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
    def aixm_field_elevation(self) -> tuple[float | None, float | None]:
        return (
            self.aixm_field_elevation_in_meter,
            self.aixm_field_elevation_accuracy_in_meter,
        )

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
            rv.append(f"(updated at {self.aixm_date_magnetic_variation})")

        if self.aixm_magnetic_variation_change:
            rv.append(
                f"(changing at {self.aixm_magnetic_variation_change:.2f} ° per year)"
            )

        return rv
