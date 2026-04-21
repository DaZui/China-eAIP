from typing import Annotated

from pydantic import Field

from ... import geojson
from ...base import BaseModel, Nil, WithAtGmlId, WithAtSrsName, WithDollar
from ..data_types import ValDistanceVerticalBaseType, ValDistanceVerticalType


class Point(WithAtGmlId, WithAtSrsName):
    """https://aixm.aero/sites/default/files/imce/AIXM511HTML/AIXM/Class_Point.html"""

    gml_pos: Annotated[
        WithDollar[tuple[geojson.Latitude, geojson.Longitude]] | None,
        Field(alias="gml:pos"),
    ] = None

    @property
    def latitude(self) -> float:
        return self.gml_pos.dollar[0] if self.gml_pos else 0

    @property
    def longitude(self) -> float:
        return self.gml_pos.dollar[1] if self.gml_pos else 0

    aixm_horizontal_accuracy: Annotated[
        # ValDistanceType | # 实际当中没有出现
        Nil | None, Field(alias="aixm:horizontalAccuracy")
    ] = None


class ElevatedPoint(Point):
    """https://aixm.aero/sites/default/files/imce/AIXM511HTML/AIXM/Class_ElevatedPoint.html"""

    aixm_elevation: Annotated[
        ValDistanceVerticalType | None, Field(alias="aixm:elevation")
    ] = None

    @property
    def computed_elevation(self) -> ValDistanceVerticalBaseType | None:
        if not (self.aixm_elevation is None or isinstance(self.aixm_elevation, Nil)):
            return self.aixm_elevation.dollar

    aixm_vertical_accuracy: Annotated[
        # ValDistanceType | # 实际当中没有出现
        Nil | None, Field(alias="aixm:verticalAccuracy")
    ] = None
    aixm_vertical_datum: Annotated[
        # CodeVerticalDatumType | # 实际当中没有出现
        Nil | None, Field(alias="aixm:verticalDatum")
    ] = None


class WithAixmLocation(BaseModel):
    class _AixmLocation(BaseModel):
        aixm_elevated_point: Annotated[ElevatedPoint, Field(alias="aixm:ElevatedPoint")]

    aixm_location: Annotated[_AixmLocation | Nil, Field(alias="aixm:location")]
