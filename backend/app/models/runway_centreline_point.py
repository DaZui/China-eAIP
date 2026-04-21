from django.db import models

from . import common


# Create your models here.
class RunwayCentrelinePoint(common.Common):
    aixm_role: common.CharField = models.CharField()
    aixm_on_runway: common.CharField = models.CharField()
