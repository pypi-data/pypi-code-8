import subprocess
import json

class AWS(object):
    def __init__(self, env):
        self.env = env

    def run_with_shell(self, command):
        subprocess.call('aws ' + command + ' --profile ' + self.env, shell=True)

    def run(self, *args):
        args = list(args)
        args.insert(0, 'aws')
        args.append('--output')
        args.append('json')
        args.append('--profile')
        args.append(self.env)

        data = subprocess.check_output(args)

        if len(data) == 0:
            return None

        return json.loads(data)