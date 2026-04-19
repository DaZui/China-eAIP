import typing

from china_eaip_dataset import geojson
from china_eaip_dataset.aixm.features.airspace import AixmGeometryCompoents
from django.db import models

from ..schemas import Properties2
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
    def features(self) -> geojson.FeatureCollection:
        features: list[geojson.Feature] = []

        components: AixmGeometryCompoents = AixmGeometryCompoents.model_validate(
            obj=self.aixm_geometry_components, by_name=True, by_alias=True
        )
        for i1, x in enumerate(iterable=components.root):
            properties: Properties2 = Properties2(
                uuid=self.uuid,
                information_valid_since=self.information_valid_since,
                information_valid_until=self.information_valid_until,
                aixm_sequence_number=self.aixm_sequence_number,
                aixm_correction_number=self.aixm_correction_number,
                aixm_type=self.aixm_type,
                aixm_designator=self.aixm_designator,
                aixm_name=self.aixm_name,
                upper_limit=x.高度上限,
                lower_limit=x.高度下限,
            )

            for i2, y in enumerate(
                iterable=x.aixm_airspace_geometry_component.aixm_the_airspace_volume.aixm_airspace_volume.aixm_horizontal_projection.aixm_elevated_surface.gml_patches.gml_polygon_patch
            ):
                for i3, z in enumerate(y.gml_exterior.gml_ring.gml_curve_member):
                    for i4, a in enumerate(
                        iterable=z.aixm_curve.gml_segments.gml_arc_by_center_point
                    ):
                        if a.is_valid:
                            features.append(
                                geojson.Feature(
                                    geometry=a.geometry,
                                    properties=properties,
                                    id=f"{self.uuid} {i1} {i2} {i3} ArcByCenterPoint {i4}",
                                )
                            )

                    for i4, b in enumerate(
                        iterable=z.aixm_curve.gml_segments.gml_circle_by_center_point
                    ):
                        if b.is_valid:
                            features.append(
                                geojson.Feature(
                                    geometry=b.geometry,
                                    properties=properties,
                                    id=f"{self.uuid} {i1} {i2} {i3} CircleByCenterPoint {i4}",
                                )
                            )

                    for i4, c in enumerate(
                        iterable=z.aixm_curve.gml_segments.gml_geodesic_string
                    ):
                        if c.is_valid:
                            features.append(
                                geojson.Feature(
                                    geometry=c.geometry,
                                    properties=properties,
                                    id=f"{self.uuid} {i1} {i2} {i3} gml_geodesic_string {i4}",
                                )
                            )

        return geojson.FeatureCollection(features=features)
