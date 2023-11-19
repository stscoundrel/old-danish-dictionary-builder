from src.parser import columns


def test_column_combining() -> None:
    input = [
        "Meta line about the page",
        "Lorem ipsum | Country roads",
        "dolor sit amet | take me home",
        "dolor sit igitur | to the place I belong",
        # Missing divider, to be recognized with group of spaces.
        "werden. Tavsen. 67; smlgn. Sch. u.     Ablat se oblat.",
    ]

    expected = [
        "Meta line about the page",
        "Lorem ipsum ",
        "dolor sit amet ",
        "dolor sit igitur ",
        "werden. Tavsen. 67; smlgn. Sch. u.",
        " Country roads",
        " take me home",
        " to the place I belong",
        "     Ablat se oblat.",
    ]

    result = columns.parse_column(input)

    assert result == expected
