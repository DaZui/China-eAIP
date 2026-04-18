import datetime

from django.db import models

BooleanField = models.BooleanField[bool, bool]
BooleanOptional = models.BooleanField[bool | None, bool | None]
CharField = models.CharField[str, str]
DateTimeField = models.DateTimeField[datetime.datetime, datetime.datetime]
FloatField = models.FloatField[float, float]
FloatOptional = models.FloatField[float | None, float | None]
IntegerField = models.IntegerField[int, int]


# Create your models here.
