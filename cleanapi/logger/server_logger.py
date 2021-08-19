import logging
from logging import handlers


_log_format = f"%(asctime)s - [%(levelname)s] - %(message)s"


def init(path_to_log='./log', level='INFO', max_log_size_mb=10, max_log_back_up_count=5) -> None:
    """
    Sets logging parameters for tornado
    :param path_to_log: path to the folder with log (relative to the location of the calling script)
    :type path_to_log: str
    :param level: logging level (DEBUG, INFO, WARNING, ERROR)
    :type level: str
    :param max_log_size_mb: log files size limit in MB
    :type max_log_size_mb: int
    :param max_log_back_up_count: count of log backups created after exceeding the size limit
    :type max_log_back_up_count: int
    """
    path_to_log = path_to_log.strip('/')

    file_handler = handlers.RotatingFileHandler(f'{path_to_log}/cleanapi.log',
                                                maxBytes=max_log_size_mb * 1048576,
                                                backupCount=max_log_back_up_count)
    file_handler.setFormatter(logging.Formatter(_log_format))

    access_logger = logging.getLogger('tornado.access')
    application_logger = logging.getLogger('tornado.application')
    general_logger = logging.getLogger('tornado.general')

    if level.upper() == 'DEBUG':
        access_logger.setLevel(logging.DEBUG)
        application_logger.setLevel(logging.DEBUG)
        general_logger.setLevel(logging.DEBUG)
    elif level.upper() == 'INFO':
        access_logger.setLevel(logging.INFO)
        application_logger.setLevel(logging.INFO)
        general_logger.setLevel(logging.INFO)
    elif level.upper() == 'ERROR':
        access_logger.setLevel(logging.ERROR)
        application_logger.setLevel(logging.ERROR)
        general_logger.setLevel(logging.ERROR)

    if not access_logger.hasHandlers():
        access_logger.addHandler(file_handler)
    if not application_logger.hasHandlers():
        application_logger.addHandler(file_handler)
    if not general_logger.hasHandlers():
        general_logger.addHandler(file_handler)
