from api.wsgi import application  # pyright: ignore[reportUnusedImport] # isort:skip
import collections.abc
import datetime
import functools
import json
import os
import pathlib
import re
import typing
import zipfile

import django.db.models
import fastapi
import pydantic
import uvicorn
import xmlschema
from app import models, schemas
from fastapi import staticfiles
from fastapi.middleware import cors, wsgi

web_app = fastapi.FastAPI(
    debug=os.environ.get("DEBUG", default="True") == "True",
    title="Aeronautical Map",
    summary="API endpoints for various aviation related information.",
    version="1.0.0",
    # description="API endpoints for various aviation related information.",
    terms_of_service="https://hanming.li",
    contact={
        "name": '李瀚明 Li Hanming "Jason" @ Li & Li 李及李',
        "url": "https://hanming.li",
    },
)
File = typing.Literal[
    "AirportHeliport",
    "Airspace",
    "AirTrafficControlService",
    "DesignatedPoint",
    "DME",
    "Glidepath",
    "Localizer",
    "MarkerBeacon",
    "Navaid",
    "NDB",
    "RadioCommunicationChannel",
    "Route",
    "RouteSegment",
    "Runway",
    "RunwayCentrelinePoint",
    "RunwayDirection",
    "Unit",
    "VOR",
]
root_path: pathlib.Path = pathlib.Path("../data")
schema: xmlschema.XMLSchema = xmlschema.XMLSchema(
    pathlib.Path("../schema/aixm511/xsd/message/AIXM_BasicMessage.xsd")
)


class BaselineDataPackage(
    pydantic.BaseModel, frozen=True, title="基准数据包 Baseline Data Package"
):
    """
    基准数据包包含特定时期内有效的完整航空数据，包括所有当前基准数据、相应的差异数据（用于跟踪与先前版本的变化）以及用于数据完整性验证的校验和文件。

    A Baseline Data Package contains the complete set of valid aeronautical data for a specific period, including all current Baseline data, corresponding differential data (to track changes from previous versions), and checksum files for data integrity verification.
    """

    @classmethod
    def list_all(
        cls, timestamp: datetime.datetime | None = None
    ) -> collections.abc.Iterable[typing.Self]:
        if timestamp is None:
            timestamp = datetime.datetime.now(datetime.UTC)
        for x in root_path.iterdir():
            if not x.is_dir() and x.suffix != ".zip":
                continue
            folder: typing.Self = cls(filename=x.stem, reference=timestamp)
            if folder.is_valid:
                yield folder

    filename: str

    @functools.cached_property
    def folder(self) -> pathlib.Path:
        """数据包所在的位置，可能是已解压的目录，也可能是尚未解压的 ZIP 压缩包。"""
        folder: pathlib.Path = root_path.joinpath(self.filename)
        if folder.is_dir():
            return folder
        return root_path.joinpath(f"{self.filename}.zip")

    reference: typing.Annotated[
        datetime.datetime,
        pydantic.Field(
            exclude=True,
            title="参考时间",
            description="用于显示当前 Package 是否有效。",
        ),
    ] = datetime.datetime.now(tz=datetime.UTC)

    @functools.cached_property
    def match(self) -> re.Match[str] | None:
        return re.fullmatch(
            pattern=r"^CN_AIP-DS_EFF(\d{12})_(AIRAC\d{4})_(V\d)$",
            string=self.filename,
        )

    @functools.cached_property
    def is_valid(self) -> bool:
        return self.match is not None

    @pydantic.computed_field(
        title="发布编号 Publication Number",
        description="符合航空情报定期颁发周期的发布，格式为 AIRAC[修订编号]（例如 AIRAC2501 表示 2025 年第一个航空情报定期颁发周期）；非航空情报定期颁发周期发布按业务需求定义。For AIRAC compliant releases, this follows the format AIRAC[Amendment Number] (e.g., AIRAC2501 for the first AIRAC cycle of 2025). For non AIRAC releases, it is defined by business requirements.",
        examples=["AIRAC2501"],
    )
    @functools.cached_property
    def publication_number(self) -> str:
        assert self.match
        return self.match[2]

    @pydantic.computed_field(
        title="版本号 Version Number",
        description='表示数据包的发布版本，格式为 V[版本号]。数据包首次发布统一为“V0”。Indicates the release version of the package, formatted as V[Version Number]. The initial release of a package is uniformly "V0".',
        examples=["V0"],
    )
    @functools.cached_property
    def version_number(self) -> str:
        assert self.match
        return self.match[3]

    @pydantic.computed_field(
        title="生效时间 Effective Time",
        description="数据包数据生效的时间。The time when the data in the package becomes valid.",
        examples=[datetime.datetime.fromisoformat("2025-01-22T16:00Z")],
    )
    @functools.cached_property
    def effective_since(self) -> datetime.datetime:
        assert self.match
        return datetime.datetime.strptime(self.match[1], "%Y%m%d%H%M").replace(
            tzinfo=datetime.UTC
        )

    @functools.cached_property
    def effective_until(self) -> datetime.datetime:
        return self.effective_since + datetime.timedelta(days=28)

    @pydantic.computed_field
    @functools.cached_property
    def status(self) -> typing.Literal["expired", "current", "upcoming"]:
        if self.reference >= self.effective_until:
            return "expired"
        if self.reference >= self.effective_since:
            return "current"
        return "upcoming"

    def read_baseline(self, keyword: File) -> pathlib.Path | bytes:
        """定位 Baseline 中文件名含有 keyword 的 XML，返回其路径或内容。"""
        if self.folder.is_dir():
            for file in self.folder.joinpath("Baseline").iterdir():
                if f"_{keyword}_" in file.stem:
                    return file
        else:
            with zipfile.ZipFile(self.folder) as archive:
                for name in archive.namelist():
                    path: pathlib.PurePosixPath = pathlib.PurePosixPath(name)
                    if path.parent.name == "Baseline" and f"_{keyword}_" in path.stem:
                        return archive.read(name)
        raise FileNotFoundError(f"{self.filename} 中没有 {keyword}")

    def read_file(self, keyword: File) -> typing.Any:
        cache_file: pathlib.Path = pathlib.Path(
            f"./cache/{self.filename}/{keyword}.json"
        )
        if not cache_file.exists():
            cache_file.parent.mkdir(parents=True, exist_ok=True)
            cache_file.write_text(
                data=json.dumps(
                    obj=schema.to_dict(
                        source=self.read_baseline(keyword), force_dict=True
                    ),
                    indent=2,
                    sort_keys=True,
                    ensure_ascii=False,
                    default=str,
                )
            )
        return json.loads(s=cache_file.read_text())


