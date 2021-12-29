# ---------------------------------------------------------------------------------------------------------------
# HELPER LOGGER
# Name: logger.py
# Desc: Encapsula funciones para logging
# ---------------------------------------------------------------------------------------------------------------

import logging
import logging.handlers
import os
import socket
import uuid
from logging import LoggerAdapter
from time import gmtime

from cloghandler import ConcurrentRotatingFileHandler

from helpers import config as config


def rotate_handler(formatter):
    if config.conf.get_bool('log.rotate.enabled'):
        path_file = config.conf.get_string('log.rotate.path_file')
        # Use an absolute path to prevent file rotation trouble.
        logfile = os.path.abspath(path_file)
        max_size = config.conf.get_int('log.rotate.max_size')
        backup_count = config.conf.get_int('log.rotate.backup_count')
        rh = ConcurrentRotatingFileHandler(logfile, "a", max_size, backup_count)
        rh.setFormatter(formatter)
        return rh
    else:
        return None


def console_handler(formatter):
    if config.conf.get_bool('log.console.enabled'):
        ch = logging.StreamHandler()
        ch.setFormatter(formatter)
        return ch
    else:
        return None


def get_logger(logger_name, log_level):
    # formatter = logging.Formatter('%(asctime)s.%(msecs)03dZ|%(levelname)s|%(threadName)s|%(uow)s|%(x-request-id)s|'
    #                               '%(hostname)s|USER-AGENT|%(x-forwarded-for)s|%(message)s',
    #                               datefmt='%Y-%m-%dT%H:%M:%S')
    formatter = logging.Formatter('%(asctime)s.%(msecs)03dZ|%(levelname)s|%(uow)s|%(hostname)s|%(message)s',
                                  datefmt='%Y-%m-%dT%H:%M:%S')
    formatter.converter = gmtime
    new_logger = logging.getLogger(logger_name)
    new_logger.setLevel(log_level)

    possible_handlers = [rotate_handler(formatter), console_handler(formatter)]
    [new_logger.addHandler(h) for h in possible_handlers if h is not None]

    logger_adapter = LoggerAdapter(new_logger, __extra)

    return logger_adapter


def __generate_uow():
    return str(uuid.uuid4())


def refresh_uow():
    global uow, __extra
    uow = __generate_uow()
    __extra['uow'] = uow


uow = str(uuid.uuid4())
__extra = {'uow': uow,
           'hostname': socket.gethostname(),
           'x-request-id': str(uuid.uuid4())
           }

logger = get_logger('Optimus Prime',
                    config.conf.get_int('log.level'))
