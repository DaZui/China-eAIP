import collections.abc
import typing

import pydantic

type Longitude = typing.Annotated[
    float,
    pydantic.Field(
        allow_inf_nan=False,
        description="Positive for E; Negative for W.",
        ge=-180,
        le=180,
        title="Longitude / Easting",
    ),
]
type Latitude = typing.Annotated[
    float,
    pydantic.Field(
        allow_inf_nan=False,
        description="Positive for N; Negative for S.",
        ge=-90,
        le=90,
        title="Latitude / Northing",
    ),
]
type Altitude = typing.Annotated[
    float,
    pydantic.Field(
        allow_inf_nan=False,
        description="In meter. 1 ft = 0.3048 m.",
        title="Altitude / Elevation",
    ),
]
type Position2D = typing.Annotated[
    tuple[Longitude, Latitude],
    pydantic.Field(
        description="(longitude, latitude)",
        examples=[(116.391220088889, 39.9073541194444)],
        title="GeoJSON Position without Altitude",
    ),
]
type Position3D = typing.Annotated[
    tuple[Longitude, Latitude, Altitude],
    pydantic.Field(
        description="(longitude, latitude, altitude)",
        examples=[(116.391220088889, 39.9073541194444, 110)],
        title="GeoJSON Position with Altitude",
    ),
]
type Position = Position3D | Position2D


class Point(pydantic.BaseModel, title="GeoJSON Point"):
    type: typing.Literal["Point"] = "Point"
    coordinates: Position3D


class LineString(pydantic.BaseModel, title="GeoJSON LineString"):
    type: typing.Literal["LineString"] = "LineString"
    coordinates: collections.abc.Sequence[Position]


class GeometryCollection(pydantic.BaseModel, title="GeoJSON GeometryCollection"):
    type: typing.Literal["GeometryCollection"] = "GeometryCollection"
    geometries: collections.abc.Sequence[Point | LineString]


class Feature(pydantic.BaseModel, title="GeoJSON Feature"):
    type: typing.Literal["Feature"] = "Feature"
    geometry: Point | GeometryCollection
    properties: typing.Any
    id: str


class TypedFeature[Geometry: Point | GeometryCollection, Properties: typing.Any](
    pydantic.BaseModel, title="Typed GeoJSON Feature"
):
    type: typing.Literal["Feature"] = "Feature"
    geometry: Geometry
    properties: Properties
    id: str
