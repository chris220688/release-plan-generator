# Local imports
from release_plan_generator.modules.module import Module
from release_plan_generator.utils.config_parser import get_dict_cfg


CONF = 'release_plan_generator/modules/conf/static_modules.ini'

class StaticModule(Module):
    """ Static module class that creates an statics module.

        Inherits from Module class.
    """

    def __init__(self, name):
        super().__init__(name)
        # The root directory of the module
        self.root_dir = get_dict_cfg(CONF, 'STATIC_DIRS', self.name)['root_dir']
        # The directory we need to be, before running the backup commands
        self.backup_from = get_dict_cfg(CONF, 'STATIC_DIRS', self.name)['backup_from']
        # The module we need to tar once we cd in the backup_from directory
        self.backup_target = get_dict_cfg(CONF, 'STATIC_DIRS', self.name)['backup_target']
        # The directory from which we need to untar
        self.untar_dir = get_dict_cfg(CONF, 'STATIC_DIRS', self.name)['untar_dir']
        # A pattern that matches the artifacts produced for the module
        self.tar_regex = get_dict_cfg(CONF, 'STATIC_DIRS', self.name)['tar_regex']
