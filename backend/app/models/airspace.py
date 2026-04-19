import typing

from china_eaip_dataset import geojson
from china_eaip_dataset.aixm.features.airspace import AixmGeometryCompoents
from django.db import models

from . import common


# Create your models here.
class Airspace(common.Common):
    aixm_type: common.CharField = models.CharField()
    aixm_designator: common.CharField = models.CharField()
    aixm_name: common.CharField = models.CharField()
    aixm_geometry_components: models.JSONField[typing.Any, typing.Any] = (
        models.JSONField()
    )

    @property
    def feature(self) -> geojson.FeatureCollection:
        features: list[geojson.Feature] = []

        components: AixmGeometryCompoents = AixmGeometryCompoents.model_validate(
            self.aixm_geometry_components, by_name=True, by_alias=True
        )
        for i1, x in enumerate(iterable=components.root):
            # print(
            #     x.aixm_airspace_geometry_component.aixm_the_airspace_volume.aixm_airspace_volume.aixm_lower_limit,
            #     x.aixm_airspace_geometry_component.aixm_the_airspace_volume.aixm_airspace_volume.aixm_lower_limit_reference,
            #     x.aixm_airspace_geometry_component.aixm_the_airspace_volume.aixm_airspace_volume.aixm_upper_limit,
            #     x.aixm_airspace_geometry_component.aixm_the_airspace_volume.aixm_airspace_volume.aixm_upper_limit_reference,
            # )
            for i2, y in enumerate(
                iterable=x.aixm_airspace_geometry_component.aixm_the_airspace_volume.aixm_airspace_volume.aixm_horizontal_projection.aixm_elevated_surface.gml_patches.gml_polygon_patch
            ):
                for i3, z in enumerate(y.gml_exterior.gml_ring.gml_curve_member):
                    # for i4, a in enumerate(
                    #     z.aixm_curve.gml_segments.gml_arc_by_center_point
                    # ):
                    #     print(i1, i2, i3, "Arc", i4)
                    # for i4, b in enumerate(
                    #     z.aixm_curve.gml_segments.gml_circle_by_center_point
                    # ):
                    #     print(i1, i2, i3, "Circle", i4)
                    for i4, c in enumerate(
                        z.aixm_curve.gml_segments.gml_geodesic_string
                    ):
                        if not c.is_valid:
                            continue

                        print(i1, i2, i3, "String", i4)

                        features.append(
                            geojson.Feature(
                                geometry=c.geometry,
                                properties={
                                    "name": self.aixm_name,
                                    "type": self.aixm_type,
                                    "designator": self.aixm_designator,
                                    "upper_limit": x.upper_limit_display,
                                    "lower_limit": x.lower_limit_display,
                                    #    x.aixm_airspace_geometry_component.aixm_the_airspace_volume.aixm_airspace_volume.aixm_lower_limit_reference,
                                    #    x.aixm_airspace_geometry_component.aixm_the_airspace_volume.aixm_airspace_volume.aixm_upper_limit,
                                    #    x.aixm_airspace_geometry_component.aixm_the_airspace_volume.aixm_airspace_volume.aixm_upper_limit_reference,
                                },
                                id=f"{self.uuid} {i1} {i2} {i3} String {i4}",
                            )
                        )

        return geojson.FeatureCollection(features=features)
