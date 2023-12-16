from typing import Final

from src.parser.columns import parse_column
from src.parser.page import Page

# Filenames of pages to be split & line index where split should happen.
LETTER_SPLIT_MAPPING: Final[dict[str, int]] = {
    "87-axelkøbstad.txt": 50,
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
        combined_column_2_lines = parse_column(
            [lines[0]] + lines[split_point + 1 :]  # noqa: E203
        )

        page1, page2 = (Page(combined_column_1_lines), Page(combined_column_2_lines))

        # We expect pages to have two letters maximum.
        letters = page1.get_letters_in_page()
        assert len(letters) == 2

        # Inject letters to correct pages, indicating both are not available in both.
        page1.set_letters_in_page([letters[0]])
        page2.set_letters_in_page([letters[1]])

        return page1, page2
