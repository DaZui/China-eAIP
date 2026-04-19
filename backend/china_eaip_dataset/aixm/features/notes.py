from typing import Annotated

from pydantic import Field

from ...base import BaseModel, Nil, WithAtGmlId
from ..data_types import CodeNotePurposeType, TextNoteType, TextPropertyNameType


class _LinguisticNote(WithAtGmlId):
    """https://aixm.aero/sites/default/files/imce/AIXM511HTML/AIXM/Class_LinguisticNote.html"""

    aixm_note: Annotated[TextNoteType, Field(alias="aixm:note")]


class _Note(WithAtGmlId):
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
        aixm_note: Annotated[_Note, Field(alias="aixm:Note")]

    aixm_annotation: Annotated[
        list[_AixmAnnotationItem], Field(alias="aixm:annotation")
    ] = []

    @property
    def annotation(self) -> str:
        return "\n\n".join(
            sorted(
                {
                    f"{x.aixm_note.aixm_property_name} {x.aixm_note.aixm_purpose}:\n"
                    + "\n".join(
                        sorted(
                            {
                                f"{y.aixm_linguistic_note.aixm_note.at_lang}: {y.aixm_linguistic_note.aixm_note.dollar}"
                                for y in x.aixm_note.aixm_translated_note
                                if not isinstance(y.aixm_linguistic_note.aixm_note, Nil)
                            }
                        )
                    )
                    for x in self.aixm_annotation
                }
            )
        )
