# Standard library imports
import os


def delete_file(file):
    """ Delete a file in a specific path.

        Args:
            file: The file to be deleted
    """

    try:
        os.remove(file)
    except OSError:
        pass

def get_files(extention, directory):
    """ List all the files of a directory that
        have a specific extention.

        Args:
            extention: The extention of the files to search
            directory: The directory to search for files
    """

    tars = [file for file in os.listdir(directory)
            if file.endswith(extention)]
    return tars

def write_to_file(file, text, new_line=True):
    """ Append some text to a file.

        Args:
            file: The file to append some text to
            text: The text to append
    """

    with open(file, 'a') as output_file:
        text = text + '\n' if new_line else text
        output_file.write(text)

def write_title(file, title):
    """ Write a title in a specific file.
        Uses write_to_file to append to the file

        Args:
            file: The file to append the title to
            title: The title to append
    """

    text = '\n==========================\n'
    text += title
    text += '\n==========================\n'
    write_to_file(file, text)

