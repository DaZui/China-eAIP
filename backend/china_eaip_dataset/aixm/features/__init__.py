import datetime
from typing import Annotated, Literal

from pydantic import Field

from ...base import (
    BaseModel,
    SpecialUuid,
    WithAtGmlId,
    WithAtOwns,
    WithAtXlinkType,
    WithDollar,
    WithGmlTimePeriod,
)
from .airport_heliport import (
    AirportHeliport,
    Runway,
    RunwayCentrelinePoint,
    RunwayDirection,
)
from .airspace import Airspace
from .navaids_points import (
    DME,
    NDB,
    VOR,
    DesignatedPoint,
    Glidepath,
    Localizer,
    MarkerBeacon,
    Navaid,
)
from .organisation import Unit
from .routes import Route, RouteSegment
from .service import AirTrafficControlService, RadioCommunicationChannel


class _WithGcoCharacterString[Inner: str = str](BaseModel):
    gco_character_string: Annotated[Inner, Field(alias="gco:CharacterString")]


class _WithGcoDateTime(BaseModel):
    gco_date_time: Annotated[datetime.datetime, Field(alias="gco:DateTime")]


class _GmxCodeLists[CodeList: str, CodeListValue: str](WithDollar[CodeListValue]):
    at_code_list: Annotated[CodeList, Field(alias="@codeList")]
    at_code_list_value: Annotated[CodeListValue, Field(alias="@codeListValue")]


class _GmdCiAddress(BaseModel):
    gmd_administrative_area: Annotated[
        _WithGcoCharacterString[Literal["Beijing"]],
        Field(alias="gmd:administrativeArea"),
    ]
    gmd_city: Annotated[
        _WithGcoCharacterString[Literal["Beijing"]], Field(alias="gmd:city")
    ]
    gmd_country: Annotated[
        _WithGcoCharacterString[Literal["China"]], Field(alias="gmd:country")
    ]
    gmd_delivery_point: Annotated[
        tuple[
            _WithGcoCharacterString[
                Literal[
                    "No.9 Xiedao West Road, Chaoyang District Beijing 100018, People's Republic of China"
                ]
            ]
        ],
        Field(alias="gmd:deliveryPoint"),
    ]
    gmd_electronic_mail_address: Annotated[
        tuple[_WithGcoCharacterString[Literal["aipchina@atmb.net.cn"]]],
        Field(alias="gmd:electronicMailAddress"),
    ]
    gmd_postal_code: Annotated[
        _WithGcoCharacterString[Literal["100018"]], Field(alias="gmd:postalCode")
    ]


class _GmdAddress(WithAtXlinkType):
    gmd_ci_address: Annotated[_GmdCiAddress, Field(alias="gmd:CI_Address")]


class _GmdCiTelephone(BaseModel):
    gmd_voice: Annotated[
        tuple[_WithGcoCharacterString[Literal["86-10-57803699"]]],
        Field(alias="gmd:voice"),
    ]


class _GmdPhone(WithAtXlinkType):
    gmd_ci_telephone: Annotated[_GmdCiTelephone, Field(alias="gmd:CI_Telephone")]


class _GmdCiContact(BaseModel):
    gmd_address: Annotated[_GmdAddress, Field(alias="gmd:address")]
    gmd_phone: Annotated[_GmdPhone, Field(alias="gmd:phone")]


class _GmdContactInfo(WithAtXlinkType):
    gmd_ci_contact: Annotated[_GmdCiContact, Field(alias="gmd:CI_Contact")]


class _GmdRole(BaseModel):
    gmd_ci_role_code: Annotated[
        _GmxCodeLists[
            Literal[
                "http://www.aixm.aero/schema/5.1/ISO_19139_Schemas/resources/Codelist/gmxCodelists.xml#CI_RoleCode"
            ],
            Literal["publisher"],
        ],
        Field(alias="gmd:CI_RoleCode"),
    ]


class _GmdCiResponsibleParty(BaseModel):
    gmd_contact_info: Annotated[_GmdContactInfo, Field(alias="gmd:contactInfo")]
    gmd_organisation_name: Annotated[
        _WithGcoCharacterString[
            Literal[
                "Aeronautical Information Service Center of Air Traffic Management Bureau, Civil Aviation Administration of China"
            ]
        ],
        Field(alias="gmd:organisationName"),
    ]
    gmd_role: Annotated[_GmdRole, Field(alias="gmd:role")]


