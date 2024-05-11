def clamp(x, min_x, max_x):
    """
    Clamp a number to a range.
    :param x: The number to clamp.
    :param min_x: The minimum value.
    :param max_x: The maximum value.
    :return: The clamped number.
    """
    return min(max(x, min_x), max_x)
