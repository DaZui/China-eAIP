import datetime
import decimal
import re
import typing

import pydantic
from china_eaip_dataset import geojson
from china_eaip_dataset.aixm.data_types import ValDistanceVerticalSpecialBaseType
from china_eaip_dataset.aixm.features.airport_heliport import (
    AirportHeliportAvailability,
    FlightCharacteristic,
    RunwayDeclaredDistance,
)
from china_eaip_dataset.aixm.features.notes import Note
from china_eaip_dataset.aixm.helpers import extract_value, to_meter
from china_eaip_dataset.base import Nil


class _Common(pydantic.BaseModel):
    uuid: str
    information_valid_since: typing.Annotated[
        datetime.datetime, pydantic.Field(serialization_alias="有效期自")
    ]
    information_valid_until: typing.Annotated[
        datetime.datetime, pydantic.Field(serialization_alias="有效期至")
    ]
    aixm_sequence_number: typing.Annotated[
        int, pydantic.Field(serialization_alias="大版本号")
    ]
    aixm_correction_number: typing.Annotated[
        int, pydantic.Field(serialization_alias="小版本号")
    ]


class _WithAnnotation(pydantic.BaseModel):
    aixm_annotation: typing.Annotated[list[Note], pydantic.Field(exclude=True)]


class Point(pydantic.BaseModel):
    latitude: float | None
    longitude: float | None

    @pydantic.computed_field
    @property
    def geometry(self) -> geojson.Point | None:
        if self.longitude and self.latitude:
            return geojson.Point(coordinates=(self.longitude, self.latitude))


class ElevatedPoint(Point):
    aixm_elevation: float | None
    aixm_special_elevation: ValDistanceVerticalSpecialBaseType | typing.Literal[""]

    @pydantic.computed_field
    @property
    def geometry(self) -> geojson.Point | None:
        if self.longitude and self.latitude and self.aixm_elevation:
            return geojson.Point(
                coordinates=(self.longitude, self.latitude, self.aixm_elevation)
            )
        return super().geometry

    def geometry_with_given_elevation(
        self, elevation: float | None
    ) -> geojson.Point | None:
        if self.longitude and self.latitude and elevation:
            return geojson.Point(coordinates=(self.longitude, self.latitude, elevation))
        return self.geometry


class RunwayCentrelinePoint(_Common, _WithAnnotation):
    aixm_on_runway: str
    aixm_role: str
    aixm_associated_declared_distances: typing.Annotated[
        list[RunwayDeclaredDistance], pydantic.Field(exclude=True)
    ]
    aixm_location: ElevatedPoint | None

    @pydantic.computed_field
    @property
    def 距离s(self) -> dict[str, list[float]]:
        rv: dict[str, list[float]] = {}
        for x in self.aixm_associated_declared_distances:
            if isinstance(x.aixm_type, Nil):
                continue
            key: str = x.aixm_type.dollar
            for y in x.aixm_declared_distance:
                s: decimal.Decimal | None = to_meter(
                    value=y.aixm_runway_declared_distance_value.aixm_distance
                )
                if s:
                    if key not in rv:
                        rv[key] = []
                    rv[key].append(float(s))
        return rv


class RunwayDirection(_Common):
    aixm_designator: str
    aixm_true_bearing: float
    aixm_used_runway: str
    中线点s: list[RunwayCentrelinePoint] = []


