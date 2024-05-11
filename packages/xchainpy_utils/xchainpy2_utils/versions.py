import sys

if sys.version_info >= (3, 8):
    from importlib import metadata
else:
    import importlib_metadata as metadata


def get_version(package_name: str) -> str:
    """
    Get the version of the specified package.
    :param package_name: The name of the package.
    :return: The version of the package.
    """
    return metadata.version(package_name)


PACKAGE_VERSION = get_version('xchainpy2_utils')
