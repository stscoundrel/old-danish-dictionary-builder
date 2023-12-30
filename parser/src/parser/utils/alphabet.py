from typing import Final

# Full alphabet.
OLD_DANISH_ALPHABET: Final[str] = "abcdefghijklmnopqrstuvwxyzæøå"

# Abridged alphabet for only comparing letters that may start headwords.
HEADWORDS_ALPHABET: Final[str] = "abdefghijklmnoprstuvxyzæøå"


def is_after_in_alphabet(letter1: str, letter2: str) -> bool:
    return OLD_DANISH_ALPHABET.index(letter1.lower()) > OLD_DANISH_ALPHABET.index(
        letter2.lower()
    )


def is_before_in_alphabet(letter1: str, letter2: str) -> bool:
    return not is_after_in_alphabet(letter1, letter2)


def letters_are_sequantial(letter1: str, letter2: str) -> bool:
    first_index = HEADWORDS_ALPHABET.index(letter1.lower())
    second_index = HEADWORDS_ALPHABET.index(letter2.lower())

    return abs(first_index - second_index) <= 1
