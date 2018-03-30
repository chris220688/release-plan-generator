# Local imports
from release_plan_generator.boxes.server import Server
from release_plan_generator.utils.config_parser import get_str_cfg


CONF = 'release_plan_generator/boxes/conf/appservers.ini'

class Appserver(Server):
    """ Application server class that creates
        an application server.

        Inherits from Server class.
    """

    def __init__(self, name):
        super().__init__(name)
        self.apps_dir = get_str_cfg(CONF, 'DEFAULT', 'APPS_DIR')
        self.backup_dir = get_str_cfg(CONF, 'DEFAULT', 'BACKUP_DIR')

    def get_apps_dir(self):
        return self.apps_dir

    def get_backup_dir(self):
        return self.backup_dir

    def set_backup_dir(self, directory):
        self.backup_dir = directory