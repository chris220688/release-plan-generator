# Local imports
from release_plan_generator.boxes.server import Server
from release_plan_generator.utils.config_parser import get_str_cfg


CONF = 'release_plan_generator/boxes/conf/webservers.ini'

class Webserver(Server):
    """ Webserver class that creates a webserver.

        Inherits from Server class.
    """

    def __init__(self, name):
        super().__init__(name)
        self.backup_dir = get_str_cfg(CONF, 'DEFAULT', 'BACKUP_DIR')

    def get_backup_dir(self):
        return self.backup_dir

    def set_backup_dir(self, directory):
        self.backup_dir = directory