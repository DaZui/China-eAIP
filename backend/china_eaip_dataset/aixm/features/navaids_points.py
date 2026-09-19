from typing import Annotated

from pydantic import Field

from ...base import BaseModel, Link, Nil, WithAtGmlId
from ..abstract_feature import AixmTimeSlice
from ..data_types import (
    CodeAuralMorseType,
    CodeDesignatedPointDesignatorType,
    CodeDMEChannelType,
    CodeNavaidDesignatorType,
    CodeNavaidPurposeType,
    CodeNavaidServiceType,
    CodeNorthReferenceType,
    DateYearType,
    TextNameType,
    ValAngleType,
    ValFrequencyType,
    ValMagneticVariationType,
)
from .geometry import Point, WithAixmLocation
from .notes import WithAixmAnnotation


class DesignatedPoint(AixmTimeSlice):
    """https://aixm.aero/sites/default/files/imce/AIXM511HTML/AIXM/Class_DesignatedPoint.html"""

    aixm_designator: Annotated[
        CodeDesignatedPointDesignatorType, Field(alias="aixm:designator")
    ]
    aixm_name: Annotated[TextNameType, Field(alias="aixm:name")]

    class _AixmLocation(BaseModel):
        aixm_point: Annotated[Point, Field(alias="aixm:Point")]

    aixm_location: Annotated[_AixmLocation, Field(alias="aixm:location")]
    aixm_airport_heliport: Annotated[
        Link | None, Field(alias="aixm:airportHeliport")
    ] = None


class _NavaidEquipment(AixmTimeSlice, WithAixmAnnotation, WithAixmLocation):
    """https://aixm.aero/sites/default/files/imce/AIXM511HTML/AIXM/Class_NavaidEquipment.html"""

    aixm_designator: Annotated[CodeNavaidDesignatorType, Field(alias="aixm:designator")]
    aixm_name: Annotated[TextNameType, Field(alias="aixm:name")]
    aixm_magnetic_variation: Annotated[
        ValMagneticVariationType, Field(alias="aixm:magneticVariation")
    ]
    aixm_magnetic_variation_accuracy: Annotated[
        ValAngleType, Field(alias="aixm:magneticVariationAccuracy")
    ]
    aixm_date_magnetic_variation: Annotated[
        DateYearType, Field(alias="aixm:dateMagneticVariation")
    ]


class DME(_NavaidEquipment):
    """https://aixm.aero/sites/default/files/imce/AIXM511HTML/AIXM/Class_DME.html"""

    aixm_channel: Annotated[CodeDMEChannelType, Field(alias="aixm:channel")]


class Glidepath(_NavaidEquipment):
    """https://aixm.aero/sites/default/files/imce/AIXM511HTML/AIXM/Class_Glidepath.html"""

    aixm_frequency: Annotated[ValFrequencyType, Field(alias="aixm:frequency")]


class Localizer(Glidepath):
    """https://aixm.aero/sites/default/files/imce/AIXM511HTML/AIXM/Class_Localizer.html"""

    aixm_magnetic_bearing: Annotated[Nil, Field(alias="aixm:magneticBearing")]
    aixm_magneticBearingAccuracy: Annotated[
        ValAngleType, Field(alias="aixm:magneticBearingAccuracy")
    ]
    aixm_true_bearing: Annotated[Nil, Field(alias="aixm:trueBearing")]
    aixm_trueBearingAccuracy: Annotated[
        ValAngleType, Field(alias="aixm:trueBearingAccuracy")
    ]


class MarkerBeacon(Glidepath):
    """https://aixm.aero/sites/default/files/imce/AIXM511HTML/AIXM/Class_MarkerBeacon.html"""

    aixm_aural_morse_code: Annotated[
        CodeAuralMorseType, Field(alias="aixm:auralMorseCode")
    ]


class _NavaidOperationalStatus(WithAtGmlId, WithAixmAnnotation):
    """https://aixm.aero/sites/default/files/imce/AIXM511HTML/AIXM/Class_NavaidOperationalStatus.html"""


class Navaid(AixmTimeSlice, WithAixmLocation):
    """https://aixm.aero/sites/default/files/imce/AIXM511HTML/AIXM/Class_Navaid.html"""

    aixm_type: Annotated[CodeNavaidServiceType, Field(alias="aixm:type")]
    aixm_designator: Annotated[CodeNavaidDesignatorType, Field(alias="aixm:designator")]
    aixm_name: Annotated[TextNameType, Field(alias="aixm:name")]
    aixm_purpose: Annotated[CodeNavaidPurposeType, Field(alias="aixm:purpose")]
    aixm_served_airport: Annotated[
        list[Link], Field(default_factory=list, alias="aixm:servedAirport")
    ]

    class _AixmNavaidEquipmentItem(BaseModel):
        class _AixmNavaidComponent(WithAtGmlId):
            aixm_the_navaid_component: Annotated[
                Link, Field(alias="aixm:theNavaidEquipment")
            ]

        aixm_navaid_component: Annotated[
            _AixmNavaidComponent, Field(alias="aixm:NavaidComponent")
        ]

    aixm_navaid_equipment: Annotated[
        list[_AixmNavaidEquipmentItem],
        Field(default_factory=list, alias="aixm:navaidEquipment"),
    ]

    class _AixmAvailabilityItem(BaseModel):
        aixm_navaid_operational_status: Annotated[
            _NavaidOperationalStatus, Field(alias="aixm:NavaidOperationalStatus")
        ]

    aixm_availability: Annotated[
        list[_AixmAvailabilityItem],
        Field(default_factory=list, alias="aixm:availability"),
    ]


class NDB(Glidepath):
    """https://aixm.aero/sites/default/files/imce/AIXM511HTML/AIXM/Class_NDB.html"""


class VOR(Glidepath):
    """https://aixm.aero/sites/default/files/imce/AIXM511HTML/AIXM/Class_VOR.html"""

    aixm_zero_bearing_direction: Annotated[
        CodeNorthReferenceType, Field(alias="aixm:zeroBearingDirection")
    ]
