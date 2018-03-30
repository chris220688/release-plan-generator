# Local imports
from release_plan_generator.utils.config_parser import get_str_cfg


CONF = 'release_plan_generator/modules/conf/modules.ini'

class Module():
    """ Module class that creates a module. """

    def __init__(self, name):
        self.name = name
        self.backup_extention = get_str_cfg(CONF, 'DEFAULT', 'BACKUP_EXTENTION')

    def add_artifact(self, artifact):
        self.artifact = artifact
