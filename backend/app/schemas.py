import datetime

import pydantic
from china_eaip_dataset import geojson


class _Common(pydantic.BaseModel):
    uuid: str
    information_valid_since: datetime.datetime
    information_valid_until: datetime.datetime
    aixm_sequence_number: int
    aixm_correction_number: int


class Properties(_Common):
    aixm_location_indicator_icao: str
    aixm_designator_iata: str
    aixm_magnetic_variation: float | None
    aixm_magnetic_variation_accuracy: float | None
    aixm_date_magnetic_variation: int | None
    aixm_magnetic_variation_change: float | None
    aixm_annotations: str
    aixm_availability: str

    aixm_name_display: str
    aixm_field_elevation_display: list[str]
    aixm_reference_temperature_display: list[str]
    aixm_magnetic_variation_display: list[str]


class AirportHeliport(geojson.TypedFeature[geojson.Point, Properties]):
    pass


class Properties2(_Common):
    aixm_type: str
    aixm_designator: str
    aixm_name: str


class Airspace(geojson.TypedFeature[geojson.GeometryCollection, Properties2]):
    pass
