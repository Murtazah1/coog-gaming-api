import logging
from logging.handlers import RotatingFileHandler


def logger_setup():
    # makes api logger
    logger = logging.getLogger("api_logger")

    # setting the level to debug makes it so you get all the error messages
    logger.setLevel(logging.DEBUG)

    # the format will be in date - name - level - message
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s")

    # file handler for writing logs to the file, 1Mb per file with 3 backups
    file_handler = RotatingFileHandler(
        "api.log", maxBytes=1024 * 1024, backupCount=3)

    file_handler.setFormatter(formatter)

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger


logger = logger_setup()
