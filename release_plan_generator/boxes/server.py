# Local imports
from release_plan_generator.utils.config_parser import get_str_cfg


CONF = 'release_plan_generator/boxes/conf/servers.ini'

class Server:
    """ Server class that creates a server. """

    def __init__(self, name):
        self.name = name
        self.users_dir = get_str_cfg(CONF, 'DEFAULT', 'USERS_DIR')

    def get_name(self):
        return self.name

    def get_users_dir(self):
        return self.users_dir
