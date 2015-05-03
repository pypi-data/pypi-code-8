#!/usr/bin/env python

__author__ = 'Alex Gomes'

import os
import errno
import pprint


class IO:
    """ Class to store alx data
    """
    path = ".alx"
    file = "my_data.py"

    alx_header = """''' ALX data
    \n'''"""

    alx_version = "0.1.0"


    def path_data_dir(self):
        return os.path.join(os.sep, os.path.expanduser('~'), IO.path)


    def path_data_file(self):
        return os.path.join(os.sep, self.path_data_dir(), IO.file)


    def data_check(self):
        try:
            dirPath = self.path_data_dir()

            if not os.path.exists(dirPath):
                os.makedirs(dirPath)

            filePath = self.path_data_file()

            if not os.path.isfile(filePath):
                save = {}
                self.export_data(save);

            return dirPath

        except OSError as exception:
            if exception.errno != errno.EEXIST:
                raise ()

        return None



    def write_data(self, data):
        try:
            fileObj = open(self.path_data_file(), 'w')
            fileObj.write(data)
            fileObj.close()

        except OSError as exception:
            if exception.errno != errno.EEXIST:
                raise ()


    def export_data(self, save):
        data = (IO.alx_header + "\n"
                                "alx_version = " + pprint.pformat(IO.alx_version) + "\n" +
                "alx_save = " + pprint.pformat(save) + "\n")

        self.write_data(data)