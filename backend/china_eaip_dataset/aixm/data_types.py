import datetime
import decimal
from typing import Annotated, Literal

from pydantic import Field, StringConstraints

from ..base import Nil, WithDollar

type _AlphaType = Annotated[str, StringConstraints(pattern=r"^[A-Z]*$")]
"""https://aixm.aero/sites/default/files/imce/AIXM511HTML/AIXM/DataType_AlphaType.html"""
type _AlphanumericType = Annotated[str, StringConstraints(pattern=r"^([A-Z]|\d)*$")]
"""https://aixm.aero/sites/default/files/imce/AIXM511HTML/AIXM/DataType_AlphanumericType.html"""
type CodeAirportHeliportDesignatorBaseType = Annotated[
    _AlphanumericType, StringConstraints(min_length=3, max_length=6)
]
"""https://aixm.aero/sites/default/files/imce/AIXM511HTML/AIXM/DataType_CodeAirportHeliportDesignatorBaseType.html"""
type CodeAirportHeliportDesignatorType = (
    Nil | WithDollar[CodeAirportHeliportDesignatorBaseType]
)
"""https://aixm.aero/sites/default/files/imce/AIXM511HTML/AIXM/DataType_CodeAirportHeliportDesignatorType.html"""
type _CodeFlightBaseType = Literal["OAT", "GAT", "ALL", "OTHER"]
"""https://aixm.aero/sites/default/files/imce/AIXM511HTML/AIXM/DataType_CodeFlightBaseType.html"""
type CodeFlightType = Nil | WithDollar[_CodeFlightBaseType]
"""https://aixm.aero/sites/default/files/imce/AIXM511HTML/AIXM/DataType_CodeFlightType.html"""
type _CodeFlightRuleBaseType = Literal["IFR", "VFR", "ALL", "OTHER"]
"""https://aixm.aero/sites/default/files/imce/AIXM511HTML/AIXM/DataType_CodeFlightRuleBaseType.html"""
type CodeFlightRuleType = Nil | WithDollar[_CodeFlightRuleBaseType]
"""https://aixm.aero/sites/default/files/imce/AIXM511HTML/AIXM/DataType_CodeFlightRuleType.html"""
type _CodeMilitaryStatusBaseType = Literal["MIL", "CIVIL", "ALL", "OTHER"]
"""https://aixm.aero/sites/default/files/imce/AIXM511HTML/AIXM/DataType_CodeMilitaryStatusBaseType.html"""
type CodeMilitaryStatusType = Nil | WithDollar[_CodeMilitaryStatusBaseType]
"""https://aixm.aero/sites/default/files/imce/AIXM511HTML/AIXM/DataType_CodeMilitaryStatusType.html"""
type _CodeFlightPurposeBaseType = (
    Literal["SCHEDULED", "NON_SCHEDULED", "PRIVATE", "AIR_TRAINING"]
    | Literal["AIR_WORK", "ALL", "PARTICIPANT", "OTHER"]
)
"""https://aixm.aero/sites/default/files/imce/AIXM511HTML/AIXM/DataType_CodeFlightPurposeBaseType.html"""
type CodeFlightPurposeType = Nil | WithDollar[_CodeFlightPurposeBaseType]
"""https://aixm.aero/sites/default/files/imce/AIXM511HTML/AIXM/DataType_CodeFlightPurposeType.html"""
type CodeIATABaseType = Annotated[
    _AlphaType, StringConstraints(min_length=3, max_length=3)
]
"""https://aixm.aero/sites/default/files/imce/AIXM511HTML/AIXM/DataType_CodeIATABaseType.html"""
type CodeIATAType = Nil | WithDollar[CodeIATABaseType]
"""https://aixm.aero/sites/default/files/imce/AIXM511HTML/AIXM/DataType_CodeIATAType.html"""
type CodeICAOBaseType = Annotated[
    _AlphaType, StringConstraints(min_length=4, max_length=4)
]
"""https://aixm.aero/sites/default/files/imce/AIXM511HTML/AIXM/DataType_CodeICAOBaseType.html"""
type CodeICAOType = Nil | WithDollar[CodeICAOBaseType]
"""https://aixm.aero/sites/default/files/imce/AIXM511HTML/AIXM/DataType_CodeICAOType.html"""
type _CodeAirportHeliportBaseType = Literal["AD", "AH", "HP", "LS", "OTHER"]
"""https://aixm.aero/sites/default/files/imce/AIXM511HTML/AIXM/DataType_CodeAirportHeliportBaseType.html"""
type CodeAirportHeliportType = Nil | WithDollar[_CodeAirportHeliportBaseType]
"""https://aixm.aero/sites/default/files/imce/AIXM511HTML/AIXM/DataType_CodeAirportHeliportType.html"""
type _CodeYesNoBaseType = Literal["YES", "NO", "OTHER"]
"""https://aixm.aero/sites/default/files/imce/AIXM511HTML/AIXM/DataType_CodeYesNoBaseType.html"""
type CodeYesNoType = Nil | WithDollar[_CodeYesNoBaseType]
"""https://aixm.aero/sites/default/files/imce/AIXM511HTML/AIXM/DataType_CodeYesNoType.html"""
type _CodeMilitaryOperationsBaseType = Literal["CIVIL", "MIL", "JOINT", "OTHER"]
"""https://aixm.aero/sites/default/files/imce/AIXM511HTML/AIXM/DataType_CodeMilitaryOperationsBaseType.html"""
type CodeMilitaryOperationsType = Nil | WithDollar[_CodeMilitaryOperationsBaseType]
"""https://aixm.aero/sites/default/files/imce/AIXM511HTML/AIXM/DataType_CodeMilitaryOperationsType.html"""
type _ValDistanceBaseType = Annotated[decimal.Decimal, Field(ge=0)]
"""https://aixm.aero/sites/default/files/imce/AIXM511HTML/AIXM/DataType_ValDistanceBaseType.html"""
type _UomDistanceType = Literal["NM", "KM", "M", "FT", "MI", "CM", "OTHER"]
"""https://aixm.aero/sites/default/files/imce/AIXM511HTML/AIXM/DataType_UomDistanceType.html"""


