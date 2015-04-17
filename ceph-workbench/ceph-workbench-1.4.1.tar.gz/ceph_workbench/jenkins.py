# -*- mode: python; coding: utf-8 -*-
#
# Copyright (C) 2015 <contact@redhat.com>
#
# Author: Loic Dachary <loic@dachary.org>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see `<http://www.gnu.org/licenses/>`.
#
import argparse
import grp
import json
import logging
import os
import re
import requests
import subprocess

from ceph_workbench import util


class Jenkins:

    def __init__(self, args):
        self.args = args
        self.args.port_range = 3000
        self.args.jenkins_slave = 'ceph-jenkins-slave'
        self.args.libguestfs = 'libguestfs'

    def run(self):
        if self.args.publish_build_to_pull_request:
            return self.publish_build_to_pull_request()
        elif self.args.jenkins_make_check_bot:
            return subprocess.call([self.args.libdir +
                                    '/jenkins-make-check-bot'])
        elif self.args.jenkins_docker_run_slave:
            return self.docker_run_slave(self.args.jenkins_docker_run_slave)
        elif self.args.jenkins_docker_destroy_slave:
            return self.docker_destroy_slave(
                self.args.jenkins_docker_destroy_slave)

    @staticmethod
    def get_parser():
        parser = argparse.ArgumentParser(
            description="Jenkins",
            conflict_handler='resolve',
        )
        parser.add_argument('--jenkins-docker-run-slave',
                            help=('run the jenkins slave in docker and '
                                  'register it to the jenkins master'))
        parser.add_argument('--jenkins-make-check-bot',
                            help='run the jenkins-make-check-bot helper')
        parser.add_argument('--publish-build-to-pull-request',
                            help='add a comment to pull request XXX')
        parser.add_argument('--jenkins-git-branch',
                            help=('only for --publish-build-to-pull-request, '
                                  'force the GIT_BRANCH value'))
        parser.add_argument('--jenkins-url',
                            help='URL of the jenkins server')
        parser.add_argument('--jenkins-ssh-host',
                            help='jenkins host name for ssh protocol')
        parser.add_argument('--jenkins-ssh-port',
                            help='jenkins port for ssh protocol')
        parser.add_argument('--jenkins-ssh-key',
                            help='jenkins ssh private key')
        parser.add_argument('--jenkins-user',
                            help='jenkins user name for API authentication')
        parser.add_argument('--jenkins-password',
                            help='jenkins password for API authentication')
        parser.add_argument('--github-repo',
                            help='GitHub repo (for instance ceph/ceph)')
        parser.add_argument('--github-token',
                            help='GitHub authentication token')
        parser.add_argument('--libdir',
                            help='directory containing helpers programs')
        parser.add_argument('--datadir',
                            help='directory for persistent data')
        return parser

    @staticmethod
    def factory(argv):
        return Jenkins(Jenkins.get_parser().parse_args(argv))

    def publish_build_to_pull_request(self):
        r = requests.get(self.args.jenkins_url + '/' +
                         self.args.publish_build_to_pull_request + '/api/json')
        r.raise_for_status()
        report = r.json()
        logging.debug("publish_build_to_pull_request: downstream " +
                      str(report))
        for action in report['actions']:
            if "causes" in action:
                cause = action['causes'][0]
                upstream = (cause['upstreamUrl'] + '/' +
                            str(cause['upstreamBuild']))
        r = requests.get(self.args.jenkins_url + '/' + upstream + '/api/json')
        r.raise_for_status()
        report = r.json()
        logging.debug("publish_build_to_pull_request: upstream " + str(report))
        if self.args.jenkins_git_branch:
            branch_name = self.args.jenkins_git_branch
        else:
            for action in report['actions']:
                if "lastBuiltRevision" in action:
                    branch = action["lastBuiltRevision"]["branch"][0]
                    branch_name = branch['name']
        runs = {}
        for run in report['runs']:
            if run['number'] == report['number']:
                r = requests.get(run['url'] + 'api/json')
                r.raise_for_status()
                runs[run['url']] = r.json()['result']
        body = report['result'] + ": " + report['url'] + "\n"
        for url in sorted(runs):
            body += "* " + runs[url] + " " + url + "\n"
        logging.debug("publish_build_to_pull_request: " + body)
        if 'pull/' in branch_name:
            (pr,) = re.findall('\d+$', branch_name)
            payload = {'body': body}
            r = requests.post('https://api.github.com/repos/' +
                              self.args.github_repo + '/issues/' +
                              pr + '/comments?access_token=' +
                              self.args.github_token,
                              data=json.dumps(payload))
            r.raise_for_status()
            return r.json()['body']
        else:
            return body

    def run_cli(self, *args, **kwargs):
        jar = '/tmp/jenkins-cli.jar'
        if not os.path.exists(jar):
            r = requests.get(self.args.jenkins_url +
                             '/jnlpJars/jenkins-cli.jar')
            with open(jar, 'wb') as fd:
                for chunk in r.iter_content(4096):
                    fd.write(chunk)
        cmd = ['java', '-jar', jar, '-s', self.args.jenkins_url] + list(args)
        s = subprocess.Popen(cmd,
                             stdin=subprocess.PIPE,
                             stdout=subprocess.PIPE,
                             stderr=subprocess.PIPE)
        if 'payload' in kwargs:
            payload = kwargs['payload'].encode('utf-8')
        else:
            payload = None
        (stdoutdata, stderrdata) = s.communicate(input=payload)
        stdoutdata = stdoutdata.decode('utf-8')
        stderrdata = stderrdata.decode('utf-8')
        logging.debug(" ".join(cmd) + ":" +
                      " stdout " + stdoutdata +
                      " stderr " + stderrdata)
        return stdoutdata + stderrdata

    def master_port(self, name):
        (number,) = re.findall('(\d+)$', name)
        return str(self.args.port_range + int(number))

    def slave_port(self, name):
        (number,) = re.findall('(\d+)$', name)
        return str(4000 + int(number))

    def find_node(self, name):
        r = requests.get(self.args.jenkins_url + '/computer/api/json')
        r.raise_for_status()
        return name in map(lambda x: x['displayName'], r.json()['computer'])

    def destroy_node(self, name):
        if self.find_node(name):
            self.run_cli("delete-node", name)

    def next_node_name(self):
        r = requests.get(self.args.jenkins_url + '/computer/api/json')
        r.raise_for_status()
        nodes = r.json()['computer']
        highest = 0
        for node in nodes:
            name_with_number = re.findall('(\d+)$', node['displayName'])
            if name_with_number:
                highest = max(highest, int(name_with_number[0]))
        highest += 1
        return "slave%03d" % highest

    def create_node(self, name):
        # assume the master is running in docker and slaves are accessed
        # via a ssh tunel open on the docker host
        credentials = self.slave_credential_id()
        port = self.master_port(name)
        payload = """
<?xml version="1.0" encoding="UTF-8"?>
<slave>
  <name>{name}</name>
  <description></description>
  <remoteFS>/home/ubuntu</remoteFS>
  <numExecutors>1</numExecutors>
  <mode>NORMAL</mode>
  <retentionStrategy class="hudson.slaves.RetentionStrategy$Always"/>
  <launcher class="hudson.plugins.sshslaves.SSHLauncher"
       plugin="ssh-slaves@1.9">
    <host>localhost</host>
    <port>{port}</port>
    <credentialsId>{credentials}</credentialsId>
    <maxNumRetries>0</maxNumRetries>
    <retryWaitTime>0</retryWaitTime>
  </launcher>
  <label>docker ceph-workbench</label>
  <nodeProperties/>
  <userId>admin</userId>
</slave>
""".format(port=port,
           name=name,
           credentials=credentials)
        logging.debug('create_node: ' + name + ' ' + payload)
        self.run_cli('create-node', name, payload=payload)
        r = requests.get(self.args.jenkins_url +
                         '/computer/' + name + '/api/json')
        r.raise_for_status()
        return r.json()

    def slave_credential_id(self):
        auth = (self.args.jenkins_user, self.args.jenkins_password)
        r = requests.get(self.args.jenkins_url +
                         '/credential-store/domain/_/api/json',
                         auth=auth)
        r.raise_for_status()
        slave_description = 'for jenkins slaves'
        credentials = {}
        for credential in list(r.json()['credentials']):
            c = requests.get(self.args.jenkins_url +
                             ('/credential-store/domain/_/credential/' +
                              credential + '/api/json'),
                             auth=auth)
            c.raise_for_status()
            credentials[c.json()['description']] = credential

        if slave_description in credentials:
            return credentials[slave_description]
        else:
            raise Exception('no "' + slave_description + '" credential in ' +
                            str(credentials))

    def docker_build_slave(self):
        if self.args.jenkins_slave not in util.sh('docker images'):
            util.sh('docker build -t ' + self.args.jenkins_slave + " " +
                    self.args.libdir + '/jenkins-slave-docker')
            return True
        return False

    def docker_build_libguestfs(self):
        if self.args.libguestfs not in util.sh('docker images'):
            util.sh('docker build -t ' + self.args.libguestfs + " " +
                    self.args.libdir + '/libguestfs-docker')
            return True
        return False

    def prepare_qemu_img(self, os_type, os_version, arch):
        self.docker_build_libguestfs()
        libdir = os.path.abspath(self.args.libdir)
        util.sh('docker run --rm ' +
                ' -v $(pwd):$(pwd) ' +
                ' -v ' + libdir + ':' + libdir +
                ' -w $(pwd) ' +
                ' --user ' + str(os.getuid()) + ' ' +
                self.args.libguestfs + ' ' + libdir + '/' +
                'create-qemu-img ' + os_type + ' ' + os_version + ' ' + arch)
        return True

    def docker_destroy_slave(self, name):
        util.sh('docker stop ' + name + ' || true')
        util.sh('docker rm ' + name + ' || true')
        return self.destroy_node(name)

    def docker_run_slave(self, name):
        if name == 'new':
            name = self.next_node_name()
            self.create_node(name)
        self.docker_build_slave()
        slave_port = self.slave_port(name)
        datadir = os.path.abspath(self.args.datadir) + '/' + name
        if not os.path.exists(datadir):
            os.makedirs(datadir, 0o755)
        master_port = self.master_port(name)
        known_hosts = ('-o UserKnownHostsFile=/dev/null '
                       '-o StrictHostKeyChecking=no ')
        script = """
#!/bin/bash
chown -R jenkins /home/jenkins
groupmod --gid {docker_group_id} docker
ssh {known_hosts} -f -N -R {port}:localhost:22 {host}
/usr/sbin/sshd -D -E /var/log/auth.log
""".format(port=master_port,
           host=self.args.jenkins_ssh_host,
           known_hosts=known_hosts,
           docker_group_id=grp.getgrnam('docker').gr_gid)
        open(datadir + '/setup.sh', 'w').write(script)
        dotssh = datadir + '/.ssh'
        if not os.path.exists(dotssh):
            os.mkdir(dotssh, 0o755)
            if self.args.jenkins_ssh_key:
                key = '-i ' + self.args.jenkins_ssh_key + ' '
            else:
                key = ''
            if self.args.jenkins_ssh_port:
                port = '-P ' + self.args.jenkins_ssh_port + ' '
            else:
                port = ''
            util.sh('scp ' + known_hosts + key + port +
                    self.args.jenkins_ssh_host +
                    ':/var/jenkins_home/.ssh/id_rsa* ' +
                    dotssh)
            util.sh('cp ' +
                    dotssh + '/id_rsa.pub ' +
                    dotssh + '/authorized_keys')
        util.sh('docker stop ' + name + ' || true')
        util.sh('docker rm ' + name + ' || true')
        util.sh('docker run -d --name ' + name + ' ' +
                ' -p ' + slave_port + ':22 ' +
                ' -v ' + datadir + ':/home/jenkins ' +
                ' -v /var/run/docker.sock:/run/docker.sock ' +
                self.args.jenkins_slave + ' ' +
                ' bash /home/jenkins/setup-ssh.sh')
        return name
