# Standard library imports
import argparse
import calendar
import datetime


def get_args():
    """ Get the command line arguments.

        Invalid arguments will get caught by
        the configparser exception handling

        Returns:
            args: An object with four attributes:
                    1. environment
                    2. app_modules
                    3. static_modules
                    4. conf_modules
    """

    # Instantiate the parser
    parser = argparse.ArgumentParser(description='Release commands generator')

    parser.add_argument('-e', '--environment',
        dest='environment',
        help='The name of the environment as specified in environments.ini')

    parser.add_argument('-a', '--app_modules',
        nargs = '*',
        dest='app_modules',
        help='A list of application modules as specified in app_modules.ini')

    parser.add_argument('-s', '--static_modules',
        nargs = '*',
        dest='static_modules',
        help='A list of static modules as specified in static_modules.ini')

    parser.add_argument('-c', '--conf_modules',
        nargs = '*',
        dest='conf_modules',
        help='A list of configuration modules as specified in conf_modules.ini')

    args = parser.parse_args()

    return args

def get_date():
    """ Get the current date in a specific format.

        Returns:
            The current datetime in YYYY-mm-dd_HHMM format 
    """

    date_now = datetime.datetime.today()

    return date_now.strftime('%Y-%m-%d_%H%M')

def get_day():
    """ Get the current day

        Returns:
            The currenct day. i.e Wednesday 
    """

    date_today = datetime.date.today()
    day_today = calendar.day_name[date_today.weekday()]

    return day_today
