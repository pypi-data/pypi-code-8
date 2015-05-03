#!/usr/bin/env python

__author__ = 'Alex Gomes'

import alxlib.data.io
import logging, os, sys, subprocess


class Save:
    """

    """
    io = None

    def __init__(self):
        try:
            Save.io = alxlib.data.io.IO()
            path = Save.io.data_check()
            sys.path.append(path)
            logging.debug("path: {0}".format(path))
        except:
            raise ()

    #Save
    def set_cmd(self, name, cmd):
        logging.debug("{0}->set_cmd(name:{1}, cmd:{2})".format(os.path.abspath(__file__), name, cmd))

        try:
            import my_data
            my_data.alx_save[name.lower()] = cmd

            if name.lower() is not "last":
                my_data.alx_save["last"] = cmd

            Save.io.export_data(my_data.alx_save)
        except:
            raise ()

    def get_cmd(self, name):
        try:
            import my_data
            return  my_data.alx_save.get(name, None)
        except:
            raise ()

        return None


    #Run
    def run_cmd(self, cmd):
        try:
            subprocess.call(cmd, shell=True)
        except:
            raise ()


    #Flush
    def flush_cmd(self, name):

        try:
            import my_data
            my_data.alx_save.pop(name, None)
            Save.io.export_data(my_data.alx_save)
        except:
            raise ()

    def flush_all(self):
        try:
            Save.io.export_data({})
        except:
            raise ()