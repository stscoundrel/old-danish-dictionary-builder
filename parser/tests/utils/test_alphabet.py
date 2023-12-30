from src.parser.utils.alphabet import (
    is_after_in_alphabet,
    is_before_in_alphabet,
    letters_are_sequantial,
)


def test_alphabet_letter_order() -> None:
    assert is_after_in_alphabet("B", "A") is True
    assert is_after_in_alphabet("Q", "K") is True
    assert is_after_in_alphabet("A", "Å") is False
    assert is_after_in_alphabet("A", "B") is False

    assert is_before_in_alphabet("B", "A") is False
    assert is_before_in_alphabet("Q", "K") is False
    assert is_before_in_alphabet("A", "Å") is True
    assert is_before_in_alphabet("A", "B") is True


def test_letters_are_sequential() -> None:
    assert letters_are_sequantial("A", "A") is True
    assert letters_are_sequantial("A", "B") is True
    assert letters_are_sequantial("B", "A") is True

    assert letters_are_sequantial("A", "D") is False
    assert letters_are_sequantial("A", "Å") is False
