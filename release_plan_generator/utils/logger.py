# Local imports
import logging
import datetime


LOG_FILE = 'logs/log'

def logger(func):
    """ A decorator function that adds logging functionality 

        If you decorate a function with @logger, whenever
        you call this function, the call event will be logged
        to a file.
    """

    logging.basicConfig(filename=LOG_FILE, level=logging.INFO)

    def wrapper(*args, **kwargs):

        date = datetime.datetime.today().strftime('%Y-%m-%d %H:%M')
        info = ' [{}] {} ran with args: {}, and kwargs: {}'.format(str(date), func.__name__, args, kwargs)

        logging.info(info)

        return func(*args, **kwargs)

    return wrapper