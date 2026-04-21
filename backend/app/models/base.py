import decimal
import typing

import china_eaip_dataset.aixm.features.geometry
from china_eaip_dataset.aixm.data_types import ValDistanceVerticalSpecialBaseType
from django.db import models

from .common import CharField, DecimalOptional


class Point(models.Model):
    latitude: DecimalOptional = models.DecimalField(
        null=True, decimal_places=10, max_digits=12
    )
    longitude: DecimalOptional = models.DecimalField(
        null=True, decimal_places=10, max_digits=13
    )


class ElevatedPoint(Point):
    aixm_elevation: DecimalOptional = models.DecimalField(
        null=True, decimal_places=3, max_digits=7
    )
    aixm_special_elevation: CharField = models.CharField()

    @classmethod
    def from_xml(
        cls, item: china_eaip_dataset.aixm.features.geometry.ElevatedPoint
    ) -> typing.Self:
        digital_elevation: decimal.Decimal | None = (
            item.computed_elevation
            if isinstance(item.computed_elevation, decimal.Decimal)
            else None
        )
        special_elevation: ValDistanceVerticalSpecialBaseType | typing.Literal[""] = (
            item.computed_elevation
            if isinstance(item.computed_elevation, str)
            and item.computed_elevation in ("CEILING", "GND", "FLOOR", "UNL")
            else ""
        )

        return cls.objects.get_or_create(
            latitude=None if item.gml_pos is None else item.gml_pos.dollar[0],
            longitude=None if item.gml_pos is None else item.gml_pos.dollar[1],
            aixm_elevation=digital_elevation,
            aixm_special_elevation=special_elevation,
        )[0]
