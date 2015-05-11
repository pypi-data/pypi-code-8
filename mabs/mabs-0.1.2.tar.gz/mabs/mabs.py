#!/usr/bin/env  python
#coding:utf-8
#function: upload files throuth ssh protocal and excute command

import paramiko
import sys
import threading
import os
from multiprocessing.dummy import Pool as ThreadPool
from time import sleep,ctime
from optparse import OptionParser
import collections
import logging
import sh

# my scripts
from hosts_settings import *


MULTI_PROC = 2  #process
pool = ThreadPool(MULTI_PROC)

common_set = ConfigParser.RawConfigParser(allow_no_value=True)
common_set.read('/etc/ansible/secret.ini')
get_timeout = common_set.get('common_settings', 'timeout')

class Tran_Base(object):
    """
    use ftp to put or get file
    use ssh to execute commands
    """

    def __init__(self, paralist, gothreading=True, timeout=None):
        self.hostname = paralist[0]
        self.port = int(paralist[1])
        self.username = paralist[2]
        self.pwd = paralist[3]
        self.commandline = paralist[4]
        self.logging = self.logger_log()
        self.logqueue = []
        self.success = 0
        self.fail = 0
        self.timeout = timeout
        if gothreading == True:
            self.main = self.main()

    def logger_log(self):
        """
        use this to log file,
        the destination is /var/log/mabslog.txt
        """
        logging.basicConfig(filename = os.path.join(
                '/var/log', 'mabslog.txt'), level = logging.INFO,
                    format = '%(asctime)s - %(levelname)s: %(message)s')
        return logging

    def notify(self, color, msg):
        """
        provide 4 colors to use for output
        c == critical    red
        w == waring      yellow
        b == info        blue
        g == info_return light-blue
        """
        c, w ,b ,g = '\033[1;40;31m', '\033[1;40;33m', '\033[1;40;34m', '\033[1;40;38m'
        endc = '\033[0m'
        if color == 'c':
            return """ %s %s %s""" %(c, msg, endc)
        if color == 'w':
            return """ %s %s %s""" %(w, msg, endc)
        if color == 'g':
            return """ %s %s %s""" %(g, msg, endc)
        if color == 'b':
            return """ %s %s %s""" %(b, msg, endc)

    @staticmethod
    def Usage():
        print '*' * 90
        print '\033[1;40;36m'
        print '''
            Usage:
            mabs.py -H web1 -C 'ls;echo 0'

            or
            mabs.py --hostfile iplist.txt --commfile commands.txt

            or
            mabs.py --hostfile iplist.txt -C 'ls;echo 0'

            or
            mabs.py -H web1 --commfile commands.txt

            or(if directory not exists,we will create the diretory automatically)
            mabs.py -H web1 -C 'putfile /tmp/a /tmp/test/b'
            mabs.py -H web1 -C 'putline /tmp/a /tmp/b'
            mabs.py -H web1 -C 'getfile /tmp/a /tmp/b'
            mabs.py -H web1 -C 'getline /tmp/a /tmp/b'

            or add -s only show hosts
            mabs.py -H Web1 -s

            *******************cat command.txt********************
            putfile /tmp/a /tmp/e
            getfile /tmp/c /tmp/a

            ******************************************************
            or
            *******************cat command.txt********************
            ls
            ls;echo '1'
            testif=1
            if [[ if $testif == 1 ]];then
                echo 'if is ok'
            fi
            ******************************************************

            *******************cat iplist.txt*********************
            ip port username password

            you can see log at /var/log/mabslog.txt
            '''
        print '\033[0m'
        print '*' * 90

    def distinguish(self):
        """
        verify whether we should connect clients
        """
        try:
            filetype = self.commandline.split(' ')[0].strip()
            if filetype not in ['getfile', 'putfile', 'putline', 'getline']:
                raise
            return filetype
        except:
            return 'com'

    def ssh_conn(self):
        '''
        start to connect the ssh clients
        '''
        try:
            self.ssh = paramiko.SSHClient()
            self.ssh.load_system_host_keys()
            self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            self.ssh.connect(self.hostname, port=self.port,
                    username=self.username, password=self.pwd, timeout=self.timeout)
        except:
            log = self.hostname + " can't be authorized,check password, port and user: ,%s"%e
            print self.notify('c', log)
            self.ssh.close()

    def ftp_conn(self):
        """
        start to connect the sftp clients
        """
        try:
            t = paramiko.Transport((
                        self.hostname, self.port))
        except:
            log = "can not connect %s %s" %(self.hostname, self.port)
            self.logqueue.append(self.notify('c', log))
            self.logging.error(log)
            sys.exit(2)
        try:
            t.connect(username=self.username, password=self.pwd)
            self.sftp = paramiko.SFTPClient.from_transport(t)
        except:
            log = self.hostname + " password wrong or username not exists"
            print self.notify('c', log + '\n  crtl + c to exit')
            self.logqueue.append(self.notify('c', log))
            self.logging.error(log)
            t.close()
            sys.exit(2)

    def fileget(self):
        filetran = self.commandline.split(' ')
        local = filetran[1].strip()
        remote = filetran[2].strip()
        return local, remote

    def close_all(self):
        self.sftp.close()
        self.ssh.close()

    def send_file_support_shell(self, machine):
        '''
        add putfile getfile $(),`` shell support
        '''
        find_comm1 = re.compile(r"`(.*)`")
        find_comm2 = re.compile(r"\$\((.*)\)")
        machine = ' '.join(machine.split('__'))
        try:
            commorigin = find_comm1.search(machine).group(0)
            commtext1 = find_comm1.search(machine).group(1)
            comm_data = os.popen(commtext1).read().strip()
            machine = machine.replace(commorigin, comm_data)
        except:
            pass
        try:
            commorigin = find_comm2.search(machine).group(0)
            commtext2 = find_comm2.search(machine).group(1)
            comm_data = os.popen(commtext2).read().strip()
            machine = machine.replace(commorigin, comm_data)
        except:
            pass
        return machine


