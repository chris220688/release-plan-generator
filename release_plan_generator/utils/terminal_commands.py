# Standard library imports
from string import Template

# Local imports
from release_plan_generator.utils.file_operations import (
    delete_file,
    get_files,
    write_to_file,
    write_title
)
from release_plan_generator.utils.logger import logger


@logger
def ssh(user, env, box, output_file, break_line=True):
    """ Generate a linux ssh command

        Args:
            user: The user to ssh as
            env: The environment to ssh to (i.e preprod)
            box: The box to ssh to (i.e staging_appserver_1)

        Returns:
            The ssh command as a string
    """

    data = dict(user=user, env=env, box=box)

    command = Template('ssh ${user}@${env}-${box} ').substitute(data)

    write_to_file(output_file, command, break_line)

@logger
def mkdir(path, output_file):
    """ Generate a linux mkdir command

        Args:
            path: The path to create the directory

        Returns:
            The mkdir command as a string
    """

    data = dict(path=path)

    command = Template('mkdir ${path} ').substitute(data)
    
    write_to_file(output_file, command)

@logger
def cd(path, output_file):
    """ Generate a linux cd command

        Args:
            path: The directory to cd

        Returns:
            The cd command as a string
    """

    data = dict(path=path)

    command = Template('cd ${path} ').substitute(data)
    
    write_to_file(output_file, command)

@logger
def tar(directory, destination, output_file):
    """ Generate a linux tar command to tar a directory

        Args:
            directory: The directory to tar
            destination: The name of the artifact to be produced

        Returns:
            The tar command as a string
    """

    data = dict(directory=directory, destination=destination)

    command = Template('tar -cvzf ${destination} ${directory} ').substitute(data)
    
    write_to_file(output_file, command)

@logger
def untar(file, destination, output_file):
    """ Generate a linux tar command to untar an artifact

        Args:
            file: The artifact to untar
            destination: The directory to untar the artifact

        Returns:
            The tar command as a string
    """

    data = dict(file=file, destination=destination)

    command = Template('tar zxvf ${file} ${destination}').substitute(data)
    
    write_to_file(output_file, command)

@logger
def scp(user, env, box, file, destination, output_file):
    """ Generate a linux scp command

        Args:
            user: The user to ssh as
            env:  The environment to ssh to (i.e preprod)
            box:  The box to ssh to (i.e preprod_appserver_1)
            file: The file to scp
            destination: The directory to scp the file to

        Returns:
            The scp command as a string
    """

    data = dict(user=user, env=env, box=box, file=file, destination=destination)

    template = Template('scp ${file} ${user}@${env}-${box}:${destination}')

    command = template.substitute(data)
    
    write_to_file(output_file, command)

@logger
def dbaccess(file, output_file):
    """ Generate an informix dbaccess command to run a sql script

        Args:
            file: The sql script to run

        Returns:
            The dbaccess command as a string
    """

    data = dict(file=file)

    template = Template('dbaccess $$DB_ALIAS ${file} 2>&1 | tee ${file}.log')

    command = template.substitute(data)
    
    write_to_file(output_file, command)
