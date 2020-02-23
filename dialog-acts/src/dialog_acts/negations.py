import re

from dialog_acts.lexicon.language_resources import (
    YES_WORDS_NEGATABLE_LHS, YES_WORDS_NEGATABLE_RHS,
    NO_WORDS_NON_NEGATABLE)
from dialog_acts.util import find_negation_word

def _find_non_negatable_no_word(text):
    match = re.search(NO_WORDS_NON_NEGATABLE, text)
    if match:
        return (True, match.group(0))
    return (False, None)

def _negation_on_lhs(text, negation_word=None):
    match = re.search(YES_WORDS_NEGATABLE_LHS, text)
    if match:
        if match.group(0):
            return (True, match.group(0))    
    return (False, None)

def _negation_on_rhs(text, negation_word=None):
    match = re.search(YES_WORDS_NEGATABLE_RHS, text)
    if match:
        if match.group(0):
            return (True, match.group(0)) 
    return (False, None)

def _find_negatable_yes_word(text, negation_word=None):
    idx = text.find(negation_word)
    # check for no word on left-hand side 
    right_from_no = text[idx:]
    maybe_lhs_no_word = _negation_on_lhs(right_from_no, negation_word=negation_word)
    if maybe_lhs_no_word[0]:
        return (True, f'{negation_word} {maybe_lhs_no_word[1]}')
    # check for no word on right-hand side 
    left_from_no = text[:idx]
    maybe_rhs_no_word = _negation_on_rhs(left_from_no, negation_word=negation_word)
    if maybe_rhs_no_word[0]:
        return (True, f'{maybe_rhs_no_word[1]} {negation_word}')
    return (False, None)

def is_negate(text):
    """
    A negation/rejection is either a
        1) dedicated, non-negatable no-word ('no', 'nope')
        2) negated yes-word with negation in pre position ('not right')
        3) negated yes-word with negation in post position ('absolutely not')
    Strategy:
        1) attempt to match a non-negatable no-word
        Failing that,
        2) attempt to match a negation ('not'), 
        and if successful, attempt to match negatable yes-word that licenses negation
        2.1) in pre position, 
        or in 
        2.2) in post position
    """
    sure_no = _find_non_negatable_no_word(text)
    if sure_no[0]:
        return sure_no

    negation_word = find_negation_word(text)
    if negation_word[0]:
        maybe_no = _find_negatable_yes_word(text, negation_word=negation_word[1])
        if maybe_no[0]:
            return (True, negation_word[1], maybe_no[1])
    return (False, None, None)
