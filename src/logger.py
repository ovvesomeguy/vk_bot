import logging.config
import logging
import os

LOGGER_ADDR = 'logs.log'
LOGGER_STRUCT = {
    "version": 1,
    "handlers":{
        "fileHandler":{
            "class": "logging.FileHandler",
            "formatter": "myFormatter",
            "filename": LOGGER_ADDR
        }
    },
    "formatters":{
        "myFormatter":{
            "format":"%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        }
    },
    "loggers": {
        "cuteRaccoon":{
            "handlers": ["fileHandler"],
            "level": "INFO"
        }
    }
}
def log(message):
    logging.config.dictConfig(LOGGER_STRUCT)
    logger = logging.getLogger('cuteRaccoon')
    logger.info(message)