# 允许 CORS 跨站访问
web_app.add_middleware(middleware_class=cors.CORSMiddleware, allow_origins=["*"])


# raw/*.zip 解压后的离线 eAIP 网页包目录 (docker-compose 中以只读方式挂载)
aip_root: pathlib.Path = pathlib.Path(
    os.environ.get("EAIP_CONTENT_ROOT", default="../content")
)


class EaipWebPackage(
    pydantic.BaseModel, frozen=True, title="电子 AIP 网页包 eAIP Web Package"
):
    """
    由 raw/ 中对应的 zip 解压得到的离线 eAIP 站点，目录名形如 EAIP2026-10.V1.4_Web。

    An offline eAIP website extracted from the corresponding zip in raw/, with a
    directory name such as EAIP2026-10.V1.4_Web.
    """

    @classmethod
    def list_all(cls) -> collections.abc.Iterable[typing.Self]:
        if not aip_root.is_dir():
            return
        for folder in sorted(aip_root.iterdir()):
            match: re.Match[str] | None = re.fullmatch(
                pattern=r"EAIP(\d{4})-(\d{2})\.(V[\d.]+)_Web",
                string=folder.name,
            )
            if not folder.is_dir() or match is None:
                continue
            yield cls(
                name=folder.name,
                year=int(match[1]),
                issue=int(match[2]),
                version=match[3],
                modified=datetime.datetime.fromtimestamp(
                    timestamp=folder.stat().st_mtime, tz=datetime.UTC
                ),
            )

    name: str = pydantic.Field(
        title="目录名 Folder Name",
        description="解压后的目录名，同时也是站点根路径下的访问路径。",
        examples=["EAIP2026-10.V1.4_Web"],
    )
    year: int = pydantic.Field(title="年份 Year", examples=[2026])
    issue: int = pydantic.Field(title="期号 Issue Number", examples=[10])
    version: str = pydantic.Field(title="版本号 Version Number", examples=["V1.4"])
    modified: datetime.datetime = pydantic.Field(
        title="解压时间 Extracted At",
        description="数据包解压到服务器的时间。",
    )

    @pydantic.computed_field(
        title="访问路径 URL",
        description="站点根路径下访问该 eAIP 站的相对地址。",
        examples=["/EAIP2026-10.V1.4_Web/"],
    )
    @functools.cached_property
    def url(self) -> str:
        return f"/{self.name}/"


