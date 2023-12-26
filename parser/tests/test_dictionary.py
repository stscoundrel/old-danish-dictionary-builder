from src.parser.dictionary import Dictionary, DictionaryPage
from src.parser.entry import EntryStatus
from tests import open_test_file


def test_combines_entries() -> None:
    v_to_x = DictionaryPage(
        name="3554-vævel.txt", lines=open_test_file("split-v-to-x.txt")
    )
    x_to_y = DictionaryPage(
        name="3555-ybisk.txt", lines=open_test_file("split-x-to-y.txt")
    )
    y_continuation = DictionaryPage(
        name="3556-ydekorn.txt", lines=open_test_file("split-y-continuation.txt")
    )

    dictionary = Dictionary(
        [
            v_to_x,
            x_to_y,
            y_continuation,
        ]
    )

    entries = dictionary.get_entries()

    expected_headwords = [
        "fremede",  # Partial, as previous page is not loaded in test.
        "Vævel",
        "Vævle",
        "Vævleri",
        "Vævling",
        "Vævere",
        "Væverembede",
        "Væverhus",
        "Vævermude",
        "Væverskib",
        "Væverskøjte",
        "Væverskøn",
        "Væverestuve",
        "Væveri",
        "Væve(r)ske",
        "Vævig",
        "Vævned",
        "Vævster",
        "Væxe",
        "Vø",
        "Vøjne",
        "Vørn",
        "Vøv",
        "X",
        # Without combining, we'd have partial "SP" here.
        "Ybisk",
        "Yde",
        "Yde",
        "Yd(e)færdig",
        "Ydefærds",
        "Ydefør",
        "Ydegås",
        "Ydeko",
        # Without combining, we'd have partial "Il" here.
        "Ydekomn",
        "Ydelam",
        "Yde",
        "Yelig",
        "Yding",
        "Ydsk",
        "Ydsom",
        "Yde",
        "Ydre",
        "Ydermere",
        "Yderst",
        "Ydertop",
        "Ytres",
        "Ydig",
        "Ydmyg",
        "Ylde",
        "Yle",
        "Ym",
        "Ymle",
        "Ymme",
        "Ymmel",
        "Ymte",
        "Ymne",
        "Ymnu",
        "Yfilmpe",
    ]

    assert [entry.headword for entry in entries] == expected_headwords

    # Two entries should have been combined with the entry that followed them.
    assert entries[23].headword == "X"
    assert entries[23].status == EntryStatus.VALID
    assert entries[23].definitions == (
        "i forb x for v (u) 0: 10 for 5 (efter talværdien som romertal) i ud- tryk om at bedrage; for L "
        "at skriffve 0, for V at sætte X. Ska 11 (= vår V schriven X. (Lappenbergs udg) 1. v 187); TkA I. "
        '131 (ovf. u. fram); I SP €2" (ovf. IV. 662211); med x for v jeg vilde let mit regenskab forklare. '
        "ABI. 58b; jeg X for V har skrevet og været falsk og treedsk. KS 120; at dskrive x for v, at skære "
        'een en skak- lose 0: veed, hvad een tjener, saa hand derved skakker noget. PSO IL. 27"; — P Pårs '
        "B 3 53 (ovt. II. 4893); at skrive 9 for 1, naar du skrev X' for V: BruunR II. 327 (rim på du). — "
        "(forstå) sin v og x 9: f., hvad der er for-elagtigt; den karl forstaar sin v og x, faar Rygen sogn "
        "for Mors annex. BruuoR II. 288. Jf Hex fort t. skab 217 (ovf. IV. 589b2:). Samme brug i i Sv "
        "(se Dalin: X) og T (se Sanders: W)."
    )

    # Two entries should have been combined with the entry that followed them.
    assert entries[31].headword == "Ydeko"
    assert entries[31].status == EntryStatus.VALID

    assert entries[31].definitions == (
        "no. ko, der gaves som afgift; hwat som the giffuit haffueere en two marck for een ydhe koo (1466). "
        "DC 183; 58 ydhekiør (1523). DM4 II. 4; tilltallit kronens bønder for the icke ville yde hannom "
        "theris yde-koer (1553). Rsv I 210. Jf Bernts Il. 179; skatteko ovf. —"
    )
