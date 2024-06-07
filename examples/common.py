import os


def sep(title='', simple=False):
    if not simple:
        title = ' '.join(title.upper())
    title = f' {title} ' if title else ''
    print(f'{title:-^120}')


def get_phrase():
    phrase = os.environ.get('PHRASE')
    if not phrase:
        raise ValueError("PHRASE env var is empty! Usage: PHRASE='your phrase here' python3 YOUR_SCRIPT.py")
    return phrase


def get_thornode_url():
    thornode = os.environ.get('THORNODE')
    return thornode
