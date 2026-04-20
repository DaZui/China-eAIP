from django.db import models

from . import common


# Create your models here.
class Runway(common.Common):
    aixm_designator: common.CharField = models.CharField()
    aixm_nominal_length_in_meter: common.FloatOptional = models.FloatField(null=True)
    aixm_length_accuracy_in_meter: common.FloatOptional = models.FloatField(null=True)
    aixm_nominal_width_in_meter: common.FloatOptional = models.FloatField(null=True)
    aixm_width_accuracy_in_meter: common.FloatOptional = models.FloatField(null=True)
    aixm_width_shoulder_in_meter: common.FloatOptional = models.FloatField(null=True)
    aixm_annotations: common.CharField = models.CharField()
    aixm_associated_airport_heliport: common.CharField = models.CharField()

    @property
    def 长度(self) -> tuple[float | None, float | None]:
        return (self.aixm_nominal_length_in_meter, self.aixm_length_accuracy_in_meter)

    @property
    def 宽度(self) -> tuple[float | None, float | None]:
        return (self.aixm_nominal_width_in_meter, self.aixm_width_accuracy_in_meter)

    @property
    def 路肩宽度(self) -> tuple[float | None, None]:
        return (self.aixm_width_shoulder_in_meter, None)
