import datetime
import re
import typing

import pydantic
from china_eaip_dataset import geojson
from china_eaip_dataset.aixm.data_types import (
    CodeVerticalReferenceBaseType,
    ValDistanceVerticalBaseType,
)


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


class Runway(_Common, _WithAnnotation):
    aixm_designator: str
    aixm_associated_airport_heliport: str
    长度: tuple[float | None, float | None]
    宽度: tuple[float | None, float | None]
    路肩宽度: tuple[float | None, None]

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


class Properties(_Common, _WithAnnotation):
    aixm_location_indicator_icao: typing.Annotated[
        str, pydantic.Field(serialization_alias="ICAO代码")
    ]
    aixm_designator_iata: typing.Annotated[
        str, pydantic.Field(serialization_alias="IATA代码")
    ]
    aixm_magnetic_variation: float | None
    aixm_magnetic_variation_accuracy: float | None
    aixm_date_magnetic_variation: int | None
    aixm_magnetic_variation_change: float | None
    aixm_availability: str

    aixm_field_elevation: typing.Annotated[
        tuple[float | None, float | None], pydantic.Field(serialization_alias="海拔")
    ]
    aixm_reference_temperature_in_celcius: typing.Annotated[
        float | None, pydantic.Field(serialization_alias="温度")
    ]

    aixm_name_display: typing.Annotated[str, pydantic.Field(serialization_alias="名称")]
    aixm_magnetic_variation_display: list[str]

    runways: list[Runway]

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


class AirportHeliport(geojson.TypedFeature[geojson.Point, Properties]):
    pass


class Properties2(_Common):
    aixm_type: str
    aixm_designator: str
    aixm_name: str

    upper_limit: tuple[
        float | None, ValDistanceVerticalBaseType | CodeVerticalReferenceBaseType
    ]
    lower_limit: tuple[
        float | None, ValDistanceVerticalBaseType | CodeVerticalReferenceBaseType
    ]


class Airspace(_Common):
    aixm_type: str
    aixm_designator: str
    aixm_name: str

    features: geojson.FeatureCollection


class AirspaceComponent(pydantic.BaseModel):
    upper_limit: tuple[
        float | None, ValDistanceVerticalBaseType | CodeVerticalReferenceBaseType
    ]
    lower_limit: tuple[
        float | None, ValDistanceVerticalBaseType | CodeVerticalReferenceBaseType
    ]
