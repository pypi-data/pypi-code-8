from constructor import Infrastructure
import os
import imp
import argparse
import subprocess
from AWS import AWS

def main():
    parser = argparse.ArgumentParser(description='Constructor')

    parser.add_argument('--init', action="store_true", default=False)
    parser.add_argument('--env', type=str, help='Environment to launch in.', default='dev')

    args = parser.parse_args()

    aws = AWS(args.env)

    if args.init:
        aws.run_with_shell('configure')
        groups = aws.run('ec2', 'describe-security-groups')['SecurityGroups']
        groups = [item for item in groups if item['GroupName'] == 'web-server']
        if len(groups) == 0:
            aws.run(
                'ec2', 'create-security-group',
                '--group-name', 'web-server',
                '--description', 'Generic web server with SSH access'
            )

            aws.run(
                'ec2', 'authorize-security-group-ingress',
                '--group-name', 'web-server',
                '--protocol', 'tcp',
                '--port', '22',
                '--cidr', '0.0.0.0/0'
            )

            aws.run(
                'ec2', 'authorize-security-group-ingress',
                '--group-name', 'web-server',
                '--protocol', 'tcp',
                '--port', '80',
                '--cidr', '0.0.0.0/0'
            )

            aws.run(
                'ec2', 'authorize-security-group-ingress',
                '--group-name', 'web-server',
                '--protocol', 'tcp',
                '--port', '443',
                '--cidr', '0.0.0.0/0'
            )

            subprocess.call('mkdir -p ~/.constructor', shell=True)
            subprocess.call(
                'aws ec2 create-key-pair --key-name dev --query \'KeyMaterial\' --output text --profile dev > ~/.constructor/' + args.env + '.pem', shell=True
            )
            subprocess.call('chmod 400 ~/.constructor/' + args.env + '.pem', shell=True)

            if os.path.isfile(os.path.expanduser('~/.constructor/id_rsa')):
                subprocess.call('ssh-keygen -f ~/.constructor/id_rsa -t rsa -P \'\'', shell=True)
                print "Run: cat ~/.constructor/id_rsa.pub | pbcopy"
                print "And add your key to your git hosting."
    else:
        infrastructure = Infrastructure(environment=args.env)
        blueprint = imp.load_source('blueprint', 'blueprint.py')
        blueprint.build(infrastructure)