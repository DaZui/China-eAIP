import datetime
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
from china_eaip_dataset.aixm.helpers import extract_value
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
    aixm_annotation: list[Note]


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
    aixm_associated_declared_distances: list[RunwayDeclaredDistance]
    aixm_location: ElevatedPoint | None


class RunwayDirection(_Common):
    aixm_designator: str
    aixm_true_bearing: float | None
    aixm_true_bearing_accuracy: float | None
    aixm_used_runway: str
    中线点s: list[RunwayCentrelinePoint] = []

    @pydantic.computed_field
    @property
    def 航向角(self) -> tuple[float | None, float | None]:
        return (self.aixm_true_bearing, self.aixm_true_bearing_accuracy)


class Runway(_Common, _WithAnnotation):
    aixm_designator: str
    aixm_nominal_length: float | None
    aixm_length_accuracy: float | None
    aixm_nominal_width: float | None
    aixm_width_accuracy: float | None
    aixm_width_shoulder: float | None
    aixm_associated_airport_heliport: str

    方向s: list[RunwayDirection] = []

    @pydantic.computed_field
    @property
    def 长度(self) -> tuple[float | None, float | None]:
        return (self.aixm_nominal_length, self.aixm_length_accuracy)

    @pydantic.computed_field
    @property
    def 宽度(self) -> tuple[float | None, float | None]:
        return (self.aixm_nominal_width, self.aixm_width_accuracy)

    @pydantic.computed_field
    @property
    def 路肩宽度(self) -> tuple[float | None, None]:
        return (self.aixm_width_shoulder, None)

    # @pydantic.computed_field
    # @property
    # def notes(
    #     self,
    # ) -> list[tuple[tuple[str, float, float, str], tuple[str, float, float, str]]]:
    #     try:
    #         items: list[str] = self.aixm_annotation.splitlines()
    #         length: int = len(items)
    #         方向s: list[list[str]] = [items[: length // 2], items[length // 2 :]]
    #         跑道s: set[tuple[str, float, float, str]] = set()
    #         for 方向 in 方向s:
    #             跑道编号: str = 方向[0][3:-1]
    #             if len(方向) == 3:
    #                 道面材质: str = f"{方向[1]} {方向[2]}"
    #                 起点, 终点 = 0, self.长度[0] or 0
    #                 跑道s.add((跑道编号, 起点, 终点, 道面材质))
    #             else:
    #                 for i in range(1, len(方向), 3):
    #                     道面材质: str = f"{方向[i + 1]} {方向[i + 2]}"
    #                     起点, 终点 = [float(x) for x in 方向[i][1:-2].split("-")]
    #                     跑道s.add((跑道编号, 起点, 终点, 道面材质))
    #         排序后跑道s = sorted(跑道s)

    #         长度: int = len(排序后跑道s)

    #         return list(zip(排序后跑道s[: 长度 // 2], 排序后跑道s[长度 // 2 :][::-1]))

    #     except Exception as e:
    #         print(e)
    #         return [
    #             (("", 0, 0, self.aixm_annotation), ("", 0, 0, self.aixm_annotation))
    #         ]


class AirportHeliport(_Common, _WithAnnotation):
    aixm_designator: str
    aixm_name: str
    aixm_location_indicator_icao: str
    aixm_designator_iata: str
    aixm_type: str
    aixm_certified_icao: bool | None
    aixm_control_type: str
    aixm_field_elevation: float | None
    aixm_magnetic_variation: float | None
    aixm_date_magnetic_variation: float | None
    aixm_reference_temperature: float | None
    aixm_certification_date: datetime.date | None
    aixm_certification_expiration_date: datetime.date | None
    aixm_arp: ElevatedPoint
    aixm_served_city: str
    aixm_availability: list[AirportHeliportAvailability]

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
