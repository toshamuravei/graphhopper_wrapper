from collections import namedtuple


GraphHopperServer = namedtuple('GraphHopperServer', 'host port default_params')

LOG_CONFIG = {
    'version': 1,
    'formatters': {
        'colored': {
            '()': 'colorlog.ColoredFormatter',
            'format': '%(log_color)s[%(levelname)s] %(asctime)s:%(name)s:%(reset)s %(white)s%(message)s',
            'log_colors': {
                'DEBUG': 'cyan',
                'INFO': 'green',
                'WARNING': 'yellow',
                'ERROR': 'red',
                'CRITICAL': 'red',
            }
        }
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'level': 'DEBUG',
            'formatter': 'colored',
            'stream': 'ext://sys.stdout'
        },
    },
    'loggers': {
        'wrapper': {
            'level': 'DEBUG',
            'handlers': ['console']  # ['sentry', 'console'],
        }
    },
    'disable_existing_loggers': False
}