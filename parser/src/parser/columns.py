from typing import Final

_divider: Final[str] = "|"
_spaces_divider: Final[str] = "    "


def _get_column_divider(line: str) -> str:
    if _divider in line:
        # Divider was read in OCR, simple case.
        return _divider

    # If divider is missing, it was probably misread.
    # If divider is missing, it generally means there will be a
    # grouping of spaces where the divider should be.
    # Four spaces seems common enough case to act as divider.
    return _spaces_divider


def _get_divided_lines(line: str) -> list[str]:
    divider = _get_column_divider(line)
    divided = line.split(divider)

    # If we're dealing with spaces divider, we want to preserve
    # the whitespace after the split. Therefore, append it to
    # all but the first item in split list.
    if divider == _spaces_divider:
        print("APPENDING SPACES")
        for idx, divided_part in enumerate(divided[1:]):
            divided[idx + 1] = f"{_spaces_divider}{divided_part}"

    return divided


def parse_column(page: list[str]) -> list[str]:
    left_column = []
    right_column = []

    for line in page[1:]:  # First line is meta info.
        divided = _get_divided_lines(line)

        match len(divided):
            case 1:
                left_column.append(line)
            case 2:
                left_column.append(divided[0])
                right_column.append(divided[1])
            case _:
                print("Unexpected split!")
                print(line)

    return [page[0]] + left_column + right_column


def parse_columns(pages: list[list[str]]) -> list[list[str]]:
    single_column_pages = []

    for page in pages:
        single_column_pages.append(parse_column(page))

    return single_column_pages
