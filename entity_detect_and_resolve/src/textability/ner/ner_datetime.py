import maya

from typing import Any

from textability.nlp_provider import detect_entities


def resolve_datetime(doc: Any):
    results = []
    for ent in filter(lambda x: x.label_ in ['DATE', 'TIME'], doc.ents):
        try:
            results.append((ent.text, maya.when(ent.text).iso8601()))
        except Exception as _:
            print(f'Cannot resolve {ent.label_}: [{ent.text}]')
            results.append((ent.text, None))
    return results


def detect_and_resolve(text: str):
    doc = detect_entities(text)
    return resolve_datetime(doc)
