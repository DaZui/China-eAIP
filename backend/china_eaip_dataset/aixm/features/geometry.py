from typing import Annotated

from pydantic import Field

from ... import geojson
from ...base import BaseModel, Nil, WithAtGmlId, WithAtSrsName, WithDollar
from ..data_types import CodeVerticalDatumType, ValDistanceType, ValDistanceVerticalType


class Point(WithAtGmlId, WithAtSrsName):
    """https://aixm.aero/sites/default/files/imce/AIXM511HTML/AIXM/Class_Point.html"""

    gml_pos: Annotated[
        WithDollar[tuple[geojson.Latitude, geojson.Longitude]] | None,
        Field(alias="gml:pos"),
    ] = None
    aixm_horizontal_accuracy: Annotated[
        ValDistanceType | None, Field(alias="aixm:horizontalAccuracy")
    ] = None

    def point(self, elevation: float = 0) -> geojson.Point:
        if self.gml_pos is None:
            return geojson.Point(coordinates=(0, 0, elevation))
        return geojson.Point(
            coordinates=(self.gml_pos.dollar[1], self.gml_pos.dollar[0], elevation)
        )


class ElevatedPoint(Point):
    """https://aixm.aero/sites/default/files/imce/AIXM511HTML/AIXM/Class_ElevatedPoint.html"""

    aixm_elevation: Annotated[
        ValDistanceVerticalType | None, Field(alias="aixm:elevation")
    ] = None
    aixm_vertical_accuracy: Annotated[
        ValDistanceType | None, Field(alias="aixm:verticalAccuracy")
    ] = None
    aixm_vertical_datum: Annotated[
        CodeVerticalDatumType | None, Field(alias="aixm:verticalDatum")
    ] = None


class WithAixmLocation(BaseModel):
    class _AixmLocation(BaseModel):
        aixm_elevated_point: Annotated[ElevatedPoint, Field(alias="aixm:ElevatedPoint")]

    aixm_location: Annotated[_AixmLocation | Nil, Field(alias="aixm:location")]
