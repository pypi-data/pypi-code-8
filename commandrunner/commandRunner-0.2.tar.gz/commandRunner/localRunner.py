import os
import re
import types
from commandRunner import commandRunner
from subprocess import call


class localRunner(commandRunner.commandRunner):

    def __init__(self, **kwargs):
        commandRunner.commandRunner.__init__(self, **kwargs)

    def __translate_command(self, command):
        '''
            takes the command string and substitutes the relevant files names
        '''
        # interpolate the file names if needed
        command = command.replace("$OUTPUT", self.out_path)
        if self.in_path is not None:
            command = command.replace("$INPUT", self.in_path)
        return(command)

    def prepare(self):
        '''
            Makes a directory and then moves the input data file there
        '''
        if not os.path.exists(self.path):
            os.makedirs(self.path)

        if self.data is not None:
            fh = open(self.in_path, 'w')
            fh.write(self.data)
            fh.close()

    def run_cmd(self):
        '''
            run the command we constructed when the object was initialised.
            If exit is 0 then pass back if not decide what to do next. (try
            again?)
        '''
        exit_status = None
        try:
            exit_status = call(self.command, shell=True)
        except Exception as e:
            raise OSError

        if exit_status == 0:
            if os.path.exists(self.out_path):
                with open(self.out_path, 'r') as content_file:
                    self.output_data = content_file.read()
        else:
            raise OSError
        return(exit_status)

    def tidy(self):
        '''
            Delete everything in the tmp dir and then remove the temp dir
        '''
        if os.path.exists(self.in_path):
            os.remove(self.in_path)
        if os.path.exists(self.out_path):
            os.remove(self.out_path)
        if os.path.exists(self.path):
            os.rmdir(self.path)
