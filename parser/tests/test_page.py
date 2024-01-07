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

    # These are all problematically read by OCR & should have special handling.
    irregular_number_words_number = _single_column_test_file(
        file="irregular-meta-number-words-number.txt",
        name="1138-husbrand.txt",
    )
    irregular_three_words = _single_column_test_file(
        file="irregular-meta-three-words.txt",
        name="1233-indermere (inderst).txt",
    )
    irregular_sign_words_number = _single_column_test_file(
        file="irregular-meta-sign-words-number.txt",
        name="1549-kølve.txt",
    )
    irregular_undexpected_dash = _single_column_test_file(
        file="irregular-meta-unexpected-dash.txt",
        name="2523-skinbarlig.txt",
    )
    irregular_undexpected_spacing = _single_column_test_file(
        file="irregular-meta-unexpected-spacing.txt",
        name="2530-skjudebane.txt",
    )

    page1 = Page(lines=one_letter_left_page_input)
    page2 = Page(lines=one_letter_right_page_input)
    page3 = Page(lines=two_letters_right_page_input)
    page4 = Page(lines=one_letter_irregular_meta_input)
    page5 = Page(lines=irregular_number_words_number)
    page6 = Page(lines=irregular_three_words)
    page7 = Page(lines=irregular_sign_words_number)
    page8 = Page(lines=irregular_undexpected_dash)
    page9 = Page(lines=irregular_undexpected_spacing)

    assert page1.get_letters_in_page() == ["A"]
    assert page2.get_letters_in_page() == ["A"]
    assert page3.get_letters_in_page() == ["J", "K"]
    assert page4.get_letters_in_page() == [
        "A"
    ]  # Note: OCR would claim "A & Å", should be detected.
    assert page5.get_letters_in_page() == ["H"]
    assert page6.get_letters_in_page() == ["I"]
    assert page7.get_letters_in_page() == ["K"]
    assert page8.get_letters_in_page() == ["S"]
    assert page9.get_letters_in_page() == ["S"]


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
        "Geh. Ark. Årsb. IL 294."
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


def test_parses_entries_from_first_page() -> None:
    """
    First page in dictionary portrays many irregularities in OCR, which makes detecting
    entries trickier. Includes manual exception for Abeganteri & letter fixing for Abbot.
    """
    irregular_lines_input = _single_column_test_file(
        file="first-page.txt",
        name="0-abbot.txt",
    )

    page = Page(lines=irregular_lines_input)
    entries = page.get_entries()

    expected_headwords = [
        "Abbot",
        "Abbeddømme",
        "Abbatisse",
        "Abe",
        "Abears",
        "Abefugl",
        "Abegabe",
        "Abegant",
        "Abeganteri",
        "Aberøv",
        "Abespil",
        "Abe",
    ]

    expected_statuses = [
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

    assert [entry.headword for entry in entries] == expected_headwords
    assert [entry.status for entry in entries] == expected_statuses


def test_parses_rotated_and_re_ocrd_page() -> None:
    """
    Some page scans/images are so skewed that they need to be run through rotator
    to turn them into pages that can be read automatically. Test one of those cases.
    """
    manipulated_input1 = _single_column_test_file(
        file="simple-page-rotated-for-better-ocr.txt",
        name="97-balstyrig.txt",
    )
    manipulated_input2 = _single_column_test_file(
        file="simple-page-rotated-for-better-ocr2.txt",
        name="1109-hosskrift.txt",
    )

    page1 = Page(lines=manipulated_input1)
    page2 = Page(lines=manipulated_input2)

    assert page1.is_left_side_page() is True
    assert page2.is_left_side_page() is True

    entries1 = page1.get_entries()
    entries2 = page2.get_entries()

    expected_headwords1 = [
        "mellem",
        "Balstyrig",
        "Balstyrighed",
        "Bambe",
        "Bammende",
        "Bamsing",
        "Band",
        "Band",
        "Bandsbrev",
        # TODO: should have "Bandsdag"
        "Bandsfolk",
        "Bandføre",
    ]

    expected_statuses1 = [
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
    ]

    assert [entry.headword for entry in entries1] == expected_headwords1
    assert [entry.status for entry in entries1] == expected_statuses1

    expected_headwords2 = [
        "hoss",
        "Hosskrift",
        "Hosskrive",
        "Hoslåer",
        "Hossætte",
        "Hoste",
        "Hosstændig",
        "Hosvære",
        "Høsværelse",
        "Hourt",
        "Hov",
        "Hov",
        "Hovbar",
        "Hovblad",
        "Hovskræppe",
        "Hovalag",
        # TODO: Should have "Hovslager", but would need more tricky regex to detect it.
        "Hibertz",  # TODO: GH-67, part of previous entry.
        "Hovsmed",
    ]

    expected_statuses2 = [
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
        EntryStatus.VALID,
        EntryStatus.VALID,
        EntryStatus.VALID,
        EntryStatus.VALID,
    ]

    assert [entry.headword for entry in entries2] == expected_headwords2
    assert [entry.status for entry in entries2] == expected_statuses2
