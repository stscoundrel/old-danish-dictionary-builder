from src.parser.columns import parse_column
from src.parser.page import Page
from src.parser.page_meta import PageMeta


class PageSplitter:
    @staticmethod
    def is_split_page(filename: str) -> bool:
        return filename in PageMeta.get_pages_splits()

    @classmethod
    def split_page(cls, filename: str, lines: list[str]) -> tuple[Page, Page]:
        if not cls.is_split_page(filename):
            raise ValueError("Provided page that should not be split")

        split_point = PageMeta.get_pages_splits()[filename]

        # Split by the split point, but append meta line to the second part too.
        combined_column_1_lines = parse_column(page=lines[0:split_point], name=filename)
        combined_column_2_lines = parse_column(
            page=[lines[0]] + lines[split_point:], name=filename
        )
        page1, page2 = (
            Page(lines=combined_column_1_lines, name=filename),
            Page(lines=combined_column_2_lines, name=filename),
        )

        # We expect pages to have two letters maximum.
        letters = page1.get_letters_in_page()

        assert len(letters) == 2, f"Missing letters for {filename}"

        # Inject letters to correct pages, indicating both are not available in both.
        page1.set_letters_in_page([letters[0]])
        page2.set_letters_in_page([letters[1]])

        return page1, page2
