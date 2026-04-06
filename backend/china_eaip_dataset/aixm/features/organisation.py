from typing import Annotated

from pydantic import Field

from ..abstract_feature import AixmTimeSlice
from ..data_types import TextNameType


class Unit(AixmTimeSlice):
    aixm_name: Annotated[TextNameType, Field(alias="aixm:name")]
