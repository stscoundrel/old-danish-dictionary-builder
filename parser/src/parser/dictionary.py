from typing import NamedTuple

from src.parser import columns
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
                pages.append(
                    Page(
                        lines=columns.parse_column(
                            dictionary_page.lines, name=dictionary_page.name
                        ),
                        name=dictionary_page.name,
                    )
                )

        self._pages = pages

    def get_entries(self) -> list[Entry]:
        entries = [entry for page in self._pages for entry in page.get_entries()]

        # Combine partials to entries from previous pages.
        for idx, entry in enumerate(entries):
            if idx > 0:
                if entry.status == EntryStatus.PART_OF_PREVIOUS_ENTRY:
                    # Replace previous entry with combined entry, mark current entry for deletion.
                    # Individual entries are immutable, so we're replacing them with new instances.
                    entries[idx - 1] = Entry.combine_entries(entries[idx - 1], entry)
                    entries[idx] = Entry.mark_for_deletion(entry)

        filtered_entries = [
            entry for entry in entries if entry.status != EntryStatus.DELETED
        ]

        for entry in filtered_entries:
            if entry.status != EntryStatus.VALID:
                print("Unexpected entry!")
                print(entry.headword)
                print(entry.definitions)
                print(entry.status)

        return filtered_entries
