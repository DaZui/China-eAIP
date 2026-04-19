import functools
import typing

import pydantic

from ... import geojson
from ...base import (
    BaseModel,
    Link,
    Nil,
    WithAtGmlId,
    WithAtOwns,
    WithAtSrsName,
    WithAtXlinkType,
    WithDollar,
)
from ..abstract_feature import AixmTimeSlice
from ..data_types import (
    CodeAirspaceDesignatorType,
    CodeAirspaceType,
    CodeVerticalReferenceBaseType,
    CodeVerticalReferenceType,
    TextNameType,
    ValDistanceVerticalBaseType,
    ValDistanceVerticalType,
)
from .notes import WithAixmAnnotation


class _Unit[A: typing.Literal["deg", "KM"]](WithDollar[float]):
    at_uom: typing.Annotated[
        A | typing.Literal["UNKNOWN"], pydantic.Field(alias="@uom")
    ]


class _WithAtNumDerivatives(BaseModel):
    at_num_derivative_interior: typing.Annotated[
        typing.Literal[0], pydantic.Field(alias="@numDerivativeInterior")
    ]
    at_num_derivatives_at_end: typing.Annotated[
        typing.Literal[0], pydantic.Field(alias="@numDerivativesAtEnd")
    ]
    at_num_derivatives_at_start: typing.Annotated[
        typing.Literal[0], pydantic.Field(alias="@numDerivativesAtStart")
    ]


class _GmlPointProperty(Link):
    at_xlink_title: typing.Annotated[str, pydantic.Field(alias="@xlink:title")]


class _GmlCircleByCenterPointItem(_WithAtNumDerivatives):
    at_interpolation: typing.Annotated[
        typing.Literal["circularArcCenterPointWithRadius"],
        pydantic.Field(alias="@interpolation"),
    ]
    gml_pos: typing.Annotated[
        WithDollar[tuple[geojson.Latitude, geojson.Longitude]] | None,
        pydantic.Field(alias="gml:pos"),
    ] = None
    gml_point_property: typing.Annotated[
        _GmlPointProperty | None, pydantic.Field(alias="gml:pointProperty")
    ] = None
    at_num_arc: typing.Annotated[typing.Literal[1], pydantic.Field(alias="@numArc")]
    gml_radius: typing.Annotated[
        _Unit[typing.Literal["KM"]], pydantic.Field(alias="gml:radius")
    ]

    @functools.cached_property
    def start_angle(self) -> float:
        return 0

    @functools.cached_property
    def end_angle(self) -> float:
        return 360

    @functools.cached_property
    def center(self) -> geojson.Position2D | None:
        if self.gml_pos:
            latitude, longitude = self.gml_pos.dollar
            return longitude, latitude
        if self.gml_point_property:
            print(self.gml_point_property)

    @functools.cached_property
    def points(self) -> list[geojson.Position2D]:
        if self.center is None:
            return []
        return geojson.给定距离求一圈所有点(
            点=self.center,
            距离=self.gml_radius.dollar,
            起始角度=self.start_angle,
            终止角度=self.end_angle,
        )

    @functools.cached_property
    def is_valid(self) -> bool:
        return len(self.points) > 1

    @functools.cached_property
    def geometry(self) -> geojson.LineString:
        return geojson.LineString(coordinates=self.points)


class _GmlArcByCenterPointItem(_GmlCircleByCenterPointItem):
    gml_start_angle: typing.Annotated[
        _Unit[typing.Literal["deg"]], pydantic.Field(alias="gml:startAngle")
    ]
    gml_end_angle: typing.Annotated[
        _Unit[typing.Literal["deg"]], pydantic.Field(alias="gml:endAngle")
    ]

    @functools.cached_property
    def start_angle(self) -> float:
        return self.gml_start_angle.dollar

    @functools.cached_property
    def end_angle(self) -> float:
        return self.gml_end_angle.dollar


class _GmlGeodesicStringItem(_WithAtNumDerivatives):
    at_interpolation: typing.Annotated[
        typing.Literal["geodesic"], pydantic.Field(alias="@interpolation")
    ]
    gml_pos_list: typing.Annotated[
        WithDollar[list[float]], pydantic.Field(alias="gml:posList")
    ]

    @functools.cached_property
    def points(self) -> list[geojson.Position2D]:
        return list(zip(self.gml_pos_list.dollar[1::2], self.gml_pos_list.dollar[::2]))

    @functools.cached_property
    def is_valid(self) -> bool:
        return len(self.points) > 1

    @functools.cached_property
    def geometry(self) -> geojson.LineString:
        return geojson.LineString(coordinates=self.points)


class _GmlSegments(BaseModel):
    gml_arc_by_center_point: typing.Annotated[
        list[_GmlArcByCenterPointItem], pydantic.Field(alias="gml:ArcByCenterPoint")
    ] = []
    gml_circle_by_center_point: typing.Annotated[
        list[_GmlCircleByCenterPointItem],
        pydantic.Field(alias="gml:CircleByCenterPoint"),
    ] = []
    gml_geodesic_string: typing.Annotated[
        list[_GmlGeodesicStringItem], pydantic.Field(alias="gml:GeodesicString")
    ] = []


class _AixmCurve(WithAtGmlId, WithAixmAnnotation):
    gml_segments: typing.Annotated[_GmlSegments, pydantic.Field(alias="gml:segments")]


class _GmlCurveMemberItem(WithAtOwns, WithAtXlinkType):
    aixm_curve: typing.Annotated[_AixmCurve, pydantic.Field(alias="aixm:Curve")]


