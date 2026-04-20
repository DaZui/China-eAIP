import datetime

import pydantic
from china_eaip_dataset import geojson
from china_eaip_dataset.aixm.data_types import (
    CodeVerticalReferenceBaseType,
    ValDistanceVerticalBaseType,
)


class _Common(pydantic.BaseModel):
    uuid: str
    information_valid_since: datetime.datetime
    information_valid_until: datetime.datetime
    aixm_sequence_number: int
    aixm_correction_number: int


class _WithAnnotation(pydantic.BaseModel):
    aixm_annotations: str


class Runway(_Common, _WithAnnotation):
    aixm_designator: str
    aixm_associated_airport_heliport: str
    长度: tuple[float | None, float | None]
    宽度: tuple[float | None, float | None]
    路肩宽度: tuple[float | None, None]


class Properties(_Common, _WithAnnotation):
    aixm_location_indicator_icao: str
    aixm_designator_iata: str
    aixm_magnetic_variation: float | None
    aixm_magnetic_variation_accuracy: float | None
    aixm_date_magnetic_variation: int | None
    aixm_magnetic_variation_change: float | None
    aixm_availability: str

    aixm_field_elevation: tuple[float | None, float | None]
    aixm_reference_temperature_in_celcius: float | None

    aixm_name_display: str
    aixm_magnetic_variation_display: list[str]

    runways: list[Runway]


class AirportHeliport(geojson.TypedFeature[geojson.Point, Properties]):
    pass


class Properties2(_Common):
    aixm_type: str
    aixm_designator: str
    aixm_name: str

    upper_limit: tuple[
        float | None, ValDistanceVerticalBaseType | CodeVerticalReferenceBaseType
    ]
    lower_limit: tuple[
        float | None, ValDistanceVerticalBaseType | CodeVerticalReferenceBaseType
    ]


class Airspace(_Common):
    aixm_type: str
    aixm_designator: str
    aixm_name: str

    features: geojson.FeatureCollection


class AirspaceComponent(pydantic.BaseModel):
    upper_limit: tuple[
        float | None, ValDistanceVerticalBaseType | CodeVerticalReferenceBaseType
    ]
    lower_limit: tuple[
        float | None, ValDistanceVerticalBaseType | CodeVerticalReferenceBaseType
    ]
