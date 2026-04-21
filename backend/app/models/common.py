import datetime
import decimal

from django.db import models

BooleanField = models.BooleanField[bool, bool]
BooleanOptional = models.BooleanField[bool | None, bool | None]
CharField = models.CharField[str, str]
DateField = models.DateField[datetime.date, datetime.date]
DateOptional = models.DateField[datetime.date | None, datetime.date | None]
DateTimeField = models.DateTimeField[datetime.datetime, datetime.datetime]
DecimalField = models.DecimalField[decimal.Decimal, decimal.Decimal]
DecimalOptional = models.DecimalField[decimal.Decimal | None, decimal.Decimal | None]
FloatField = models.FloatField[float, float]
FloatOptional = models.FloatField[float | None, float | None]
IntegerField = models.IntegerField[int, int]
IntegerOptional = models.IntegerField[int | None, int | None]


# Create your models here.
class Common(models.Model):
    class Meta:
        abstract = True
        constraints: list[models.UniqueConstraint] = [
            models.UniqueConstraint(
                fields=["uuid", "aixm_sequence_number", "aixm_correction_number"],
                name="%(app_label)s %(class)s 元素唯一",
            )
        ]

    uuid: CharField = models.CharField()
    information_valid_since: DateTimeField = models.DateTimeField()
    information_valid_until: DateTimeField = models.DateTimeField()
    aixm_sequence_number: IntegerField = models.IntegerField()
    aixm_correction_number: IntegerField = models.IntegerField()
