import logging

from affirmations import is_affirm, is_negate

logging.basicConfig(level=logging.INFO)
LOGGER = logging.getLogger()

def print_result(text, pattern, result):
    LOGGER.info(f"[{text}]\n  - Pattern:   {pattern}\n  - Result:    {result}")

def traverse_patterns(patterns, texts, comment=''):
    LOGGER.info(f'===== {comment} =====')
    for p in patterns:
        cp = re.compile(p)
        for t in texts:
            res = cp.search(t)
            print_result(t, p, res)




texts = [
    "not right",
    "foo not right bar",
    "absolutely not",
    "foo absolutely not bar",
    "that's right",
    "sure absolutely"
]

negation = r'\bnot\b'
yes_word_negatable_in_post_position = r"\b(?certainly|absolutely)\b"
yes_word_negatable_in_pre_position = r"\b(?right|okay)\b"

for text in texts:
    LOGGER.info(f"Text: [{text}]")
    negation = is_negate(text)
    LOGGER.info(f"is negative: {negation[0]} -- negation: {negation[2]}")
    affirmation = is_affirm(text)
    LOGGER.info(f"is positive: {affirmation[0]} -- affirmation: {affirmation[2]}")
    LOGGER.info(f"========")






pos_lah = r'(?:absolutely|certainly)\s+(?=not)'  # detect negation with suffix negatable phrase 
neg_lah = r'(?:absolutely|certainly) (?!not).*'  # detect affirmation with suffix negatable phrase 

pos_lbh = r'(?<=not)\s+(?:right|okay)'   # detect negation with prefix negatable phrase
neg_lbh = r'(?<!not)\s+(?:right|okay)'   # detect affirmation with prefix negatable yes phrase

lah_patterns = [pos_lah, neg_lah]
lbh_patterns = [pos_lbh, neg_lbh]



# traverse_patterns([pos_lah], texts, comment='positive lookahead')
# traverse_patterns([neg_lah], texts, comment='negative lookahead')
# traverse_patterns([pos_lbh], texts, comment='positive lookbehind')
# traverse_patterns([neg_lbh], texts, comment='negative lookbehind')

