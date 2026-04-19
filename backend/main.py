from api.wsgi import application  # pyright: ignore[reportUnusedImport] # isort:skip # noqa: F401
import collections.abc
import datetime
import functools
import json
import os
import pathlib
import re
import typing

import china_eaip_dataset.aixm.features
import china_eaip_dataset.geojson
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
        cls, timestamp: datetime.datetime = datetime.datetime.now(datetime.UTC)
    ) -> collections.abc.Iterable[typing.Self]:
        for x in root_path.iterdir():
            if x.is_dir():
                folder: typing.Self = cls(filename=x.stem, reference=timestamp)
                if folder.is_valid:
                    yield folder

    filename: str

    @functools.cached_property
    def folder(self) -> pathlib.Path:
        return root_path.joinpath(self.filename)

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

    def read_file(self, keyword: File) -> typing.Any:
        for file in self.folder.joinpath("Baseline").iterdir():
            if f"_{keyword}_" in file.stem:
                cache_file = pathlib.Path(f"./cache/{self.filename}/{keyword}.json")
                if not cache_file.exists():
                    cache_file.parent.mkdir(parents=True, exist_ok=True)
                    text: str = json.dumps(
                        obj=schema.to_dict(source=file, force_dict=True),
                        indent=2,
                        sort_keys=True,
                        ensure_ascii=False,
                        default=str,
                    )
                    cache_file.write_text(data=text)
                return json.loads(s=cache_file.read_text())
        raise FileNotFoundError


# 允许 CORS 跨站访问
web_app.add_middleware(
    middleware_class=cors.CORSMiddleware,
    allow_origins=[
        "*",
    ],
)


@web_app.get(path="/api/china-eaip-datasets")
def list_all_datasets(
    timestamp: datetime.datetime = datetime.datetime.now(tz=datetime.UTC),
) -> list[BaselineDataPackage]:
    return list(BaselineDataPackage.list_all(timestamp=timestamp))


@web_app.get(path="/api/china-eaip-datasets/{filename}/{keyword}")
def airport_heliport_dataset_by_timestamp(
    filename: str, keyword: File
) -> china_eaip_dataset.aixm.features.CommonRoot:
    return china_eaip_dataset.aixm.features.CommonRoot.model_validate(
        obj=BaselineDataPackage(filename=filename).read_file(keyword=keyword)
    )


@web_app.get(path="/api/china-eaip-datasets/{filename}/AirportHeliport/elements")
def list_all_airports_heliports(
    filename: str,
) -> list[schemas.AirportHeliport]:
    package: BaselineDataPackage = BaselineDataPackage(filename=filename)
    return [
        x.feature
        for x in models.AirportHeliport.objects.filter(
            information_valid_since__lte=package.effective_since,
            information_valid_until__gte=package.effective_until,
        ).order_by("aixm_designator")
    ]


@web_app.get(path="/api/china-eaip-datasets/{filename}/Airspace/elements")
def list_all_airspaces(
    filename: str,
) -> list[china_eaip_dataset.geojson.FeatureCollection]:
    package: BaselineDataPackage = BaselineDataPackage(filename=filename)
    return [
        y
        for x in models.Airspace.objects.filter(
            aixm_type="FIR",
            # aixm_name="BEIJING FIR",
            information_valid_since__lte=package.effective_since,
            information_valid_until__gte=package.effective_until,
        ).order_by("aixm_designator")
        if len((y := x.feature).features) > 1
    ]


@web_app.get(path="/api/china-eaip-datasets/{filename}/{keyword}")
def fetch_china_eaip_dataset_by_timestamp(filename: str, keyword: File) -> typing.Any:
    return BaselineDataPackage(filename=filename).read_file(keyword=keyword)


# 挂载 django app 的其他部分
web_app.mount(
    path="/static",
    app=staticfiles.StaticFiles(
        directory="./static",
    ),
)
web_app.mount(
    path="/",
    app=wsgi.WSGIMiddleware(
        app=application,
    ),
)

if __name__ == "__main__":
    uvicorn.run(app="main:web_app", reload=True, host="::")
