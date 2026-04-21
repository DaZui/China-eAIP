import typing

import tqdm

from api.wsgi import application  # pyright: ignore[reportUnusedImport] # isort:skip # noqa: F401
from app import models
from china_eaip_dataset.aixm.data_types import to_meter
from china_eaip_dataset.aixm.features import CommonRoot
from china_eaip_dataset.aixm.features.airport_heliport import (
    AirportHeliport,
    Runway,
    RunwayCentrelinePoint,
    RunwayDirection,
)
from china_eaip_dataset.aixm.features.airspace import Airspace
from china_eaip_dataset.aixm.features.navaids_points import DesignatedPoint
from main import BaselineDataPackage


def handle_airport_heliport(folder: BaselineDataPackage):
    for airport in tqdm.tqdm(
        iterable=CommonRoot.model_validate(
            obj=folder.read_file("AirportHeliport")
        ).message_has_member,
        desc=folder.folder.stem,
    ):
        if airport.aixm_airport_heliport is None:
            continue
        info: AirportHeliport | None = airport.aixm_airport_heliport.aixm_time_slice[
            0
        ].aixm_airport_heliport_time_slice
        if info is None:
            continue

        data: dict[str, typing.Any] = {
            "information_valid_until": folder.effective_until,
            "aixm_designator": str(info.aixm_designator),
            "aixm_name": str(info.aixm_name),
            "aixm_location_indicator_icao": str(info.aixm_location_indicator_icao),
            "aixm_designator_iata": str(info.aixm_designator_iata),
            "aixm_type": str(info.aixm_type),
            "aixm_certified_icao": info.aixm_certified_icao_bool,
            "aixm_control_type": str(info.aixm_control_type),
            "aixm_field_elevation": to_meter(value=info.aixm_field_elevation),
            "aixm_field_elevation_accuracy": to_meter(
                value=info.aixm_field_elevation_accuracy
            ),
            "aixm_magnetic_variation": info.aixm_magnetic_variation_float,
            "aixm_magnetic_variation_accuracy": info.aixm_magnetic_variation_accuracy_float,
            "aixm_date_magnetic_variation": info.aixm_date_magnetic_variation_int,
            "aixm_magnetic_variation_change": info.aixm_magnetic_variation_change_float,
            "aixm_reference_temperature": info.aixm_reference_temperature_float,
            "aixm_certification_date": info.aixm_certification_date_datetime_date,
            "aixm_certification_expiration_date": info.aixm_certification_expiration_date_datetime_date,
            "aixm_served_city": str(info.aixm_served_city[0].aixm_city.aixm_name),
            "aixm_latitude": info.aixm_arp.aixm_elevated_point.latitude,
            "aixm_longitude": info.aixm_arp.aixm_elevated_point.longitude,
            "aixm_horizontal_accuracy": info.aixm_arp.aixm_elevated_point.horizontal_accuracy,
            "aixm_annotations": info.annotation,
            "aixm_availability": info.availability,
        }
        models.AirportHeliport.objects.update_or_create(
            uuid=airport.aixm_airport_heliport.at_gml_id,
            aixm_sequence_number=info.aixm_sequence_number,
            aixm_correction_number=info.aixm_correction_number,
            defaults=data,
            create_defaults={
                **data,
                "information_valid_since": info.gml_valid_time.gml_time_period.gml_begin_position.dollar,
            },
        )


def handle_airspace(folder: BaselineDataPackage):
    for airport in tqdm.tqdm(
        iterable=CommonRoot.model_validate(
            obj=folder.read_file("Airspace")
        ).message_has_member,
        desc=folder.folder.stem,
    ):
        if airport.aixm_airspace is None:
            continue
        info: Airspace | None = airport.aixm_airspace.aixm_time_slice[
            0
        ].aixm_airspace_time_slice
        if info is None:
            continue

        data: dict[str, typing.Any] = {
            "information_valid_until": folder.effective_until,
            "aixm_designator": str(info.aixm_designator),
            "aixm_name": str(info.aixm_name),
            "aixm_type": str(info.aixm_type),
            "aixm_geometry_components": info.aixm_geometry_component.model_dump(
                mode="json"
            ),
        }
        models.Airspace.objects.update_or_create(
            uuid=airport.aixm_airspace.at_gml_id,
            aixm_sequence_number=info.aixm_sequence_number,
            aixm_correction_number=info.aixm_correction_number,
            defaults=data,
            create_defaults={
                **data,
                "information_valid_since": info.gml_valid_time.gml_time_period.gml_begin_position.dollar,
            },
        )


def handle_designated_point(folder: BaselineDataPackage):
    for designated_point in tqdm.tqdm(
        iterable=CommonRoot.model_validate(
            obj=folder.read_file("DesignatedPoint")
        ).message_has_member,
        desc=folder.folder.stem,
    ):
        if designated_point.aixm_designated_point is None:
            continue
        info: DesignatedPoint | None = (
            designated_point.aixm_designated_point.aixm_time_slice[
                0
            ].aixm_designated_point_time_slice
        )
        if info is None:
            continue

        data: dict[str, typing.Any] = {
            "information_valid_until": folder.effective_until,
            "aixm_designator": str(info.aixm_designator),
            "aixm_name": str(info.aixm_name),
            "aixm_latitude": info.aixm_location.aixm_point.latitude,
            "aixm_longitude": info.aixm_location.aixm_point.longitude,
            "aixm_horizontal_accuracy_in_meter": info.aixm_location.aixm_point.horizontal_accuracy,
            "aixm_airport_heliport": ""
            if info.aixm_airport_heliport is None
            else info.aixm_airport_heliport.at_xlink_href.replace("urn:uuid:", ""),
        }
        models.DesignatedPoint.objects.update_or_create(
            uuid=designated_point.aixm_designated_point.at_gml_id,
            aixm_sequence_number=info.aixm_sequence_number,
            aixm_correction_number=info.aixm_correction_number,
            defaults=data,
            create_defaults={
                **data,
                "information_valid_since": info.gml_valid_time.gml_time_period.gml_begin_position.dollar,
            },
        )


