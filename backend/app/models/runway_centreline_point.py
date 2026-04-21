import typing

from django.db import models

from . import base, common


# Create your models here.
class RunwayCentrelinePoint(common.Common):
    aixm_role: common.CharField = models.CharField()
    aixm_on_runway: common.CharField = models.CharField()
    aixm_annotations: models.JSONField[typing.Any, typing.Any] = models.JSONField()
    aixm_associated_declared_distances: models.JSONField[typing.Any, typing.Any] = (
        models.JSONField()
    )
    aixm_location: models.ForeignKey[
        base.ElevatedPoint | None, base.ElevatedPoint | None
    ] = models.ForeignKey(to=base.ElevatedPoint, on_delete=models.PROTECT, null=True)
