from PythonWebDav import VirtualFS as vfs
import os
import time
import hashlib
import shutil

"""
class 'audioFiler' provides functions for working with the virtual audio file system
"""


class AudioFiler(object):
    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, 'instance'):
            cls.instance = super(AudioFiler, cls).__new__(cls)
        return cls.instance

    def __init__(self, folder):
        if not hasattr(AudioFiler, 'instance_inited'):
            AudioFiler.instance_inited = True
            self.fs = vfs.VFolder("/")
            self.base_folder = folder
            print("Creating virtual file system...")
            self.fs.create_audio_fs(folder)
            print("Complete!")

    def get_file(self, path):
        f = self.fs.find_file(path)
        return open(f.path, "rb")

    def isdir(self, path):
        f = self.fs.find_file(path)
        return type(f) == vfs.VFolder

    def childs(self, path):
        f = self.fs.find_file(path)
        return list(map(lambda x: x.name, f.data))

    def get_creationdate(self, path):
        f = self.fs.find_file(path)
        if type(f) == vfs.VFolder:
            return time.ctime(time.time())
        return time.ctime(os.path.getctime(f.path))

    def get_lastmodified(self, path):
        f = self.fs.find_file(path)
        if type(f) == vfs.VFolder:
            return time.ctime(time.time())
        return time.ctime(os.path.getmtime(f.path))

    def get_name(self, path):
        f = self.fs.find_file(path)
        return f.name

    def get_size(self, path):
        f = self.fs.find_file(path)
        if type(f) == vfs.VFolder:
            return str(10**5)
        return str(os.path.getsize(f.path))

    def get_mimetype(self, path):
        f = self.fs.find_file(path)
        if type(f) == vfs.vfile:
            return 'audio/mpeg'

    def get_hash(self, path):
        f = self.fs.find_file(path)
        if type(f) == vfs.vfile:
            file = open(f.path, 'rb')
            m = hashlib.md5()
            while True:
                data = file.read(8000)
                if not data:
                    break
                m.update(data)
            file.close()
            return m.hexdigest()

    def getsize(self, path):
        f = self.fs.find_file(path)
        if type(f) == vfs.VFolder:
            return str(10**5)
        return str(os.path.getsize(f.path))

    def getfreesize(self, path):
        return str(10**5)

    def create_folder(self, path):
        f = self.base_folder+path
        os.mkdir(f)

    def create_file(self, path, data, length):
        f = self.base_folder+"/"+path.split("/")[-1]
        file = open(f, "wb")
        file.write(data.read(length))
        new_art, new_alb = (path.split("/") + ["", ""])[1:3]
        if new_art != "":
            self.fs.change_data(f, artist=new_art)
        if new_alb != "":
            self.fs.change_data(f, album=new_alb)
        self.fs.add_file(f)
        print(new_alb, new_art)
        file.close()

    def move_file(self, path_from, path_to, ov_wr):
        f_from = self.base_folder+path_from
        f_to = self.base_folder+path_to
        shutil.move(f_from, f_to)
        return f_to

    def copy_file(self, path_from, path_to, ov_wr):
        f_from = self.base_folder+path_from
        f_to = self.base_folder+path_to
        shutil.copy(f_from, f_to)
        return f_to

    def delete(self, path):
        f = self.fs.find_file(path)
        if self.fs.is_unknown(path):
            os.remove(f.path)
        else:
            self.fs.change_data(f.path, artist="Unknow Artist", album="Unknow Album")
            self.fs.delete_file(path)
