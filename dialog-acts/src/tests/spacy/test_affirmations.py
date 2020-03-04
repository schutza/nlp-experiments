import pytest

from dialog_acts.spacy.affirmations import SpacyAffirmationDetector

class TestSpacyAffirmationDetector:

    def setup_method(self, test_method):
        self.detector = SpacyAffirmationDetector()

    def teardown_method(self, test_method):
        self.detector = None

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
    def test_is_affirm_with_yes_phrases(self, input_phrase, expected):
        actual = self.detector.detect(input_phrase)
        assert actual[0] == expected

    no_phrase_testdata = [
        ("not right", False),
        ("not correct", False),
        ("not true", False),
        ("absolutely not", False),
        ("certainly not", False)
    ]

    @pytest.mark.parametrize("input_phrase,expected", no_phrase_testdata)
    def test_is_affirm_no_phrases(self, input_phrase, expected):
        actual = self.detector.detect(input_phrase)
        assert actual[0] == expected

    nonsense_testdata = [
        ("foo bar", False),
        ("yadda yadda", False)
    ]

    @pytest.mark.parametrize("input_phrase,expected", no_phrase_testdata)
    def test_is_affirm_nonsense_phrases(self, input_phrase, expected):
        actual = self.detector.detect(input_phrase)
        assert actual[0] == expected
