# Local imports
from release_plan_generator.utils.config_parser import get_str_cfg, get_dict_cfg
from release_plan_generator.boxes.webserver import Webserver
from release_plan_generator.boxes.appserver import Appserver


CONF = 'release_plan_generator/environments/conf/environments.ini'

class Environment:
    """ Environment class that creates an environment, i.e preprod
        
        Upon instantiation, it sets up appservers and webservers,
        according to the configuration of the environments.ini.

    """

    def __init__(self, name):
        self.name = name
        self.ssh_user = get_str_cfg(CONF, 'DEFAULT', 'SSH_USER')

        self.set_up_webservers()
        self.set_up_appservers()

    def set_up_webservers(self):
        """ Set up the webservers for a specific environment.

            Reads the WEB_SERVERS section in environments.ini
            and pulls out the webserver boxes.

            Creates a Webserver instance for each of the boxes,
            and adds it in the environment class attributes.
        """

        # This is the WEB_SERVERS dictionary from environments.ini
        webservers_dict = get_dict_cfg(CONF, self.name, 'WEB_SERVERS')

        # This the boxes list from the webservers_dict
        webservers_list = webservers_dict['boxes']

        # This will be a list of webserver objects
        webservers = []

        for webserver in webservers_list:
            webservers.append(Webserver(webserver))

        self.webservers = webservers

    def set_up_appservers(self):
        """ Set up the appservers for a specific environment.

            Reads the APP_SERVERS section in environments.ini
            and pulls out the appserver boxes.

            Creates an AppserverOnshore instance for each of the
            boxes and adds it in the environment class attributes.
        """

        appservers_dict = get_dict_cfg(CONF, self.name, 'APP_SERVERS')

        appservers_list = appservers_dict['boxes']

        appservers = []

        for appserver in appservers_list:
            appservers.append(Appserver(appserver))

        self.appservers = appservers
