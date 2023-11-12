from src.parser import columns


def test_column_combining() -> None:
    input = [
        "Meta line about the page",
        "Lorem ipsum | Country roads",
        "dolor sit amet | take me home",
        "dolor sit igitur | to the place I belong",
    ]

    expected = [
        "Meta line about the page",
        "Lorem ipsum ",
        "dolor sit amet ",
        "dolor sit igitur ",
        " Country roads",
        " take me home",
        " to the place I belong",
    ]

    result = columns.parse_column(input)

    assert result == expected
