from pythonjsonlogger import json
import sys


LOGGING_CONFIG = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'json_formatter': {
            '()': 'pythonjsonlogger.json.JsonFormatter',
            'format': '%(asctime)s %(levelname)s %(name)s %(message)s'
        }
    },
    'handlers': {
        'console_handler': {
            'class': 'logging.StreamHandler',
            'formatter': 'json_formatter',
            'stream': sys.stdout
        }
    },
    'loggers': {
        '': {  # root logger
            'handlers': ['console_handler'],
            'level': 'INFO',
            'propagate': True
        }
    }
}
