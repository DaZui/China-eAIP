from django.db import models

from . import common


# Create your models here.
class DesignatedPoint(common.Common):
    aixm_designator: common.CharField = models.CharField()
    aixm_name: common.CharField = models.CharField()
    aixm_latitude: common.FloatField = models.FloatField()
    aixm_longitude: common.FloatField = models.FloatField()
    aixm_horizontal_accuracy_in_meter: common.FloatOptional = models.FloatField(
        null=True
    )

    # @property
    # def feature(self) -> schemas.DesignatedPoint:
    #     return schemas.DesignatedPoint(
    #         geometry=geojson.Point(
    #             coordinates=(
    #                 self.aixm_longitude,
    #                 self.aixm_latitude,
    #             )
    #         ),
    #         properties=schemas.Properties1.model_validate(
    #             obj=self, from_attributes=True
    #         ),
    #         id=self.uuid,
    #     )
