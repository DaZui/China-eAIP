import typing

import pydantic

Longitude = typing.Annotated[
    float,
    pydantic.Field(
        allow_inf_nan=False,
        description="Positive for E; Negative for W.",
        ge=-180,
        le=180,
        title="Longitude / Easting",
    ),
]
Latitude = typing.Annotated[
    float,
    pydantic.Field(
        allow_inf_nan=False,
        description="Positive for N; Negative for S.",
        ge=-90,
        le=90,
        title="Latitude / Northing",
    ),
]
Altitude = typing.Annotated[
    float,
    pydantic.Field(
        allow_inf_nan=False,
        description="In meter. 1 ft = 0.3048 m.",
        title="Altitude / Elevation",
    ),
]
Position3D = typing.Annotated[
    tuple[Longitude, Latitude, Altitude],
    pydantic.Field(
        description="(longitude, latitude, altitude)",
        examples=[(116.391220088889, 39.9073541194444, 110)],
        title="GeoJSON Position w/ Altitude",
    ),
]


class Point(pydantic.BaseModel, title="GeoJSON Point"):
    type: typing.Literal["Point"] = "Point"
    coordinates: Position3D


class Feature(pydantic.BaseModel, title="GeoJSON Feature"):
    type: typing.Literal["Feature"] = "Feature"
    geometry: Point
    properties: typing.Any
    id: str


class TypedFeature[Geometry: Point, Properties: typing.Any](
    pydantic.BaseModel, title="Typed GeoJSON Feature"
):
    type: typing.Literal["Feature"] = "Feature"
    geometry: Geometry
    properties: Properties
    id: str
