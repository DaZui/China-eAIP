import datetime
import typing

import china_eaip_dataset.aixm.features.airport_heliport
import china_eaip_dataset.base
import pydantic
from china_eaip_dataset import geojson
from china_eaip_dataset.base import Nil, WithDollar


class _Properties(pydantic.BaseModel):
    designator: str
    name: str
    locationIndicatorICAO: str
    designatorIATA: str
    type: str
    certifiedICAO: str
    controlType: str
    fieldElevationInMeter: float
    magneticVariation: str
    dateMagneticVariation: str
    referenceTemperatureInCelcius: float
    certificationDate: datetime.date | None
    certificationExpirationDate: datetime.date | None
    annotations: str
    servedCity: str
    availability: str


def none_or_value[Inner: typing.Any](x: Nil | WithDollar[Inner]) -> None | Inner:
    if isinstance(x, Nil):
        return None
    return x.dollar


class Output(china_eaip_dataset.base.BaseModel):
    @classmethod
    def list_all(
        cls, obj: china_eaip_dataset.aixm.features.CommonRoot
    ) -> list[typing.Self]:
        items: list[typing.Self] = [
            cls(
                value=x.aixm_airport_heliport.aixm_time_slice[
                    0
                ].aixm_airport_heliport_time_slice
            )
            for x in obj.message_has_member
            if x.aixm_airport_heliport
            if x.aixm_airport_heliport.aixm_time_slice[
                0
            ].aixm_airport_heliport_time_slice
        ]
        return sorted(items, key=lambda x: x.properties.locationIndicatorICAO)

    type: typing.Literal["Feature"] = "Feature"
    value: typing.Annotated[
        china_eaip_dataset.aixm.features.airport_heliport.AirportHeliport,
        pydantic.Field(exclude=True),
    ]

    @property
    def field_elevation_in_meter(self) -> float:
        if isinstance(self.value.aixm_field_elevation, Nil):
            return 0
        return self.value.aixm_field_elevation.in_m

    @property
    def reference_temperature_in_celcius(self) -> float:
        if isinstance(self.value.aixm_reference_temperature, Nil):
            return 0
        return self.value.aixm_reference_temperature.in_celsius

    @pydantic.computed_field
    @property
    def properties(self) -> _Properties:
        return _Properties(
            designator=f"{self.value.aixm_designator}".upper(),
            name=f"{self.value.aixm_name}".capitalize(),
            locationIndicatorICAO=f"{self.value.aixm_location_indicator_icao}".upper(),
            designatorIATA=f"{self.value.aixm_designator_iata}".upper(),
            type=f"{self.value.aixm_type}",
            certifiedICAO=f"{self.value.aixm_certified_icao}",
            controlType=f"{self.value.aixm_control_type}",
            fieldElevationInMeter=self.field_elevation_in_meter,
            magneticVariation=f"{self.value.aixm_magnetic_variation}",
            dateMagneticVariation=f"{self.value.aixm_date_magnetic_variation}",
            referenceTemperatureInCelcius=self.reference_temperature_in_celcius,
            certificationDate=none_or_value(self.value.aixm_certification_date),
            certificationExpirationDate=none_or_value(
                self.value.aixm_certification_expiration_date
            ),
            annotations="".join(
                f"{annotation.aixm_note.aixm_property_name}: "
                + ", ".join(
                    f"{translated_note.aixm_linguistic_note.aixm_note}"
                    for translated_note in annotation.aixm_note.aixm_translated_note
                )
                for annotation in self.value.aixm_annotation
            ),
            servedCity=f"{self.value.aixm_served_city[0].aixm_city.aixm_name}".capitalize(),
            availability=", ".join(
                f"{z.aixm_flight_characteristic.aixm_military} {z.aixm_flight_characteristic.aixm_purpose} {z.aixm_flight_characteristic.aixm_rule} {z.aixm_flight_characteristic.aixm_type}"
                for x in self.value.aixm_availability
                for y in x.aixm_airport_heliport_availability.aixm_usage
                for z in y.aixm_airport_heliport_usage.aixm_selection.aixm_condition_combination.aixm_flight
            ),
        )

    @pydantic.computed_field
    @property
    def geometry(self) -> geojson.Point:
        if self.value.aixm_arp.aixm_elevated_point.gml_pos is None:
            return geojson.Point(coordinates=(0, 0, self.field_elevation_in_meter))
        return geojson.Point(
            coordinates=(
                self.value.aixm_arp.aixm_elevated_point.gml_pos.dollar[1],
                self.value.aixm_arp.aixm_elevated_point.gml_pos.dollar[0],
                self.field_elevation_in_meter,
            )
        )

    @pydantic.computed_field
    @property
    def id(self) -> str:
        return f"{self.value.aixm_designator}"
