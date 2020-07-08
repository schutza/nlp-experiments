import spacy

NLP = spacy.load("en_core_web_sm")


def detect_entities(text: str):
    doc = NLP(text)
    for ent in doc.ents:
        print(f' Text: {ent.text}\n '
              f'Start: {ent.start_char}:{type(ent.start_char)}, End: {ent.end_char}:{type(ent.end_char)}, '
              f'Label: {ent.label_}')
    return doc
