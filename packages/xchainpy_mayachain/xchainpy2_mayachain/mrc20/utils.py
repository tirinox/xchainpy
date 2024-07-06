from urllib.parse import urlunparse, urlencode, urlparse


def build_url(base_url, params: dict) -> str:
    """
    Build a URL from a base URL and a dictionary of parameters.

    :param base_url: Base URL
    :param params: A dictionary of parameters
    :return: full URL
    """

    # Convert the parameters dictionary to a URL-encoded string
    encoded_params = urlencode(params)

    if isinstance(base_url, str):
        base_url = urlparse(base_url)

    # Combine the base URL and the encoded parameters to form the complete URL
    complete_url = urlunparse(
        (base_url.scheme, base_url.netloc, base_url.path, base_url.params, encoded_params, base_url.fragment))

    return complete_url
