import os


def sep(title='', simple=False):
    if not simple:
        title = ' '.join(title.upper())
    title = f' {title} '
    print(f'{title:-^120}')


def get_phrase():
    phrase = os.environ.get('PHRASE')
    if not phrase:
        raise ValueError("PHRASE env var is empty!")
    return phrase