class _ValDistanceTypeInner(WithDollar[_ValDistanceBaseType]):
    at_uom: Annotated[_UomDistanceType, Field(alias="@uom")] = "M"

    def __str__(self) -> str:
        return f"{self.dollar} {self.at_uom}"

    @property
    def in_m(self) -> float:
        return float(self.dollar) * CONVERT_TO_METER[self.at_uom]


type ValDistanceType = Nil | _ValDistanceTypeInner
"""https://aixm.aero/sites/default/files/imce/AIXM511HTML/AIXM/DataType_ValDistanceVerticalType.html"""
type ValDistanceVerticalBaseType = (
    decimal.Decimal | Literal["UNL", "GND", "FLOOR", "CEILING"]
)
"""https://aixm.aero/sites/default/files/imce/AIXM511HTML/AIXM/DataType_ValDistanceVerticalBaseType.html"""
type UomDistanceVerticalType = Literal["FT", "M", "FL", "SM", "OTHER"]
"""https://aixm.aero/sites/default/files/imce/AIXM511HTML/AIXM/DataType_UomDistanceVerticalType.html"""
CONVERT_TO_METER: dict[_UomDistanceType | UomDistanceVerticalType, float] = {
    "CM": 0.01,
    "FL": 30.48,
    "FT": 0.3048,
    "KM": 1000,
    "M": 1,
    "MI": 1609.344,
    "NM": 1852,
    "OTHER": 0,
    "SM": 10,
}


