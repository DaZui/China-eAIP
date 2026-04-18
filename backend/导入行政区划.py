from api.wsgi import application  # pyright: ignore[reportUnusedImport] # isort:skip  # noqa: F401
import json
import pathlib

import geojson
import shapely
from chinese_administrative_division.models import 行政区划

for x in pathlib.Path("../中国行政区划数据").iterdir():
    u: geojson.GeoJSON = geojson.GeoJSON.model_validate(obj=json.loads(s=x.read_text()))

    for feature in u.root.features:
        代码: str = feature.properties["gb"][3:]
        if 代码 == "":
            continue
        当前内容 = shapely.from_geojson(  # pyright: ignore[reportUnknownMemberType]
            geometry=feature.model_dump_json(),
        )

        国级 = 行政区划.objects.filter(代码="000000").exclude(代码=代码)
        省级 = 行政区划.objects.filter(代码=f"{代码[:2]}0000").exclude(代码=代码)
        地级 = 行政区划.objects.filter(代码=f"{代码[:4]}00").exclude(代码=代码)

        行政区划.objects.update_or_create(
            代码=代码,
            名称=feature.properties["name"],
            defaults={
                "上级_id": (
                    地级.get().pk
                    if 地级.exists()
                    else 省级.get().pk
                    if 省级.exists()
                    else 国级.get().pk
                ),
                "图形": json.loads(
                    s=shapely.to_geojson(  # pyright: ignore[reportUnknownMemberType]
                        geometry=当前内容,
                    ),
                ),
            },
        )
