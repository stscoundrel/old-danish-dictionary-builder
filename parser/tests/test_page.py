from src.parser import columns
from src.parser.entry import EntryStatus
from src.parser.page import Page
from tests import open_test_file


def _single_column_test_file(file: str, name: str) -> list[str]:
    input = open_test_file(file)
    return columns.parse_column(input, name)


def test_page_side_meta() -> None:
    left_page_input = _single_column_test_file(
        file="simple-page.txt", name="irrelevant-name"
    )
    right_page_input = _single_column_test_file(
        file="simple-page-linebreaks.txt", name="irrelevant-name"
    )

    left_page = Page(lines=left_page_input)
    right_page = Page(lines=right_page_input)

    assert left_page.is_left_side_page() is True
    assert right_page.is_right_side_page() is True

    assert left_page.is_right_side_page() is False
    assert right_page.is_left_side_page() is False


def test_page_letters_meta() -> None:
    one_letter_left_page_input = _single_column_test_file(
        file="simple-page.txt", name="irrelevant-name"
    )
    one_letter_right_page_input = _single_column_test_file(
        file="simple-page-linebreaks.txt", name="irrelevant-name"
    )
    two_letters_right_page_input = _single_column_test_file(
        "simple-page-linebreaks-two-letters.txt", name="irrelevant-name"
    )
    one_letter_irregular_meta_input = _single_column_test_file(
        file="simple-page-irregular-meta-line.txt",
        name="71-arbejdelse.txt",  # Exception by name!
    )

    page1 = Page(lines=one_letter_left_page_input)
    page2 = Page(lines=one_letter_right_page_input)
    page3 = Page(lines=two_letters_right_page_input)
    page4 = Page(lines=one_letter_irregular_meta_input)

    assert page1.get_letters_in_page() == ["A"]
    assert page2.get_letters_in_page() == ["A"]
    assert page3.get_letters_in_page() == ["J", "K"]
    assert page4.get_letters_in_page() == [
        "A"
    ]  # Note: OCR would claim "A & Å", should be detected.


def test_parses_simple_entries() -> None:
    """
    Simple entries: one letter in more-or-less straightforward OCR'd page.
    """
    one_letter_left_page_input = _single_column_test_file(
        file="simple-page.txt", name="irrelevant-name"
    )

    page = Page(lines=one_letter_left_page_input)
    entries = page.get_entries()

    expected_headwords = [
        "af",  # Partial, part of last page.
        "Afklappe",
        "Afklare",
        "Afkom",
        "Afkomme",
        "Afkomst",
        "Afkontrafej",
        "Aalborg",
        "Afkontrafeje",
        "Afkort",
        "Afkorte",
        "Afkortelse",
        "Afkvædet",
        "Afkynde",
    ]

    expected_statuses = [
        EntryStatus.PART_OF_PREVIOUS_ENTRY,
        EntryStatus.VALID,
        EntryStatus.VALID,
        EntryStatus.VALID,
        EntryStatus.VALID,
        EntryStatus.VALID,
        EntryStatus.VALID,
        EntryStatus.VALID,
        EntryStatus.VALID,
        EntryStatus.VALID,
        EntryStatus.VALID,
        EntryStatus.VALID,
        EntryStatus.VALID,
        EntryStatus.VALID,
    ]

    expected_content = (
        "go. 1) komme (bort) fra; kommer schiff paa grund oc kand ey med mindre affkomme. "
        "N. D. Mag. VI. 104; som ey bygge oc boo paa wort oc kronens goilz oc ey ere aff- "
        "komne met wore mynde (1506). Ro- senv., Gl. L. V. 202; po thet Hans Ure motte thets "
        "bedre affkomme oc guit bliffae trette oc uenighed (1549). Rosenv., Gl. D. I. 71; N. D. Mag. 1. 814. "
        "— 2) komme af; at ther will afikomme eth stort oprør och forderflue (1526). N. D. Mag. V. 215; der met "
        "er det affkommen, mand neppe kiender slecten. Hvitf. VIII 365. — 3) aflægges (t. abkommen.); at the ismaa "
        "markede ere aflagde, oc att ingen haffaer fordelle ther af, at the ere afkommen (1542). D. Mag. IV. 288. — "
        "4) overkomme; at voris depu- terede samme miinstringer, naar de afkomme kand, self skall bjwaane (1890). "
        "Geh. Ark. Årsb. IL 294. —"
    )

    assert [entry.headword for entry in entries] == expected_headwords
    assert [entry.status for entry in entries] == expected_statuses

    assert entries[4].definitions == expected_content


def test_parses_simple_entries_from_irregular_offset_page() -> None:
    """
    Page has irregular meta line, so entries start at irregular index.
    """
    irregular_lines_input = _single_column_test_file(
        file="simple-page-irregular-meta-line.txt",
        name="71-arbejdelse.txt",  # Exception by name!
    )

    page = Page(lines=irregular_lines_input)
    entries = page.get_entries()

    expected_headwords = [
        "dég,",
        "Arbejdelse",
        "Axbørst",
        "Ardag",
        "Ardzmesse",
        "Are",
        "Arel",
        "Areld",
        "Areldsæd",
        "Arene",
        "Arfbidt",
        "Arg",
    ]

    expected_statuses = [
        EntryStatus.PART_OF_PREVIOUS_ENTRY,
        EntryStatus.VALID,
        EntryStatus.VALID,
        EntryStatus.VALID,
        EntryStatus.VALID,
        EntryStatus.VALID,
        EntryStatus.VALID,
        EntryStatus.VALID,
        EntryStatus.VALID,
        EntryStatus.VALID,
        EntryStatus.VALID,
        EntryStatus.VALID,
    ]

    assert [entry.headword for entry in entries] == expected_headwords
    assert [entry.status for entry in entries] == expected_statuses
