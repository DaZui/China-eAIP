from typing import Annotated

from pydantic import Field

from ...base import BaseModel, Link, WithAtGmlId
from ..abstract_feature import AixmTimeSlice
from ..data_types import (
    CodeATCReportingType,
    CodeDirectionType,
    CodeFlightRuleType,
    CodeRNPType,
    CodeRouteDesignatorLetterType,
    CodeRouteNavigationType,
    CodeRouteType,
    CodeVerticalReferenceType,
    NoNumberType,
    ValBearingType,
    ValDistanceType,
    ValDistanceVerticalType,
)
from .notes import WithAixmAnnotation


class _SegmentPoint(WithAtGmlId):
    """https://aixm.aero/sites/default/files/imce/AIXM511HTML/AIXM/Class_SegmentPoint.html"""

    aixm_reporting_atc: Annotated[
        CodeATCReportingType, Field(alias="aixm:reportingATC")
    ]
    aixm_point_choice_fix_designated_point: Annotated[
        Link | None, Field(alias="aixm:pointChoice_fixDesignatedPoint")
    ] = None
    aixm_point_choice_navaid_system: Annotated[
        Link | None, Field(alias="aixm:pointChoice_navaidSystem")
    ] = None


class _EnRouteSegmentPoint(_SegmentPoint):
    """https://aixm.aero/sites/default/files/imce/AIXM511HTML/AIXM/Class_EnRouteSegmentPoint.html"""


class Route(AixmTimeSlice, WithAixmAnnotation):
    aixm_designator_second_letter: Annotated[
        CodeRouteDesignatorLetterType, Field(alias="aixm:designatorSecondLetter")
    ]
    aixm_designator_number: Annotated[
        NoNumberType, Field(alias="aixm:designatorNumber")
    ]
    aixm_type: Annotated[CodeRouteType, Field(alias="aixm:type")]
    aixm_flight_rule: Annotated[CodeFlightRuleType, Field(alias="aixm:flightRule")]


class _RouteAvailability(WithAtGmlId):
    aixm_direction: Annotated[CodeDirectionType, Field(alias="aixm:direction")]


class RouteSegment(AixmTimeSlice, WithAixmAnnotation):
    aixm_upper_limit: Annotated[ValDistanceVerticalType, Field(alias="aixm:upperLimit")]
    aixm_upper_limit_reference: Annotated[
        CodeVerticalReferenceType, Field(alias="aixm:upperLimitReference")
    ]
    aixm_lower_limit: Annotated[ValDistanceVerticalType, Field(alias="aixm:lowerLimit")]
    aixm_lower_limit_reference: Annotated[
        CodeVerticalReferenceType, Field(alias="aixm:lowerLimitReference")
    ]
    aixm_minimum_obstacle_clearance_altitude: Annotated[
        ValDistanceVerticalType, Field(alias="aixm:minimumObstacleClearanceAltitude")
    ]
    aixm_magnetic_track: Annotated[ValBearingType, Field(alias="aixm:magneticTrack")]
    aixm_reverse_magnetic_track: Annotated[
        ValBearingType, Field(alias="aixm:reverseMagneticTrack")
    ]
    aixm_length: Annotated[ValDistanceType, Field(alias="aixm:length")]
    aixm_minimum_enroute_altitude: Annotated[
        ValDistanceVerticalType, Field(alias="aixm:minimumEnrouteAltitude")
    ]
    aixm_navigation_type: Annotated[
        CodeRouteNavigationType, Field(alias="aixm:navigationType")
    ]
    aixm_required_navigation_performance: Annotated[
        CodeRNPType, Field(alias="aixm:requiredNavigationPerformance")
    ]

    class _AixmEndStart(BaseModel):
        aixm_en_route_segment_point: Annotated[
            _EnRouteSegmentPoint, Field(alias="aixm:EnRouteSegmentPoint")
        ]

    aixm_start: Annotated[_AixmEndStart, Field(alias="aixm:start")]
    aixm_end: Annotated[_AixmEndStart, Field(alias="aixm:end")]
    aixm_route_formed: Annotated[Link, Field(alias="aixm:routeFormed")]

    class _AixmAvailabilityItem(BaseModel):
        aixm_route_availability: Annotated[
            _RouteAvailability, Field(alias="aixm:RouteAvailability")
        ]

    aixm_availability: Annotated[
        list[_AixmAvailabilityItem], Field(alias="aixm:availability")
    ]
