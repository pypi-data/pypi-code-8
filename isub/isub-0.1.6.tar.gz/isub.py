#!/usr/bin/env python

USAGE = '''Usage:
    To get TORQUE perform any computations:
        $ isub do <commands> done <options>
        (type 'isub --help do' to get more information)

    To redo a job:
        $ isub redo <index> (<new_name>)

    To show stats on the running jobs of yours:
        $ isub [stat|s]

    To delete any jobs:
        $ isub delete <index> ...

    To list the history of the computation commands:
        $ isub [history|h|history!|H] (<start_index>)   # show the job hisory
        $ isub shrink-history (<size>)      # shrink the history erasing the oldest data

    To show the result:
        $ isub [log|l] (<index>)
        (use a negative index to count backward from the tail to the head)

    To show this document:
        $ isub help
'''

PBS_FORMAT='''#!/bin/bash
#PBS -j oe
#PBS -N %s
#PBS -o %s
''' 

import os
import sys
import time
import copy
import shutil
import argparse
import commands
import pickle as pkl



class JobObject(object):
    """ Proxy for job information """
    def __init__(self, cmd, opt, wd, archive_dir):
        """ Initialize the job information.
        param cmd: main commands
        param opt: configurations on the job
        param wd: where the job is batched
        param archive_dir: where the job information will be archived
        """
        self.cmd = cmd
        self.opt = opt
        self.wd = wd
        self.archive_dir = archive_dir

        self.status = None #the end status of `qsub`
        self.torque_id = None #the job-id assigned by TORQUE
        # ID consisting of an unique time-index and the job name
        self.job_id = str(time.time()) + '_' + opt.name
        return

    @classmethod
    def copy(cls, obj, name=None):
        """ Create a deep copy (probably with new name) """
        opt = copy.copy(obj.opt)
        if name is not None: opt.name = name
        return cls(obj.cmd, opt, obj.wd, obj.archive_dir)

    def batch(self):
        """ Batch the job """
        script_path = self.get_infopath()
        log_path = self.get_logpath()

        #if self.opt.redirect:
        #    redirection = ' 2>&1 >%s; ' % self.get_logpath()
        #    cmd = self.cmd.strip()
        #    while cmd.endswith(';'):
        #        cmd = cmd[:-1]
        #    self.cmd = redirection.join(cmd.split(';') + [''])

        # write script
        self.write_script(script_path, log_path)
        if self.opt.redirect:
            self.write_script(script_path, log_path, redirecting=True)

        # clear logfile
        if os.path.isfile(log_path):
            os.remove(log_path)
        
        # qsub commands
        if not self.opt.no_qsub is True:
            self.status, self.torque_id = \
                    commands.getstatusoutput('qsub ' + self.get_infopath(dummy=True))

    def write_script(self, script_path, log_path, redirecting=False):
        if redirecting:
            true_log_path = log_path
            true_script_path = script_path
            log_path = self.get_logpath(dummy=True)
            script_path = self.get_infopath(dummy=True)

        f = open(script_path, 'w')
        f.write(PBS_FORMAT % (self.opt.name, log_path))

        if self.opt.resource_list is not None:
            f.write('#PBS -l ' + self.opt.resource_list + '\n')

        if self.opt.mail_options is not None:
            f.write('#PBS -m ' + self.opt.mail_options + '\n')
        if self.opt.user_list is not None:
            f.write('#PBS -M ' + self.opt.user_list + '\n')

        if not redirecting:
            f.write('cd ' + self.wd + '\n')
            f.write('echo "#start `date +%s%N`" >> ' + script_path + '\n')
            f.write(self.cmd + '\n')
            f.write('echo "#stop `date +%s%N`" >> ' + script_path + '\n')
        else:
            f.write('sh ' + true_script_path + ' 2>&1 >' + true_log_path + '\n')

        f.close()

    def __repr__(self):
        """ Represent itself with its name and its current status """
        job_state = '(running)' if self.is_running() else ''
        return self.opt.name + ' ' + job_state 

    def println(self, verbose=False):
        """ Print the job information """
        print self
        if verbose:
            print_keys = ['cmd', 'opt', 'wd', 'status', 'torque_id']
            for key in print_keys:
                print '\t', key, ': ', self.__getattribute__(key)
        return

    def remove_files(self):
        """ Remove the archive file """
        assert self.status is not None, "not batched yet!"
        files = [self.get_infopath(), self.get_logpath()]
        for f in files:
            if os.path.isfile(f):
                os.remove(f)
        return

    def delete_job(self):
        """ Delete the running job """
        status, out = commands.getstatusoutput('qdel ' + self.torque_id)
        print out
        return status

    def print_result(self):
        """ Print the result in rather rich format """
        self.println(verbose=True)
        if self.has_result():
            print '---- log start ----'
            print self.retrieve_log()
            print '---- log end ----'
        else:
            print 'No result'
        
        print 'elapsed time:', self.read_time_elapsed(), '(sec)'
        return

    def get_logpath(self, dummy=False):
        """ Get the path to the result file """
        if not dummy:
            return self.archive_dir + '/' + self.job_id + '.log'
        else:
            return self.archive_dir + '/dummy.log'

    def get_infopath(self, dummy=False):
        """ Get the path to the script file """
        if not dummy:
            return self.archive_dir + '/' + self.job_id + '.isub'
        else:
            return self.archive_dir + '/dummy.isub'

    def retrieve_log(self):
        """ Get the result log into a string """
        if not os.path.isfile(self.get_logpath()):
            print "%s is not found." % self.get_logpath()
            return ''
        f = open(self.get_logpath(), 'r')
        log = ''
        for row in f:
            log += row
        return log

    def retrieve_info(self):
        """ Get the script file into a string """
        if not os.path.isfile(self.get_infopath()):
            print "%s is not found." % self.get_infopath()
            return ''
        f = open(self.get_infopath(), 'r')
        info = ''
        for row in f:
            info += row
        return info

    def read_time_elapsed(self):
        """ Get the time elapsed from the script file """
        start = None
        stop = None
        for row in self.retrieve_info().splitlines():
            words = row.split()
            if words[0] == '#start':
                start = words[1]
            elif words[0] == '#stop':
                stop = words[1]
        
        if stop is None:
            return -1
        return (int(stop) - int(start)) * 1e-9
            
    def is_running(self):
        """ Return the status of the job """
        status, out = commands.getstatusoutput(
                'qstat ' + self.torque_id)
        if status == 0:
            if out.split()[-2] == 'E':
                return False
            else:
                return True
        else:
            return False

    def has_result(self):
        """ Check whether there is the result of the job """
        if os.path.isfile(self.get_logpath()):
            return True
        else:
            return False
        

