from enum import Enum
from typing import Final, NamedTuple

KNOWN_HEADWORD_TYPOS_TO_CORRECT_VERSIONS: Final[dict[str, str]] = {
    "Azelkøbstad": "Axelkøbstad",
    "Azelvej": "Axelvej",
    "Sebbet": "Sabbat",
}


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
    def _proofread_headword(raw_headword: str) -> str:
        # OCR results in decent, but not 100% correct results. There are inevitable typos.
        # While there are no doubt typos in definitions, it is more important to patch
        # them to headwords, as that is how words are searched. Add them to mapping as
        # we come across them.
        return KNOWN_HEADWORD_TYPOS_TO_CORRECT_VERSIONS.get(raw_headword, raw_headword)

    @classmethod
    def _clean_headword_presentation(cls, raw_headword: str) -> str:
        formatted_headword = raw_headword

        # Drop ending commas when present.
        if raw_headword[-1] == ",":
            # Also capitalize, but only for entries ending in comma.
            # Combined linebreak headwords can result in incorrect
            # forms of capitalization. It is essentially error in OCR.
            formatted_headword = formatted_headword[0:-1].capitalize()

        # Fix known typos.
        return cls._proofread_headword(formatted_headword)

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
