from api.wsgi import application  # pyright: ignore[reportUnusedImport] # isort:skip # noqa: F401
import datetime

import tqdm
from app import models
from china_eaip_dataset.aixm.features import CommonRoot
from china_eaip_dataset.aixm.features.airport_heliport import AirportHeliport
from main import BaselineDataPackage

for folder in BaselineDataPackage.list_all(
    timestamp=datetime.datetime.now(tz=datetime.UTC)
):
    for airport in tqdm.tqdm(
        iterable=CommonRoot.model_validate(
            obj=folder.read_file("AirportHeliport")
        ).message_has_member,
        desc=f"{folder.folder.stem}",
    ):
        if airport.aixm_airport_heliport is None:
            continue
        info: AirportHeliport | None = airport.aixm_airport_heliport.aixm_time_slice[
            0
        ].aixm_airport_heliport_time_slice
        if info is None:
            continue

        models.AirportHeliport.objects.update_or_create(
            uuid=airport.aixm_airport_heliport.at_gml_id,
            aixm_sequence_number=info.aixm_sequence_number,
            aixm_correction_number=info.aixm_correction_number,
            aixm_designator=str(info.aixm_designator),
            aixm_name=str(info.aixm_name),
            aixm_location_indicator_icao=str(info.aixm_location_indicator_icao),
            aixm_designator_iata=str(info.aixm_designator_iata),
            aixm_type=str(info.aixm_type),
            aixm_certified_icao=info.aixm_certified_icao_bool,
            aixm_control_type=str(info.aixm_control_type),
            aixm_field_elevation=info.aixm_field_elevation_float,
            aixm_field_elevation_accuracy=info.aixm_field_elevation_accuracy_float,
            aixm_magnetic_variation=info.aixm_magnetic_variation_float,
            aixm_magnetic_variation_accuracy=info.aixm_magnetic_variation_accuracy_float,
            aixm_date_magnetic_variation=info.aixm_date_magnetic_variation_int,
            aixm_magnetic_variation_change=info.aixm_magnetic_variation_change_float,
            aixm_reference_temperature=info.aixm_reference_temperature_float,
            aixm_certification_date=info.aixm_certification_date_datetime_date,
            aixm_certification_expiration_date=info.aixm_certification_expiration_date_datetime_date,
            aixm_city=str(info.aixm_served_city[0].aixm_city.aixm_name),
            aixm_latitude=info.aixm_arp.aixm_elevated_point.latitude,
            aixm_longitude=info.aixm_arp.aixm_elevated_point.longitude,
            information_valid_since__lte=folder.effective_since,
            defaults={
                "information_valid_until": folder.effective_until,
            },
            create_defaults={
                "information_valid_since": folder.effective_since,
                "information_valid_until": folder.effective_until,
            },
        )
