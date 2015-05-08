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

    # Save
    def set_cmd(self, name, cmd):
        logging.debug("{0}->set_cmd(name:{1}, cmd:{2})".format(os.path.abspath(__file__), name, cmd))

        try:
            import my_data

            my_data.alx_save[name.lower()] = cmd

            if name.lower() is not "last":
                my_data.alx_save["last"] = cmd

            Save.io.export_data(my_data.alx_data, my_data.alx_save)
        except:
            raise ()

    def get_cmd(self, name):
        try:
            import my_data

            return my_data.alx_save.get(name, None)
        except:
            return None

        return None

    # alx_data
    def set_data(self, name, value):
        try:
            import my_data

            my_data.alx_data[name.lower()] = value

            Save.io.export_data(my_data.alx_data, my_data.alx_save)
        except:
            raise ()

    def get_data(self, name):
        try:
            import my_data

            return my_data.alx_data.get(name, None)
        except:
            return None

        return None


    def get_all(self):
        try:
            import my_data, copy

            return copy.deepcopy(my_data.alx_save)
        except:
            return None

        return None

    #Run
    def run_cmd(self, cmd, verbose):
        try:
            subprocess.call(cmd, shell=True)
            if verbose == True:
                print(cmd)
        except:
            raise ()

    #List
    def list_cmd(self, name, msg):

        try:
            cmd = self.get_cmd(name)
            if cmd is not None:
                print(cmd)
            else:
                print(msg)
        except:
            raise ()

    def list_all(self, msg):
        try:
            alx_save = self.get_all()
            if alx_save is not None:
                print("  {0:10} {1}".format("name:", "command"))
                for key, value in alx_save.items():
                    print("  {0:10} {1}".format(key + ":", value))
            else:
                print(msg)
        except Exception as e:
            raise (e)

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