class Tran_Command(Tran_Base):

    def verify_dir_exist(self, tran_type):
        remote = self.fileget()[1]
        path = os.path.dirname(remote)
        if tran_type == 'putfile' or tran_type == 'putline':
            stdin,stdout,stderr = self.ssh.exec_command('ls {0}'.format(path))
            if stderr.read():
                log = "there's no remote directory {0},and it will going to be created ".format(path)
                self.logging.warn(self.notify('g', 'warning:\n  ' + log))
                self.ssh.exec_command('mkdir -p {0}'.format(path))
                return log
        elif tran_type == 'getfile':
            if os.path.exists(path):
                pass
            else:
                log = "there's no local directory {0},and it will going to be created ".format(path)
                self.logging.warn(self.notify('g', 'warning:\n  ' + log))
                sh.mkdir('-p', path)
                return log
        return None

    def FileTran(self, tran_type):
        """
        use SFTP method to put or get file to or from the remote clients
        """
        self.ssh_conn()
        warning_log = self.verify_dir_exist(tran_type)
        self.ftp_conn()
        local, remote = self.fileget()
        local, remote = self.send_file_support_shell(local),\
                        self.send_file_support_shell(remote)
        head_log = "transfer file " + self.hostname
        if tran_type in ["putfile", "putline"]:
            try:
                flag = True
                localname = local.split('/')[-1]
                if remote.endswith('/'):
                    remote = remote + localname
                if local.startswith('/'):
                    pass
                else:
                    local = os.getcwd() + '/' + local
                if tran_type == "putfile":
                    self.sftp.put(local, remote)
                    log = '***put file %s to remote %s %s successfully' % (
                                            local, self.hostname, remote)
                    head_log += ' put file: success'
                else:
                    with open(local ,'r') as f:
                        text = f.read().strip()
                    self.ssh.exec_command("echo -e '{0}' >> {1}".format(text, remote))
                    log = '***put lines %s to remote %s %s successfully' % (
                                            local, self.hostname, remote)
                    head_log += ' put lines: success'
                self.success = 1
                self.logging.info(log)
            except:
                flag = False
                log = "***no local file %s" % local
                head_log += ' put file: fail'
                self.fail = 1
                self.logging.error(log)
        elif tran_type in ["getfile", "getline"]:
            try:
                local, remote = remote, local
                flag = True
                remotename = remote.split('/')[-1]
                if local == '.':
                    local = os.getcwd() + '/' + remotename
                if local.endswith('/'):
                    local = local + remotename
                if local.startswith('/'):
                    pass
                else:
                    local = os.getcwd() + '/' + local
                if tran_type == "getfile":
                    self.sftp.get(remote ,local)
                    log = '***get remote file %s %s to local %s successfully' % (
                                                self.hostname, remote, local)
                    head_log += ' get file: success'
                else:
                    stdin,stdout,stderr = self.ssh.exec_command("cat {0}".format(remote))
                    text = stdout.read().strip()
                    sh.echo('-e', text ,_out=local)
                    log = '***get lines %s to remote %s %s successfully' % (
                                                    remote, self.hostname, local)
                    head_log += ' get lines: success'
                self.success = 1
                self.logging.info(log)
            except:
                flag = False
                log = '***' + self.hostname + " has no remote file %s" % remote
                head_log += ' get file: fail'
                self.fail = 1
                self.logging.error(log)
        self.file_log_export(head_log, warning_log, log, flag)
        self.close_all()

    def Execu(self):
        """
        use SSH method to excute command.
        """
        access_log = ''
        try:
            self.ssh_conn()
            stdin,stdout,stderr = self.ssh.exec_command(self.commandline)
            head_log = "execute commands in " + self.hostname
            stdoutlog = self.form_log(stdout.read())
            if stdoutlog.strip():
                self.logging.info(stdoutlog)
            stderrlog = self.form_log(stderr.read())
            if stderrlog.strip():
                self.logging.error(stderrlog)
                head_log += ': fail'
                self.fail = 1
            else:
                head_log += ': success'
                if not self.fail:
                    self.success = 1
            self.notify('b', '*' * 50)
        except Exception,e:
            access_log = self.hostname + " can't be authorized,check password, port and user: ,%s"%e
            self.logging.error(access_log)
            self.fail = 1
        finally:
            self.command_log_export(head_log, stdoutlog, stderrlog, access_log)
            self.ssh.close()