class _ValDistanceVerticalTypeInner(WithDollar[ValDistanceVerticalBaseType]):
    at_uom: Annotated[UomDistanceVerticalType, Field(alias="@uom")] = "M"

    def __str__(self) -> str:
        return f"{self.dollar} {self.at_uom}"

    @property
    def in_m(self) -> float:
        if self.dollar in ("UNL", "GND", "FLOOR", "CEILING"):
            return 0
        return float(self.dollar) * CONVERT_TO_METER[self.at_uom]

    @property
    def text(self) -> str:
        if self.dollar == "GND":
            return "GND: the Surface of the Earth"
        if self.dollar == "UNL":
            return "UNL: unlimited"
        if self.dollar == "FLOOR":
            return "FLOOR: the bottom of the airspace"
        if self.dollar == "CEILING":
            return "CEILING: the top of the airspace"

        return f"{self.in_m:.1f} m / {self.in_m / CONVERT_TO_METER['FT']:.1f} ft / FL{self.in_m / CONVERT_TO_METER['FL']:.0f}"


type ValDistanceVerticalType = Nil | _ValDistanceVerticalTypeInner
"""https://aixm.aero/sites/default/files/imce/AIXM511HTML/AIXM/DataType_ValDistanceVerticalType.html"""
type _ValMagneticVariationBaseType = Annotated[decimal.Decimal, Field(ge=-180, le=180)]
"""https://aixm.aero/sites/default/files/imce/AIXM511HTML/AIXM/DataType_ValMagneticVariationBaseType.html"""
type ValMagneticVariationType = Nil | WithDollar[_ValMagneticVariationBaseType]
"""https://aixm.aero/sites/default/files/imce/AIXM511HTML/AIXM/DataType_ValMagneticVariationType.html"""
type _ValAngleBaseType = Annotated[decimal.Decimal, Field(ge=-180, le=180)]
"""https://aixm.aero/sites/default/files/imce/AIXM511HTML/AIXM/DataType_ValAngleBaseType.html"""
type ValAngleType = Nil | WithDollar[_ValAngleBaseType]
"""https://aixm.aero/sites/default/files/imce/AIXM511HTML/AIXM/DataType_ValAngleType.html"""
type _DateYearBaseType = Annotated[
    str, StringConstraints(pattern=r"^[1-9][0-9][0-9][0-9]$")
]
"""https://aixm.aero/sites/default/files/imce/AIXM511HTML/AIXM/DataType_DateYearBaseType.html"""
type DateYearType = Nil | WithDollar[_DateYearBaseType]
"""https://aixm.aero/sites/default/files/imce/AIXM511HTML/AIXM/DataType_DateYearType.html"""
type _ValMagneticVariationChangeBaseType = Annotated[
    decimal.Decimal, Field(ge=-180, le=180)
]
"""https://aixm.aero/sites/default/files/imce/AIXM511HTML/AIXM/DataType_ValMagneticVariationChangeBaseType.html"""
type ValMagneticVariationChangeType = (
    Nil | WithDollar[_ValMagneticVariationChangeBaseType]
)
"""https://aixm.aero/sites/default/files/imce/AIXM511HTML/AIXM/DataType_ValMagneticVariationChangeType.html"""
type _DateBaseType = datetime.date
"""https://aixm.aero/sites/default/files/imce/AIXM511HTML/AIXM/DataType_DateBaseType.html"""
type DateType = Nil | WithDollar[_DateBaseType]
"""https://aixm.aero/sites/default/files/imce/AIXM511HTML/AIXM/DataType_DateType.html"""
type _ValTemperatureBaseType = decimal.Decimal
"""https://aixm.aero/sites/default/files/imce/AIXM511HTML/AIXM/DataType_ValTemperatureBaseType.html"""
type _UomTemperatureType = Literal["C", "F", "K", "OTHER"]
"""https://aixm.aero/sites/default/files/imce/AIXM511HTML/AIXM/DataType_UomTemperatureType.html"""


