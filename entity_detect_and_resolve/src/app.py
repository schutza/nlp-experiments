from time import perf_counter

from textability.ner.ner_datetime import detect_and_resolve

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
