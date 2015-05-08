__author__ = 'Alex Gomes'

import os
import alxlib.data as _data


class Key:
    # Key
    def get_dir(self):
        import alxlib.save

        save = alxlib.save.Save()
        return save.get_data(_data.key_dir)

    def get_path(self):
        try:
            return os.path.join(os.sep, self.get_dir(), _data.keyfile)
        except:
            return None

    def exist(self):
        try:
            return os.path.isfile(self.get_path())
        except:
            return False