class StorageInfo(object):
    def __init__(self, size):
        self.size = size


class StorageManager(object):
    '''
    Store and manage a list of objects in directory
    '''
    def __init__(self, info_fpath):
        self.ext_jobfile = '.isubjob'
        self.info_fpath = info_fpath
        self.dpath = os.path.dirname(info_fpath)

        if os.path.isfile(info_fpath):
            self.info = pkl.load(open(info_fpath, 'r'))
        else:
            self.info = StorageInfo(0)

    def __del__(self):
        pkl.dump(self.info, open(self.info_fpath, 'w'))

    def __len__(self):
        return self.info.size

    def __getitem__(self, x):
        if isinstance(x, int):
            idx = x + len(self) if x < 0 else x
            if 0 <= idx and idx < len(self):
                return self.load_file(idx)
        elif isinstance(x, slice):
            if len(self) == 0:
                return []
            return [self[i] for i in range(*x.indices(len(self)))]
        raise IndexError

    def __iter__(self):
        return (self[i] for i in range(len(self)))

    def get_filepath(self, idx):
        return self.dpath + '/' + str(idx) + self.ext_jobfile

    def does_exist(self, idx):
        return os.path.isfile(self.get_filepath(idx))

    def load_file(self, idx):
        fpath = self.get_filepath(idx)
        if os.path.isfile(fpath):
            return pkl.load(open(fpath, 'r'))
        else:
            print "%s does not exist" % fpath
            print "The system may be broken"
            return None

    def append(self, obj):
        fpath = self.get_filepath(len(self))
        pkl.dump(obj, open(fpath, 'w'))
        self.info.size += 1

    def shrink_to(self, size):
        shrink_size = len(self) - size
        
        # remove pointed files
        for p in self[:shrink_size]: p.remove_files()

        # copy(re-index) info files
        for i in xrange(size):
            if not self.does_exist(i + shrink_size):
                continue
            old_path = self.get_filepath(i + shrink_size)
            new_path = self.get_filepath(i)
            shutil.copy(old_path, new_path)

        # remove unused info files
        for i in range(size, len(self)):
            if not self.does_exist(i):
                continue
            os.remove(self.get_filepath(i))

        self.info.size = size


