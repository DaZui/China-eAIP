import collections.abc
import math
import typing

import pydantic
import pyproj

geod = pyproj.Geod(ellps="WGS84")

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
    geometry: Point | LineString | GeometryCollection
    properties: typing.Any
    id: str


class TypedFeature[Geometry: Point | GeometryCollection, Properties: typing.Any](
    pydantic.BaseModel, title="Typed GeoJSON Feature"
):
    type: typing.Literal["Feature"] = "Feature"
    geometry: Geometry
    properties: Properties
    id: str


class FeatureCollection(pydantic.BaseModel):
    type: typing.Literal["FeatureCollection"] = "FeatureCollection"
    features: collections.abc.Sequence[Feature]


@pydantic.validate_call
def 给定距离求一圈所有点(
    点: Position, 距离: float, 起始角度: float, 终止角度: float
) -> list[Position2D]:
    azs: list[float] = [
        起始角度 + i for i in range(math.floor(终止角度 - 起始角度))
    ] + [终止角度]
    return [geod.fwd(lons=点[0], lats=点[1], az=i, dist=距离)[:2] for i in azs]
