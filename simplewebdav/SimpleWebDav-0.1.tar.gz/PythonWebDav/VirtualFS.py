import os
from mutagen.mp3 import MP3
from mutagen.easyid3 import EasyID3


class VFile(object):
    def __init__(self, filepath, name):
        self.path = filepath
        self.name = name

    def update_artist(self, newart):
        audio = MP3(self.path, ID3=EasyID3)
        audio["artist"] = newart
        audio.save()

    def update_album(self, newalb):
        audio = MP3(self.path, ID3=EasyID3)
        audio["album"] = newalb
        audio.save()


class VFolder(object):
    def __init__(self, name):
        self.name = name
        self.data = []

    def add(self, file):
        self.data.append(file)

    def delete(self, file):
        self.data.remove(file)

    def add_file(self, path):
        audio = MP3(path)
        artist, album, name = "", "", ""
        try:
            artist = audio["TPE1"].text[0]
        except:
            artist = "Unknow Artist"
        try:
            album = audio["TALB"].text[0]
        except:
            album = "Unknow Album"
        try:
            name = audio["TIT2"].text[0] + ".mp3"
        except:
            name = os.path.basename(path)
        audio_file = VFile(path, name)
        for art in self.data:
            if art.name == artist:
                for alb in art.data:
                    if alb.name == album:
                        alb.add(audio_file)
                        return
                new_album = VFolder(album)
                new_album.add(audio_file)
                art.add(new_album)
                return
        new_artist = VFolder(artist)
        new_album = VFolder(album)
        new_album.add(audio_file)
        new_artist.add(new_album)
        self.add(new_artist)
        return

    def create_audio_fs(self, path):
        root_path = path
        for d, dirs, files in os.walk(root_path):
            for file in files:
                curfile = os.path.join(d, file)
                if os.path.splitext(curfile)[1].lower() == ".mp3":
                    self.add_file(curfile)

    def update_file(self, localpath):
        f = self.find_file(localpath).path
        self.delete_file(localpath)
        self.add_file(f)

    def change_data(self, path, **kwargs):
        fil = VFile(path, "name")
        if "album" in kwargs:
            fil.update_album(kwargs["album"])
        if "artist" in kwargs:
            fil.update_artist(kwargs["artist"])

    def delete_file(self, path, level=1):
        tree = path.rstrip("/").split("/")
        for file in self.data:
            if file.name == tree[level]:
                if len(tree)-1 == level:
                    self.data.remove(file)
                    return
                file.delete_file(path, level+1)
                return
        raise FileNotFoundError

    def is_unknown(self, path):
        un_folder = "/Unknow Artist/Unknow Album"
        if path[0:len(un_folder)] == un_folder:
            return True
        return False

    def find_file(self, path, level=1):
        if path == "/":
            return self
        tree = path.rstrip("/").split("/")
        for file in self.data:
            if file.name == tree[level]:
                if len(tree)-1 == level:
                    return file
                return file.find_file(path, level+1)
        raise FileNotFoundError