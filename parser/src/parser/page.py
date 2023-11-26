class Page:
    _meta_parts: list[str] | None = None

    def __init__(self, lines: list[str]) -> None:
        self.meta = lines[0]
        self.content = lines[1:]

    def _get_meta_parts(self) -> list[str]:
        if self._meta_parts is None:
            # Meta row often contains multitude of extra spaces.
            # Just drop them from actual meta parts when splitting.
            self._meta_parts = [
                splitted for splitted in self.meta.split(" ") if splitted != ""
            ]

        return self._meta_parts

    def get_entry_separators(self) -> set[str]:
        return {f"— {letter}" for letter in self.get_letters_in_page()}

    def is_left_side_page(self) -> bool:
        return self._get_meta_parts()[0].isnumeric()

    def is_right_side_page(self) -> bool:
        return not self.is_left_side_page()

    def get_letters_in_page(self) -> set[str]:
        """
        Page can generally have 1 or 2 start letters for headwords.
        Most common case: all headwords start with same letter.
        However: it can be split between end of first & start of second letter.
        """
        letters = set()
        if self.is_left_side_page():
            letters.add(self._get_meta_parts()[1][0].upper())
            letters.add(self._get_meta_parts()[2][0].upper())

        if self.is_right_side_page():
            letters.add(self._get_meta_parts()[0][0].upper())
            letters.add(self._get_meta_parts()[1][0].upper())

        return letters
