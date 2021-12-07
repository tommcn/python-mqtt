import logging.config

LOGGING_CONFIG = {
    "version": 1,
    "disable_existing_loggers": True,
    "formatters": {
        "standard": {
            "format": "%(asctime)s [%(levelname)s] %(name)s (%(threadName)s): %(message)s"
        },
        "simple": {"format": "[%(levelname)s] %(message)s"},
    },
    "handlers": {
        "default": {
            "level": "DEBUG",
            "formatter": "simple",  # Change to "standard" for more verbose logging
            "class": "logging.StreamHandler",
            "stream": "ext://sys.stdout",
        },
    },
    "loggers": {
        "": {
            "handlers": ["default"],
            "level": "DEBUG",
            "propagate": False,
        },
        "__main__": {
            "handlers": ["default"],
            "level": "DEBUG",
            "propagate": False,
        },
    },
}


def init_logging():
    logging.config.dictConfig(LOGGING_CONFIG)
