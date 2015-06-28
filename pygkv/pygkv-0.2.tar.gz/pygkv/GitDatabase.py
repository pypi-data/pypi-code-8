import subprocess
import yaml

class Database:
    def __init__(self):
        subprocess.Popen(('git','init'), stdout=subprocess.PIPE)
        self.data = {}

    def __setitem__(self, key, value):
        hash = self.hash_object(yaml.dump(value))
        self.data[key] = hash.strip()
	
    def __getitem__(self, key):
        hash = self.data[key]
        data = self.cat_file(hash)
        return yaml.load(data)

    def hash_object(self, value):
        echo = subprocess.Popen(("echo",value), stdout = subprocess.PIPE)
        output = subprocess.check_output(("git", "hash-object", "-w", "--stdin"), stdin=echo.stdout)
        return output

    def cat_file(self,hash):
        output = subprocess.Popen(("git", "cat-file", "-p", hash), stdout=subprocess.PIPE)
        return output.stdout.read()
