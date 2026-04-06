import json
import pathlib
import typing

import main


def helper(location: str, suffix: main.File) -> None:
    data: typing.Any = main.airport_heliport_dataset_by_timestamp(
        filename=location, keyword=suffix
    ).model_dump(mode="json", by_alias=True, exclude_unset=True)
    string: str = json.dumps(obj=data, ensure_ascii=False, indent=2, sort_keys=True)
    pathlib.Path(f"cache/{location}/{suffix}.json").write_text(data=string)


def main_function() -> None:
    for x in main.list_all_datasets():
        print(x)
        for v in (
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
        ):
            helper(x.filename, v)


main_function()
