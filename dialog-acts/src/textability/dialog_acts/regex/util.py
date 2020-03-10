import re

from textability.dialog_acts.regex.lexicon.language_resources import NEGATION_WORDS

def find_negation_word(text):
    match = re.search(NEGATION_WORDS, text)
    if match:
        return (True, match.group(0))
    return (False, None)
