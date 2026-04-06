from typing import Annotated

from pydantic import Field

from ...base import BaseModel, Link, Nil, WithAtGmlId
from ..abstract_feature import AixmTimeSlice
from ..data_types import (
    CodeCommunicationChannelType,
    CodeFacilityRankingType,
    CodeLanguageType,
    TextNameType,
    ValFrequencyType,
)
from .notes import WithAixmAnnotation


class _CallsignDetail(WithAtGmlId):
    """https://aixm.aero/sites/default/files/imce/AIXM511HTML/AIXM/Class_CallsignDetail.html"""

    aixm_call_sign: Annotated[TextNameType, Field(alias="aixm:callSign")]
    aixm_language: Annotated[CodeLanguageType, Field(alias="aixm:language")]


class _Service(AixmTimeSlice, WithAixmAnnotation):
    """https://aixm.aero/sites/default/files/imce/AIXM511HTML/AIXM/Class_Service.html"""

    aixm_name: Annotated[TextNameType, Field(alias="aixm:name")]
    aixm_location: Annotated[Nil, Field(alias="aixm:location")]
    aixm_service_provider: Annotated[Link, Field(alias="aixm:serviceProvider")]

    class _AixmCallSignItem(BaseModel):
        aixm_callsign_detail: Annotated[
            _CallsignDetail, Field(alias="aixm:CallsignDetail")
        ]

    aixm_call_sign: Annotated[
        list[_AixmCallSignItem], Field(alias="aixm:call-sign")
    ] = []
    aixm_radio_communication: Annotated[
        list[Link], Field(alias="aixm:radioCommunication")
    ] = []


class _TrafficSeparationService(_Service):
    """https://aixm.aero/sites/default/files/imce/AIXM511HTML/AIXM/Class_TrafficSeparationService.html"""


class AirTrafficControlService(_TrafficSeparationService):
    """https://aixm.aero/sites/default/files/imce/AIXM511HTML/AIXM/Class_AirTrafficControlService.html"""

    aixm_client_airspace: Annotated[list[Link], Field(alias="aixm:clientAirspace")]


class RadioCommunicationChannel(AixmTimeSlice):
    """https://aixm.aero/sites/default/files/imce/AIXM511HTML/AIXM/Class_RadioCommunicationChannel.html"""

    aixm_rank: Annotated[CodeFacilityRankingType, Field(alias="aixm:rank")]
    aixm_frequencyTransmission: Annotated[
        ValFrequencyType, Field(alias="aixm:frequencyTransmission")
    ]
    aixm_frequencyReception: Annotated[
        ValFrequencyType, Field(alias="aixm:frequencyReception")
    ]
    aixm_channel: Annotated[CodeCommunicationChannelType, Field(alias="aixm:channel")]