class _GmdContactItem(WithAtXlinkType):
    gmd_ci_responsible_party: Annotated[
        _GmdCiResponsibleParty, Field(alias="gmd:CI_ResponsibleParty")
    ]


class _GmdDateType(BaseModel):
    gmd_ci_date_type_code: Annotated[
        _GmxCodeLists[
            Literal[
                "http://www.aixm.aero/schema/5.1/ISO_19139_Schemas/resources/Codelist/gmxCodeLists.xml#CI_DateTypeCode"
            ],
            Literal["publication", "revision"],
        ],
        Field(alias="gmd:CI_DateTypeCode"),
    ]


class _GmdCiDate(BaseModel):
    gmd_date: Annotated[_WithGcoDateTime, Field(alias="gmd:date")]
    gmd_date_type: Annotated[_GmdDateType, Field(alias="gmd:dateType")]


class _GmdDate(WithAtXlinkType):
    gmd_ci_date: Annotated[_GmdCiDate, Field(alias="gmd:CI_Date")]


class _GmdCiCitation(BaseModel):
    gmd_date: Annotated[tuple[_GmdDate], Field(alias="gmd:date")]
    gmd_title: Annotated[
        _WithGcoCharacterString[Literal["Date and time when provided"]],
        Field(alias="gmd:title"),
    ]


class _GmdCitation(WithAtXlinkType):
    gmd_ci_citation: Annotated[_GmdCiCitation, Field(alias="gmd:CI_Citation")]


class _GmdExtent(WithAtXlinkType, WithGmlTimePeriod):
    pass


class _GmdExTemporalExtent(BaseModel):
    gmd_extent: Annotated[_GmdExtent, Field(alias="gmd:extent")]


class _GmdTemporalElementItem(WithAtXlinkType):
    gmd_ex_temporal_extent: Annotated[
        _GmdExTemporalExtent, Field(alias="gmd:EX_TemporalExtent")
    ]


class _GmdExExtentA(BaseModel):
    gmd_temporal_element: Annotated[
        tuple[_GmdTemporalElementItem], Field(alias="gmd:temporalElement")
    ]


class _GmdExExtentB(BaseModel):
    gmd_description: Annotated[
        _WithGcoCharacterString[Literal["AIRAC"]], Field(alias="gmd:description")
    ]


class _GmdExtentItem(WithAtXlinkType):
    gmd_ex_extent: Annotated[
        _GmdExExtentA | _GmdExExtentB, Field(alias="gmd:EX_Extent")
    ]


class _GmdMdConstraints(BaseModel):
    gmd_use_limitation: Annotated[
        tuple[
            _WithGcoCharacterString[
                Literal[
                    "For evaluation and testing use only; not for operational purposes."
                ]
            ]
        ],
        Field(alias="gmd:useLimitation"),
    ]


class _GmdResourceConstraintsItem(WithAtXlinkType):
    gmd_md_constraints: Annotated[_GmdMdConstraints, Field(alias="gmd:MD_Constraints")]


class _GmdSpatialRepresentationTypeItem(BaseModel):
    gmd_md_spatial_representation_type_code: Annotated[
        _GmxCodeLists[
            Literal[
                "http://standards.iso.org/ittf/PubliclyAvailableStandards/ISO_19139_Schemas/resources/codelist/ML_gmxCodelists.xml#MD_SpatialRepresentationTypeCode"
            ],
            Literal["vector"],
        ],
        Field(alias="gmd:MD_SpatialRepresentationTypeCode"),
    ]


class _GmdMdDataIdentification(BaseModel):
    gmd_abstract: Annotated[
        _WithGcoCharacterString[
            Literal[
                "The aeronautical data for People's Republic of China are collected and published according to ICAO Annex 15, 16th Edition requirements. Refer to the DPS document for detail information."
            ]
        ],
        Field(alias="gmd:abstract"),
    ]
    gmd_citation: Annotated[_GmdCitation, Field(alias="gmd:citation")]
    gmd_extent: Annotated[
        tuple[_GmdExtentItem, _GmdExtentItem], Field(alias="gmd:extent")
    ]
    gmd_language: Annotated[
        tuple[_WithGcoCharacterString[Literal["eng"]]], Field(alias="gmd:language")
    ]
    gmd_point_of_contact: Annotated[
        tuple[_GmdContactItem], Field(alias="gmd:pointOfContact")
    ]
    gmd_resource_constraints: Annotated[
        tuple[_GmdResourceConstraintsItem], Field(alias="gmd:resourceConstraints")
    ]
    gmd_spatial_representation_type: Annotated[
        tuple[_GmdSpatialRepresentationTypeItem],
        Field(alias="gmd:spatialRepresentationType"),
    ]


