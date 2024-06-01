from typing import Final

PAGES_TO_IRREGULAR_META_LINE_INDEXES: Final[dict[str, int]] = {
    "71-arbejdelse.txt": 1,
    "97-balstyrig.txt": 1,
    "430-eftergøre.txt": 1,
    "875-gildeskorn.txt": 1,
    "897-gnistne.txt": 1,
    "1109-hosskrift.txt": 1,
    "1138-husbrand.txt": 1,
    "1233-indermere (inderst).txt": 2,
    "1267-istædelæder.txt": 1,
    "1289-jorsal.txt": 1,
    "1400-knuderig.txt": 2,
    "1461-krejge.txt": 1,
    "1508-kvartaladmiral.txt": 1,
    "1532-kæbel.txt": 2,
    "1549-kølve.txt": 2,
    "2514-skibels(e).txt": 1,
    "2523-skinbarlig.txt": 1,
    "2530-skjudebane.txt": 2,
    "2648-snablet.txt": 1,
}

# Pages that contain more than one letter should be handled as two pages.
# Filenames of pages to be split & line index where split should happen.
LETTER_SPLIT_MAPPING: Final[dict[str, int]] = {
    "87-axelkøbstad.txt": 50,
    "329-bøs.txt": 47,
    "484-fabel.txt": 4,
    "962-gørrel.txt": 37,
    "1200-høved(s)mand.txt": 24,
    "1269-ivæve.txt": 12,
    "1300-jødetempel.txt": 30,
    "1552-køterkro.txt": 7,
    "1912-mørsk.txt": 21,
    "2005-nøvelige.txt": 23,
    "2172-øxentorv.txt": 18,
    "2387-røtte (rotte).txt": 37,
    "2921-søstergård.txt": 26,
    "3156-tøve.txt": 16,
    "3554-vævel.txt": 49,
    "3555-ybisk.txt": 12,
    "3587-æven[æm]tyrlig.txt": 25,
    "3635-årtrålig.txt": 37,
}

PAGES_WITH_EXCEPTIONAL_LETTERS: Final[dict[str, list[str]]] = {
    "87-axelkøbstad.txt": ["A", "B"],
    "329-bøs.txt": ["B", "D"],
    "484-fabel.txt": ["E", "F"],
    "569-(flyning).txt": ["F"],
    "785-(Vor) Frueaften.txt": ["F"],
    "962-gørrel.txt": ["G", "H"],
    "1200-høved(s)mand.txt": ["H", "I"],
    "1269-ivæve.txt": ["I", "J"],
    "1300-jødetempel.txt": ["J", "K"],
    # Gods have mercy on that filename
    """1435-(Hellig)
Korsaften.txt""": [
        "H"
    ],
    "1552-køterkro.txt": ["K", "L"],
    "1912-mørsk.txt": ["M", "N"],
    "2005-nøvelige.txt": ["N", "O"],
    "2172-øxentorv.txt": ["O", "P"],
    "2387-røtte (rotte).txt": ["R", "S"],
    "2921-søstergård.txt": ["S", "T"],
    "3156-tøve.txt": ["T", "U"],
    "3554-vævel.txt": ["V", "X"],
    "3555-ybisk.txt": ["X", "Y"],
    "3587-æven[æm]tyrlig.txt": ["Æ", "Ø"],
    "3635-årtrålig.txt": ["Å", "Æ"],
}

KNOWN_OCR_ERROR_SEARCH_REPLACES: Final[dict[str, list[tuple[str, str]]]] = {
    "1-abelig.txt": [("Ablat se oblat.", "Ablat, se oblat.")],
    "97-balstyrig.txt": [("Bandsdoc.", "Bandsdag,")],
    "1109-hosskrift.txt": [("Hovslager", "Hovslager,")],
    "1781-midaldret.txt": [("Moth.—Middagskost,", "Moth. —Middagskost,")],
    "1820-mildelse.txt": [("Moth.—Mildre", "Moth. —Mildre")],
    "2387-røtte (rotte).txt": [
        ("Bøttelort", "Røttelort"),
        ("Røtteskår", "Røtteskar,"),
        ("Bøve", "Røve"),
    ],
    "2172-øxentorv.txt": [("Fadre", "Padre"), ("Padse.", "Padse,")],
}


class PageMeta:
    @staticmethod
    def get_meta_line_index(name: str) -> int:
        return PAGES_TO_IRREGULAR_META_LINE_INDEXES.get(name, 0)

    @staticmethod
    def get_letters_for_page(name: str) -> list[str]:
        if name not in PAGES_WITH_EXCEPTIONAL_LETTERS:
            parts = name.split("-")
            return [parts[1][0].upper()]
        else:
            return PAGES_WITH_EXCEPTIONAL_LETTERS[name]

    @staticmethod
    def get_pages_splits() -> dict[str, int]:
        return LETTER_SPLIT_MAPPING

    @staticmethod
    def get_known_search_replaces(page: str) -> list[tuple[str, str]]:
        return KNOWN_OCR_ERROR_SEARCH_REPLACES.get(page, [])
