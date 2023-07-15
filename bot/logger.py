import logging
from logging.config import dictConfig
import os


def setup_logger(debug: bool):
    if not os.path.exists('logs'):
        os.mkdir('logs')

    logging_config = {
        'version': 1,
        'disabled_existing_loggers': False,
        'formatters': {
            'verbose': {
                'format': '%(levelname)-8s - %(asctime)s - %(name)-20s - %(module)-20s : %(message)s'
            },
            'standard': {'format': '%(levelname)-8s - %(module)-20s : %(message)s'},
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
                'encoding': 'utf-8',
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

    if debug:
        logging_config['loggers']['bot']['level'] = 'DEBUG'
    dictConfig(logging_config)


def get_logger(name):
    return logging.getLogger(name)
