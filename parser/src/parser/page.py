import re
from typing import NamedTuple


class Entry(NamedTuple):
    headword: str
    definitions: str

    @staticmethod
    def from_raw_entry(raw_entry: str) -> "Entry":
        # Naive expectation: first word is headword.
        # TODO: GH-16 better detection.
        parts = raw_entry.split(" ", maxsplit=1)

        return Entry(
            headword=parts[0],
            # TODO: GH-17 clean up content.
            definitions=parts[1],
        )


class Page:
    _meta_parts: list[str] | None = None

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

        return self._meta_parts

    def get_separators_for(self, letter: str) -> list[str]:
        return [f"— {letter}", f"   {letter}"]

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

    def get_letters_in_page(self) -> set[str]:
        """
        Page can generally have 1 or 2 start letters for headwords.
        Most common case: all headwords start with same letter.
        However: it can be split between end of first & start of second letter.
        """
        letters = set()
        if self.is_left_side_page():
            letters.add(self._get_meta_parts()[1][0].upper())
            letters.add(self._get_meta_parts()[2][0].upper())

        if self.is_right_side_page():
            letters.add(self._get_meta_parts()[0][0].upper())
            letters.add(self._get_meta_parts()[1][0].upper())

        return letters

    def get_entries(self) -> list[Entry]:
        raw_entries = ["\n".join(self.content)]

        for letter in self.get_letters_in_page():
            # TODO: GH-14 may need additional separators, perhaps based on
            # the end of previous definition.
            separators_regex = "|".join(self.get_separators_for(letter))

            # Unsplit content should always be in the last entry.
            entries_for_letter = re.split(separators_regex, raw_entries[-1])

            # TODO: GH-13. Only append if not the first entry.
            # If first entry, detect if start of entry or not.
            # Probably needs to support incomplete entries to be patched later.

            # Append base letter back
            entries_for_letter = [f"{letter}{entry}" for entry in entries_for_letter]

            raw_entries = raw_entries[0:-2] + entries_for_letter

        # Format string entries to structures.
        # TODO: GH-16 recognize incorrect headwords, append to previous entries.
        entries = [Entry.from_raw_entry(raw_entry) for raw_entry in raw_entries]

        return entries