class Interface(object):
    """ Interface of `isub` """
    def __init__(self, dpath_launch):
        #make 'history' directory if it does not exists
        self.isub_home = dpath_launch
        self.dname_data = 'dat'
        self.dname_history = '.history'
        self.dname_archive = 'log'
        self.fname_history_manager = '.history'
        dirs = [self.get_dpath_archive(), self.get_dpath_history()]
        for d in dirs:
            if not os.path.isdir(d):
                os.makedirs(d)

        #set environment variable
        self.cwd = os.path.abspath(os.path.curdir)
        return
    
    def get_dpath_data(self):
        return self.isub_home + '/' + self.dname_data
    def get_dpath_history(self):
        return self.get_dpath_data() + '/' + self.dname_history
    def get_dpath_archive(self):
        return self.get_dpath_data() + '/' + self.dname_archive
    def get_history_manager(self):
        return StorageManager(self.get_dpath_history() + '/' +
                              self.fname_history_manager)

    def exit_on_error(self, message=''):
        print message
        sys.exit(1)
        return

    def parse_input(self):
        cname = sys.argv[0]
        args = sys.argv[1:]
        if len(args) == 0:
            self.exit_on_error(
                    'No argument\n' + 
                    'Type `isub help` to see what you can do with this'
                    )

        sign = args[0]
        modifier = args[1:]
        status = 0

        try:
            if 'do' in args:
                job = self.parse_job(args)
                job.batch()
                self.get_history_manager().append(job)
            elif 'redo' == sign:
                idx = int(modifier[0])
                h_manager = self.get_history_manager()
                if len(modifier) == 2:
                    self.assert_job_name(modifier[1])
                    name = modifier[1]
                else:
                    name = None

                job = JobObject.copy(h_manager[idx], name)
                job.batch()
                print job.torque_id
                status = job.status
                h_manager.append(job)

            elif 'stat' == sign or 's' == sign:
                status = self.show_stats(modifier)

            elif 'delete' == sign:
                index_list = modifier
                h_manager = self.get_history_manager()
                for i in index_list:
                    status = h_manager[int(i)].delete_job()

            elif 'history' == sign or 'h' == sign or \
                    'history!' == sign or 'H' == sign:
                h_manager = self.get_history_manager()
                start = -10 if modifier == [] else int(modifier[0])
                if start < 0: start += len(h_manager)
                start = max([start, 0])

                if 'history!' == sign or 'H' == sign:
                    for i, j in enumerate(h_manager[start:], start):
                        print i, '',
                        j.println(verbose=True)
                else:
                    for i, rec in enumerate(h_manager[start:], start):
                        print i, '', rec

            elif 'log' == sign or 'l' == sign:
                h_manager = self.get_history_manager()
                idx = -1 if modifier == [] else int(modifier[0])
                print (idx if idx >= 0 else idx + len(h_manager)), '',
                h_manager[idx].print_result()

            elif 'shrink-history' == sign:
                size = 0 if modifier == [] else int(modifier[0])
                self.get_history_manager().shrink_to(size)

            elif 'help' == sign:
                self.exit_on_error(USAGE)
            else:
                self.exit_on_error('Invalid argument(s)')

        except SyntaxError:
            print 'sorry! please report the bug to the developer(s)'

        return status

    def show_stats(self, args):
        status, output = commands.getstatusoutput('qstat ' + ' '.join(args))
        print output
        return status

    def parse_job(self, args):
        # parse commands and options
        argparser = argparse.ArgumentParser(prog='isub do <commands> done')
        argparser.add_argument('-N', '--name', required=True)
        argparser.add_argument('-l', '--resource_list', default=None)
        #argparser.add_argument('-l', '--resource_list', default='nodes=1')
        argparser.add_argument('-m','--mail_options')
        argparser.add_argument('-M', '--user_list')
        argparser.add_argument('-Q', '--no_qsub', action='store_true')
        argparser.add_argument('-R', '--redirect', action='store_true')

        # global parser
        arg_level = 0
        cmd = []
        opt = []
        for a in args:
            if a == 'do':
                arg_level += 1
            elif a == 'done':
                arg_level -= 1
            elif arg_level > 0:
                cmd.append(a)
            elif arg_level == 0:
                opt.append(a)
            else:
                print 'error: invalid commands'
        
        cmd = ' '.join(cmd)
        opt = argparser.parse_args(opt)
        self.assert_job_name(opt.name)

        return JobObject(cmd, opt, self.cwd, self.get_dpath_archive())

    @staticmethod
    def assert_job_name(string):
        illegal_chars = '/ \ ( ) < > " \' % { } [ ] @ `'.split() + [' ']
        for c in illegal_chars:
            if c in string:
                self.exit_on_error('job names must not contains "/": %s' % string)



def main():
    import sys, os
    from isub import Interface
    isub_home = os.path.join(os.path.expanduser('~'), '.isub')

    if not os.path.isdir(isub_home):
        os.makedirs(isub_home)

    status = Interface(isub_home).parse_input()
    sys.exit(status)