class _GmlRing(BaseModel):
    gml_curve_member: typing.Annotated[
        list[_GmlCurveMemberItem], pydantic.Field(alias="gml:curveMember")
    ]


class _GmlExterior(BaseModel):
    gml_ring: typing.Annotated[_GmlRing, pydantic.Field(alias="gml:Ring")]


class _GmlPolygonPatchItem(BaseModel):
    at_interpolation: typing.Annotated[
        typing.Literal["planar"], pydantic.Field(alias="@interpolation")
    ]
    gml_exterior: typing.Annotated[_GmlExterior, pydantic.Field(alias="gml:exterior")]


class _GmlPatches(BaseModel):
    gml_polygon_patch: typing.Annotated[
        list[_GmlPolygonPatchItem], pydantic.Field(alias="gml:PolygonPatch")
    ]


class _AixmElevatedSurface(WithAtGmlId, WithAtSrsName):
    """https://aixm.aero/sites/default/files/imce/AIXM511HTML/AIXM/Class_Surface.html"""

    gml_patches: typing.Annotated[_GmlPatches, pydantic.Field(alias="gml:patches")]


type _LimitAndReference = tuple[
    float | None, ValDistanceVerticalBaseType | CodeVerticalReferenceBaseType
]


def _display_upper_lower_limit(
    limit: ValDistanceVerticalType, reference: CodeVerticalReferenceType
) -> _LimitAndReference:
    if isinstance(limit, Nil):
        return None, "OTHER"

    if limit.dollar in ("GND", "UNL", "FLOOR", "CEILING"):
        return None, limit.dollar

    if isinstance(reference, Nil):
        return limit.in_m, "OTHER"

    return limit.in_m, reference.dollar


class _AirspaceVolume(WithAtGmlId):
    """https://aixm.aero/sites/default/files/imce/AIXM511HTML/AIXM/Class_AirspaceVolume.html"""

    aixm_upper_limit: typing.Annotated[
        ValDistanceVerticalType, pydantic.Field(alias="aixm:upperLimit")
    ]
    aixm_upper_limit_reference: typing.Annotated[
        CodeVerticalReferenceType, pydantic.Field(alias="aixm:upperLimitReference")
    ]
    aixm_lower_limit: typing.Annotated[
        ValDistanceVerticalType, pydantic.Field(alias="aixm:lowerLimit")
    ]
    aixm_lower_limit_reference: typing.Annotated[
        CodeVerticalReferenceType, pydantic.Field(alias="aixm:lowerLimitReference")
    ]

    @functools.cached_property
    def 高度上限(self) -> _LimitAndReference:
        return _display_upper_lower_limit(
            limit=self.aixm_upper_limit, reference=self.aixm_upper_limit_reference
        )

    @functools.cached_property
    def 高度下限(self) -> _LimitAndReference:
        return _display_upper_lower_limit(
            limit=self.aixm_lower_limit, reference=self.aixm_lower_limit_reference
        )

    class _AixmHorizontalProjection(BaseModel):
        aixm_elevated_surface: typing.Annotated[
            _AixmElevatedSurface, pydantic.Field(alias="aixm:ElevatedSurface")
        ]

    aixm_horizontal_projection: typing.Annotated[
        _AixmHorizontalProjection, pydantic.Field(alias="aixm:horizontalProjection")
    ]


class _AixmAirspaceGeometryComponent(WithAtGmlId):
    """https://aixm.aero/sites/default/files/imce/AIXM511HTML/AIXM/Class_AirspaceGeometryComponent.html"""

    class _AixmTheAirspaceVolume(BaseModel):
        aixm_airspace_volume: typing.Annotated[
            _AirspaceVolume, pydantic.Field(alias="aixm:AirspaceVolume")
        ]

    aixm_the_airspace_volume: typing.Annotated[
        _AixmTheAirspaceVolume, pydantic.Field(alias="aixm:theAirspaceVolume")
    ]


class _AixmGeometryComponentItem(BaseModel):
    aixm_airspace_geometry_component: typing.Annotated[
        _AixmAirspaceGeometryComponent,
        pydantic.Field(alias="aixm:AirspaceGeometryComponent"),
    ]

    @functools.cached_property
    def 高度上限(self) -> _LimitAndReference:
        return self.aixm_airspace_geometry_component.aixm_the_airspace_volume.aixm_airspace_volume.高度上限

    @functools.cached_property
    def 高度下限(self) -> _LimitAndReference:
        return self.aixm_airspace_geometry_component.aixm_the_airspace_volume.aixm_airspace_volume.高度下限


class AixmGeometryCompoents(pydantic.RootModel[list[_AixmGeometryComponentItem]]):
    root: list[_AixmGeometryComponentItem]


class Airspace(AixmTimeSlice, WithAixmAnnotation):
    """https://aixm.aero/sites/default/files/imce/AIXM511HTML/AIXM/Class_Airspace.html"""

    aixm_type: typing.Annotated[CodeAirspaceType, pydantic.Field(alias="aixm:type")]
    aixm_designator: typing.Annotated[
        CodeAirspaceDesignatorType, pydantic.Field(alias="aixm:designator")
    ]
    aixm_name: typing.Annotated[TextNameType, pydantic.Field(alias="aixm:name")]

    aixm_geometry_component: typing.Annotated[
        AixmGeometryCompoents, pydantic.Field(alias="aixm:geometryComponent")
    ]
