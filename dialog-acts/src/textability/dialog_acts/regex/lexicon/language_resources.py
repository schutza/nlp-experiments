YES_WORDS_NON_NEGATABLE = r"\b(yes|yep|yup|yay|yey|yeah|i want it|that's what I said|affirmative|yessir)\b"

YES_WORDS_NEGATABLE_RHS = r'\b(certainly|absolutely)\b'
"""
These yes words are negatable, and license a negation occurring
on the right-hand side, e.g. 'certainly not'
"""

YES_WORDS_NEGATABLE_LHS = r'\b(right|okay|ok|sure|true|correct|what I said)\b'
"""
These yes words are negatable, and license a negation occurring
on their left-hand side, e.g. 'not okay'
"""

NO_WORDS_NON_NEGATABLE = r"\b(no|nope|nah|incorrect|never|nah|nay|that's not what I said)\b"

NEGATION_WORDS = r'\b(not|hardly)\b'