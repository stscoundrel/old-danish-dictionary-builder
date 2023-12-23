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
        "no. lovlig udsalgsplads forpå axel tilførte varer; tbet føre the till tyskeland, som the aff arildz magnificus "
        "et magnus. $. R. D. Il.tid pleege at føre till svineborgh, som er theres rette axel torgh (1480). Fynske Aktstk. "
        "90; the haftde sielft ingen axeltoxff (1941). Geb. Ark. Årsb. TIL till. 33; ingen borger maakiøbe øxen paa "
        "landsbyerne, dog bor-geme i kiøbstederne dermet ikke skal være formeent at købe paa deris axel- tore (1615). "
        "Rosenv., G1. L. IV. 816; bønderne skulle føre deris vare ti] kiøbstæderne og dem paa offentlig axel-torve "
        'fal holde. Chr. V. D. L. 38-18-26. "'
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
