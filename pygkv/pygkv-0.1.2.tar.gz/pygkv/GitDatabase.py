import subprocess

class Database:
    def __init__(self):
        subprocess.Popen(('git','init'), stdout=subprocess.PIPE)
        self.data = {}

    def __setitem__(self, key, value):
        hash = self.hash_object(value)
        self.data[key] = hash.strip()
	
    def __getitem__(self, key):
        hash = self.data[key]
        data = self.cat_file(hash)
        return data.strip().decode('utf-8')

    def hash_object(self, value):
        if not isinstance(value,str):
            value = str(value)
        echo = subprocess.Popen(("echo",value), stdout = subprocess.PIPE)
        output = subprocess.check_output(("git", "hash-object", "-w", "--stdin"), stdin=echo.stdout)
        return output

    def cat_file(self,hash):
        output = subprocess.Popen(("git", "cat-file", "-p", hash), stdout=subprocess.PIPE)
        return output.stdout.read()
