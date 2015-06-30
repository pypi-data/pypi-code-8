import os
import os.path
from .serializer import dump, load
from .targeting import Target

__all__ = ['UserFacts']


class UserFacts:

    def __init__(self, filename):
        self.filename = filename

    @property
    def data(self):
        try:
            with open(self.filename) as file:
                return load(file)
        except FileNotFoundError:
            return {}

    def read(self, target):
        return Target(target).read(self.data)

    def write(self, target, value, merge=False):
        data = Target(target).write(self.data, value, merge)
        self._write(data)

    def delete(self, target):
        data = Target(target).delete(self.data)
        self._write(data)

    def _write(self, data):
        os.makedirs(os.path.dirname(self.filename), exist_ok=True)
        with open(self.filename, 'w') as file:
            file.write(dump(data))
