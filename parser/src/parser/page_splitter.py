from typing import Final

from src.parser.columns import parse_column
from src.parser.page import Page

# Pages that contain more than one letter should be handled as two pages.
# Filenames of pages to be split & line index where split should happen.
LETTER_SPLIT_MAPPING: Final[dict[str, int]] = {
    "87-axelkøbstad.txt": 50,
    "329-bøs.txt": 47,
    "484-fabel.txt": 4,
    "962-gørrel.txt": 37,
    "1200-høved(s)mand.txt": 24,
    "1269-ivæve.txt": 12,
    "1300-jødetempel.txt": 30,
    "1552-køterkro.txt": 7,
    "1912-mørsk.txt": 21,
    "2005-nøvelige.txt": 23,
    "2172-øxentorv.txt": 18,
    "2639-røtte (rotte).txt": 38,
    "3173-søstergård.txt": 26,
    "3408-tøve.txt": 16,
    "3806-vævel.txt": 49,
    "3807-ybisk.txt": 12,
    "3839-æven[æm]tyrlig.txt": 25,  # TODO: GH-37
    "3887-årtrålig.txt": 37,
    "3912-æven[æm]tyrlig.txt": 25,  # TODO: GH-37
}


class PageSplitter:
    @staticmethod
    def is_split_page(filename: str) -> bool:
        return filename in LETTER_SPLIT_MAPPING

    @classmethod
    def split_page(cls, filename: str, lines: list[str]) -> tuple[Page, Page]:
        if not cls.is_split_page(filename):
            raise ValueError("Provided page that should not be split")

        split_point = LETTER_SPLIT_MAPPING[filename]

        # Split by the split point, but append meta line to the second part too.
        combined_column_1_lines = parse_column(lines[0:split_point])
        combined_column_2_lines = parse_column([lines[0]] + lines[split_point:])
        page1, page2 = (Page(combined_column_1_lines), Page(combined_column_2_lines))

        # We expect pages to have two letters maximum.
        letters = page1.get_letters_in_page()
        assert len(letters) <= 2

        # Should there only be one letter, the metaline is incorrect. For example, page E - F.
        # In that case, it is safe enough to expect that the first is incorrect & should be the
        # previous letter of the alphabet. May later need custom mapping if more complex cases appear.
        if len(letters) == 1:
            letters = [cls._get_previous_letter_of_dictionary(letters[0]), letters[0]]

        assert len(letters) == 2

        # Inject letters to correct pages, indicating both are not available in both.
        page1.set_letters_in_page([letters[0]])
        page2.set_letters_in_page([letters[1]])

        return page1, page2

    @staticmethod
    def _get_previous_letter_of_dictionary(letter: str) -> str:
        # TODO: actual logic if needed. Currently only covers
        # special-case-by-special-case.
        if letter == "F":
            return "E"

        raise NotImplementedError(f"No handling for letter {letter}!")
