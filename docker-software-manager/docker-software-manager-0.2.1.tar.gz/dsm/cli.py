#!/usr/bin/python

import sys
import argparse
import os
import shutil
import subprocess
import pipes
import datetime
from string import Template
from ConfigParser import SafeConfigParser

class dsm():
    def __init__(self):
        # path of this script
        self.basepath = os.path.dirname(os.path.realpath(__file__))

        # read config file
        self.config = SafeConfigParser()
        self.config.readfp(open(os.path.join(self.basepath, 'defaults.conf')))
        self.configpath = '/etc/docker-software-manager/'
        self.config.read(os.path.join(self.configpath,'docker-software-manager.conf'))

        # further paths
        if os.path.isabs(self.config.get('main', 'basepath')):
            self.softwarepath = os.path.join(self.config.get('main', 'basepath'), 'software')
        else:
            self.softwarepath = os.path.join(self.basepath, self.config.get('main', 'basepath'), 'software')
        #self.composepath = os.path.join(self.basepath, 'docker-compose/docker-compose')
        
    # helpers
    def getTarget(self, name):
        return os.path.normpath(os.path.join(self.softwarepath, name))

    def isExisting(self, target):
        # check if software exists
        return os.path.exists(target)

    # subcommand install
    def install(self, args):
        print "Installing tools"
        
        # install docker-gen
        print "[    ] Installing docker-gen",
        subprocess.call([os.path.join(self.basepath, 'docker-gen/update.sh')])
        subprocess.call([os.path.join(self.basepath, 'docker-gen/install.sh')])
        subprocess.call(['systemctl', 'enable', os.path.join(self.basepath, 'docker-gen/docker-gen-nginx.service')])
        print "\r[done] Installing docker-gen"
        
        ## install config files
        print "[    ] Installing config files"
        if not os.path.isdir(self.configpath):
            os.makedirs(self.configpath)
        if not os.path.exists(os.path.join(self.configpath, 'docker-software-manager.conf')):
            subprocess.call(['cp', os.path.join(self.basepath, 'defaults.conf'), os.path.join(self.configpath, 'docker-software-manager.conf')])
        else:
            print "docker-software-manager.tmpl allready exists."
            print "You can find the default version at {0}".format(os.path.join(self.basepath, 'defaults.conf'))
        if not os.path.exists(os.path.join(self.configpath, 'nginx.tmpl')):
            subprocess.call(['cp', os.path.join(self.basepath, 'docker-gen/nginx.tmpl'), os.path.join(self.configpath, 'nginx.tmpl')])
        else:
            print "nginx.tmpl allready exists."
            print "You can find the default version at {0}".format(os.path.join(self.basepath, 'docker-gen/nginx.tmpl'))
        print "[done] Installing config files"
        
        print "Creating software directory"
        if not os.path.isdir(self.softwarepath):
            os.makedirs(self.softwarepath)

    #subcommand remove
    def remove(self, args):
        print "Removing installed tools"
        
        # remove docker-gen
        print "[    ] Removing docker-gen",
        subprocess.call([os.path.join(self.basepath, 'docker-gen/remove.sh')])
        subprocess.call(['systemctl', 'disable', os.path.join(self.basepath, 'docker-gen/docker-gen-nginx.service')])
        print "\r[done] Removing docker-gen"
        
        print "Not removing config directory!"
        print "Run `rm -r {0}` to remove it, but pay attenuation: this will erase config!".format(self.configpath)
        
        print "Not removing software directory!"
        print "Run `rm -r {0}` to remove it, but pay attenuation: this will erase data!".format(self.softwarepath)

    #subcommand list
    def ls(self, args):
        if os.path.isdir(self.softwarepath):
            software_list = [x for x in os.listdir(self.softwarepath) if os.path.isdir(os.path.join(self.softwarepath, x))]
            
            if len(software_list):
                print "Existing software:"
                for x in software_list:
                    print "- {0}".format(x)
            else:
                print "No software existing!"
        else:
            print "Software directory does not exist! Please run `dsm install` first."

    #subcommand create
    def create(self, args):
        target = self.getTarget(args.name)
        
        # check if software exists allready
        if self.isExisting(target):
            print "Software allready exists!"
            return
        
        # create git repository
        print "[    ] Initiating git repository",
        subprocess.call(['git', 'init', target])
        print "\r[done] Initiating git repository"
        
        # copy software template to software directory
        print "[    ] Copying software template",
        # shutil.copytree(os.path.join(basepath, 'software-template/'), target) # problem with base dirctory
        for x in os.listdir(os.path.join(self.basepath, 'software-template/')):
            src = os.path.join(os.path.join(self.basepath, 'software-template/'), x)
            dest = os.path.join(target, x)
            if os.path.isdir(src):
                shutil.copytree(src, dest)
            else:
                shutil.copy2(src, dest)
        print "\r[done] Copying software template"
        
        # modify files with software name
        print "[    ] Modifying software template",
        with open(os.path.join(target, 'software.service'), "r+") as f:
            string = f.read() # read in file
            f.seek(0) # go back to start
            f.truncate() # clear file
            f.write(Template(string).substitute(name=args.name)) # write everything back
            f.close()
        
        with open(os.path.join(target, 'docker-compose.yml'), "r+") as f:
            string = f.read() # read in file
            f.seek(0) # go back to start
            f.truncate() # clear file
            f.write(Template(string).substitute(name=args.name)) # write everything back
            f.close()
            
        os.rename(os.path.join(target, 'software.service'), os.path.join(target, "{0}.service".format(args.name)))
        print "\r[done] Modifying software template"
            
        # do initial commit
        print "[    ] Doing initial commit",
        subprocess.call(['git', '-C', target, 'add', '--all'])
        subprocess.call(['git', '-C', target, 'commit', '-m', 'Initial commit'])
        print "\r[done] Doing initial commit"
        
        print "Software directory \"{0}\" created".format(args.name)

    #subcommand activate
    def activate(self, args):
        target = self.getTarget(args.name)
        
        # check if software exists
        if self.isExisting(target):
            command = ['systemctl', 'enable', pipes.quote(os.path.join(target, "{0}.service".format(args.name)))]
            subprocess.call(command)
        else:
            print "Software does not exist!"

    #subcommand deactivate
    def deactivate(self, args):
        target = self.getTarget(args.name)
        
        # check if software exists
        if self.isExisting(target):
            command = ['systemctl', 'disable', pipes.quote(os.path.join(target, "{0}.service".format(args.name)))]
            subprocess.call(command)
        else:
            print "Software does not exist!"

    #subcommand start
    def start(self, args):
        target = self.getTarget(args.name)
        
        # check if software exists
        if self.isExisting(target):
            command = ['systemctl', 'start', "{0}.service".format(args.name)]
            subprocess.call(command)
        else:
            print "Software does not exist!"

    #subcommand stop
    def stop(self, args):
        target = self.getTarget(args.name)
        
        # check if software exists
        if self.isExisting(target):
            command = ['systemctl', 'stop', "{0}.service".format(args.name)]
            subprocess.call(command)
        else:
            print "Software does not exist!"

    #subcommand status
    def status(self, args):
        target = self.getTarget(args.name)
        
        # check if software exists
        if self.isExisting(target):
            print "systemd status:"
            command = ['systemctl', 'status', "{0}.service".format(args.name)]
            subprocess.call(command)
        else:
            print "Software does not exist!"

    #subcommand ps
    def ps(self, args):
        target = self.getTarget(args.name)
        
        # check if software exists
        if self.isExisting(target):
            command = ['docker-compose', '-f', pipes.quote(os.path.join(target, "docker-compose.yml")), '-p', args.name, 'ps']
            subprocess.call(command)
        else:
            print "Software does not exist!"

    #subcommand kill
    def kill(self, args):
        target = self.getTarget(args.name)
        
        # check if software exists
        if self.isExisting(target):
            command = ['docker-compose', '-f', pipes.quote(os.path.join(target, "docker-compose.yml")), '-p', args.name, 'kill']
            subprocess.call(command)
        else:
            print "Software does not exist!"
            
    #subcommand rm
    def rm(self, args):
        target = self.getTarget(args.name)
        
        # check if software exists
        if self.isExisting(target):
            command = ['docker-compose', '-f', pipes.quote(os.path.join(target, "docker-compose.yml")), '-p', args.name, 'rm']
            subprocess.call(command)
        else:
            print "Software does not exist!"

    #subcommand logs
    def logs(self, args):
        target = self.getTarget(args.name)
        
        # check if software exists
        if self.isExisting(target):
            command = ['docker-compose', '-f', pipes.quote(os.path.join(target, "docker-compose.yml")), '-p', args.name, 'logs']
            process = subprocess.Popen(command, stdin=subprocess.PIPE)
            process.communicate()
        else:
            print "Software does not exist!"

    #subcommand edit
    def edit(self, args):
        target = self.getTarget(args.name)
        
        # check if software exists
        if self.isExisting(target):
            editor = self.config.get('main', 'editor')
            command = [editor, pipes.quote(os.path.join(target, "docker-compose.yml"))]
            subprocess.call(command)
        else:
            print "Software does not exist!"

    #subcommand backup
    def backup(self, args):
        target = self.getTarget(args.name)
        
        # check if software exists
        if self.isExisting(target):
            filename = os.path.join(target, 'backups/', "{0}-{1}.tar.gz".format(args.name, datetime.datetime.now().strftime("%Y%m%d-%H%M%S")))
            command = ['tar', '-zc', '-f', filename, '-C', target, '.', '--exclude=backups']
            subprocess.call(command)
        else:
            print "Software does not exist!"
        
    def run(self):      
        # define argument parser
        parser = argparse.ArgumentParser(description="Docker software manager")
        subparsers = parser.add_subparsers()

        #subcommand install  
        parser_install = subparsers.add_parser('install')
        parser_install.set_defaults(func=self.install)
            
        # subcommand remove
        parser_remove = subparsers.add_parser('remove')
        parser_remove.set_defaults(func=self.remove)

        # subcommand list
        parser_list = subparsers.add_parser('list')
        parser_list.set_defaults(func=self.ls)

        # subcommand create
        parser_create = subparsers.add_parser('create')
        parser_create.add_argument("name",
                            help="name of the software", metavar='name')
        parser_create.set_defaults(func=self.create)
            
        # subcommand activate
        parser_activate = subparsers.add_parser('activate')
        parser_activate.add_argument("name",
                            help="name of the software", metavar='name')
        parser_activate.set_defaults(func=self.activate)

        # subcommand deactivate        
        parser_deactivate = subparsers.add_parser('deactivate')
        parser_deactivate.add_argument("name",
                            help="name of the software", metavar='name')
        parser_deactivate.set_defaults(func=self.deactivate)
           
        # subcommand start
        parser_start = subparsers.add_parser('start')
        parser_start.add_argument("name",
                            help="name of the software", metavar='name')
        parser_start.set_defaults(func=self.start)
                
        # subcommand stop
        parser_stop = subparsers.add_parser('stop')
        parser_stop.add_argument("name",
                            help="name of the software", metavar='name')
        parser_stop.set_defaults(func=self.stop)
                
        # subcommand status
        parser_status = subparsers.add_parser('status')
        parser_status.add_argument("name",
                            help="name of the software", metavar='name')
        parser_status.set_defaults(func=self.status)
                
        # subcommand ps
        parser_ps = subparsers.add_parser('ps')
        parser_ps.add_argument("name",
                            help="name of the software", metavar='name')
        parser_ps.set_defaults(func=self.ps)
        
        # subcommand kill
        parser_kill = subparsers.add_parser('kill')
        parser_kill.add_argument("name",
                            help="name of the software", metavar='name')
        parser_kill.set_defaults(func=self.kill)
        
        # subcommand rm
        parser_rm = subparsers.add_parser('rm')
        parser_rm.add_argument("name",
                            help="name of the software", metavar='name')
        parser_rm.set_defaults(func=self.rm)
                
        # subcommand logs
        parser_logs = subparsers.add_parser('logs')
        parser_logs.add_argument("name",
                            help="name of the software", metavar='name')
        parser_logs.set_defaults(func=self.logs)

        # subcommand edit
        parser_edit = subparsers.add_parser('edit')
        parser_edit.add_argument("name",
                            help="name of the software", metavar='name')
        parser_edit.set_defaults(func=self.edit)

        # subcommand backup
        parser_backup = subparsers.add_parser('backup')
        parser_backup.add_argument("name",
                            help="name of the software", metavar='name')
        parser_backup.set_defaults(func=self.backup)

        # parse given arguments
        args = parser.parse_args()
        args.func(args)

def main():
    app = dsm()
    app.run()
    
if __name__ == "__main__":
    main()
