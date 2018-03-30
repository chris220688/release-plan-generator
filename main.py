# Standard library imports
import calendar
import itertools
import logging
import os
import re
import sys

# Local imports
from release_plan_generator.utils.file_operations import (
    delete_file,
    get_files,
    write_to_file,
    write_title
)
from release_plan_generator.utils.terminal_commands import (
    ssh,
    mkdir,
    cd,
    tar,
    untar,
    scp,
    dbaccess
)
from release_plan_generator.utils.logger import logger
from release_plan_generator.utils.other_utils import (
    get_args,
    get_date,
    get_day
)
from release_plan_generator.environments.environment import Environment
from release_plan_generator.modules.app_module import AppModule
from release_plan_generator.modules.static_module import StaticModule
from release_plan_generator.modules.conf_module import ConfModule


ARTIFACTS_DIR = './artifacts'
OUTPUT_FILE = './output/commands.txt'
ARTIFACT_EXT = '.tgz'

class CmdGenerator:
    """ A class that handles the creation of the commands """

    @logger
    def __init__(self, environment, app_modules=[], static_modules=[], conf_modules=[]):
        """ Initialise the necessary attributes for a CmdGenerator object """

        self.artifacts_dir = ARTIFACTS_DIR
        self.output_file = OUTPUT_FILE
        self.artifact_ext = ARTIFACT_EXT
        self.date_now = get_date()

        # Instantiate an Environment (i.e staging)
        self.environment = Environment(environment)

        self.ssh_user = self.environment.ssh_user

        # Get the webservers of the environment
        self.webservers = self.environment.webservers
        for webserver in self.webservers:
            webserver.set_backup_dir(webserver.backup_dir + self.date_now + '/')

        # Get the appservers of the environment
        self.appservers = self.environment.appservers
        for appserver in self.appservers:
            appserver.set_backup_dir(appserver.backup_dir + self.date_now + '/')

        # Instantiate the static modules
        self.has_static_modules = True if static_modules else False
        self.static_modules = [StaticModule(static_module) for static_module in static_modules]

        # Instantiate the app modules
        self.has_app_modules = True if app_modules else False
        self.app_modules = [AppModule(app_module) for app_module in app_modules]

        # Instantiate the conf modules
        self.has_conf_modules = True if conf_modules else False
        self.conf_modules = [ConfModule(conf_module) for conf_module in conf_modules]

        # Scan the artifacts directory for files
        self.tars = self._get_tars()
        self.sql_scripts = self._get_sql_scripts()

        # Match the artifacts with the modules
        self._match_modules_with_tars()

        # Delete any existed commands.txt file and start fresh
        delete_file(self.output_file)

    def _match_modules_with_tars(self):
        """ Matches the artifcacts with the modules.

            Uses the tar_regex attribute of the module from the configs
            and tries to find a match in the artifacts.

            If an artifact is found that matches the regex pattern, it assigns
            it to the artifact attribute to the module object.
        """

        # Match static modules
        for static_module in self.static_modules:
            matched = False
            for tar in self.tars:
                if re.search(static_module.tar_regex, tar):
                    static_module.add_artifact(tar)
                    matched = True
                    break

            if matched:
                print('Matched: ', static_module.artifact, '-->', static_module.name)
            else:
                print('Could not find match for static module: ', static_module.name)
                sys.exit(0)

        # Match app modules
        for app_module in self.app_modules:
            matched = False
            for tar in self.tars:
                if re.search(app_module.tar_regex, tar):
                    app_module.add_artifact(tar)
                    matched = True
                    break

            if matched:
                print('Matched: ', app_module.artifact, '-->', app_module.name)
            else:
                print('Could not find match for app module: ', app_module.name)
                sys.exit(0)

        # Match conf modules
        for conf_module in self.conf_modules:
            matched = False
            for tar in self.tars:
                if re.search(conf_module.tar_regex, tar):
                    conf_module.add_artifact(tar)
                    matched = True
                    break

            if matched:
                print('Matched: ', conf_module.artifact, '-->', conf_module.name)
            else:
                print('Could not find match for conf module: ', conf_module.name)
                sys.exit(0)

    def _print_tickets(self):
        """ Prints the tickets for the current release.

            Currently only prints the title
        """

        write_title(self.output_file, get_day() + ' Tickets')

    def _print_apps(self):
        """ Prints the apps that were passed as arguments by
            the user.
        """

        modules_nbr = len(self.static_modules) + len(self.app_modules) + len(self.conf_modules)

        write_title(self.output_file, 'Modules ({})'.format(modules_nbr))

        for static_module in self.static_modules:
            write_to_file(self.output_file, static_module.name)

        for app_module in self.app_modules:
            write_to_file(self.output_file, app_module.name)

        for conf_module in self.conf_modules:
            write_to_file(self.output_file, conf_module.name + '-conf')

    def _get_sql_scripts(self):
        """ Identifies any sql scripts in the artifacts directory

            Returns:
                sqls: Any sql scripts, if found
        """

        sqls = get_files('.sql', self.artifacts_dir)

        return sqls

    def _print_sql_scripts(self):
        """ Prints any sql scripts in the output file. """

        write_title(self.output_file, 'Database ({})'.format(len(self.sql_scripts)))

        for sql in self.sql_scripts:
             write_to_file(self.output_file, sql)

    def _get_tars(self):
        """ Identifies any tar files in the artifacts directory """

        tars = get_files(self.artifact_ext, self.artifacts_dir)

        return tars

    def _print_tars(self):
        """ Prints any tar files in the output file. """

        write_title(self.output_file, 'Artifacts ({})'.format(len(self.tars)))

        for tar in self.tars:
            write_to_file(self.output_file, tar)

    def _create_backup_dirs(self):
        """ Generates the commands to be used for creating
            the backup directories in the environment boxes.
        """

        write_title(self.output_file, 'Create backup directories')

        if self.has_static_modules:
            for webserver in self.webservers:

                ssh(self.ssh_user,
                    self.environment.name,
                    webserver.name,
                    break_line=False,
                    output_file=self.output_file)

                mkdir(webserver.backup_dir, output_file=self.output_file)

        if self.has_app_modules or self.has_conf_modules:
            for appserver in self.appservers:

                ssh(self.ssh_user,
                    self.environment.name,
                    appserver.name,
                    break_line=False,
                    output_file=self.output_file)

                mkdir(appserver.backup_dir, output_file=self.output_file)

    def _create_backups(self):
        """ Generates the commands to be used for taking
            the backups in the environment boxes.
        """       

        write_title(self.output_file, 'Backup webserver statics')

        if self.has_static_modules:
            for webserver in self.webservers:

                ssh(self.ssh_user,
                    self.environment.name,
                    webserver.name,
                    output_file=self.output_file)

                for static_module in self.static_modules:

                    cd(static_module.backup_from, output_file=self.output_file)

                    destination = webserver.backup_dir + static_module.name + static_module.backup_extention + self.artifact_ext

                    directory = static_module.backup_target

                    tar(directory, destination, output_file=self.output_file)

        write_title(self.output_file, 'Backup app-server modules')

        if self.has_app_modules or self.has_conf_modules:
            for appserver in self.appservers:

                ssh(self.ssh_user,
                    self.environment.name,
                    appserver.name,
                    output_file=self.output_file)

                for app_module in self.app_modules:

                    cd(app_module.backup_from, output_file=self.output_file)

                    destination = appserver.backup_dir + app_module.name + app_module.backup_extention + self.artifact_ext

                    directory = app_module.backup_target

                    tar(directory, destination, output_file=self.output_file)

                for conf_module in self.conf_modules:

                    cd(conf_module.backup_from, output_file=self.output_file)

                    destination = appserver.backup_dir + conf_module.name + '-conf' + conf_module.backup_extention + self.artifact_ext

                    directory = conf_module.backup_target

                    tar(directory, destination, output_file=self.output_file)

                write_to_file(self.output_file, '')

    def _scp_artifacts(self):
        """ Generates the commands to be used for seding
            the artifacts in the environment boxes.
        """

        write_title(self.output_file, 'scp artifacts')

        # cd to the directory of the artifacts
        cd(self.artifacts_dir, output_file=self.output_file)

        if self.has_static_modules:
            for webserver in self.webservers:

                file_to_scp = '*'
                scp(self.ssh_user,
                    self.environment.name,
                    webserver.name,
                    file_to_scp,
                    webserver.backup_dir,
                    output_file=self.output_file)

        if self.has_app_modules or self.has_conf_modules:
            for appserver in self.appservers:

                file_to_scp = '*'
                scp(self.ssh_user,
                    self.environment.name,
                    appserver.name,
                    file_to_scp,
                    appserver.backup_dir,
                    output_file=self.output_file)

    def _run_sql_scripts(self):
        """ Generates the commands to be used
            for running the sql scripts.
        """

        write_title(self.output_file, 'Run SQL scripts')

        for script in self.sql_scripts:
            dbaccess(script, output_file=self.output_file)

    def _deploy_artifacts(self):
        """ Generates the commands to be used for deploying
            the artifacts in the environment.
        """

        write_title(self.output_file, 'Deploy artifacts')

        if self.has_static_modules:
            for webserver in self.webservers:

                ssh(self.ssh_user,
                    self.environment.name,
                    webserver.name,
                    output_file=self.output_file)

                for static_module in self.static_modules:

                    cd(static_module.untar_dir, output_file=self.output_file)

                    destination = ''
                    untar(webserver.backup_dir + static_module.artifact,
                          destination,
                          output_file=self.output_file)

        write_to_file(self.output_file, '')

        if self.has_app_modules or self.has_conf_modules:
            for appserver in self.appservers:

                ssh(self.ssh_user,
                    self.environment.name,
                    appserver.name,
                    output_file=self.output_file)

                for module in itertools.chain(self.app_modules, self.conf_modules):

                    cd(module.untar_dir, output_file=self.output_file)

                    destination = ''
                    untar(appserver.backup_dir + module.artifact,
                          destination,
                          output_file=self.output_file)

                write_to_file(self.output_file, '')

    def _rollback_plan(self):
        """ Generates the rollback commands. """

        write_title(self.output_file, 'Rollback plan')

        if self.has_static_modules:
            for webserver in self.webservers:

                ssh(self.ssh_user,
                    self.environment.name,
                    webserver.name,
                    output_file=self.output_file)

                for static_module in self.static_modules:

                    cd(static_module.untar_dir, output_file=self.output_file)

                    file = webserver.backup_dir + static_module.name + static_module.backup_extention + self.artifact_ext

                    destination = ''

                    untar(file, destination, output_file=self.output_file)

                write_to_file(self.output_file, '')

        if self.has_app_modules:
            for appserver in self.appservers:

                ssh(self.ssh_user,
                    self.environment.name,
                    appserver.name,
                    output_file=self.output_file)

                for app_module in self.app_modules:

                    cd(app_module.untar_dir, output_file=self.output_file)

                    file = appserver.backup_dir + app_module.name + app_module.backup_extention + self.artifact_ext

                    destination = ''

                    untar(file, destination, output_file=self.output_file)

                for conf_module in self.conf_modules:

                    cd(conf_module.untar_dir, output_file=self.output_file)

                    file = appserver.backup_dir + conf_module.name + '-conf' + conf_module.backup_extention + self.artifact_ext

                    destination = ''

                    untar(file, destination, output_file=self.output_file)

                write_to_file(self.output_file, '')

    def generate_commands(self):
        """ Initialises the commands generation steps """

        print('Generating commands')

        self._print_tickets()
        self._print_apps()
        self._print_sql_scripts()
        self._print_tars()
        self._create_backup_dirs()
        self._create_backups()
        self._scp_artifacts()
        self._run_sql_scripts()
        self._deploy_artifacts()
        self._rollback_plan()


if __name__ == '__main__':

    args = get_args()

    cmd = CmdGenerator(
        environment=args.environment,
        app_modules=args.app_modules,
        static_modules=args.static_modules,
        conf_modules=args.conf_modules
    )

    cmd.generate_commands()
