import datetime
import typing

import pydantic


class BaseModel(pydantic.BaseModel, extra="forbid"):
    pass


SpecialUuid = typing.Annotated[
    str,
    pydantic.BeforeValidator(func=lambda x: x.replace("uuid.", "")),
    pydantic.PlainSerializer(func=lambda x: f"uuid.{x}"),
]


class WithAtGmlId(BaseModel):
    at_gml_id: typing.Annotated[SpecialUuid, pydantic.Field(alias="@gml:id")]


class WithAtOwns(BaseModel):
    at_owns: typing.Annotated[typing.Literal[False], pydantic.Field(alias="@owns")]


class WithAtSrsName(BaseModel):
    at_srs_name: typing.Annotated[
        typing.Literal["urn:ogc:def:crs:EPSG::4326"] | None,
        pydantic.Field(alias="@srsName"),
    ] = None


class WithAtXlinkType(BaseModel):
    at_xlink_type: typing.Annotated[
        typing.Literal["simple"],
        pydantic.Field(alias="@xlink:type"),
    ]


class Link(WithAtOwns, WithAtXlinkType):
    at_xlink_href: typing.Annotated[str, pydantic.Field(alias="@xlink:href")]


class WithDollar[Inner: typing.Any = str](BaseModel):
    dollar: typing.Annotated[Inner, pydantic.Field(alias="$")]

    def __str__(self) -> str:
        return str(self.dollar)


class Nil(BaseModel, validate_by_name=True):
    at_nil_reason: typing.Annotated[
        typing.Literal[
            "inapplicable", "missing", "template", "unknown", "withheld", "other"
        ],
        pydantic.Field(alias="@nilReason"),
    ]
    """https://aixm.aero/sites/default/files/imce/AIXM511HTML/ISO%2019136/DataType_NilReasonEnumeration.html"""
    at_xmlns_xsi: typing.Annotated[
        typing.Literal["http://www.w3.org/2001/XMLSchema-instance"],
        pydantic.Field(alias="@xmlns:xsi"),
    ]
    at_xsi_nil: typing.Annotated[
        typing.Literal["true"], pydantic.Field(alias="@xsi:nil")
    ]

    def __str__(self) -> str:
        return ""


class _GmlBeginPosition(WithDollar[datetime.datetime]):
    at_frame: typing.Annotated[
        typing.Literal["#ISO-8601"],
        pydantic.Field(alias="@frame"),
    ]


class _GmlEndPosition(BaseModel):
    at_frame: typing.Annotated[
        typing.Literal["#ISO-8601"],
        pydantic.Field(alias="@frame"),
    ]
    at_indeterminate_position: typing.Annotated[
        typing.Literal["unknown"],
        pydantic.Field(alias="@indeterminatePosition"),
    ]


class _GmlTimePeriod(WithAtGmlId):
    at_frame: typing.Annotated[
        typing.Literal["#ISO-8601"],
        pydantic.Field(alias="@frame"),
    ]
    gml_begin_position: typing.Annotated[
        _GmlBeginPosition,
        pydantic.Field(alias="gml:beginPosition"),
    ]
    gml_end_position: typing.Annotated[
        _GmlEndPosition,
        pydantic.Field(alias="gml:endPosition"),
    ]


class WithGmlTimePeriod(BaseModel):
    gml_time_period: typing.Annotated[
        _GmlTimePeriod,
        pydantic.Field(alias="gml:TimePeriod"),
    ]
