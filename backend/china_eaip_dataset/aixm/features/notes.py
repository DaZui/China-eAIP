from typing import Annotated

from pydantic import Field

from ...base import BaseModel, WithAtGmlId
from ..data_types import CodeNotePurposeType, TextNoteType, TextPropertyNameType


class _LinguisticNote(WithAtGmlId):
    """https://aixm.aero/sites/default/files/imce/AIXM511HTML/AIXM/Class_LinguisticNote.html"""

    aixm_note: Annotated[TextNoteType, Field(alias="aixm:note")]


class Note(WithAtGmlId):
    """https://aixm.aero/sites/default/files/imce/AIXM511HTML/AIXM/Class_Note.html"""

    aixm_property_name: Annotated[
        TextPropertyNameType, Field(alias="aixm:propertyName")
    ]
    aixm_purpose: Annotated[CodeNotePurposeType, Field(alias="aixm:purpose")]

    class _AixmTranslatedNoteItem(BaseModel):
        aixm_linguistic_note: Annotated[
            _LinguisticNote, Field(alias="aixm:LinguisticNote")
        ]

    aixm_translated_note: Annotated[
        list[_AixmTranslatedNoteItem], Field(alias="aixm:translatedNote")
    ]


class WithAixmAnnotation(BaseModel):
    class _AixmAnnotationItem(BaseModel):
        aixm_note: Annotated[Note, Field(alias="aixm:Note")]

    aixm_annotation: Annotated[
        list[_AixmAnnotationItem], Field(alias="aixm:annotation")
    ] = []
