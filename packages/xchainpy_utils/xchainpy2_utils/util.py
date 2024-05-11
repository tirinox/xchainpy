import logging
from enum import Enum


class XChainProtocol(Enum):
    """
    Enum representing the different DeFi protocols supported by XChainPy2.
    """
    THORCHAIN = 'THORCHAIN'
    MAYA = 'MAYA'


def class_logger(self, prefix=''):
    """
    Get a logger with the class name as the prefix.
    :param self: The class instance.
    :param prefix: The prefix to use in the logger.
    :return: A logger with the class name as the prefix.
    """
    return logging.getLogger(prefix + self.__class__.__name__)


def remove_0x_prefix(s: str):
    """
    Remove the '0x' prefix from a string if it exists.
    :param s: The input string.
    :return: The string without the '0x' prefix.
    """
    return s[2:] if s.lower().startswith('0x') else s
