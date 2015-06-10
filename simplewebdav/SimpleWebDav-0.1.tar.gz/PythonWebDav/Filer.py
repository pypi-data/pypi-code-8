import os
import time
import mimetypes
import hashlib
import shutil

"""
class 'Filer' provides functions for working with the real file system
"""


class Filer(object):
    def __init__(self, folder):
        """
        Constructor input takes directories path (Those
which you used during creating server).
        """
        self.base_folder = folder

    def get_file(self, path):
        """
         It takes local path to file(With the type of struct
you created)Method must return open file.
        """
        f = self.base_folder + path
        return open(f, "rb")

    def isdir(self, path):
        """
 It takes local path to file. Method must return True
if this way point out our directory, returns False otherwise.
        """
        f = self.base_folder + path
        return os.path.isdir(f)

    def childs(self, path):
        """
         It takes path to directory (Is determined by
function isdir). Method must return list of all elements in this
directory.
        """
        f = self.base_folder+path
        return os.listdir(f)

    def get_creationdate(self, path):
        """
        It takes local path to file. Method
must return time which was taken during file creation.
        """
        f = self.base_folder+path
        return time.ctime(os.path.getctime(f))

    def get_lastmodified(self, path):
        """
         It takes local path to file. Method
must return time of last change that was made to file.
        """
        f = self.base_folder+path
        return time.ctime(os.path.getmtime(f))

    def get_name(self, path):
        """
         It takes local path to file or directory. Method
must return name of file or directory.Will be shown in file
manager.
        """
        f = self.base_folder+path
        return os.path.basename(f)

    def get_size(self, path):
        """
        It takes local path to file. Method must return
the size of it in bytes.
        """
        f = self.base_folder+path
        return str(os.path.getsize(f))

    def get_mimetype(self, path):
        """
        It takes local path to file. Returns MIMEType
of file.
        """
        f = self.base_folder+path
        return mimetypes.guess_type(f)[0]

    def get_hash(self, path):
        """
         It takes local path to file. Method must return
the hash of file.
        Example with MD5:
        """
        f = self.base_folder+path
        file = open(f, 'rb')
        m = hashlib.md5()
        while True:
            data = file.read(8000)
            if not data:
                break
            m.update(data)
        file.close()
        return m.hexdigest()

    def get_freesize(self, path):
        """
        It takes local path to directory. Method
must return the amount of free space.
        """
        f = self.base_folder+path
        return str(shutil.disk_usage(f).free)

    def create_folder(self, path):
        """
         It takes local path. Method must create
directory on it. Method doesn't return anything.
Important remark: In our directory anything could happen. Its
important that representation of your data was harmonized
with the server requests.
        """
        f = self.base_folder+path
        os.mkdir(f)

    def create_file(self, path, data, length):
        """
         It takes local path. Method
must create a file on this path and write on it files from data.
Third argument length - size of files we create. Method
doesn’t return anything.
        """
        f = self.base_folder+path
        file = open(f, "wb")
        file.write(data.read(length))
        file.close()

    def move_file(self, path_from, path_to, ov_wr):
        """
         It takes two local paths.
Must move file from path_from to path_to. ov_wr - bool
variable. If True, we overwrite file, if False - we don't. Returns
absolute path to file after moving.(Not local)
        """
        f_from = self.base_folder+path_from
        f_to = self.base_folder+path_to
        shutil.move(f_from, f_to)
        return f_to

    def copy_file(self, path_from, path_to, ov_wr):
        """
        It takes two local paths.
Must copy file from path_from to path_to. ov_wr - bool
variable, when true - we will overwrite file, when False - we
wont. Returns absolute path to file after moving.(Not local)
        """
        f_from = self.base_folder+path_from
        f_to = self.base_folder+path_to
        shutil.copy(f_from, f_to)
        return f_to

    def delete(self, path):
        """
        It takes local path to file or directory. Method
must delete file or directory on this path. Method doesn't
return anything.
        """
        f = self.base_folder+path
        if self.isdir(path):
            os.rmdir(f)
        else:
            os.remove(f)