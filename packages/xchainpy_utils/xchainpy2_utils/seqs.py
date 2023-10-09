from itertools import islice


def batched(iterable, n):
    "Batch data into lists of length n. The last batch may be shorter."
    # batched('ABCDEFG', 3) --> ABC DEF G
    it = iter(iterable)
    while True:
        batch = list(islice(it, n))
        if not batch:
            return
        yield batch


def unique_by_key(items, key):
    """
    Filter out duplicate items by key function
    Guaranteed that there will be no duplicates y = key(item)
    :param items: iterable of items
    :param key: function to get key from item
    :return: list of unique items
    """
    unique_keys = set()
    return list(filter(
        lambda item: (k := key(item)) not in unique_keys and not unique_keys.add(k),
        items
    ))


def key_attr_getter(msg, key: str):
    """
    Get attribute from object or value from dict by key
    :param msg: object or dict
    :param key: str
    :return:
    """
    if hasattr(msg, key):
        return getattr(msg, key)
    elif isinstance(msg, dict):
        return dict.__getitem__(msg, key)
    else:
        raise LookupError()
