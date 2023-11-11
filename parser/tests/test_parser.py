from src.parser import parser


def test_column_combining() -> None:
    input = [
        "Meta line about the page",
        "Lorem ipsum | Country roads",
        "dolor sit amet | take me home",
        "dolor sit igitur | to the place I belong",
    ]

    expected = [
        "Lorem ipsum",
        "dolor sit amet",
        "dolor sit igitur",
        "Country roads",
        "take me home",
        "to the place I belong",
    ]

    result = parser.parse_column(input)

    assert result == expected
