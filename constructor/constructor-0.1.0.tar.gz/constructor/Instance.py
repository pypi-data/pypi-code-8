import os
import subprocess

from SymfonyProject import SymfonyProject
from LocalMysql import LocalMysql

BLUEPRINTS_DIRECTORY = '~/.constructor'

class Instance(object):

    def __init__(self, infrastructure, id, instance_dns, pem_file):
        self.id = id
        self.infrastructure = infrastructure
        self.instance_dns = instance_dns
        self.pem_file = pem_file

    def add_security_group(self, group):
        info = self.infrastructure.aws(
            'ec2', 'describe-instance-attribute',
            '--attribute', 'groupSet',
            '--instance-id', self.id
        )
        group_ids = [item['GroupId'] for item in info['Groups']]
        group_ids.append(group.id)

        self.infrastructure.aws(
            *([
                'ec2', 'modify-instance-attribute',
                '--instance-id', self.id,
                '--groups'
            ] + group_ids)
        )

    def provision(self):
        RSA_KEY = os.path.expanduser(BLUEPRINTS_DIRECTORY + '/id_rsa')
        self.upload_file(RSA_KEY, '~/.ssh/id_rsa')
        self.upload_file(os.path.dirname(__file__) + '/20auto-upgrades', '~/20auto-upgrades')
        self.run_commands(
            'sudo apt-get update',
            'sudo apt-get install unattended-upgrades',
            'sudo mv 20auto-upgrades /etc/apt/apt.conf.d/20auto-upgrades',
            'sudo service unattended-upgrades restart',
            'sudo mkdir -p /opt/apps; sudo chown ubuntu:ubuntu /opt/apps/',
            'ssh-keyscan github.com >> ~/.ssh/known_hosts'
        )

    def setup_generic_php(self, post_max_size='50M', upload_max_filesize='50M', max_file_uploads='50'):
        self.run_commands(
            'sudo apt-get update',
            'sudo apt-get install --assume-yes git-core nginx php5-fpm php5-cli php5-curl php5-mysql php5-redis',
            'curl -sS https://getcomposer.org/installer | php',
            'sudo mv composer.phar /usr/local/bin/composer',
            "sudo sed -i -e 's/post_max_size = [0-9]*M/post_max_size = " + post_max_size + "/g' /etc/php5/fpm/php.ini",
            "sudo sed -i -e 's/upload_max_filesize = [0-9]*M/upload_max_filesize = " + upload_max_filesize + "/g' /etc/php5/fpm/php.ini",
            "sudo sed -i -e 's/max_file_uploads = [0-9]*/max_file_uploads = " + max_file_uploads + "/g' /etc/php5/fpm/php.ini",
            "sudo sh -c \"printf '\\nslowlog = /var/log/php5-fpm-\\$pool.log.slow\\n' >> /etc/php5/fpm/pool.d/www.conf\"",
            "sudo sh -c \"printf '\\nrequest_slowlog_timeout = 30s\\n' >> /etc/php5/fpm/pool.d/www.conf\"",
            "sudo sh -c \"printf '\\ncatch_workers_output = yes\\n' >> /etc/php5/fpm/pool.d/www.conf\"",
            "sudo sed -i -e 's/pm.max_children = [0-9]*/pm.max_children = 100/g' /etc/php5/fpm/pool.d/www.conf",
            "sudo service php5-fpm restart",
            "sudo chmod 0644 /var/log/php5-fpm*"
        )

    def install(self, *packages):
        self.run_command(
            'sudo apt-get install --assume-yes ' + ' '.join(packages)
        )

    def install_node(self):
        self.run_commands(
            'sudo apt-get install --assume-yes nodejs npm',
            'sudo ln -s /usr/bin/nodejs /usr/bin/node'
        )

    def install_redis(self):
        self.run_command('sudo apt-get install --assume-yes redis-server')

    def create_mysql(self, password):
        self.run_commands(
            "sudo debconf-set-selections <<< 'mysql-server mysql-server/root_password password " + password + "'",
            "sudo debconf-set-selections <<< 'mysql-server mysql-server/root_password_again password " + password + "'",
            "sudo apt-get -y install mysql-server"
        )
        return LocalMysql(instance=self, password=password)

    def use_redis_php_sessions(self, host='localhost', port=6379):
        self.run_commands(
            "sudo sed -i -e 's/^session.save_handler = files/session.save_handler = redis/g' /etc/php5/fpm/php.ini",
            "sudo sh -c \"printf '\\nsession.save_path = \\\"tcp://" + host + ":" + str(port) + "?weight=1\\\"\\n' >> /etc/php5/fpm/php.ini\"",
            "sudo sed -i -e 's/^session.cookie_lifetime = 0/session.cookie_lifetime = 2764800/g' /etc/php5/fpm/php.ini",
            "sudo sed -i -e 's/^session.gc_maxlifetime = 1440/session.gc_maxlifetime = 2764800/g' /etc/php5/fpm/php.ini",
        )

    def install_bower(self):
        self.run_commands(
            'sudo npm install bower -g',
            'sudo rm -fr /home/ubuntu/tmp',
            'sudo rm -fr /home/ubuntu/.npm'
        )

    def install_grunt(self):
        self.run_commands(
            'sudo npm install grunt-cli -g',
            'sudo rm -fr /home/ubuntu/tmp',
            'sudo rm -fr /home/ubuntu/.npm'
        )

    def install_gulp(self):
        self.run_commands(
            'sudo npm install gulp -g',
            'sudo rm -fr /home/ubuntu/tmp',
            'sudo rm -fr /home/ubuntu/.npm'
        )

    def install_my_key(self):
        self.upload_file(os.path.expanduser('~/.ssh/id_rsa.pub'), '~/id_rsa.pub')
        self.run_commands(
            'cat ~/id_rsa.pub >> ~/.ssh/authorized_keys',
            'rm ~/id_rsa.pub'
        )
        print "Instance ready, use the following command to SSH in:"
        print ' '.join(['ssh', 'ubuntu@' + self.instance_dns])

    def clone_symfony_project(self, repo):
        self.clone_project(repo)
        return SymfonyProject(self, '/opt/apps/' + repo.split('/')[-1])

    def clone_project(self, repo):
        self.run_command('cd /opt/apps; git clone ' + repo)

    def use_nginx_config(self, file):
        self.upload_file(file, '~/default.conf')
        self.run_command('sudo mv ~/default.conf /etc/nginx/sites-available/default')
        self.run_command('sudo service nginx restart')

    def run_script(self, script):
        print "Running script: " + script
        scriptname = os.path.basename(script)
        self.upload_file(script, destination = '~/' + scriptname)
        self.run_command('~/' + scriptname)
        self.run_command('rm ~/' + scriptname)

    def upload_file(self, file, destination = None):
        if destination is None:
            destination = '~/' + file

        try:
            print subprocess.check_output(['scp', '-i', self.pem_file, file, 'ubuntu@' + self.instance_dns + ':' + destination], stderr=subprocess.STDOUT)
        except subprocess.CalledProcessError as e:
            print 'Error:'
            print e.output
            raise e

    def run_commands(self, *commands):
        return self.run_command(";".join(commands))

    def run_command(self, command):
        print "Run command: " + command
        print subprocess.check_output(['ssh', '-i', self.pem_file, 'ubuntu@' + self.instance_dns, command], stderr=subprocess.STDOUT)

    def get_ssh_command(self):
        return ' '.join(['ssh', '-i', self.pem_file, 'ubuntu@' + self.instance_dns])