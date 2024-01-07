from typing import Final

# Full alphabet.
OLD_DANISH_ALPHABET: Final[str] = "abcdefghijklmnopqrstuvwxyzæøå"

# Abridged alphabet for only comparing letters that may start headwords.
HEADWORDS_ALPHABET: Final[str] = "abdefghijklmnopqrstuvwxyzæøå"


def is_after_in_alphabet(letter1: str, letter2: str) -> bool:
    return OLD_DANISH_ALPHABET.index(letter1.lower()) > OLD_DANISH_ALPHABET.index(
        letter2.lower()
    )


def is_before_in_alphabet(letter1: str, letter2: str) -> bool:
    return not is_after_in_alphabet(letter1, letter2)


def letters_are_sequantial(letter1: str, letter2: str) -> bool:
    try:
        first_index = HEADWORDS_ALPHABET.index(letter1.lower())
        second_index = HEADWORDS_ALPHABET.index(letter2.lower())
    except ValueError:
        raise ValueError(f"No comparison found for letters: {letter1} & {letter2}")

    return abs(first_index - second_index) <= 1