class _ValTemperatureTypeInner(WithDollar[_ValTemperatureBaseType]):
    at_uom: Annotated[_UomTemperatureType, Field(alias="@uom")]

    def __str__(self) -> str:
        return f"{self.dollar} {self.at_uom}"

    @property
    def in_celsius(self) -> float:
        subtract: float = {"K": 273.15, "F": 32}.get(self.at_uom, 0)
        return (float(self.dollar) - subtract) * {"F": 5 / 9}.get(self.at_uom, 1)


type ValTemperatureType = Nil | _ValTemperatureTypeInner
"""https://aixm.aero/sites/default/files/imce/AIXM511HTML/AIXM/DataType_ValTemperatureType.html"""
type _TextPropertyNameBaseType = Annotated[
    str, StringConstraints(min_length=1, max_length=60, pattern=r"^[A-Za-z\-_]*$")
]
"""https://aixm.aero/sites/default/files/imce/AIXM511HTML/AIXM/DataType_TextPropertyNameBaseType.html"""
type TextPropertyNameType = Nil | WithDollar[_TextPropertyNameBaseType]
"""https://aixm.aero/sites/default/files/imce/AIXM511HTML/AIXM/DataType_TextPropertyNameType.html"""
type _CodeNotePurposeBaseType = Literal[
    "DESCRIPTION", "REMARK", "WARNING", "DISCLAIMER"
]
"""https://aixm.aero/sites/default/files/imce/AIXM511HTML/AIXM/DataType_CodeNotePurposeBaseType.html"""
type CodeNotePurposeType = Nil | WithDollar[_CodeNotePurposeBaseType]
"""https://aixm.aero/sites/default/files/imce/AIXM511HTML/AIXM/DataType_CodeNotePurposeType.html"""
type Character2Type = str
"""https://aixm.aero/sites/default/files/imce/AIXM511HTML/AIXM/DataType_Character2Type.html"""
type TextNoteBaseType = Annotated[
    Character2Type, StringConstraints(min_length=1, max_length=10000)
]
"""https://aixm.aero/sites/default/files/imce/AIXM511HTML/AIXM/DataType_TextNoteBaseType.html"""


class _TextNoteTypeInner(WithDollar[TextNoteBaseType]):
    """https://aixm.aero/sites/default/files/imce/AIXM511HTML/AIXM/DataType_TextNoteType.html"""

    at_lang: Annotated[str, Field(alias="@lang")]


