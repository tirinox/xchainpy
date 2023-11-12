def sep(title='', simple=False):
    if not simple:
        title = ' '.join(title.upper())
    title = f' {title} '
    print(f'{title:-^120}')
