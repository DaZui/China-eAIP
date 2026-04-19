import typing

from china_eaip_dataset import geojson
from china_eaip_dataset.aixm.features.airspace import AixmGeometryCompoents
from django.db import models

from .. import schemas
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
    def geometries(self) -> geojson.GeometryCollection:
        s: AixmGeometryCompoents = AixmGeometryCompoents.model_validate(
            self.aixm_geometry_components, by_name=True
        )
        rv: list[geojson.LineString] = []
        for x in s.root:
            for y in x.aixm_airspace_geometry_component.aixm_the_airspace_volume.aixm_airspace_volume.aixm_horizontal_projection.aixm_elevated_surface.gml_patches.gml_polygon_patch:
                for z in y.gml_exterior.gml_ring.gml_curve_member:
                    for a in z.aixm_curve.gml_segments.gml_arc_by_center_point:
                        print(a)
                    for b in z.aixm_curve.gml_segments.gml_circle_by_center_point:
                        print(b)
                    for c in z.aixm_curve.gml_segments.gml_geodesic_string:
                        points: list[tuple[float, float]] = list(
                            zip(
                                c.gml_pos_list.dollar[1::2],
                                c.gml_pos_list.dollar[::2],
                            )
                        )

                        if len(points) < 2:
                            continue

                        rv.append(geojson.LineString(coordinates=points))

        return geojson.GeometryCollection(geometries=rv)

    @property
    def feature(self) -> schemas.Airspace:
        print(self.geometries)
        return schemas.Airspace(
            geometry=self.geometries,
            properties=schemas.Properties2.model_validate(
                obj=self, from_attributes=True
            ),
            id=self.uuid,
        )