class _GmdIdentificationInfoItem(WithAtXlinkType):
    gmd_md_data_identification: Annotated[
        _GmdMdDataIdentification, Field(alias="gmd:MD_DataIdentification")
    ]


class _GmdMdMetadata(BaseModel):
    at_id: Annotated[SpecialUuid, Field(alias="@id")]
    gmd_contact: Annotated[tuple[_GmdContactItem], Field(alias="gmd:contact")]
    gmd_date_stamp: Annotated[_WithGcoDateTime, Field(alias="gmd:dateStamp")]
    gmd_identification_info: Annotated[
        tuple[_GmdIdentificationInfoItem], Field(alias="gmd:identificationInfo")
    ]


class AixmMessageMetadata(WithAtOwns):
    gmd_md_metadata: Annotated[_GmdMdMetadata, Field(alias="gmd:MD_Metadata")]


class _GmlIdentifier(WithDollar):
    at_code_space: Annotated[Literal["urn:uuid:"], Field(alias="@codeSpace")]


class CommonRoot(WithAtGmlId):
    aixm_message_metadata: Annotated[
        AixmMessageMetadata, Field(alias="aixm:messageMetadata")
    ]
    at_xmlns_aixm: Annotated[
        Literal["http://www.aixm.aero/schema/5.1.1"], Field(alias="@xmlns:aixm")
    ]
    at_xmlns_gco: Annotated[
        Literal["http://www.isotc211.org/2005/gco"], Field(alias="@xmlns:gco")
    ]
    at_xmlns_gmd: Annotated[
        Literal["http://www.isotc211.org/2005/gmd"], Field(alias="@xmlns:gmd")
    ]
    at_xmlns_gml: Annotated[
        Literal["http://www.opengis.net/gml/3.2"], Field(alias="@xmlns:gml")
    ]
    at_xmlns_gsr: Annotated[
        Literal["http://www.isotc211.org/2005/gsr"], Field(alias="@xmlns:gsr")
    ]
    at_xmlns_gss: Annotated[
        Literal["http://www.isotc211.org/2005/gss"], Field(alias="@xmlns:gss")
    ]
    at_xmlns_gts: Annotated[
        Literal["http://www.isotc211.org/2005/gts"], Field(alias="@xmlns:gts")
    ]
    at_xmlns_message: Annotated[
        Literal["http://www.aixm.aero/schema/5.1.1/message"],
        Field(alias="@xmlns:message"),
    ]
    at_xmlns_xlink: Annotated[
        Literal["http://www.w3.org/1999/xlink"], Field(alias="@xmlns:xlink")
    ]

    class _MessageHasMemberItem(WithAtXlinkType, WithAtOwns):
        class _AixmContent(WithAtGmlId):
            gml_identifier: Annotated[_GmlIdentifier, Field(alias="gml:identifier")]

            class _AixmTimeSliceItem(WithAtOwns):
                aixm_airport_heliport_time_slice: Annotated[
                    AirportHeliport | None,
                    Field(alias="aixm:AirportHeliportTimeSlice"),
                ] = None
                aixm_airspace_time_slice: Annotated[
                    Airspace | None, Field(alias="aixm:AirspaceTimeSlice")
                ] = None
                aixm_air_traffic_control_service_time_slice: Annotated[
                    AirTrafficControlService | None,
                    Field(alias="aixm:AirTrafficControlServiceTimeSlice"),
                ] = None
                aixm_designated_point_time_slice: Annotated[
                    DesignatedPoint | None, Field(alias="aixm:DesignatedPointTimeSlice")
                ] = None
                aixm_dme_time_slice: Annotated[
                    DME | None, Field(alias="aixm:DMETimeSlice")
                ] = None
                aixm_glidepath_time_slice: Annotated[
                    Glidepath | None, Field(alias="aixm:GlidepathTimeSlice")
                ] = None
                aixm_localizer_time_slice: Annotated[
                    Localizer | None, Field(alias="aixm:LocalizerTimeSlice")
                ] = None
                aixm_marker_beacon_time_slice: Annotated[
                    MarkerBeacon | None, Field(alias="aixm:MarkerBeaconTimeSlice")
                ] = None
                aixm_navaid_time_slice: Annotated[
                    Navaid | None, Field(alias="aixm:NavaidTimeSlice")
                ] = None
                aixm_ndb_time_slice: Annotated[
                    NDB | None, Field(alias="aixm:NDBTimeSlice")
                ] = None
                aixm_radio_communication_channel_time_slice: Annotated[
                    RadioCommunicationChannel | None,
                    Field(alias="aixm:RadioCommunicationChannelTimeSlice"),
                ] = None
                aixm_route_time_slice: Annotated[
                    Route | None, Field(alias="aixm:RouteTimeSlice")
                ] = None
                aixm_route_segment_time_slice: Annotated[
                    RouteSegment | None, Field(alias="aixm:RouteSegmentTimeSlice")
                ] = None
                aixm_runway_time_slice: Annotated[
                    Runway | None, Field(alias="aixm:RunwayTimeSlice")
                ] = None
                aixm_runway_centreline_point_time_slice: Annotated[
                    RunwayCentrelinePoint | None,
                    Field(alias="aixm:RunwayCentrelinePointTimeSlice"),
                ] = None
                aixm_runway_direction_time_slice: Annotated[
                    RunwayDirection | None, Field(alias="aixm:RunwayDirectionTimeSlice")
                ] = None
                aixm_unit_time_slice: Annotated[
                    Unit | None, Field(alias="aixm:UnitTimeSlice")
                ] = None
                aixm_vor_time_slice: Annotated[
                    VOR | None, Field(alias="aixm:VORTimeSlice")
                ] = None

            aixm_time_slice: Annotated[
                tuple[_AixmTimeSliceItem], Field(alias="aixm:timeSlice")
            ]

        aixm_airport_heliport: Annotated[
            _AixmContent | None, Field(alias="aixm:AirportHeliport")
        ] = None
        aixm_airspace: Annotated[_AixmContent | None, Field(alias="aixm:Airspace")] = (
            None
        )
        aixm_air_traffic_control_service: Annotated[
            _AixmContent | None, Field(alias="aixm:AirTrafficControlService")
        ] = None
        aixm_designated_point: Annotated[
            _AixmContent | None, Field(alias="aixm:DesignatedPoint")
        ] = None
        aixm_dme: Annotated[_AixmContent | None, Field(alias="aixm:DME")] = None
        aixm_glidepath: Annotated[
            _AixmContent | None, Field(alias="aixm:Glidepath")
        ] = None
        aixm_localizer: Annotated[
            _AixmContent | None, Field(alias="aixm:Localizer")
        ] = None
        aixm_marker_beacon: Annotated[
            _AixmContent | None, Field(alias="aixm:MarkerBeacon")
        ] = None
        aixm_navaid: Annotated[_AixmContent | None, Field(alias="aixm:Navaid")] = None
        aixm_ndb: Annotated[_AixmContent | None, Field(alias="aixm:NDB")] = None
        aixm_radio_communication_channel: Annotated[
            _AixmContent | None, Field(alias="aixm:RadioCommunicationChannel")
        ] = None
        aixm_route: Annotated[_AixmContent | None, Field(alias="aixm:Route")] = None
        aixm_route_segment: Annotated[
            _AixmContent | None, Field(alias="aixm:RouteSegment")
        ] = None
        aixm_runway: Annotated[_AixmContent | None, Field(alias="aixm:Runway")] = None
        aixm_runway_centreline_point: Annotated[
            _AixmContent | None, Field(alias="aixm:RunwayCentrelinePoint")
        ] = None
        aixm_runway_direction: Annotated[
            _AixmContent | None, Field(alias="aixm:RunwayDirection")
        ] = None
        aixm_unit: Annotated[_AixmContent | None, Field(alias="aixm:Unit")] = None
        aixm_vor: Annotated[_AixmContent | None, Field(alias="aixm:VOR")] = None

    message_has_member: Annotated[
        list[_MessageHasMemberItem], Field(alias="message:hasMember")
    ]
