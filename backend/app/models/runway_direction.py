from django.db import models

from . import common


# Create your models here.
class RunwayDirection(common.Common):
    aixm_designator: common.CharField = models.CharField()
    aixm_true_bearing: common.DecimalField = models.DecimalField(
        decimal_places=2, max_digits=5
    )
    aixm_used_runway: common.CharField = models.CharField()
