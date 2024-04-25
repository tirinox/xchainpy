import sys

if sys.version_info >= (3, 8):
    from importlib import metadata
else:
    import importlib_metadata as metadata


def get_version(package_name: str) -> str:
    return metadata.version(package_name)


PACKAGE_VERSION = get_version('xchainpy2_utils')
