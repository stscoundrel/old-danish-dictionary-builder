from src.parser.entry import Entry, EntryStatus


def test_parses_single_definition_as_list() -> None:
    entry = Entry(headword="Foo", definitions="Foo bar baz", status=EntryStatus.VALID)

    expected_definitions = ["Foo bar baz"]

    assert entry.definitions_list == expected_definitions


def test_parses_single_numbered_definition_as_list() -> None:
    entry = Entry(
        headword="Bable",
        definitions="go. 1) at tale uforståe- ligt. Moth;",
        status=EntryStatus.VALID,
    )

    expected_definitions = ["go.", "1) at tale uforståe- ligt. Moth;"]

    assert entry.definitions_list == expected_definitions


def test_parses_multiple_definitions_as_list() -> None:
    entry = Entry(
        headword="Afkom",
        definitions=(
            "go. 1) komme (bort) fra; kommer schiff paa grund oc kand ey med mindre affkomme. "
            "N. D. Mag. VI. 104; som ey bygge oc boo paa wort oc kronens goilz oc ey ere aff- "
            "komne met wore mynde (1506). Ro- senv., Gl. L. V. 202; po thet Hans Ure motte thets "
            "bedre affkomme oc guit bliffae trette oc uenighed (1549). Rosenv., Gl. D. I. 71; N. D. Mag. 1. 814. "
            "— 2) komme af; at ther will afikomme eth stort oprør och forderflue (1526). N. D. Mag. V. 215; der met "
            "er det affkommen, mand neppe kiender slecten. Hvitf. VIII 365. — 3) aflægges (t. abkommen.); at the ismaa "
            "markede ere aflagde, oc att ingen haffaer fordelle ther af, at the ere afkommen (1542). D. Mag. IV. 288. — "
            "4) overkomme; at voris depu- terede samme miinstringer, naar de afkomme kand, self skall bjwaane (1890). "
            "Geh. Ark. Årsb. IL 294."
        ),
        status=EntryStatus.VALID,
    )

    expected_definitions = [
        "go.",
        "1) komme (bort) fra; kommer schiff paa grund oc kand ey med mindre affkomme. N. D. Mag. VI. 104; som ey bygge oc boo paa wort oc kronens goilz oc ey ere aff- komne met wore mynde (1506). Ro- senv., Gl. L. V. 202; po thet Hans Ure motte thets bedre affkomme oc guit bliffae trette oc uenighed (1549). Rosenv., Gl. D. I. 71; N. D. Mag. 1. 814. —",  # noqa: E501
        "2) komme af; at ther will afikomme eth stort oprør och forderflue (1526). N. D. Mag. V. 215; der met er det affkommen, mand neppe kiender slecten. Hvitf. VIII 365. —",  # noqa: E501
        "3) aflægges (t. abkommen.); at the ismaa markede ere aflagde, oc att ingen haffaer fordelle ther af, at the ere afkommen (1542). D. Mag. IV. 288. —",  # noqa: E501
        "4) overkomme; at voris depu- terede samme miinstringer, naar de afkomme kand, self skall bjwaane (1890). Geh. Ark. Årsb. IL 294.",  # noqa: E501
    ]

    assert entry.definitions_list == expected_definitions


def test_parses_incorrectly_numbered_definitions_list() -> None:
    entry = Entry(
        headword="Foo",
        definitions="Foo bar baz 1) bar bar 3) baz baz 2) foo foo ",
        status=EntryStatus.VALID,
    )

    # Should not split if numbering does not make sense.
    expected_definitions = ["Foo bar baz 1) bar bar 3) baz baz 2) foo foo "]

    assert entry.definitions_list == expected_definitions