class Runway(_Common, _WithAnnotation):
    aixm_designator: str
    aixm_nominal_length: float
    aixm_nominal_width: float
    aixm_width_shoulder: float | None
    aixm_associated_airport_heliport: str

    方向s: list[RunwayDirection] = []

    @pydantic.computed_field
    @property
    def notes(
        self,
    ) -> list[tuple[tuple[str, float, float, str], tuple[str, float, float, str]]]:
        # try:
        跑道s: set[tuple[str, float, float, str]] = set()
        for x in self.aixm_annotation:
            for y in x.aixm_translated_note:
                text: str = extract_value(y.aixm_linguistic_note.aixm_note) or ""
                segments: list[str] = text.replace(":", "\n").splitlines()
                总长度: int = len(segments)
                for 跑道 in [segments[: 总长度 // 2], segments[总长度 // 2 :]]:
                    if len(跑道) == 3:
                        output: tuple[str, float, float, str] = (
                            跑道[0][3:],
                            0,
                            self.aixm_nominal_length,
                            f"{跑道[1]} {跑道[2]}",
                        )
                        跑道s.add(output)
                    else:
                        跑道编号: str = 跑道[0][3:]
                        for a, b, c in [
                            跑道[idx : idx + 3] for idx in range(1, len(跑道), 3)
                        ]:
                            起, 止 = (int(x) for x in a[1:-2].split("-"))
                            跑道s.add((跑道编号, 起, 止, f"{b} {c}"))

        排序后跑道s: list[tuple[str, float, float, str]] = sorted(跑道s)
        长度: int = len(排序后跑道s)
        return list(zip(排序后跑道s[: 长度 // 2], 排序后跑道s[长度 // 2 :][::-1]))


class AirportHeliport(_Common, _WithAnnotation):
    # aixm_designator: str
    aixm_name: typing.Annotated[str, pydantic.Field(exclude=True)]
    aixm_location_indicator_icao: str
    aixm_designator_iata: str
    # aixm_type: str
    # aixm_certified_icao: bool | None
    # aixm_control_type: str
    aixm_field_elevation: float | None
    aixm_magnetic_variation: float | None
    aixm_date_magnetic_variation: float | None
    aixm_reference_temperature: float | None
    # aixm_certification_date: datetime.date | None
    # aixm_certification_expiration_date: datetime.date | None
    aixm_arp: typing.Annotated[ElevatedPoint, pydantic.Field(exclude=True)]
    aixm_served_city: typing.Annotated[str, pydantic.Field(exclude=True)]
    aixm_availability: typing.Annotated[
        list[AirportHeliportAvailability], pydantic.Field(exclude=True)
    ]

    跑道s: list[Runway] = []

    @pydantic.computed_field
    @property
    def 坐标点(self) -> geojson.Point | None:
        return self.aixm_arp.geometry_with_given_elevation(
            elevation=self.aixm_field_elevation
        )

    @pydantic.computed_field
    @property
    def 注解s(self) -> dict[str, set[str]]:
        def standardization(x: str) -> str:
            return re.sub(pattern=r" *\(", repl=" (", string=x)

        rv: dict[
            typing.Literal["Site at AD", "Direction and distance from city"] | str,
            set[str],
        ] = {"Site at AD": set(), "Direction and distance from city": set()}

        def insert(key: str, value: str) -> None:
            if key not in rv:
                rv[key] = set()
            rv[key].add(standardization(value))

        for x in self.aixm_annotation:
            prefix: str = f"{x.aixm_property_name} {x.aixm_purpose}"
            for y in x.aixm_translated_note:
                if isinstance(y.aixm_linguistic_note.aixm_note, Nil):
                    continue
                matches: re.Match[str] | None = re.fullmatch(
                    pattern=r"Site at AD:(.*?),Direction and distance from city:(.*)",
                    string=y.aixm_linguistic_note.aixm_note.dollar,
                )
                if matches:
                    insert(key="Site at AD", value=matches[1])
                    insert(key="Direction and distance from city", value=matches[2])
                else:
                    insert(key=prefix, value=y.aixm_linguistic_note.aixm_note.dollar)
        return rv

    @pydantic.computed_field
    @property
    def 名称(self) -> str:
        if self.aixm_served_city == self.aixm_name:
            return self.aixm_name.title()
        return f"{self.aixm_served_city} / {self.aixm_name}".title()

    @pydantic.computed_field
    @property
    def 用途s(self) -> list[tuple[str, str, str, str]]:
        characteristics: list[FlightCharacteristic] = [
            y.aixm_airport_heliport_usage.aixm_selection.aixm_condition_combination.aixm_flight[
                0
            ].aixm_flight_characteristic
            for x in self.aixm_availability
            for y in x.aixm_usage
        ]
        return sorted(
            {
                (
                    extract_value(value=s.aixm_military) or "",
                    extract_value(value=s.aixm_purpose) or "",
                    extract_value(value=s.aixm_rule) or "",
                    extract_value(value=s.aixm_type) or "",
                )
                for s in characteristics
            }
        )