class TranTune(Tran_Command):

    def file_log_export(self, head_log='', warning_log='', log='', flag=''):
        self.logqueue.append(self.notify('b', '*' * 50))
        self.logqueue.append(self.notify('w', head_log))
        self.logqueue.append(self.notify('b', '*' * 50))
        if warning_log:
            self.logqueue.append(self.notify('w', warning_log))
        if flag:
            self.logqueue.append(self.notify('g', 'succeed return:\n  ' + log))
        else:
            self.logqueue.append(self.notify('c', 'failed return:\n  ' + log))

    def form_log(self, log):
        """
        form the outputting logs more elegantly
        """
        logout = log.split('\n')
        logout.insert(0, ' ')
        return '\n        '.join(logout)

    def command_log_export(self, head_log='', stdoutlog='', stderrlog='', access_log=''):
        self.logqueue.append(self.notify('b', '*' * 50))
        self.logqueue.append(self.notify('w', head_log))
        self.logqueue.append(self.notify('b', '*' * 50))
        self.logqueue.append(self.notify('b', 'exec command:%s' %
                                    self.form_log(self.commandline)))
        if stdoutlog.strip():
            self.logqueue.append(self.notify('g', '\n  succeeded return:' + stdoutlog))
        if stderrlog.strip():
            self.logqueue.append(self.notify('c', '\n  failed return:' + stderrlog))
        self.notify('b', '*' * 50)
        if access_log:
            self.logqueue.append(self.notify('c', access_log))

    def main(self):
        commtype = self.distinguish()
        if commtype == "com":
            commandline = self.commandline.strip()
            self.Execu()
        else:
            self.FileTran(commtype)
        for i in self.logqueue:
            print i
        return self.logqueue

