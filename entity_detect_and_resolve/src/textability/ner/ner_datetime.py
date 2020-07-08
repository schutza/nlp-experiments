import maya

from time import perf_counter
from typing import Any

from textability.nlp_provider import detect_entities


def _resolve_datetime(doc: Any):
    results = []
    for ent in filter(lambda x: x.label_ == 'DATE', doc.ents):
        try:
            results.append((ent.text, maya.when(ent.text).iso8601()))
        except Exception as _:
            print(f'Cannot resolve DATE: [{ent.text}]')
            results.append((ent.text, None))
    return results


def detect_and_resolve(text: str):
    doc = detect_entities(text)
    return _resolve_datetime(doc)


if __name__ == '__main__':
    text = input('> ')

    while text:
        now = perf_counter()
        results = detect_and_resolve(text)
        duration = perf_counter() - now
        print(f'Detection took {int(duration * 1000)} ms')
        for result in results:
            date_text, date_resolved = result
            if date_resolved is not None:
                print(f'Datetime for {date_text}: {date_resolved}')
            else:
                print(f'No resolution found for [{date_text}]')
        text = input('> ')
