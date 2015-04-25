import os

def show_files(dir_path):
    """
    Directory path
    """
    if os.path.exists(dir_path):
        dir_files = os.listdir(dir_path)

        return dir_files
    else:
        return "Path does not exists."

def print_files(dir_path):
    """
    List all the files of a given directory.
    """
    file_list = show_files(dir_path)
    for file in file_list:
        print file + " ",
