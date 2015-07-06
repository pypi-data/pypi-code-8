import os
import re
import types
from subprocess import call


class commandRunner():

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

    def __init__(self, **kwargs):
        '''
            Constructs a local job
            takes
            tmp_id=, tmp_path=,
            in_glob=, out_glob=,
            command=, input_data=
        '''

        # if anything is passed it must be a string
        for key, value in kwargs.items():
            if not isinstance(value, str) and value is not None:
                raise TypeError('Argument {} not a string: {}'.format(key,
                                                                      value))

        if os.path.isdir(kwargs['tmp_path']):
            self.tmp_path = kwargs.pop('tmp_path', '')
        else:
            raise OSError('tmp_path provided does not exist')

        self.tmp_id = kwargs.pop('tmp_id', '')
        self.in_glob = kwargs.pop('in_glob', '')
        self.out_glob = kwargs.pop('out_glob', '')
        self.data = kwargs.pop('input_data', '')
        self.tmp_path = re.sub("/$", '', self.tmp_path)
        self.path = self.tmp_path+"/"+self.tmp_id+"/"
        if self.in_glob is not None:
            self.in_glob = re.sub("^\.", '', self.in_glob)
            self.in_path = self.path+self.tmp_id+"."+self.in_glob
        self.out_glob = re.sub("^\.", '', self.out_glob)
        self.out_path = self.path+self.tmp_id+"."+self.out_glob
        self.command = self.__translate_command(kwargs.pop('command', ''))

        # ensure we have an in_glob if we have been passed data
        if self.data is not None and self.in_glob is None:
            raise ValueError('in_glob missing but data provided')

        if self.tmp_path is None:
            raise ValueError('tmp_path missing')

        if "$INPUT" in self.command and self.in_glob is None:
            raise ValueError("$INPUT present in command "
                             "but no in_glob provided")

        if self.command is None:
            raise ValueError('command is required')

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
        raise NotImplementedError

    def run_cmd(self):
        '''
            run the command we constructed when the object was initialised.
            If exit is 0 then pass back if not decide what to do next. (try
            again?)
        '''
        raise NotImplementedError

    def tidy(self):
        '''
            Delete everything in the tmp dir and then remove the temp dir
        '''
        raise NotImplementedError
