import logging
from logging.handlers import RotatingFileHandler


def config_logging(filename):
    """This function configure the logging format and handler
    Args:
        filename (str): the log file name
    """
    # define the log format
    log_format = "%(asctime)s - %(levelname)s - %(message)s"
    # configure the root logger
    logging.basicConfig(level=logging.DEBUG, format=log_format)
    # create a rotating file handler
    file_handler = RotatingFileHandler(filename, maxBytes=10240, backupCount=0)
    file_handler.setFormatter(logging.Formatter(log_format))
    logging.getLogger('').addHandler(file_handler)

    return logging
