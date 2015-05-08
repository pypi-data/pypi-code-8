#!/usr/bin/env python

__author__ = 'Alex Gomes'

import os
import errno
import pprint
import alxlib.data

class IO:
    """ Class to store alx data
    """

    alx_header = """''' ALX data
    \n'''"""

    alx_version = "0.2.0"


    def path_data_dir(self):
        return os.path.join(os.sep, os.path.expanduser('~'), alxlib.data.my_path)


    def path_data_file(self):
        return os.path.join(os.sep, self.path_data_dir(), alxlib.data.my_data)


    def data_check(self):
        try:
            dirPath = self.path_data_dir()

            if not os.path.exists(dirPath):
                os.makedirs(dirPath)

            filePath = self.path_data_file()

            if not os.path.isfile(filePath):
                self.export_data({}, {})

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


    def export_data(self, alx_data, alx_save):
        data = (IO.alx_header + "\n"
                                "alx_version = " + pprint.pformat(IO.alx_version) + "\n" +
                "alx_data = " + pprint.pformat(alx_data) + "\n"
                "alx_save = " + pprint.pformat(alx_save) + "\n")

        self.write_data(data)