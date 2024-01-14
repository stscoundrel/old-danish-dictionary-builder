import re
from typing import Final

from src.parser.entry import Entry
from src.parser.page_meta import PageMeta

METALINE_ENTRY_SEPARATOR: Final[str] = "—"


class Page:
    _page_number: int | None = None
    _letters_in_page: list[str] | None = None
    _raw_content: list[str]

    def __init__(self, lines: list[str], name: str) -> None:
        # While pages have irregular meta lines, column parsing should've offsetted it already.
        self.meta = lines[0]
        self._raw_content = lines[1:]
        self.name = name
        self.content = self._proofread_lines(lines[1:])

    def _proofread_lines(self, raw_content: list[str]) -> list[str]:
        # For known OCR erors in line, search/replace them here
        # based on mapping of page name => known errors.
        content = raw_content

        if search_replaces := PageMeta.get_known_search_replaces(self.name):
            for search, replace in search_replaces:
                for idx, line in enumerate(content):
                    content[idx] = line.replace(search, replace)

        return content

    def get_separators_for(self, letter: str) -> list[str]:
        return [
            rf"(\b{letter}[\w\S]+\b,)",  # Capital letter and words ends in comma.
            rf"(\b{letter}[\w\S]+\b-)",  # Capital letter and words ends in dash, ie. linebreak.
        ]

    def get_entry_separators(self) -> set[str]:
        return {
            separator
            for letter in self.get_letters_in_page()
            for separator in self.get_separators_for(letter)
        }

    def get_page_number(self) -> int:
        if not self._page_number:
            parts = self.name.split("-")
            self._page_number = int(parts[0])

        return self._page_number

    def is_left_side_page(self) -> bool:
        if self.get_page_number() % 2 == 0:
            return False

        return True

    def is_right_side_page(self) -> bool:
        return not self.is_left_side_page()

    def get_letters_in_page(self) -> list[str]:  # noqa: C901
        """
        Page can generally have 1 or 2 start letters for headwords.
        Most common case: all headwords start with same letter.
        However: it can be split between end of first & start of second letter.
        """
        if not self._letters_in_page:
            self._letters_in_page = PageMeta.get_letters_for_page(self.name)

        return self._letters_in_page

    def set_letters_in_page(self, letters: list[str]) -> None:
        self._letters_in_page = letters

    def get_entries(self) -> list[Entry]:
        def _line_is_entry(line: str) -> bool:
            # Break into words, omitting spacing the beginning.
            parts = line.lstrip().split(" ")

            # Some exotic parts do not respect length, probably linebreakish thing.
            # If it breaks, its not an entry.
            try:
                parts[0][-1]
            except IndexError:
                return False

            # Compare first letter to expected/allowed letters of page.
            if (
                len(parts) == 1
                and not parts[0][0].upper() in self.get_letters_in_page()
            ):
                return False

            # Check if first words ends like entries should.
            return len(parts) == 1 and parts[0][-1] in [",", "-"]

        raw_entries = ["\n".join(self.content)]

        letters = self.get_letters_in_page()

        assert (
            len(letters) == 1
        ), "Should only have one letter per page when parsing entries!"

        for letter in self.get_letters_in_page():
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
                        # Line may contain linebreaks, which are not required at the beginning.
                        line_without_breaks = line.lstrip("\\n")
                        entries_for_letter[
                            -1
                        ] = f"{entries_for_letter[-1]} {line_without_breaks}"

            raw_entries = raw_entries[0:-2] + entries_for_letter

        # Format string entries to structures.
        entries = [
            Entry.from_raw_entry(
                raw_entry=raw_entry,
                allowed_start_letters=self.get_letters_in_page(),
            )
            for raw_entry in raw_entries
            # Some lines are either empty, or consists of title letter, or consist of linebreaks.
            # Drop them from entry parsing.
            if len(raw_entry.replace("\n", "")) > 1
        ]

        return entries
