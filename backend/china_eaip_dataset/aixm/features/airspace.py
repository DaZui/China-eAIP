from typing import Annotated, Literal

from pydantic import Field

from ... import geojson
from ...base import (
    BaseModel,
    Link,
    Unit,
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
    CodeVerticalReferenceType,
    TextNameType,
    ValDistanceVerticalType,
)
from .notes import WithAixmAnnotation


class _WithAtNumDerivatives(BaseModel):
    at_num_derivative_interior: Annotated[
        Literal[0], Field(alias="@numDerivativeInterior")
    ]
    at_num_derivatives_at_end: Annotated[
        Literal[0], Field(alias="@numDerivativesAtEnd")
    ]
    at_num_derivatives_at_start: Annotated[
        Literal[0], Field(alias="@numDerivativesAtStart")
    ]


class _WithAtInterpolation[
    Inner: Literal["circularArcCenterPointWithRadius", "geodesic", "planar"]
](BaseModel):
    at_interpolation: Annotated[Inner, Field(alias="@interpolation")]


class _GmlPointProperty(Link):
    at_xlink_title: Annotated[str, Field(alias="@xlink:title")]


class _GmlCircleByCenterPointItem(
    _WithAtInterpolation[Literal["circularArcCenterPointWithRadius"]],
    _WithAtNumDerivatives,
):
    gml_pos: Annotated[
        WithDollar[tuple[geojson.Latitude, geojson.Longitude]] | None,
        Field(alias="gml:pos"),
    ] = None
    gml_point_property: Annotated[
        _GmlPointProperty | None, Field(alias="gml:pointProperty")
    ] = None
    at_num_arc: Annotated[Literal[1], Field(alias="@numArc")]
    gml_radius: Annotated[Unit[Literal["KM"], float], Field(alias="gml:radius")]


class _GmlArcByCenterPointItem(_GmlCircleByCenterPointItem):
    gml_end_angle: Annotated[Unit[Literal["deg"], float], Field(alias="gml:endAngle")]
    gml_start_angle: Annotated[
        Unit[Literal["deg"], float], Field(alias="gml:startAngle")
    ]


class _GmlGeodesicStringItem(
    _WithAtInterpolation[Literal["geodesic"]], _WithAtNumDerivatives
):
    gml_pos_list: Annotated[WithDollar[list[float]], Field(alias="gml:posList")]


class _GmlSegments(BaseModel):
    gml_arc_by_center_point: Annotated[
        list[_GmlArcByCenterPointItem], Field(alias="gml:ArcByCenterPoint")
    ] = []
    gml_circle_by_center_point: Annotated[
        list[_GmlCircleByCenterPointItem], Field(alias="gml:CircleByCenterPoint")
    ] = []
    gml_geodesic_string: Annotated[
        list[_GmlGeodesicStringItem], Field(alias="gml:GeodesicString")
    ] = []


class _AixmCurve(WithAtGmlId, WithAixmAnnotation):
    gml_segments: Annotated[_GmlSegments, Field(alias="gml:segments")]


class _GmlCurveMemberItem(WithAtOwns, WithAtXlinkType):
    aixm_curve: Annotated[_AixmCurve, Field(alias="aixm:Curve")]


class _GmlRing(BaseModel):
    gml_curve_member: Annotated[
        list[_GmlCurveMemberItem], Field(alias="gml:curveMember")
    ]


class _GmlExterior(BaseModel):
    gml_ring: Annotated[_GmlRing, Field(alias="gml:Ring")]


class _GmlPolygonPatchItem(_WithAtInterpolation[Literal["planar"]]):
    gml_exterior: Annotated[_GmlExterior, Field(alias="gml:exterior")]


class _GmlPatches(BaseModel):
    gml_polygon_patch: Annotated[
        list[_GmlPolygonPatchItem], Field(alias="gml:PolygonPatch")
    ]


class _AixmElevatedSurface(WithAtGmlId, WithAtSrsName):
    gml_patches: Annotated[_GmlPatches, Field(alias="gml:patches")]


class _AixmHorizontalProjection(BaseModel):
    aixm_elevated_surface: Annotated[
        _AixmElevatedSurface, Field(alias="aixm:ElevatedSurface")
    ]


class _AirspaceVolume(WithAtGmlId):
    aixm_upper_limit: Annotated[ValDistanceVerticalType, Field(alias="aixm:upperLimit")]
    aixm_upper_limit_reference: Annotated[
        CodeVerticalReferenceType, Field(alias="aixm:upperLimitReference")
    ]
    aixm_lower_limit: Annotated[ValDistanceVerticalType, Field(alias="aixm:lowerLimit")]
    aixm_lower_limit_reference: Annotated[
        CodeVerticalReferenceType, Field(alias="aixm:lowerLimitReference")
    ]
    aixm_horizontal_projection: Annotated[
        _AixmHorizontalProjection, Field(alias="aixm:horizontalProjection")
    ]


class Airspace(AixmTimeSlice, WithAixmAnnotation):
    """https://aixm.aero/sites/default/files/imce/AIXM511HTML/AIXM/Class_Airspace.html"""

    aixm_type: Annotated[CodeAirspaceType, Field(alias="aixm:type")]
    aixm_designator: Annotated[
        CodeAirspaceDesignatorType, Field(alias="aixm:designator")
    ]
    aixm_name: Annotated[TextNameType, Field(alias="aixm:name")]

    class _AixmGeometryComponentItem(BaseModel):
        class _AixmAirspaceGeometryComponent(WithAtGmlId):
            class _AixmTheAirspaceVolume(BaseModel):
                aixm_airspace_volume: Annotated[
                    _AirspaceVolume, Field(alias="aixm:AirspaceVolume")
                ]

            aixm_the_airspace_volume: Annotated[
                _AixmTheAirspaceVolume, Field(alias="aixm:theAirspaceVolume")
            ]

        aixm_airspace_geometry_component: Annotated[
            _AixmAirspaceGeometryComponent,
            Field(alias="aixm:AirspaceGeometryComponent"),
        ]

    aixm_geometry_component: Annotated[
        list[_AixmGeometryComponentItem], Field(alias="aixm:geometryComponent")
    ] = []
