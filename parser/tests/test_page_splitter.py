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

    expected_f_headwords = ["Fabel", "Fabelhøne", "Fabel", "Fabian", "Fad"]

    assert [entry.headword for entry in f_entries] == expected_f_headwords

    assert (
        f_entries[1].definitions
        == ".no. = fabelhans (om kvinder). Moth. Smlgn. byhøne."
    )


def test_splits_page_of_numbers_in_column_separators() -> None:
    """
    Background: some pages have numbers written in column margin. No idea why.
    This harms OCR, as it reads a number (or something else) instead of column indicator,
    meaning we'll end up splitting columns incorrectly.

    This test case guards one of those cases without caring much how it was/is solved.
    """

    v_to_y = open_test_file("split-x-to-y.txt")

    page_x, page_y = PageSplitter.split_page("3555-ybisk.txt", v_to_y)

    # Page side should be shared between the split siblings.
    assert page_x.is_left_side_page() is True
    assert page_y.is_left_side_page() is True

    # Pages should have separated available letters.
    assert page_x.get_letters_in_page() == ["X"]
    assert page_y.get_letters_in_page() == ["Y"]

    # Pages should have expected amounts of entries.
    x_entries = page_x.get_entries()
    y_entries = page_y.get_entries()
    assert len(x_entries) == 1
    assert len(y_entries) == 8

    assert x_entries[0].status == EntryStatus.PART_OF_PREVIOUS_ENTRY
    assert x_entries[0].headword == "SP"  # Not an actual headword, as stated by status.

    assert x_entries[0].definitions == (
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
        "Yd(e)færdig",
        "Ydefærds",
        "Ydefør",
        "Ydegås",
        "Ydeko",
    ]

    assert [entry.headword for entry in y_entries] == expected_y_headwords


def test_splits_page_with_irregular_meta_line() -> None:
    """
    This page has irregular meta line + words are incorrectly OCR'd together,
    making standard letter detection tricky.
    """

    g_to_h = open_test_file("irregular-meta-split-page.txt")

    page_g, page_h = PageSplitter.split_page("962-gørrel.txt", g_to_h)

    # Page side should be shared between the split siblings.
    assert page_g.is_right_side_page() is True
    assert page_h.is_right_side_page() is True

    # Pages should have separated available letters.
    assert page_g.get_letters_in_page() == ["G"]
    assert page_h.get_letters_in_page() == ["H"]

    # Pages should have expected amounts of entries.
    g_entries = page_g.get_entries()
    h_entries = page_h.get_entries()
    assert len(g_entries) == 9
    assert len(h_entries) == 3

    expected_g_headwords = [
        "Gørrel",
        "Gørle",
        "Gørrelvand",
        "Gørsom",
        "Gørtel",
        "Gøtøle",
        "Gøttersk",
        "Gøttigsk",
        "Gøvling",
    ]

    expected_h_headwords = [
        "Had",
        "Hesiodus,",  # Looks like entry, part of previous.
        "Højsgaard,",  # Looks like entry, part of previous.
    ]

    expected_h_statuses = [
        EntryStatus.VALID,
        EntryStatus.PART_OF_PREVIOUS_ENTRY,
        EntryStatus.PART_OF_PREVIOUS_ENTRY,
    ]

    assert [entry.headword for entry in g_entries] == expected_g_headwords
    assert [entry.headword for entry in h_entries] == expected_h_headwords
    assert [entry.status for entry in h_entries] == expected_h_statuses

    assert g_entries[0].definitions == "no. svælg. Moth. Smlgn.1.surgel."
    assert g_entries[1].definitions == "go. skylle hals. en. Moth."
    assert g_entries[2].definitions == "no. vand Ul at skylle halsen med, Moth"
    assert g_entries[4].definitions == "se u. gjord."
    assert g_entries[-1].definitions == (
        "no. kvist; forgyldte taarne-flag nu kugle-smelted dratter, bruun-blan-glassered steen "
        "fra goflingenedstator (1075). Stolpe, Daxs- pressen i Dmrk. IL 82. Smlen. Molb. Diall: giævling."
    )


def test_splits_page_with_letter_and_entry_expections() -> None:
    """
    Essentially combination of other known cases:
    - Meta line letters cant be parsed
    - Entries starting letters have been misread by ORC. Should be proofread by entry handling.
    """

    o_to_p = open_test_file("split-o-to-p.txt")

    page_o, page_p = PageSplitter.split_page("2172-øxentorv.txt", o_to_p)

    # Page side should be shared between the split siblings.
    assert page_o.is_right_side_page() is True
    assert page_p.is_right_side_page() is True

    # Pages should have separated available letters.
    assert page_o.get_letters_in_page() == ["O"]
    assert page_p.get_letters_in_page() == ["P"]

    # Pages should have expected amounts of entries.
    o_entries = page_o.get_entries()
    p_entries = page_p.get_entries()
    assert len(o_entries) == 6
    assert len(p_entries) == 12

    expected_o_headwords = ["Oxentorv", "Oxen", "Oxel", "Oxle", "Oya", "Oæfle"]

    expected_p_headwords = [
        "Pa",
        "Pabret",
        "Padde",
        "Paddefod",
        "Paddehat",
        "Paddelegplaster",
        "Paddepyt",
        "Paddesten",
        "Padel",
        # TODO: Should have "Padre", but is OCR'd as "Fadre". Hard to detect.
        "Padren",
        # TODO: Should have "Padse". Has period instead of comma in OCR, hard to detect.
        "Pagagi",
        "Page",
    ]

    expected_o_statuses = [
        EntryStatus.VALID,
        EntryStatus.VALID,
        EntryStatus.VALID,
        EntryStatus.VALID,
        EntryStatus.VALID,
        EntryStatus.VALID,
    ]

    expected_p_statuses = [
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

    assert [entry.headword for entry in o_entries] == expected_o_headwords
    assert [entry.headword for entry in p_entries] == expected_p_headwords
    assert [entry.status for entry in o_entries] == expected_o_statuses
    assert [entry.status for entry in p_entries] == expected_p_statuses

    assert o_entries[0].definitions == "no. kvægtorv. Moth."
    assert (
        o_entries[1].definitions == "to. parrelysten, tyregal. Moth. Smlgu. isl. ysna."
    )
    assert o_entries[-1].definitions == (
        "no. overmagt; ther ær icke skam at fly for oæfle, Romant, Digtn. I. 101.n. (Cl. Pedersen. "
        "V. 69.30: offuer mackt). Smlgu. isl. ofrefti; gl. sv. oåtfle, se Såderwall: ofifle."
    )

    assert p_entries[0].definitions == "se på."
    assert p_entries[7].definitions == (
        "no. en art forstening; ComD $ 90 (ovf. II 483 3.23) = | bufonius,» i krotenstein. Navnene "
        "skrive sig fra,at forsteningen mentes at danne sig i padders hoved, jf Rinm: paddsten; Nemn I. 710-11; "
        "tudsesten udf. Over- troisk brug, jf Frisch L551a: kroten- stein."
    )
    assert p_entries[-1].definitions == "se paje."
