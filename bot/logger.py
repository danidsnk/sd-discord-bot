import logging
from logging.config import dictConfig
import os

LOGGING_CONFIG = {
    'version': 1,
    'disabled_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '%(levelname)-10s - %(asctime)s - %(module)-15s : %(message)s'
        },
        'standard': {'format': '%(levelname)-10s - %(name)-15s : %(message)s'},
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'standard',
        },
        'file': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': 'logs/infos.log',
            'mode': 'w',
            'formatter': 'verbose',
        },
    },
    'loggers': {
        'bot': {
            'handlers': ['console', 'file'],
            'level': 'INFO',
            'propagate': False
        },
        'discord': {
            'handlers': ['console', 'file'],
            'level': 'INFO',
            'propagate': False,
        },
    },
}


def setup_logger(debug: bool):
    if not os.path.exists('logs'):
        os.mkdir('logs')

    if debug:
        LOGGING_CONFIG['loggers']['bot']['level'] = 'DEBUG'
    dictConfig(LOGGING_CONFIG)


def get_logger(name):
    return logging.getLogger(name)
