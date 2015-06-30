import os
import re
from subprocess import call


class commandRunner:

    tmp_id = None
    tmp_path = None
    in_glob = None
    out_glob = None
    command = None
    data = None
    output_data = None
    in_path = None
    out_path = None
    path = None

    def __init__(self, tmp_id, tmp_path, in_glob, out_glob, cmd, data):
        ''' Constructs a local job '''

        if os.path.isdir(tmp_path):
            self.tmp_path = tmp_path
        else:
            raise OSError

        self.tmp_id = tmp_id
        self.in_glob = in_glob
        self.out_glob = out_glob
        self.data = data
        self.tmp_path = re.sub("/$", '', self.tmp_path)
        self.in_glob = re.sub("^\.", '', self.in_glob)
        self.out_glob = re.sub("^\.", '', self.out_glob)
        self.path = self.tmp_path+"/"+self.tmp_id+"/"
        self.out_path = self.path+self.tmp_id+"."+self.out_glob
        self.in_path = self.path+self.tmp_id+"."+self.in_glob
        self.command = self.__translate_command(cmd)

    def __translate_command(self, command):
        '''
            takes the command string and substitutes the relevant files names
        '''
        # interpolate the file names if needed
        command = command.replace("$OUTPUT", self.out_path)
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
