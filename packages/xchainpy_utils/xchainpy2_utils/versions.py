import functools
import inspect
import sys
import warnings

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


def deprecated(reason="This function is deprecated."):
    def decorator(func):
        is_coroutine = inspect.iscoroutinefunction(func)

        @functools.wraps(func)
        async def async_wrapper(*args, **kwargs):
            warnings.warn(f"{func.__name__} is deprecated: {reason}",
                          category=DeprecationWarning,
                          stacklevel=2)
            return await func(*args, **kwargs)

        @functools.wraps(func)
        def sync_wrapper(*args, **kwargs):
            warnings.warn(f"{func.__name__} is deprecated: {reason}",
                          category=DeprecationWarning,
                          stacklevel=2)
            return func(*args, **kwargs)

        return async_wrapper if is_coroutine else sync_wrapper

    return decorator
