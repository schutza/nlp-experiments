import re

from dialog_acts.lexicon.language_resources import (
    YES_WORDS_NON_NEGATABLE, YES_WORDS_NEGATABLE_LHS, YES_WORDS_NEGATABLE_RHS)
from dialog_acts.util import find_negation_word

def _find_non_negatable_yes_word(text):
    match = re.search(YES_WORDS_NON_NEGATABLE, text)
    if match:
        return (True, match.group(0))
    return (False, None)



def _find_negatable_yes_word(text, negation_word=None):
    lhs_license = re.search(YES_WORDS_NEGATABLE_LHS, text)
    if lhs_license:
        if negation_word:
            # check whether it is in licensed position
            idx = text.find(lhs_license.group(0))
            lhs = text[:idx]
            if re.search(negation_word ,lhs):
                return (False, None)
        else:
            return (True, lhs_license.group(0))
    rhs_license = re.search(YES_WORDS_NEGATABLE_RHS, text)
    if rhs_license:
        if negation_word:
            # check whether it is in licensed position
            idx = text.find(rhs_license.group(0))
            rhs = text[idx:]
            if re.search(negation_word ,rhs):
                return (False, None)
        else:
            return (True, rhs_license.group(0))
    return (False, None)

def is_affirm(text):
    """
    An affirmation is either a
        1) dedicated, non-negatable yes-word ('yes', 'yeah', 'yep')
        2) non-negated yes-word 
        2.1) licensed negation not occurring on left-hand side: 'not right'
        2.2) licensed negation not occurring on right-hand side ('absolutely not')
    Strategy:
        1) attempt to match a non-negatable yes-word
        Failing that,
        2) attempt to match negatable yes-word ('correct', 'right'), 
        and if successful, attempt to confirm no negation occurring on licensed side
        2.1) no negation on left-hand side, 
        or in 
        2.2) no negation on right-hand side
    """
    sure_yes = _find_non_negatable_yes_word(text)
    if sure_yes[0]:
        return (sure_yes[0], None, sure_yes[1])

    maybe_negation_word = find_negation_word(text)
    if maybe_negation_word:
        maybe_yes = _find_negatable_yes_word(text, negation_word=maybe_negation_word[1])
    else:
        maybe_yes = _find_negatable_yes_word(text, negation_word=None)

    if maybe_yes[0]:
        return (True, maybe_negation_word[1] if maybe_negation_word[0] else None, maybe_yes[1])
    return (False, None, None)
