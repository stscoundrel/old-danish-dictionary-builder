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
    "2387-røtte (rotte).txt": 38,
    "2921-søstergård.txt": 26,
    "3156-tøve.txt": 16,
    "3554-vævel.txt": 49,
    "3555-ybisk.txt": 12,
    "3587-æven[æm]tyrlig.txt": 25,
    "3635-årtrålig.txt": 37,
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
        combined_column_1_lines = parse_column(page=lines[0:split_point], name=filename)
        combined_column_2_lines = parse_column(
            page=[lines[0]] + lines[split_point:], name=filename
        )
        page1, page2 = (
            Page(lines=combined_column_1_lines),
            Page(lines=combined_column_2_lines),
        )

        # We expect pages to have two letters maximum.
        letters = page1.get_letters_in_page()
        assert len(letters) <= 2

        # Should there only be one letter, the metaline is incorrect.
        # It is irregular enough, so lets just fetch correct ones via mapping.
        if len(letters) == 1:
            letters = cls._get_letters_for_filename(filename)

        assert len(letters) == 2, f"Missing letters for {filename}"

        # Inject letters to correct pages, indicating both are not available in both.
        page1.set_letters_in_page([letters[0]])
        page2.set_letters_in_page([letters[1]])

        return page1, page2

    @staticmethod
    def _get_letters_for_filename(filename: str) -> list[str]:
        match filename:
            case "484-fabel.txt":
                return ["E", "F"]
            case "1552-køterkro.txt":
                return ["K", "L"]
            case "2172-øxentorv.txt":
                return ["O", "P"]
            case "2387-røtte (rotte).txt":
                return ["R", "S"]
            case "3554-vævel.txt":
                return ["V", "X"]
            case "3555-ybisk.txt":
                return ["V", "Y"]
            case _:
                raise NotImplementedError(f"No letters handling for {filename}!")
