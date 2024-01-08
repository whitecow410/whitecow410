# The Bot Made By AwkwardTeam. (WhiteCow, Sear_, YT Mango)
# Made For Miracle.
# Comment By  Sear_
# The Comment is for helping the code investigator/developer understand Codes.
# Credits to Miracle Development Team.


# Import Packages #
import logging
from logging.config import dictConfig

LOGGING_CONFIG = {
    "version": 1,
    "disabled_existing_loggers": False,
    "formatters": {
        "precise": {
            "format": "%(asctime)s | [%(levelname)s] - %(module)-8s : %(message)s",
            "datefmt": "%Y-%m-%d %H:%M"
        },
        "usage": {
            "format": "[%(levelname)s] - %(naem)-8s : %(message)s",
        }
    },
    "handlers": {
        "console": {
            "level": "DEBUG",
            "class": "logging.StreamHandler",
            "formatter": "precise"
        },
        "console2": {
            "level": "WARNING",
            "class": "logging.StreamHandler",
            "formatter": "precise"
        },
        "file": {
            "level": "INFO",
            "class": "logging.FileHandler",
            "filename": "logs/infos.log",
            "mode": "w",
            "formatter": "precise"
        },
    },
    "loggers": {
        "bot": {
            "handlers": ["console"],
            "level": "INFO",
            "propagate": False
        },
        "discord": {
            "handlers": ["console2", "file"],
            "level": "INFO",
            "propagate": False
        },
        "command": {
            "handlers": ["console", "file"],
            "level": "INFO",
            "propagate": False
        }
    }
}

dictConfig(LOGGING_CONFIG)