#if __name__ == '__main__':
#    a = TranTune('128.192.0.132', '22', 'root', 'python', 'ls;ls')
#    a = TranTune('128.192.0.132', '22', 'root', 'python', 'putfile /tmp/a /tmp/b')
#    a = TranTune('128.192.0.132', '22', 'root', 'python', 'getfile /tmp/c /tmp/b')
#    a.main()



def verify_file(args):
    """
    verify whether args is a string or a file
    if args is a file,class will read it.
    returns will always be a dictory.
    """
    key = args.keys()[0]
    if key == 'hostfile':
        with open(args['hostfile'], 'r') as f1:
            confs = f1.readlines()
        return {'confs': confs}
    elif key == 'commfile':
        with open(args['commfile'], 'r') as f2:
            comms = f2.readlines()
        return {'comms': comms}
    elif key == 'host':
        confs = args['host']
        return {'confs': confs}
    elif key == 'command':
        comms = args['command']
        return {'comms': comms}

def collect_comm(comms):
    """
    collecting commands whatever is file or string, and always
    turn it to be a strings.
    """
    exists_comms = []
    for comm in comms:
        if comm.startswith('#') and len(comm) > 1:
            break
        exists_comms.append(comm)
        comms = ''.join(exists_comms)
    return comms

class Collect_file(object):
    """
    return argv is a strings
    argv: putfile /tmp/a /tmp/
          getfile /tmp/a /tmp/
    if argv is startwith putfile or getfile and more than 2 line,
       it will a usage.
    """
    def __init__(self, comms):
        self.exists_comms = []
        self.comms = comms

    def one_file(self, comms):
        if comms.split()[0] in ['putfile', 'getfile', 'putline', 'getline']:
            if not re.search(r'\;', comms):
                self.exists_comms.append(comms)
            else:
                TranTune.Usage()
                sys.exit(2)

    def collect(self):
        if isinstance(self.comms, str):
            self.one_file(self.comms)
        else:
            for comm in self.comms:
                if comm.startswith('#') and len(comm) > 1:
                    break
                self.one_file(comm)
        return self.exists_comms

def trantune_for_mul(config):
    tran = TranTune(config, gothreading=False, timeout=get_timeout)
    tran.main()
    return tran.success, tran.fail, tran.hostname

def MyMul(args):
    """
    args must be [{'commfile': 'commfile.txt'}, {'hostfile': 'hostfile.txt'}],
    or [{'commfile': 'ls'}, {'host': '192.168.1.1'}]
    and use mul-thread

    """
    threads = []
    config = []
    for i in args:
        idict = verify_file(i)
        key = idict.keys()[0]
        if key == 'confs':
            confs = idict['confs']
            if isinstance(confs, list):
                confs = '\n'.join(confs)
        elif key == 'comms':
            comms = idict['comms']
            if isinstance(comms, list):
                comms = '\n'.join(comms)
    for conf in confs.split('\n'):
        if not conf.startswith('#') and len(conf) >= 1:
            ip, port, username, pwd = conf.strip().split(' ')
            file_comms = Collect_file(comms).collect()
            if file_comms:
                [config.append([ip, port, username, pwd, i])
                        for i in file_comms]
            else:
                comms = collect_comm(comms)
                config.append([ip, port, username, pwd, comms])
    try:
        result = pool.map_async(trantune_for_mul, config).get(999999)
    except KeyboardInterrupt:
        print 'got ^C while pool mapping, terminating the pool'
        pool.terminate()
        sys.exit(2)
    finally:
        pool.close()
        pool.join()

    success_list = [(i[0], i[2]) for i in result if i[0]==1]
    fail_list = [(i[1], i[2]) for i in result if i[1]==1]
    print '\033[1;40;33m'
    print '  ' + '*' * 50
    print '  ' + '*' * 50
    print '\033[0m'
    if fail_list:
        print '\033[1;40;31m'
        print '  failed events:' + str(len(fail_list)) + ' host: ' + ','.join(
                            i[1] for i in fail_list)
        print '\033[0m'
    if success_list:
        print '\033[1;40;38m'
        if fail_list:
            print '  succeed events: ' + str(len(success_list)) + ' host: ' + ','.join(
                            i[1] for i in success_list)
        else:
            print '  all succeed, ' + ' host: ' + ','.join(
                            i[1] for i in success_list)
        print '\033[0m'
    print '\033[1;40;33m'
    print '  ' + '*' * 50
    print '  ' + '*' * 50
    print '\033[0m'

