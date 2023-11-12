from typing import Final

_divider: Final[str] = "|"


def parse_column(page: list[str]) -> list[str]:
    left_column = []
    right_column = []

    for line in page[1:]:  # First line is meta info.
        divided = line.split(_divider)

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