type TextNoteType = Nil | _TextNoteTypeInner
"""https://aixm.aero/sites/default/files/imce/AIXM511HTML/AIXM/DataType_TextNoteType.html"""
type _Character3Type = Annotated[
    str,
    StringConstraints(
        pattern=r"^([A-Z]|[0-9]|[, !\"&#$%'\(\)\*\+\-\./:;<=>\?@\[\\\]\^_\|\{\}])*$"
    ),
]
"""https://aixm.aero/sites/default/files/imce/AIXM511HTML/AIXM/DataType_Character3Type.html"""
type TextNameBaseType = Annotated[
    _Character3Type, StringConstraints(min_length=1, max_length=60)
]
"""https://aixm.aero/sites/default/files/imce/AIXM511HTML/AIXM/DataType_TextNameBaseType.html"""
type TextNameType = Nil | WithDollar[TextNameBaseType]
"""https://aixm.aero/sites/default/files/imce/AIXM511HTML/AIXM/DataType_TextNameType.html"""
type _CodeAirspaceBaseType = (
    Literal["NAS", "FIR", "FIR_P", "UIR", "UIR_P", "CTA", "CTA_P", "OCA_P", "OCA", "P"]
    | Literal["UTA", "UTA_P", "TMA", "TMA_P", "CTR", "CTR_P", "OTA", "SECTOR", "ATZ_P"]
    | Literal["SECTOR_C", "TSA", "CBA", "RCA", "RAS", "AWY", "MTR", "POLITICAL", "HTZ"]
    | Literal["R", "D", "ADIZ", "NO_FIR", "PART", "CLASS", "D_OTHER", "NAS_P", "OTHER"]
    | Literal["TRA", "A", "W", "PROTECT", "AMA", "ASR", "ADV", "UADV", "ATZ"]
)
"""https://aixm.aero/sites/default/files/imce/AIXM511HTML/AIXM/DataType_CodeAirspaceBaseType.html"""
type CodeAirspaceType = Nil | WithDollar[_CodeAirspaceBaseType]
"""https://aixm.aero/sites/default/files/imce/AIXM511HTML/AIXM/DataType_CodeAirspaceType.html"""
type CodeAirspaceDesignatorBaseType = Annotated[
    _Character3Type, StringConstraints(min_length=1, max_length=13)
    # 原为 10，因 ZYHBAP02(05) 改为 12，因 ZYTLAP02(10)1 改为 13
]
"""https://aixm.aero/sites/default/files/imce/AIXM511HTML/AIXM/DataType_CodeAirspaceDesignatorBaseType.html"""
type CodeAirspaceDesignatorType = Nil | WithDollar[CodeAirspaceDesignatorBaseType]
"""https://aixm.aero/sites/default/files/imce/AIXM511HTML/AIXM/DataType_CodeAirspaceDesignatorType.html"""
type CodeVerticalReferenceBaseType = Literal["SFC", "MSL", "W84", "STD", "OTHER"]
"""https://aixm.aero/sites/default/files/imce/AIXM511HTML/AIXM/DataType_CodeVerticalReferenceBaseType.html"""
type CodeVerticalReferenceType = Nil | WithDollar[CodeVerticalReferenceBaseType]
"""https://aixm.aero/sites/default/files/imce/AIXM511HTML/AIXM/DataType_CodeVerticalReferenceType.html"""
type CodeLanguageBaseType = Annotated[str, StringConstraints(pattern=r"^[a-z]{3}$")]
"""https://aixm.aero/sites/default/files/imce/AIXM511HTML/AIXM/DataType_CodeLanguageBaseType.html"""
type CodeLanguageType = Nil | WithDollar[CodeLanguageBaseType]
"""https://aixm.aero/sites/default/files/imce/AIXM511HTML/AIXM/DataType_CodeLanguageType.html"""
type CodeDesignatedPointDesignatorBaseType = (
    Annotated[_AlphanumericType, StringConstraints(min_length=1, max_length=5)]
    | Literal["****"]  # 原无，中国版有
)
"""https://aixm.aero/sites/default/files/imce/AIXM511HTML/AIXM/DataType_CodeDesignatedPointDesignatorBaseType.html"""
type CodeDesignatedPointDesignatorType = (
    Nil | WithDollar[CodeDesignatedPointDesignatorBaseType]
)
"""https://aixm.aero/sites/default/files/imce/AIXM511HTML/AIXM/DataType_CodeDesignatedPointDesignatorType.html"""
type CodeNavaidDesignatorBaseType = Annotated[
    _AlphanumericType, StringConstraints(min_length=1, max_length=4)
]
"""https://aixm.aero/sites/default/files/imce/AIXM511HTML/AIXM/DataType_CodeNavaidDesignatorBaseType.html"""
type CodeNavaidDesignatorType = Nil | WithDollar[CodeNavaidDesignatorBaseType]
"""https://aixm.aero/sites/default/files/imce/AIXM511HTML/AIXM/DataType_CodeNavaidDesignatorType.html"""
type CodeVerticalDatumBaseType = Literal["EGM_96", "AHD", "NAVD88", "OTHER"]
"""https://aixm.aero/sites/default/files/imce/AIXM511HTML/AIXM/DataType_CodeVerticalDatumBaseType.html"""
type CodeVerticalDatumType = Nil | WithDollar[CodeVerticalDatumBaseType]
"""https://aixm.aero/sites/default/files/imce/AIXM511HTML/AIXM/DataType_CodeVerticalDatumType.html"""
type CodeDMEChannelBaseType = (
    Annotated[str, StringConstraints(pattern=r"^[1-9][XY]$")]
    | Annotated[str, StringConstraints(pattern=r"^[1,5-7]\d[XY]$")]
    | Annotated[str, StringConstraints(pattern=r"^[2-4,8-9]\d[XYZ]$")]
    | Annotated[str, StringConstraints(pattern=r"^1[0-1]\d[XYZ]$")]
    | Annotated[str, StringConstraints(pattern=r"^12[0-6][XY]$")]
    | Annotated[str, StringConstraints(pattern=r"^[2-4][02468]W$")]
    | Annotated[str, StringConstraints(pattern=r"^5[0-6]Z$")]
    | Literal["50W", "52W", "54W", "56W", "17Z", "18Z", "19Z", "18W", "OTHER"]
)
"""https://aixm.aero/sites/default/files/imce/AIXM511HTML/AIXM/DataType_CodeDMEChannelBaseType.html"""
type CodeDMEChannelType = Nil | WithDollar[CodeDMEChannelBaseType]
"""https://aixm.aero/sites/default/files/imce/AIXM511HTML/AIXM/DataType_CodeDMEChannelType.html"""
type _ValFrequencyBaseType = Annotated[decimal.Decimal, Field(gt=0)]
"""https://aixm.aero/sites/default/files/imce/AIXM511HTML/AIXM/DataType_ValFrequencyBaseType.html"""
type _UomFrequencyType = Literal["HZ", "KHZ", "MHZ", "GHZ", "OTHER"]
"""https://aixm.aero/sites/default/files/imce/AIXM511HTML/AIXM/DataType_UomFrequencyType.html"""


