from typing import Annotated, Literal

from pydantic import Field

from ..base import WithAtGmlId, WithAtOwns, WithAtXlinkType, WithGmlTimePeriod


class _GmlValidTime(WithAtXlinkType, WithAtOwns, WithGmlTimePeriod):
    pass


class AixmTimeSlice(WithAtGmlId):
    """https://aixm.aero/sites/default/files/imce/AIXM511HTML/AIXM/Other_AIXMTimeSlice.html"""

    gml_valid_time: Annotated[_GmlValidTime, Field(alias="gml:validTime")]
    aixm_interpretation: Annotated[
        Literal["BASELINE"], Field(alias="aixm:interpretation")
    ]
    aixm_sequence_number: Annotated[int, Field(alias="aixm:sequenceNumber")]
    aixm_correction_number: Annotated[int, Field(alias="aixm:correctionNumber")]