def handle_runway(folder: BaselineDataPackage):
    for runway in tqdm.tqdm(
        iterable=CommonRoot.model_validate(
            obj=folder.read_file("Runway")
        ).message_has_member,
        desc=folder.folder.stem,
    ):
        if runway.aixm_runway is None:
            continue
        info: Runway | None = runway.aixm_runway.aixm_time_slice[
            0
        ].aixm_runway_time_slice
        if info is None:
            continue

        data: dict[str, typing.Any] = {
            "information_valid_until": folder.effective_until,
            "aixm_designator": str(info.aixm_designator),
            "aixm_nominal_length": to_meter(value=info.aixm_nominal_length),
            "aixm_length_accuracy": to_meter(value=info.aixm_length_accuracy),
            "aixm_nominal_width": to_meter(value=info.aixm_nominal_width),
            "aixm_width_accuracy": to_meter(value=info.aixm_width_accuracy),
            "aixm_width_shoulder": to_meter(value=info.aixm_width_shoulder),
            "aixm_annotations": info.annotation,
            "aixm_associated_airport_heliport": info.aixm_associated_airport_heliport.at_xlink_href.replace(
                "urn:uuid:", ""
            ),
        }
        models.Runway.objects.update_or_create(
            uuid=runway.aixm_runway.at_gml_id,
            aixm_sequence_number=info.aixm_sequence_number,
            aixm_correction_number=info.aixm_correction_number,
            defaults=data,
            create_defaults={
                **data,
                "information_valid_since": info.gml_valid_time.gml_time_period.gml_begin_position.dollar,
            },
        )


def handle_runway_centreline_point(folder: BaselineDataPackage):
    for runway_centreline_point in tqdm.tqdm(
        iterable=CommonRoot.model_validate(
            obj=folder.read_file("RunwayCentrelinePoint")
        ).message_has_member,
        desc=folder.folder.stem,
    ):
        if runway_centreline_point.aixm_runway_centreline_point is None:
            continue
        info: RunwayCentrelinePoint | None = (
            runway_centreline_point.aixm_runway_centreline_point.aixm_time_slice[
                0
            ].aixm_runway_centreline_point_time_slice
        )
        if info is None:
            continue

        data: dict[str, typing.Any] = {
            "information_valid_until": folder.effective_until,
            "aixm_role": str(info.aixm_role),
            "aixm_on_runway": info.aixm_on_runway.at_xlink_href.replace(
                "urn:uuid:", ""
            ),
        }
        models.RunwayCentrelinePoint.objects.update_or_create(
            uuid=runway_centreline_point.aixm_runway_centreline_point.at_gml_id,
            aixm_sequence_number=info.aixm_sequence_number,
            aixm_correction_number=info.aixm_correction_number,
            defaults=data,
            create_defaults={
                **data,
                "information_valid_since": info.gml_valid_time.gml_time_period.gml_begin_position.dollar,
            },
        )


def handle_runway_direction(folder: BaselineDataPackage):
    for runway_direction in tqdm.tqdm(
        iterable=CommonRoot.model_validate(
            obj=folder.read_file("RunwayDirection")
        ).message_has_member,
        desc=folder.folder.stem,
    ):
        if runway_direction.aixm_runway_direction is None:
            continue
        info: RunwayDirection | None = (
            runway_direction.aixm_runway_direction.aixm_time_slice[
                0
            ].aixm_runway_direction_time_slice
        )
        if info is None:
            continue

        data: dict[str, typing.Any] = {
            "information_valid_until": folder.effective_until,
            "aixm_designator": str(info.aixm_designator),
            "aixm_true_bearing": info.aixm_true_bearing_float,
            "aixm_true_bearing_accuracy": info.aixm_true_bearing_accuracy_float,
            "aixm_used_runway": info.aixm_used_runway.at_xlink_href.replace(
                "urn:uuid:", ""
            ),
        }
        models.RunwayDirection.objects.update_or_create(
            uuid=runway_direction.aixm_runway_direction.at_gml_id,
            aixm_sequence_number=info.aixm_sequence_number,
            aixm_correction_number=info.aixm_correction_number,
            defaults=data,
            create_defaults={
                **data,
                "information_valid_since": info.gml_valid_time.gml_time_period.gml_begin_position.dollar,
            },
        )


for folder in sorted(BaselineDataPackage.list_all(), key=lambda x: x.filename):
    # handle_airport_heliport(folder=folder)
    # handle_airspace(folder=folder)
    # handle_designated_point(folder=folder)
    # handle_runway(folder=folder)
    # handle_runway_direction(folder=folder)
    handle_runway_centreline_point(folder=folder)
