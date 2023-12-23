import re
from typing import Final

from src.parser.entry import Entry

METALINE_ENTRY_SEPARATOR: Final[str] = "—"


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
                splitted.replace("\n", "")
                for splitted in self.meta.split(" ")
                if splitted != ""
            ]

            # We generally expect to get three parts: page number, first entry, last entry.
            # (or reverse for other side pages)
            # However, occasionally entries are dashed together. Try to separate them.
            if len(self._meta_parts) == 2:
                number_part = (
                    self._meta_parts[0]
                    if self.is_left_side_page()
                    else self._meta_parts[1]
                )
                words_part = (
                    self._meta_parts[1]
                    if self.is_left_side_page()
                    else self._meta_parts[0]
                )

                if METALINE_ENTRY_SEPARATOR in words_part:
                    split_words = words_part.split(METALINE_ENTRY_SEPARATOR)
                    formatted_meta_parts = (
                        [number_part, *split_words]
                        if self.is_left_side_page()
                        else [*split_words, number_part]
                    )
                    self._meta_parts = formatted_meta_parts

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
            # If it breaks, its not an entry.
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
                        continue

                    if _line_is_entry(line):
                        entries_for_letter.append(line)
                    else:
                        entries_for_letter[-1] = f"{entries_for_letter[-1]}{line}"

            raw_entries = raw_entries[0:-2] + entries_for_letter

        # Format string entries to structures.
        entries = [
            Entry.from_raw_entry(raw_entry)
            for raw_entry in raw_entries
            # Some lines are either empty, or consists of title letter, or consist of linebreaks.
            # Drop them from entry parsing.
            if len(raw_entry.replace("\n", "")) > 1
        ]

        return entries
