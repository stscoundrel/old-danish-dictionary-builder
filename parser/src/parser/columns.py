from typing import Final

from src.parser.page_meta import PageMeta

_vertical_divider: Final[str] = "|"
_exlamation_divider: Final[str] = " ! "
_spaces_divider: Final[str] = "   "


def _get_column_divider(line: str) -> str | None:
    if _vertical_divider in line:
        # Divider was read in OCR, simple case.
        return _vertical_divider

    if _exlamation_divider in line:
        # Occasionally vertical line is read as exlamation mark.
        return _exlamation_divider

    # If divider is missing, it was probably misread.
    # It generally means there will be a
    # grouping of spaces where the divider should be.
    # Four spaces seems common enough case to act as divider.
    if _spaces_divider in line:
        return _spaces_divider

    # No clear divider found, other handling needed.
    return None


def _get_divided_lines(line: str) -> list[str]:
    divider = _get_column_divider(line)

    if divider:
        divided = line.split(divider, 1)

        # If we're dealing with spaces divider, we want to preserve
        # the whitespace after the split. Therefore, append it to
        # all but the first item in split list.
        if divider == _spaces_divider:
            for idx, divided_part in enumerate(divided[1:]):
                divided[idx + 1] = f"{_spaces_divider}{divided_part}"

        return divided

    # No clear divider available. Most likely issue of OCR not reading it correctly.
    # Our best bet: divide it in the middle. Sometimes there are two spaces there,
    # but there are more exotic scenarios too. For now, lets see how far we get with
    # just division down the middle. Based on small sample size it is accurate enough
    # not to break entries, but will cause some typos along the way.
    return [line[: len(line) // 2], line[len(line) // 2 :]]  # noqa: E203


def parse_column(page: list[str], name: str) -> list[str]:
    left_column = []
    right_column = []

    meta_line_index = PageMeta.get_meta_line_index(name=name)
    content_start_index = meta_line_index + 1  # Dont parse meta into columns.

    for line in page[content_start_index:]:
        if len(line) > 20:  # Skip letter headings and oddities.
            divided = _get_divided_lines(line)

            match len(divided):
                case 0:
                    # Empty line
                    continue
                case 1:
                    left_column.append(line)
                case 2:
                    left_column.append(divided[0])
                    right_column.append(divided[1])
                case _:
                    print("Unexpected split!")
                    print(line)

    return [page[meta_line_index]] + left_column + right_column
