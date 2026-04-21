from typing import Annotated

from pydantic import Field

from ...base import BaseModel, Link, Nil, WithAtGmlId
from ..abstract_feature import AixmTimeSlice
from ..data_types import (
    CodeAirportHeliportDesignatorType,
    CodeAirportHeliportType,
    CodeDeclaredDistanceType,
    CodeFlightPurposeType,
    CodeFlightRuleType,
    CodeFlightType,
    CodeIATAType,
    CodeICAOType,
    CodeMilitaryOperationsType,
    CodeMilitaryStatusType,
    CodeRunwayPointRoleType,
    CodeYesNoType,
    DateType,
    DateYearType,
    MustValDistanceType,
    TextDesignatorType,
    TextNameType,
    ValAngleType,
    ValBearingType,
    ValDistanceType,
    ValDistanceVerticalType,
    ValMagneticVariationType,
    ValTemperatureType,
)
from .geometry import ElevatedPoint, WithAixmLocation
from .notes import WithAixmAnnotation


class FlightCharacteristic(WithAtGmlId):
    """https://aixm.aero/sites/default/files/imce/AIXM511HTML/AIXM/Class_FlightCharacteristic.html"""

    aixm_type: Annotated[CodeFlightType, Field(alias="aixm:type")]
    aixm_rule: Annotated[CodeFlightRuleType, Field(alias="aixm:rule")]
    aixm_military: Annotated[CodeMilitaryStatusType, Field(alias="aixm:military")]
    aixm_purpose: Annotated[CodeFlightPurposeType, Field(alias="aixm:purpose")]


class _City(WithAtGmlId):
    """https://aixm.aero/sites/default/files/imce/AIXM511HTML/AIXM/Class_City.html"""

    aixm_name: Annotated[TextNameType, Field(alias="aixm:name")]


class _ConditionCombination(WithAtGmlId):
    """https://aixm.aero/sites/default/files/imce/AIXM511HTML/AIXM/Class_ConditionCombination.html"""

    class _AixmFlightItem(BaseModel):
        aixm_flight_characteristic: Annotated[
            FlightCharacteristic, Field(alias="aixm:FlightCharacteristic")
        ]

    aixm_flight: Annotated[tuple[_AixmFlightItem], Field(alias="aixm:flight")]


class _UsageCondition(WithAtGmlId):
    """https://aixm.aero/sites/default/files/imce/AIXM511HTML/AIXM/Class_UsageCondition.html"""

    class _AixmSelection(BaseModel):
        aixm_condition_combination: Annotated[
            _ConditionCombination, Field(alias="aixm:ConditionCombination")
        ]

    aixm_selection: Annotated[_AixmSelection, Field(alias="aixm:selection")]


class _AirportHeliportUsage(_UsageCondition):
    """https://aixm.aero/sites/default/files/imce/AIXM511HTML/AIXM/Class_AirportHeliportUsage.html"""


class AirportHeliportAvailability(WithAtGmlId):
    """https://aixm.aero/sites/default/files/imce/AIXM511HTML/AIXM/Class_AirportHeliportAvailability.html"""

    class _AixmUsageItem(BaseModel):
        aixm_airport_heliport_usage: Annotated[
            _AirportHeliportUsage, Field(alias="aixm:AirportHeliportUsage")
        ]

    aixm_usage: Annotated[list[_AixmUsageItem], Field(alias="aixm:usage")]


class AirportHeliport(AixmTimeSlice, WithAixmAnnotation):
    """https://aixm.aero/sites/default/files/imce/AIXM511HTML/AIXM/Class_AirportHeliport.html"""

    aixm_designator: Annotated[
        CodeAirportHeliportDesignatorType, Field(alias="aixm:designator")
    ]
    aixm_name: Annotated[TextNameType, Field(alias="aixm:name")]
    aixm_location_indicator_icao: Annotated[
        CodeICAOType, Field(alias="aixm:locationIndicatorICAO")
    ]
    aixm_designator_iata: Annotated[CodeIATAType, Field(alias="aixm:designatorIATA")]
    aixm_type: Annotated[CodeAirportHeliportType, Field(alias="aixm:type")]
    aixm_certified_icao: Annotated[CodeYesNoType, Field(alias="aixm:certifiedICAO")]

    @property
    def aixm_certified_icao_bool(self) -> bool | None:
        if not isinstance(self.aixm_certified_icao, Nil):
            if self.aixm_certified_icao.dollar == "YES":
                return True
            if self.aixm_certified_icao.dollar == "NO":
                return False

    aixm_control_type: Annotated[
        CodeMilitaryOperationsType, Field(alias="aixm:controlType")
    ]
    aixm_field_elevation: Annotated[
        ValDistanceVerticalType, Field(alias="aixm:fieldElevation")
    ]
    aixm_field_elevation_accuracy: Annotated[
        Nil,  # 原为 ValDistanceVerticalType，实际未出现
        Field(alias="aixm:fieldElevationAccuracy"),
    ]
    aixm_magnetic_variation: Annotated[
        ValMagneticVariationType, Field(alias="aixm:magneticVariation")
    ]
    aixm_magnetic_variation_accuracy: Annotated[
        Nil,  # 原为 ValAngleType
        Field(alias="aixm:magneticVariationAccuracy"),
    ]
    aixm_date_magnetic_variation: Annotated[
        DateYearType, Field(alias="aixm:dateMagneticVariation")
    ]
    aixm_magnetic_variation_change: Annotated[
        Nil,  # 原为 ValMagneticVariationChangeType
        Field(alias="aixm:magneticVariationChange"),
    ]
    aixm_reference_temperature: Annotated[
        ValTemperatureType, Field(alias="aixm:referenceTemperature")
    ]
    aixm_certification_date: Annotated[DateType, Field(alias="aixm:certificationDate")]
    aixm_certification_expiration_date: Annotated[
        DateType, Field(alias="aixm:certificationExpirationDate")
    ]

    class _AixmArpItem(BaseModel):
        aixm_elevated_point: Annotated[ElevatedPoint, Field(alias="aixm:ElevatedPoint")]

    aixm_arp: Annotated[_AixmArpItem, Field(alias="aixm:ARP")]

    class _AixmServedCityItem(BaseModel):
        aixm_city: Annotated[_City, Field(alias="aixm:City")]

    aixm_served_city: Annotated[
        tuple[_AixmServedCityItem], Field(alias="aixm:servedCity")
    ]

    class _AixmAvailabilityItem(BaseModel):
        aixm_airport_heliport_availability: Annotated[
            AirportHeliportAvailability,
            Field(alias="aixm:AirportHeliportAvailability"),
        ]

    aixm_availability: Annotated[
        tuple[_AixmAvailabilityItem], Field(alias="aixm:availability")
    ]


