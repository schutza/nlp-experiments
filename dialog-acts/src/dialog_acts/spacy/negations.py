import spacy
from spacy.matcher import Matcher
from spacy.matcher import PhraseMatcher

from dialog_acts.base_detectors import DialogActDetector


negation_outright_pattern = [
    {"LOWER": {"IN": ["no", "nah", "nay", "ney", "nope", "never", "incorrect"]}}
]

negation_then_affirmation_pattern = [
    {"DEP": {"IN": ["neg", "advmod"]}},
    {"LOWER": {"IN": ["right", "correct", "true"]}}
]

affirmation_then_negation_pattern = [
    {"LOWER": {"IN": ["absolutely", "certainly", "definitely"]}},
    {"LOWER": "not"}
]

patterns = [
    negation_outright_pattern,
    negation_then_affirmation_pattern,
    affirmation_then_negation_pattern
]

negation_phrases = [
    "not what I said"
]

class SpacyNegationDetector(DialogActDetector):

    def __init__(self):
        self._nlp = spacy.load("en_core_web_sm")

        self._phrase_matcher = PhraseMatcher(self._nlp.vocab, attr="LOWER")
        negation_phrase_patterns = [self._nlp.make_doc(text) for text in negation_phrases]
        self._phrase_matcher.add("AffirmationPhrases", None, *negation_phrase_patterns)

        self._matcher = Matcher(self._nlp.vocab)
        self._matcher.add("Negation", None, *patterns)

    def detect(self, text, language='en'):
        doc = self._nlp(text)

        phrase_matches = self._phrase_matcher(doc)
        if phrase_matches:
            (match_id, start, end) = phrase_matches[0]
            span = doc[start:end]
            return (True, None, span.text)

        matches = self._matcher(doc)
        if matches:
            (match_id, start, end) = matches[0]
            span = doc[start:end]
            return (True, None, span.text)

        return (False, None)
