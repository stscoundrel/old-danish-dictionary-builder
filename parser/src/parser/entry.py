from enum import Enum
from typing import NamedTuple


class EntryStatus(Enum):
    VALID = ("valid",)
    PART_OF_PREVIOUS_ENTRY = "part-of-previous-entry"


class Entry(NamedTuple):
    headword: str
    definitions: str
    status: EntryStatus

    @staticmethod
    def _clean_definitions(raw_definitions: str) -> str:
        # Drop all linebreaks.
        cleaned_definitions = raw_definitions.replace("\n", "")

        return " ".join(
            [splitted for splitted in cleaned_definitions.split(" ") if splitted != ""]
        )

    @staticmethod
    def _clean_headword(raw_headword: str) -> str:
        # Drop linebreaks, headword may end in one even
        # though the headword is alreay complete.
        return raw_headword.replace("\n", "").strip()

    @staticmethod
    def _clean_headword_presentation(raw_headword: str) -> str:
        formatted_headword = raw_headword

        # Drop ending commas when present.
        if raw_headword[-1] == ",":
            # Also capitalize, but only for entries ending in comma.
            # Combined linebreak headwords can result in incorrect
            # forms of capitalization. It is essentially error in OCR.
            formatted_headword = formatted_headword[0:-1].capitalize()

        return formatted_headword

    @classmethod
    def from_raw_entry(cls, raw_entry: str) -> "Entry":
        # Naive expectation: first word is headword.
        parts = raw_entry.split(" ", maxsplit=1)
        status = EntryStatus.VALID

        headword = cls._clean_headword(parts[0])
        definitions = cls._clean_definitions(parts[1])

        # Headwords are expected to end in comma.
        if len(headword) > 0 and headword[-1] not in [",", "-"]:
            status = EntryStatus.PART_OF_PREVIOUS_ENTRY

        # Headwords with line breaks end in dash.
        # Glue the headword back together.
        if len(headword) > 0 and headword[-1] == "-":
            headword = f"{headword[0:-1]}{definitions.split(' ')[0]}"
            definitions = " ".join(definitions.split(" ")[1:])

        return Entry(
            headword=cls._clean_headword_presentation(headword),
            definitions=definitions,
            status=status,
        )
