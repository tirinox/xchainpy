import logging


def class_logger(self, prefix=''):
    return logging.getLogger(prefix + self.__class__.__name__)
