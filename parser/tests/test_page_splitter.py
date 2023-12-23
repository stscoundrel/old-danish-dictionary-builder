from src.parser.entry import EntryStatus
from src.parser.page_splitter import PageSplitter
from tests import open_test_file


def test_is_split_page() -> None:
    assert PageSplitter.is_split_page("foo") is False
    assert PageSplitter.is_split_page("bar") is False
    assert PageSplitter.is_split_page("baz") is False

    assert PageSplitter.is_split_page("87-axelkøbstad.txt") is True


def test_splits_page_correctly() -> None:
    a_to_b = open_test_file("split-a-to-b.txt")

    page_a, page_b = PageSplitter.split_page("87-axelkøbstad.txt", a_to_b)

    # Page side should be shared between the split siblings.
    assert page_a.is_left_side_page() is True
    assert page_b.is_left_side_page() is True

    # Pages should have separated available letters.
    assert page_a.get_letters_in_page() == ["A"]
    assert page_b.get_letters_in_page() == ["B"]

    # Pages should have expected amounts of entries.
    a_entries = page_a.get_entries()
    assert len(a_entries) == 10

    expected_a_headwords = [
        "hvilken",  # Partial entry.
        "Axelkøbstad",
        "Axelskav",
        "Axeltorg",
        "Axelseng",
        "Axeltand",
        "Axelvej",
        "Axel",
        "Axelmærke",
        "Axeniere",
    ]

    assert [entry.headword for entry in a_entries] == expected_a_headwords

    # Assert content of the last entry, ensure nothing was cut off.
    assert (
        a_entries[-1].definitions
        == "go. tildele; blev vort sogn axenieret en polsk oberst (1660). D. Saml. Il. 296; vistnok fordrejet for assignere."
    )

    b_entries = page_b.get_entries()
    assert len(page_b.get_entries()) == 3

    expected_b_headwords = [
        "Bable",
        "Babel",  # TODO: GH-29, should be part of previous entry.
        "Babler",
    ]

    assert [entry.headword for entry in b_entries] == expected_b_headwords

    # Assert content of the last first, ensure nothing was cut off.
    assert (
        b_entries[0].definitions == "go. 1) at tale uforståe- ligt. Moth;"
    )  # TODO: GH-29, part of content in next entry.

    # Axeltorg was originally line-splitted headword. Ensure no content was lost in parsing.
    expected_content = (
        "no. lovlig udsalgsplads forpå axel tilførte varer; tbet føre the till tyskeland, som the aff arildtid pleege at "
        "føre till svineborgh, som er theres rette axel torgh (1480). Fynske Aktstk. 90; the haftde sielft ingen axeltoxff "
        "(1941). Geb. Ark. Årsb. TIL till. 33; ingen borger maakiøbe øxen paa landsbyerne, dog bor-geme i kiøbstederne "
        "dermet ikke skal være formeent at købe paa deris axel- tore (1615). Rosenv., G1. L. IV. 816; bønderne skulle "
        'føre deris vare ti] kiøbstæderne og dem paa offentlig axel-torve fal holde. Chr. V. D. L. 38-18-26. "'
    )

    assert a_entries[3].definitions == expected_content


def test_splits_page_of_unknown_first_letter_correctly() -> None:
    """
    Background: page e-to-f has no full entries for E,
    so letter has to be deduced separately.
    """

    e_to_f = open_test_file("split-e-to-f.txt")

    page_e, page_f = PageSplitter.split_page("484-fabel.txt", e_to_f)

    # Page side should be shared between the split siblings.
    assert page_e.is_right_side_page() is True
    assert page_f.is_right_side_page() is True

    # Pages should have separated available letters.
    assert page_e.get_letters_in_page() == ["E"]
    assert page_f.get_letters_in_page() == ["F"]

    # Pages should have expected amounts of entries.
    e_entries = page_e.get_entries()
    f_entries = page_f.get_entries()
    assert len(e_entries) == 1
    assert len(f_entries) == 5

    # The E-page should have incomplete entry.
    assert e_entries[0].status == EntryStatus.PART_OF_PREVIOUS_ENTRY
    assert (
        e_entries[0].headword == "hawe"
    )  # Not an actual headword, as stated by status.

    assert e_entries[0].definitions == (
        "olden swin oc haleff olden-gaffwe aff skoflwen oc gester), som aff andre hans thener oc en skeligh eytte "
        "om areth, sagefaldh oc brøde (1493). D. Mag. IV. 12. Vistnok = ejgt (9: ægt), se d. 0."
    )

    expected_f_headwords = ["Fabel", "Fabelhøne,.no.", "Fabel", "Fabian", "Fad"]

    assert [entry.headword for entry in f_entries] == expected_f_headwords

    assert f_entries[1].definitions == "= fabelhans (om kvinder). Moth. Smlgn. byhøne."


def test_splits_page_of_numbers_in_column_separators() -> None:
    """
    Background: some pages have numbers written in column margin. No idea why.
    This harms OCR, as it reads a number (or something else) instead of column indicator,
    meaning we'll end up splitting columns incorrectly.

    This test case guards one of those cases without caring much how it was/is solved.
    """

    v_to_y = open_test_file("split-v-to-y.txt")

    page_v, page_y = PageSplitter.split_page("3555-ybisk.txt", v_to_y)

    # Page side should be shared between the split siblings.
    assert page_v.is_right_side_page() is True
    assert page_y.is_right_side_page() is True

    # Pages should have separated available letters.
    assert page_v.get_letters_in_page() == ["V"]
    assert page_y.get_letters_in_page() == ["Y"]

    # Pages should have expected amounts of entries.
    v_entries = page_v.get_entries()
    y_entries = page_y.get_entries()
    assert len(v_entries) == 1
    assert len(y_entries) == 7

    assert v_entries[0].status == EntryStatus.PART_OF_PREVIOUS_ENTRY
    assert v_entries[0].headword == "SP"  # Not an actual headword, as stated by status.

    assert v_entries[0].definitions == (
        '€2" (ovf. IV. 662211); med x for v jeg vilde let mit regenskab forklare. ABI. 58b; '
        "jeg X for V har skrevet og været falsk og treedsk. KS 120; at dskrive x for v, at skære "
        'een en skak- lose 0: veed, hvad een tjener, saa hand derved skakker noget. PSO IL. 27"; — '
        "P Pårs B 3 53 (ovt. II. 4893); at skrive 9 for 1, naar du skrev X' for V: BruunR II. 327 "
        "(rim på du). — (forstå) sin v og x 9: f., hvad der er for-elagtigt; den karl forstaar sin v "
        "og x, faar Rygen sogn for Mors annex. BruuoR II. 288. Jf Hex fort t. skab 217 (ovf. IV. "
        "589b2:). Samme brug i i Sv (se Dalin: X) og T (se Sanders: W)."
    )

    expected_y_headwords = [
        "Ybisk",
        "Yde",
        "Yde",
        # TODO: GH-42 missing Yaeyfærdig here.
        "Ydefærds",
        "Ydefør",
        "Ydegås",
        "Ydeko",
    ]

    assert [entry.headword for entry in y_entries] == expected_y_headwords
