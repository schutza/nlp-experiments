import pytest

from dialog_acts.affirmations import is_affirm

yes_phrase_testdata = [
    ("that's right", True),
    ("okay", True),
    ("ok", True),
    ("yes", True),
    ("for sure", True),
    ("right", True),
    ("correct", True),
    ("absolutely", True),
    ("yep", True),
    ("yeah", True),
    ("certainly", True),
    ("i want it", True),
    ("yup", True),
    ("yessir", True),
    ("affirmative", True),
    ("true", True)
]

@pytest.mark.parametrize("input_phrase,expected", yes_phrase_testdata)
def test_is_affirm_with_yes_phrases(input_phrase, expected):
    actual = is_affirm(input_phrase)
    assert actual[0] == expected

no_phrase_testdata = [
    ("not right", False),
    ("not correct", False),
    ("not true", False),
    ("absolutely not", False),
    ("certainly not", False)
]

@pytest.mark.parametrize("input_phrase,expected", no_phrase_testdata)
def test_is_affirm_no_phrases(input_phrase, expected):
    actual = is_affirm(input_phrase)
    assert actual[0] == expected

nonsense_testdata = [
    ("foo bar", False),
    ("yadda yadda", False)
]

@pytest.mark.parametrize("input_phrase,expected", no_phrase_testdata)
def test_is_affirm_nonsense_phrases(input_phrase, expected):
    actual = is_affirm(input_phrase)
    assert actual[0] == expected
