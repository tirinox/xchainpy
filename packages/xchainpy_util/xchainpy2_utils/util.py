import logging
from enum import Enum


class XChainProtocol(Enum):
    THORCHAIN = 'THORCHAIN'
    MAYA = 'MAYA'


def class_logger(self, prefix=''):
    return logging.getLogger(prefix + self.__class__.__name__)