class Verify_bool(TranTune):
    """
    use bool to verify args whether can or
    can not put together for optparser
    """

    def __init__(self):
        pass

    def common_verify(self, a, b, flag='h'):
        seebool = a and b
        if seebool:
            if flag == 'h':
                self.warning_host()
            else:
                self.warning_comm()
            sys.exit(1)
        else:
            return seebool

    def warning_host(self):
        print self.notify('c', "do not put -H --hostfile together")

    def warning_comm(self):
        print self.notify('c', "do not put -C --commfile together")

def file_parse(files):
    find_comm1 = re.compile(r"`(.*)`")
    find_comm2 = re.compile(r"\$\((.*)\)")
    try:
        commtext1 = find_comm1.search(files).group(1)
        comm_data = '__'.join(commtext1.split(' '))
        files = files.replace(commtext1, comm_data)
    except:
        pass
    try:
        commtext2 = find_comm2.search(files).group(1)
        comm_data = '__'.join(commtext2.split(' '))
        files = files.replace(commtext2, comm_data)
    except:
        pass
    return files

if __name__ == '__main__':
    parser = OptionParser()
    parser.add_option("-H", "--host", dest="host",
            help = "define the groups or host,like -h web1 ,-h group-name1")
    parser.add_option("-C", "--command", dest="command",
            help = "execute simple command")
    parser.add_option("", "--hostfile", dest="hostfile",
            help = "define the host file, like --hostfile hostfile.txt")
    parser.add_option("", "--commfile", dest="commfile",
            help = "define the command file, like --commfile commfile.txt")
    parser.add_option("-s", "--show", action="store_true", dest="show_clients",
            help = "display all the clients, like -s")
    parser.add_option("-u", "--user", dest="user",
            help = "define the use to execute command, like -u root")
    (options, args) = parser.parse_args()
    verify = Verify_bool()
    host_bool = verify.common_verify(
                            options.host, options.hostfile)
    comm_bool = verify.common_verify(
                            options.command, options.commfile, 'comm')
    paraset = [options.host, options.hostfile, options.command, options.commfile]
    if options.command:
        options.command = file_parse(options.command)
    if options.host:
        ini_host = HostSearch()
        options.host = ini_host.tidy_parse(options.host)
    if options.user:
        try:
            options.host = ' '.join(
                    [i if i != 'root' else options.user for i in options.host.split()])
        except:
            pass
    paradict = {'host': options.host,
                'hostfile': options.hostfile,
                'command': options.command,
                'commfile': options.commfile}
    paras = [{i:j} for i,j in paradict.items() if j]
    if options.show_clients:
        try:
            j=0
            toparalist = paradict['host'].split('\n')
            for i in toparalist:
                print str(j) + ': ' + i.split()[0]
                j = j + 1
        except:
            j=0
            toparalist = paradict['hostfile'].split('\n')
            for i in toparalist:
                print str(j) + ': ' + i.split()[0]
                j = j + 1
        for x, y in collections.Counter(toparalist).items():
            if y > 1:
                print '\033[1;40;33m'
                print "be careful! {0}'s numbers is: {1}".format(x.split()[0], str(y))
                print '\033[0m'
        sys.exit(0)
    if host_bool and comm_bool:
            print '\033[1;40;36m'
            print "choose two -H --hostfile -C --commfile together"
            print '\033[0m'
            sys.exit(1)
    if len(paras) != 2:
        TranTune.Usage()
        sys.exit()
    MyMul(paras)
    sleep(0.1)
