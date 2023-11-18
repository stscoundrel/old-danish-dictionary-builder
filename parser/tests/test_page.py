from src.parser import columns
from src.parser.page import Page
from tests import open_test_file


def _single_column_test_file(file: str) -> list[str]:
    input = open_test_file(file)
    return columns.parse_column(input)


def test_page_side_meta() -> None:
    left_page_input = _single_column_test_file("simple-page.txt")
    right_page_input = _single_column_test_file("simple-page-linebreaks.txt")

    left_page = Page(left_page_input)
    right_page = Page(right_page_input)

    assert left_page.is_left_side_page() is True
    assert right_page.is_right_side_page() is True

    assert left_page.is_right_side_page() is False
    assert right_page.is_left_side_page() is False


def test_page_letters_meta() -> None:
    one_letter_left_page_input = _single_column_test_file("simple-page.txt")
    one_letter_right_page_input = _single_column_test_file("simple-page-linebreaks.txt")
    two_letters_right_page_input = _single_column_test_file(
        "simple-page-linebreaks-two-letters.txt"
    )

    page1 = Page(one_letter_left_page_input)
    page2 = Page(one_letter_right_page_input)
    page3 = Page(two_letters_right_page_input)

    assert page1.get_letters_in_page() == {"A"}
    assert page2.get_letters_in_page() == {"A"}
    assert page3.get_letters_in_page() == {"J", "K"}


def test_parses_simple_entries() -> None:
    """
    Simple entries: one letter in more-or-less straightforward OCR'd page.
    """
    one_letter_left_page_input = _single_column_test_file("simple-page.txt")

    page = Page(one_letter_left_page_input)
    entries = page.get_entries()

    expected_headwords = [
        "Aaf",  # Incorrect! TODO: GH-13
        "Afkomme,",
        "Afkomst,",
        "Afkontrafej,",
        "Afkon-\n\n",  # Incorrect! TODO: GH-15
        "Afkort,",
        "Afkorte,",
        "Afkortelse,",
        "Afkvædet,",
        "Afkynde,",
    ]

    assert [entry.headword for entry in entries] == expected_headwords
