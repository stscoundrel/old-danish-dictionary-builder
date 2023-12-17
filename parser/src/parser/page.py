import re
from enum import Enum
from typing import Final, NamedTuple

METALINE_ENTRY_SEPARATOR: Final[str] = "—"


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
            headword=headword,
            definitions=definitions,
            status=status,
        )


class Page:
    _meta_parts: list[str] | None = None
    _letters_in_page: list[str] | None = None

    def __init__(self, lines: list[str]) -> None:
        self.meta = lines[0]
        self.content = lines[1:]

    def _get_meta_parts(self) -> list[str]:
        if self._meta_parts is None:
            # Meta row often contains multitude of extra spaces.
            # Just drop them from actual meta parts when splitting.
            self._meta_parts = [
                splitted for splitted in self.meta.split(" ") if splitted != ""
            ]

            # We generally expect to get three parts: page number, first entry, last entry.
            # However, occasionally entries are dashed together. Try to separate them.
            if (
                len(self._meta_parts) == 2
                and METALINE_ENTRY_SEPARATOR in self._meta_parts[1]
            ):
                self._meta_parts = [
                    self._meta_parts[0],
                    *self._meta_parts[1].split(METALINE_ENTRY_SEPARATOR),
                ]

        return self._meta_parts

    def get_separators_for(self, letter: str) -> list[str]:
        return [
            rf"(\b{letter}\w+\b,)",  # Capital letter and words ends in comma.
            rf"(\b{letter}\w+\b-)",  # Capital letter and words ends in dash, ie. linebreak.
        ]

    def get_entry_separators(self) -> set[str]:
        return {
            separator
            for letter in self.get_letters_in_page()
            for separator in self.get_separators_for(letter)
        }

    def is_left_side_page(self) -> bool:
        return self._get_meta_parts()[0].isnumeric()

    def is_right_side_page(self) -> bool:
        return not self.is_left_side_page()

    def get_letters_in_page(self) -> list[str]:
        """
        Page can generally have 1 or 2 start letters for headwords.
        Most common case: all headwords start with same letter.
        However: it can be split between end of first & start of second letter.
        """
        if not self._letters_in_page:
            letters = set()
            if self.is_left_side_page():
                letters.add(self._get_meta_parts()[1][0].upper())
                letters.add(self._get_meta_parts()[2][0].upper())

            if self.is_right_side_page():
                letters.add(self._get_meta_parts()[0][0].upper())
                letters.add(self._get_meta_parts()[1][0].upper())

            self._letters_in_page = sorted(list(letters))

        return self._letters_in_page

    def set_letters_in_page(self, letters: list[str]) -> None:
        self._letters_in_page = letters

    def get_entries(self) -> list[Entry]:
        def _line_is_entry(line: str) -> bool:
            parts = line.split(" ")

            # Some exotic parts do not respect length, probably linebreakish thing.
            # If it breaks, its not an
            try:
                parts[0][-1]
            except IndexError:
                return False

            return len(parts) == 1 and parts[0][-1] in [",", "-"]

        raw_entries = ["\n".join(self.content)]

        for letter in self.get_letters_in_page():
            # TODO: GH-14 may need additional separators, perhaps based on
            # the end of previous definition.
            separators_regex = "|".join(self.get_separators_for(letter))

            # Unsplit content should always be in the last entry.
            line_entries_for_letter = re.split(separators_regex, raw_entries[-1])

            entries_for_letter = []

            for idx, line in enumerate(line_entries_for_letter):
                if line:
                    if idx == 0:
                        entries_for_letter.append(line)

                    if _line_is_entry(line):
                        entries_for_letter.append(line)
                    else:
                        entries_for_letter[-1] = f"{entries_for_letter[-1]}{line}"

            raw_entries = raw_entries[0:-2] + entries_for_letter

        # Format string entries to structures.
        entries = [
            Entry.from_raw_entry(raw_entry)
            for raw_entry in raw_entries
            if raw_entry != ""
        ]

        return entries
