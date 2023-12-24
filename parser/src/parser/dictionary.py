from typing import NamedTuple

from src.parser.entry import Entry, EntryStatus
from src.parser.page import Page
from src.parser.page_splitter import PageSplitter


class DictionaryPage(NamedTuple):
    name: str
    lines: list[str]


class Dictionary:
    _pages: list[Page]

    def __init__(self, dictionary_pages: list[DictionaryPage]) -> None:
        pages: list[Page] = []

        for dictionary_page in dictionary_pages:
            if PageSplitter.is_split_page(dictionary_page.name):
                page1, page2 = PageSplitter.split_page(
                    filename=dictionary_page.name, lines=dictionary_page.lines
                )
                pages.append(page1)
                pages.append(page2)
            else:
                pages.append(Page(lines=dictionary_page.lines))

        self._pages = pages

    def get_entries(self) -> list[Entry]:
        entries = [entry for page in self._pages for entry in page.get_entries()]

        # Combine partials to entries from previous pages.
        for idx, entry in enumerate(entries):
            if idx > 0:
                if entry.status == EntryStatus.PART_OF_PREVIOUS_ENTRY:
                    entries[idx - 1] = Entry.combine_entries(entries[idx - 1], entry)

        # TODO: GH-47 log or handle for entries that remain invalid.
        filtered_entries = [
            entry for entry in entries if entry.status == EntryStatus.VALID
        ]

        return filtered_entries
