from typing import Final

PAGES_TO_IRREGULAR_META_LINE_INDEXES: Final[dict[str, int]] = {
    "71-arbejdelse.txt": 1,
    "430-eftergøre.txt": 1,
    "875-gildeskorn.txt": 1,
    "897-gnistne.txt": 1,
    "1109-hosskrift.txt": 1,  # TODO GH-58: maybe test case?
    "1138-husbrand.txt": 1,  # TODO GH-58: maybe test case?
    "1233-indermere (inderst).txt": 1,  # TODO GH-58: maybe test case?
    "1267-istædelæder.txt": 1,
    "1289-jorsal.txt": 1,
    "1400-knuderig.txt": 2,
    "1461-krejge.txt": 1,
    "1508-kvartaladmiral.txt": 1,
    "1532-kæbel.txt": 2,
    "1549-kølve.txt": 1543,  # TODO GH-58: maybe test case?
    "2514-skibels(e).txt": 1,  # TODO GH-58: maybe test case?
    "2523-skinbarlig.txt": 1,  # TODO GH-58: maybe test case?
    "2530-skjudebane.txt": 2,  # TODO GH-58: maybe test case?
    "2648-snablet.txt": 1,
}


class MetaLine:
    @staticmethod
    def get_meta_line_index(name: str, lines: list[str]) -> int:
        return PAGES_TO_IRREGULAR_META_LINE_INDEXES.get(name, 0)
