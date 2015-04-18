import os
from pycrm114.storage import Storage


class FileSystemStorage(Storage):
    def update_control_block(self, control_block):
        control_block.dump(open(self._controlblock_file, "w"))

    def update_data_block(self, data_block):
        data_block.dump(open(self._datablock_file, "w"))

    def __init__(self, data_dir):
        if not os.path.isdir(data_dir):
            os.makedirs(data_dir)
        self.data_dir = data_dir
        self._datablock_file = os.path.join(self.data_dir, "datablock.txt")
        self._controlblock_file = os.path.join(self.data_dir, "controlblock.txt")
    @property
    def data_block_file(self):
        return self._datablock_file if os.path.isfile(self._datablock_file) else None

    @property
    def control_block_file(self):
        return self._controlblock_file if os.path.isfile(self._controlblock_file) else None
