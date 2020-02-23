import re

from language_resources import YES_WORD_NON_NEGATABLE, YES_WORD_NEGATABLE_LHS, YES_WORD_NEGATABLE_RHS, \
    NO_WORD_NON_NEGATABLE, NEGATION_WORD

def match_non_negatable_yes_word(text):
    match = re.search(YES_WORD_NON_NEGATABLE, text)
    if match:
        return (True, match.group(0))
    return (False, None)

def match_non_negatable_no_word(text):
    match = re.search(NO_WORD_NON_NEGATABLE, text)
    if match:
        return (True, match.group(0))
    return (False, None)

def match_negatable_yes_word_affirmation(text, negation_word=None):
    rhs_license = re.search(YES_WORD_NEGATABLE_RHS, text)
    if rhs_license:
        if negation_word:
            # check whether it is in licensed position
            idx = text.find(rhs_license.group(0))
            rhs = text[idx:]
            if re.search(negation_word ,rhs):
                return (False, None)
        else:
            return (True, rhs_license.group(0))
    lhs_license = re.search(YES_WORD_NEGATABLE_LHS, text)
    if lhs_license:
        if negation_word:
            # check whether it is in licensed position
            idx = text.find(lhs_license.group(0))
            lhs = text[:idx]
            if re.search(negation_word ,lhs):
                return (False, None)
        else:
            return (True, lhs_license.group(0))
    return (False, None)

def match_negation_word(text):
    match = re.search(NEGATION_WORD, text)
    if match:
        return (True, match.group(0))
    return (False, None)

def negation_in_pre_position(text, negation_word=None):
    match = re.search(YES_WORD_NEGATABLE_LHS, text)
    if match:
        if match.group(0):
            return (True, match.group(0))    
    return (False, None)

def negation_in_post_position(text, negation_word=None):
    match = re.search(YES_WORD_NEGATABLE_RHS, text)
    if match:
        if match.group(0):
            return (True, match.group(0)) 
    return (False, None)

def match_negatable_yes_word(text, negation_word=None):
    idx = text.find(negation_word)
    right_from_no = text[idx:]
    maybe_pre_no = negation_in_pre_position(right_from_no, negation_word=negation_word)
    left_from_no = text[:idx]
    maybe_post_no = negation_in_post_position(left_from_no, negation_word=negation_word)
    
    if maybe_pre_no[0]:
        return (True, f'{negation_word} {maybe_pre_no[1]}')
    if maybe_post_no[0]:
        return (True, f'{maybe_post_no[1]} {negation_word}')
    return (False, None)

def is_affirm(text):
    # An affirmation is either a
    #  1) dedicated, non-negatable yes-word ('yes', 'yeah', 'yep')
    #  2) non-negated yes-word 
    #  2.1) no negation occurring in licensed pre position: 'not right'
    #  2.2) no negation occurring in licensed post position ('absolutely not')
    # Strategy:
    #  1) attempt to match a non-negatable yes-word
    #  Failing that,
    #  2) attempt to match negatable yes-word ('correct', 'right'), 
    #     and if successful, attempt to confirm no negation occurring on licensed side
    #  2.1) no negation in pre position, or in 
    #  2.2) no negation in post position
    sure_yes = match_non_negatable_yes_word(text)
    if sure_yes[0]:
        return (sure_yes[0], None, sure_yes[1])

    maybe_negation_word = match_negation_word(text)
    if maybe_negation_word:
        maybe_yes = match_negatable_yes_word_affirmation(text, negation_word=maybe_negation_word[1])
    else:
        maybe_yes = match_negatable_yes_word_affirmation(text, negation_word=None)

    if maybe_yes[0]:
        return (True, maybe_negation_word[1] if maybe_negation_word[0] else None, maybe_yes[1])
    return (False, None, None)

def is_negate(text):
    # A negation/rejection is either a
    #  1) dedicated, non-negatable no-word ('no', 'nope')
    #  2) negated yes-word with negation in pre position ('not right')
    #  3) negated yes-word with negation in post position ('absolutely not')
    # Strategy:
    #  1) attempt to match a non-negatable no-word
    #  Failing that,
    #  2) attempt to match a negation ('not'), 
    #     and if successful, attempt to match negatable yes-word that licenses negation
    #  2.1) in pre position, or in 
    #  2.2) in post position
    sure_no = match_non_negatable_no_word(text)
    if sure_no[0]:
        return sure_no

    negation_word = match_negation_word(text)
    if negation_word[0]:
        maybe_no = match_negatable_yes_word(text, negation_word=negation_word[1])
        if maybe_no[0]:
            return (True, negation_word[1], maybe_no[1])
    return (False, None, None)
