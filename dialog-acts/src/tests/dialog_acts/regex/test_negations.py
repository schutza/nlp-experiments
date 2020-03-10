import pytest

from textability.dialog_acts.regex.negations import RegexNegationDetector

class TestRegexNegationDetector:

    def setup_method(self, test_method):
        self.detector = RegexNegationDetector()


    def teardown_method(self, test_method):
        self.detector = None

    no_phrase_testdata = [
        ("no", True),
        ("nah", True),
        ("nay", True),
        ("never", True),
        ("not what I said", True),
        ("nope", True),
        ("incorrect", True),
        ("nah", True),
        ("not right", True),
        ("not correct", True),
        ("not true", True),
        ("absolutely not", True),
        ("certainly not", True)
    ]

    @pytest.mark.parametrize("input_phrase,expected", no_phrase_testdata)
    def test_is_negate_no_phrases(self, input_phrase, expected):
        actual = self.detector.detect(input_phrase)
        assert actual[0] == expected

    yes_phrase_testdata = [
        ("that's right", False),
        ("okay", False),
        ("ok", False),
        ("yes", False),
        ("for sure", False),
        ("right", False),
        ("correct", False),
        ("absolutely", False),
        ("yep", False),
        ("yeah", False),
        ("certainly", False),
        ("i want it", False),
        ("yup", False),
        ("yessir", False),
        ("affirmative", False),
        ("true", False)
    ]

    @pytest.mark.parametrize("input_phrase,expected", yes_phrase_testdata)
    def test_is_negate_with_yes_phrases(self, input_phrase, expected):
        actual = self.detector.detect(input_phrase)
        assert actual[0] == expected

    nonsense_testdata = [
        ("foo bar", False),
        ("yadda yadda", False)
    ]

    @pytest.mark.parametrize("input_phrase,expected", nonsense_testdata)
    def test_is_negate_nonsense_phrases(self, input_phrase, expected):
        actual = self.detector.detect(input_phrase)
        assert actual[0] == expected