class Runway(AixmTimeSlice, WithAixmAnnotation):
    """https://aixm.aero/sites/default/files/imce/AIXM511HTML/AIXM/Class_Runway.html"""

    aixm_designator: Annotated[TextDesignatorType, Field(alias="aixm:designator")]
    aixm_nominal_length: Annotated[
        MustValDistanceType,  # 原为 ValDistanceType
        Field(alias="aixm:nominalLength"),
    ]
    aixm_length_accuracy: Annotated[
        Nil,  # 原为 ValDistanceType
        Field(alias="aixm:lengthAccuracy"),
    ]
    aixm_nominal_width: Annotated[
        MustValDistanceType,  # 原为 ValDistanceType
        Field(alias="aixm:nominalWidth"),
    ]
    aixm_width_accuracy: Annotated[
        Nil,  # 原为 ValDistanceType
        Field(alias="aixm:widthAccuracy"),
    ]
    aixm_width_shoulder: Annotated[ValDistanceType, Field(alias="aixm:widthShoulder")]
    aixm_associated_airport_heliport: Annotated[
        Link, Field(alias="aixm:associatedAirportHeliport")
    ]


class _RunwayDeclaredDistanceValue(WithAtGmlId):
    """https://aixm.aero/sites/default/files/imce/AIXM511HTML/AIXM/Class_RunwayDeclaredDistanceValue.html"""

    aixm_distance: Annotated[ValDistanceType, Field(alias="aixm:distance")]
    aixm_distance_accuracy: Annotated[
        ValDistanceType, Field(alias="aixm:distanceAccuracy")
    ]


class RunwayDeclaredDistance(WithAtGmlId):
    """https://aixm.aero/sites/default/files/imce/AIXM511HTML/AIXM/Class_RunwayDeclaredDistance.html"""

    aixm_type: Annotated[CodeDeclaredDistanceType, Field(alias="aixm:type")]

    class _AixmDeclaredValueItem(BaseModel):
        aixm_runway_declared_distance_value: Annotated[
            _RunwayDeclaredDistanceValue,
            Field(alias="aixm:RunwayDeclaredDistanceValue"),
        ]

    aixm_declared_distance: Annotated[
        list[_AixmDeclaredValueItem], Field(alias="aixm:declaredValue")
    ]


class RunwayCentrelinePoint(AixmTimeSlice, WithAixmAnnotation, WithAixmLocation):
    """https://aixm.aero/sites/default/files/imce/AIXM511HTML/AIXM/Class_RunwayCentrelinePoint.html"""

    aixm_role: Annotated[CodeRunwayPointRoleType, Field(alias="aixm:role")]

    class _AixmAssociatedDeclaredDistanceItem(BaseModel):
        aixm_runway_declared_distance: Annotated[
            RunwayDeclaredDistance, Field(alias="aixm:RunwayDeclaredDistance")
        ]

    aixm_associated_declared_distance: Annotated[
        list[_AixmAssociatedDeclaredDistanceItem],
        Field(alias="aixm:associatedDeclaredDistance"),
    ]
    aixm_on_runway: Annotated[Link, Field(alias="aixm:onRunway")]


class RunwayDirection(AixmTimeSlice):
    aixm_designator: Annotated[TextDesignatorType, Field(alias="aixm:designator")]
    aixm_true_bearing: Annotated[ValBearingType, Field(alias="aixm:trueBearing")]

    @property
    def aixm_true_bearing_float(self) -> float | None:
        if not isinstance(self.aixm_true_bearing, Nil):
            return float(self.aixm_true_bearing.dollar)

    aixm_true_bearing_accuracy: Annotated[
        ValAngleType, Field(alias="aixm:trueBearingAccuracy")
    ]

    @property
    def aixm_true_bearing_accuracy_float(self) -> float | None:
        if not isinstance(self.aixm_true_bearing_accuracy, Nil):
            return float(self.aixm_true_bearing_accuracy.dollar)

    aixm_used_runway: Annotated[Link, Field(alias="aixm:usedRunway")]