class _ValFrequencyTypeInner(WithDollar[_ValFrequencyBaseType]):
    at_uom: Annotated[_UomFrequencyType, Field(alias="@uom")]

    def __str__(self) -> str:
        return f"{self.dollar} {self.at_uom}"

    @property
    def in_hz(self) -> float:
        return float(self.dollar) * {"KHZ": 1e3, "MHZ": 1e6, "GHZ": 1e9}.get(
            self.at_uom, 1
        )


type ValFrequencyType = Nil | _ValFrequencyTypeInner
"""https://aixm.aero/sites/default/files/imce/AIXM511HTML/AIXM/DataType_ValFrequencyType.html"""
type _ValBearingBaseType = Annotated[decimal.Decimal, Field(ge=0, le=360)]
"""https://aixm.aero/sites/default/files/imce/AIXM511HTML/AIXM/DataType_ValBearingBaseType.html"""
type ValBearingType = Nil | WithDollar[_ValBearingBaseType]
"""https://aixm.aero/sites/default/files/imce/AIXM511HTML/AIXM/DataType_ValBearingType.html"""
type _CodeAuralMorseBaseType = Annotated[str, StringConstraints(pattern=r"^([\-\.]*)$")]
"""https://aixm.aero/sites/default/files/imce/AIXM511HTML/AIXM/DataType_CodeAuralMorseBaseType.html"""
type CodeAuralMorseType = Nil | WithDollar[_CodeAuralMorseBaseType]
"""https://aixm.aero/sites/default/files/imce/AIXM511HTML/AIXM/DataType_CodeAuralMorseType.html"""
type _CodeNavaidServiceBaseType = (
    Literal["VOR", "DME", "NDB", "TACAN", "MKR", "ILS", "ILS_DME", "MLS", "MLS_DME"]
    | Literal["VOR_DME", "NDB_DME", "TLS", "LOC", "LOC_DME", "NDB_MKR", "DF", "SDF"]
    | Literal["VORTAC", "OTHER"]
)
"""https://aixm.aero/sites/default/files/imce/AIXM511HTML/AIXM/DataType_CodeNavaidServiceBaseType.html"""
type CodeNavaidServiceType = Nil | WithDollar[_CodeNavaidServiceBaseType]
"""https://aixm.aero/sites/default/files/imce/AIXM511HTML/AIXM/DataType_CodeNavaidServiceType.html"""
type CodeNavaidPurposeBaseType = Literal["TERMINAL", "ENROUTE", "ALL", "OTHER"]
"""https://aixm.aero/sites/default/files/imce/AIXM511HTML/AIXM/DataType_CodeNavaidPurposeBaseType.html"""
type CodeNavaidPurposeType = Nil | WithDollar[CodeNavaidPurposeBaseType]
"""https://aixm.aero/sites/default/files/imce/AIXM511HTML/AIXM/DataType_CodeNavaidPurposeType.html"""
type _CodeRouteDesignatorLetterBaseType = (
    Literal["A", "B", "G", "H", "J", "L", "M", "N", "P", "Q", "R", "T", "V", "W", "Y"]
    | Literal["Z", "OTHER"]
)
"""https://aixm.aero/sites/default/files/imce/AIXM511HTML/AIXM/DataType_CodeRouteDesignatorLetterBaseType.html"""
type CodeRouteDesignatorLetterType = (
    Nil | WithDollar[_CodeRouteDesignatorLetterBaseType]
)
"""https://aixm.aero/sites/default/files/imce/AIXM511HTML/AIXM/DataType_CodeRouteDesignatorLetterType.html"""
type _NoNumberBaseType = Annotated[int, Field(ge=0)]
"""https://aixm.aero/sites/default/files/imce/AIXM511HTML/AIXM/DataType_NoNumberBaseType.html"""
type NoNumberType = Nil | WithDollar[_NoNumberBaseType]
"""https://aixm.aero/sites/default/files/imce/AIXM511HTML/AIXM/DataType_NoNumberType.html"""
type _CodeRouteBaseType = Literal["ATS", "NAT", "OTHER"]
"""https://aixm.aero/sites/default/files/imce/AIXM511HTML/AIXM/DataType_CodeRouteBaseType.html"""
type CodeRouteType = Nil | WithDollar[_CodeRouteBaseType]
"""https://aixm.aero/sites/default/files/imce/AIXM511HTML/AIXM/DataType_CodeRouteType.html"""
type _CodeRouteNavigationBaseType = Literal[
    "CONV", "RNAV", "TACAN", "OTHER", "OTHER:RNP"  # 中国特有
]
"""https://aixm.aero/sites/default/files/imce/AIXM511HTML/AIXM/DataType_CodeRouteNavigationBaseType.html"""
type CodeRouteNavigationType = Nil | WithDollar[_CodeRouteNavigationBaseType]
"""https://aixm.aero/sites/default/files/imce/AIXM511HTML/AIXM/DataType_CodeRouteNavigationType.html"""
type _CodeRNPBaseType = Annotated[
    decimal.Decimal, Field(ge=0, le=99.9, multiple_of=0.1)
]
"""https://aixm.aero/sites/default/files/imce/AIXM511HTML/AIXM/DataType_CodeRNPBaseType.html"""
type CodeRNPType = Nil | WithDollar[_CodeRNPBaseType]
"""https://aixm.aero/sites/default/files/imce/AIXM511HTML/AIXM/DataType_CodeRNPType.html"""
type _TextDesignatorBaseType = Annotated[
    _Character3Type, StringConstraints(min_length=1, max_length=16)
]
"""https://aixm.aero/sites/default/files/imce/AIXM511HTML/AIXM/DataType_TextDesignatorBaseType.html"""
type TextDesignatorType = Nil | WithDollar[_TextDesignatorBaseType]
"""https://aixm.aero/sites/default/files/imce/AIXM511HTML/AIXM/DataType_TextDesignatorType.html"""
type _CodeRunwayPointRoleBaseType = (
    Literal["ABEAM_ELEVATION", "ABEAM_GLIDESLOPE", "ABEAM_PAR", "ABEAM_RER", "DISTHR"]
    | Literal["ABEAM_TDR", "START_RUN", "LAHSO", "OTHER", "START", "END", "MID", "TDZ"]
    | Literal["THR"]
)
"""https://aixm.aero/sites/default/files/imce/AIXM511HTML/AIXM/DataType_CodeRunwayPointRoleBaseType.html"""
type CodeRunwayPointRoleType = Nil | WithDollar[_CodeRunwayPointRoleBaseType]
"""https://aixm.aero/sites/default/files/imce/AIXM511HTML/AIXM/DataType_CodeRunwayPointRoleType.html"""
type _CodeDeclaredDistanceBaseType = Literal[
    "LDA", "TORA", "TODA", "ASDA", "DTHR", "TODAH", "RTODAH", "LDAH", "OTHER"
]
"""https://aixm.aero/sites/default/files/imce/AIXM511HTML/AIXM/DataType_CodeDeclaredDistanceBaseType.html"""
type CodeDeclaredDistanceType = Nil | WithDollar[_CodeDeclaredDistanceBaseType]
"""https://aixm.aero/sites/default/files/imce/AIXM511HTML/AIXM/DataType_CodeDeclaredDistanceType.html"""
type CodeNorthReferenceBaseType = Literal["TRUE", "MAG", "GRID", "OTHER"]
"""https://aixm.aero/sites/default/files/imce/AIXM511HTML/AIXM/DataType_CodeNorthReferenceBaseType.html"""
type CodeNorthReferenceType = Nil | WithDollar[CodeNorthReferenceBaseType]
"""https://aixm.aero/sites/default/files/imce/AIXM511HTML/AIXM/DataType_CodeNorthReferenceType.html"""
type CodeATCReportingBaseType = Literal[
    "COMPULSORY", "ON_REQUEST", "NO_REPORT", "OTHER"
]
"""https://aixm.aero/sites/default/files/imce/AIXM511HTML/AIXM/DataType_CodeATCReportingBaseType.html"""
type CodeATCReportingType = Nil | WithDollar[CodeATCReportingBaseType]
"""https://aixm.aero/sites/default/files/imce/AIXM511HTML/AIXM/DataType_CodeATCReportingType.html"""
type CodeDirectionBaseType = Literal["FORWARD", "BACKWARD", "BOTH", "OTHER"]
"""https://aixm.aero/sites/default/files/imce/AIXM511HTML/AIXM/DataType_CodeDirectionBaseType.html"""
type CodeDirectionType = Nil | WithDollar[CodeDirectionBaseType]
"""https://aixm.aero/sites/default/files/imce/AIXM511HTML/AIXM/DataType_CodeDirectionType.html"""
type CodeCommunicationChannelBaseType = Literal["OTHER"]
"""https://aixm.aero/sites/default/files/imce/AIXM511HTML/AIXM/DataType_CodeCommunicationChannelBaseType.html"""
type CodeCommunicationChannelType = Nil | WithDollar[CodeCommunicationChannelBaseType]
"""https://aixm.aero/sites/default/files/imce/AIXM511HTML/AIXM/DataType_CodeCommunicationChannelType.html"""
type CodeFacilityRankingBaseType = Literal[
    "PRIMARY", "SECONDARY", "ALTERNATE", "EMERG", "GUARD", "OTHER"
]
"""https://aixm.aero/sites/default/files/imce/AIXM511HTML/AIXM/DataType_CodeFacilityRankingBaseType.html"""
type CodeFacilityRankingType = Nil | WithDollar[CodeFacilityRankingBaseType]
"""https://aixm.aero/sites/default/files/imce/AIXM511HTML/AIXM/DataType_CodeFacilityRankingType.html"""
