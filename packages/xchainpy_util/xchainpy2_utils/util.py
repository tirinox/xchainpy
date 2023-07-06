import logging
from enum import Enum


class XChainProtocol(Enum):
    THORCHAIN = 'THORCHAIN'
    MAYA = 'MAYA'


def class_logger(self, prefix=''):
    return logging.getLogger(prefix + self.__class__.__name__)


def remove_0x_prefix(s: str):
    return s[2:] if s.lower().startswith('0x') else s
