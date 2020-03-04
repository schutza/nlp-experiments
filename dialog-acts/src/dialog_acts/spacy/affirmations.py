import spacy
from spacy.matcher import Matcher
from spacy.matcher import PhraseMatcher

from dialog_acts.base_detectors import DialogActDetector


affirmation_outright_pattern = [
    {"LOWER": {"IN": ["yes", "yep", "yessir", "affirmative", "yeah", "yup"]}}
]

affirmation_not_negated_lhs_pattern = [
    {"LOWER": {"IN": ["right", "okay", "ok", "true", "correct"]}}
]

affirmation_not_negated_rhs_pattern = [
    {"LOWER": {"IN": ["absolutely", "certainly", "definitely"]}}
]

affirmation_token_patterns = [
    affirmation_outright_pattern,
    affirmation_not_negated_lhs_pattern,
    affirmation_not_negated_rhs_pattern
]

affirmation_phrases = [
    "I want it",
    "for sure"
]

negated_affirmation_phrases = [
    "absolutely not", "certainly not", "definitely not", 
    "not right", "not ok", "not okay", "not true", "not correct"
]

class SpacyAffirmationDetector(DialogActDetector):

    def __init__(self):
        self._nlp = spacy.load("en_core_web_sm")

        self._phrase_matcher_negative = PhraseMatcher(self._nlp.vocab, attr="LOWER")
        negated_affirmation_phrase_patterns = [self._nlp.make_doc(text) for text in negated_affirmation_phrases]
        self._phrase_matcher_negative.add("NegatedAffirmationPhrases", None, *negated_affirmation_phrase_patterns)

        self._phrase_matcher = PhraseMatcher(self._nlp.vocab, attr="LOWER")
        affirmation_phrase_patterns = [self._nlp.make_doc(text) for text in affirmation_phrases]
        self._phrase_matcher.add("AffirmationPhrases", None, *affirmation_phrase_patterns)

        self._token_matcher = Matcher(self._nlp.vocab)
        self._token_matcher.add("Affirmation", None, *affirmation_token_patterns)

    def detect(self, text, language='en'):
        doc = self._nlp(text)

        negated_phrase_matches = self._phrase_matcher_negative(doc)
        if negated_phrase_matches:
            (match_id, start, end) = negated_phrase_matches[0]
            span = doc[start:end]
            return (False, None, span.text)

        phrase_matches = self._phrase_matcher(doc)
        if phrase_matches:
            (match_id, start, end) = phrase_matches[0]
            span = doc[start:end]
            return (True, None, span.text)

        token_matches = self._token_matcher(doc)
        if token_matches:
            (match_id, start, end) = token_matches[0]
            span = doc[start:end]
            return (True, None, span.text)

        return (False, None)
