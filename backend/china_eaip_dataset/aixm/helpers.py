import datetime
import decimal

from ..base import Nil, WithDollar
from .data_types import (
    UomDistanceType,
    UomDistanceVerticalType,
    ValDistanceType,
    ValDistanceVerticalType,
    ValTemperatureType,
)


def extract_value[T: str | decimal.Decimal | datetime.date](
    value: Nil | WithDollar[T],
) -> T | None:
    if not isinstance(value, Nil):
        return value.dollar


def to_meter(
    value: ValDistanceType | ValDistanceVerticalType | None,
) -> decimal.Decimal | None:
    if value is None or isinstance(value, Nil):
        return None
    if value.dollar in ("UNL", "GND", "FLOOR", "CEILING"):
        return None

    CONVERT_TO_METER: dict[UomDistanceType | UomDistanceVerticalType, str] = {
        "CM": "0.01",
        "FL": "30.48",
        "FT": "0.3048",
        "KM": "1000",
        "M": "1",
        "MI": "1609.344",
        "NM": "1852",
        "OTHER": "0",
        "SM": "10",
    }

    return value.dollar * decimal.Decimal(value=CONVERT_TO_METER[value.at_uom])


def to_celsius(value: ValTemperatureType | None) -> decimal.Decimal | None:
    if value is None or isinstance(value, Nil) or value.at_uom == "OTHER":
        return None
    output: decimal.Decimal = value.dollar
    if value.at_uom == "K":
        output -= decimal.Decimal("273.15")
    if value.at_uom == "F":
        output -= decimal.Decimal("32")
        output /= decimal.Decimal("1.8")
    return output
