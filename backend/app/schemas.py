import datetime
import re
import typing

import pydantic
from china_eaip_dataset import geojson
from china_eaip_dataset.aixm.features.airport_heliport import RunwayDeclaredDistance
from china_eaip_dataset.aixm.features.notes import Note


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
    aixm_annotations: str


class RunwayCentrelinePoint(_Common):
    aixm_on_runway: str
    aixm_role: str
    aixm_annotations: list[Note]
    aixm_associated_declared_distances: list[RunwayDeclaredDistance]


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
    aixm_annotations: str
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

    @pydantic.computed_field
    @property
    def notes(
        self,
    ) -> list[tuple[tuple[str, float, float, str], tuple[str, float, float, str]]]:
        try:
            items: list[str] = self.aixm_annotations.splitlines()
            length: int = len(items)
            方向s: list[list[str]] = [items[: length // 2], items[length // 2 :]]
            跑道s: set[tuple[str, float, float, str]] = set()
            for 方向 in 方向s:
                跑道编号: str = 方向[0][3:-1]
                if len(方向) == 3:
                    道面材质: str = f"{方向[1]} {方向[2]}"
                    起点, 终点 = 0, self.长度[0] or 0
                    跑道s.add((跑道编号, 起点, 终点, 道面材质))
                else:
                    for i in range(1, len(方向), 3):
                        道面材质: str = f"{方向[i + 1]} {方向[i + 2]}"
                        起点, 终点 = [float(x) for x in 方向[i][1:-2].split("-")]
                        跑道s.add((跑道编号, 起点, 终点, 道面材质))
            排序后跑道s = sorted(跑道s)

            长度: int = len(排序后跑道s)

            return list(zip(排序后跑道s[: 长度 // 2], 排序后跑道s[长度 // 2 :][::-1]))

        except Exception as e:
            print(e)
            return [
                (("", 0, 0, self.aixm_annotations), ("", 0, 0, self.aixm_annotations))
            ]


class AirportHeliport(_Common, _WithAnnotation):
    aixm_designator: str
    aixm_name: str
    aixm_location_indicator_icao: str
    aixm_designator_iata: str
    aixm_type: str
    aixm_certified_icao: bool | None
    aixm_control_type: str
    aixm_field_elevation: float | None
    aixm_field_elevation_accuracy: float | None
    aixm_magnetic_variation: float | None
    aixm_magnetic_variation_accuracy: float | None
    aixm_date_magnetic_variation: int | None
    aixm_magnetic_variation_change: float | None
    aixm_reference_temperature: float | None
    aixm_certification_date: datetime.date | None
    aixm_certification_expiration_date: datetime.date | None
    aixm_served_city: str
    aixm_latitude: float
    aixm_longitude: float
    aixm_horizontal_accuracy: float | None
    aixm_annotations: str
    aixm_availability: str

    跑道s: list[Runway] = []

    @pydantic.computed_field
    @property
    def geometry(self) -> geojson.Point:
        return geojson.Point(
            coordinates=(
                self.aixm_longitude,
                self.aixm_latitude,
                self.aixm_field_elevation or 0,
            )
        )

    @pydantic.computed_field
    @property
    def notes(self) -> list[tuple[str, str]]:
        matches: re.Match[str] | None = re.fullmatch(
            pattern=r"^(Site at AD): (.*), (Direction and distance from city): (.*)$",
            string=self.aixm_annotations.replace("\n", " "),
        )
        if matches is None:
            return [("Annotations", self.aixm_annotations)]

        def standardization(x: str) -> str:
            return re.sub(pattern=r" *\(", repl=" (", string=x)

        return [
            (matches[1], standardization(x=matches[2])),
            (matches[3], standardization(x=matches[4])),
        ]

    @pydantic.computed_field
    @property
    def 名称(self) -> str:
        if self.aixm_served_city == self.aixm_name:
            return self.aixm_name.title()
        return f"{self.aixm_served_city} / {self.aixm_name}".title()

    @pydantic.computed_field
    @property
    def 海拔(self) -> tuple[float | None, float | None]:
        return self.aixm_field_elevation, self.aixm_field_elevation_accuracy

    @pydantic.computed_field
    @property
    def 地磁偏角(self) -> tuple[float | None, float | None, int | None, float | None]:
        return (
            self.aixm_magnetic_variation,
            self.aixm_magnetic_variation_accuracy,
            self.aixm_date_magnetic_variation,
            self.aixm_magnetic_variation_change,
        )