@web_app.get(
    path="/api/china-eaip-datasets/EaipWebPackages",
    response_model=list[EaipWebPackage],
)
def 列出所有电子AIP网页包() -> list[EaipWebPackage]:
    """列出已解压的各期电子 AIP 网页包，供前端在同一站点下跳转浏览。"""
    return sorted(
        EaipWebPackage.list_all(),
        key=lambda package: (
            package.year,
            package.issue,
            *[int(part) for part in package.version.lstrip("V").split(".")],
        ),
        reverse=True,
    )


def 根据时间戳建立查询(timestamp: pydantic.AwareDatetime) -> django.db.models.Q:
    return django.db.models.Q(
        information_valid_since__lte=timestamp, information_valid_until__gt=timestamp
    )


@web_app.get(path="/api/china-eaip-datasets/AirportHeliports")
def 列出所有机场(
    query: typing.Annotated[
        django.db.models.Q,
        fastapi.Depends(dependency=根据时间戳建立查询, use_cache=True),
    ],
) -> list[schemas.AirportHeliport]:
    airports: django.db.models.QuerySet[models.AirportHeliport] = (
        models.AirportHeliport.objects.filter(query).order_by("aixm_designator")
    )
    runways: django.db.models.QuerySet[models.Runway] = models.Runway.objects.filter(
        query
    ).order_by("aixm_designator")
    runway_centreline_points: django.db.models.QuerySet[
        models.RunwayCentrelinePoint
    ] = models.RunwayCentrelinePoint.objects.filter(query)
    runway_directions: django.db.models.QuerySet[models.RunwayDirection] = (
        models.RunwayDirection.objects.filter(query).order_by("aixm_designator")
    )

    rv: list[schemas.AirportHeliport] = []
    for airport in airports:
        output_airport: schemas.AirportHeliport = (
            schemas.AirportHeliport.model_validate(obj=airport, from_attributes=True)
        )
        for runway in runways.filter(aixm_associated_airport_heliport=airport.uuid):
            output_runway: schemas.Runway = schemas.Runway.model_validate(
                obj=runway, from_attributes=True
            )
            for direction in runway_directions.filter(aixm_used_runway=runway.uuid):
                output_direction: schemas.RunwayDirection = (
                    schemas.RunwayDirection.model_validate(
                        obj=direction, from_attributes=True
                    )
                )
                for centreline_point in runway_centreline_points.filter(
                    aixm_on_runway=direction.uuid
                ):
                    output_centreline_point: schemas.RunwayCentrelinePoint = (
                        schemas.RunwayCentrelinePoint.model_validate(
                            obj=centreline_point, from_attributes=True
                        )
                    )
                    output_direction.中线点s.append(output_centreline_point)
                output_runway.方向s.append(output_direction)
            output_airport.跑道s.append(output_runway)
        rv.append(output_airport)
    return rv


@web_app.get(
    path="/api/china-eaip-datasets/Runways", response_model=list[schemas.Runway]
)
def 列出一座机场的所有跑道(
    airportHeliportId: str, timestamp: pydantic.AwareDatetime
) -> django.db.models.QuerySet[models.Runway]:
    return models.Runway.objects.filter(
        aixm_associated_airport_heliport=airportHeliportId,
        information_valid_since__lte=timestamp,
        information_valid_until__gt=timestamp,
    ).order_by("aixm_designator", "information_valid_since")


# 挂载 django app 的其他部分
web_app.mount(path="/static", app=staticfiles.StaticFiles(directory="./static"))
web_app.mount(path="/", app=wsgi.WSGIMiddleware(app=application))

if __name__ == "__main__":
    uvicorn.run(app="main:web_app", reload=True, host="::")
