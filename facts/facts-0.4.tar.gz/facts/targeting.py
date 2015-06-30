from copy import deepcopy

__all__ = ['NotFound', 'Target']


class NotFound(KeyError):
    pass


class WrongType(ValueError):
    pass


class Target(str):

    def __init__(self, target):
        if target is None:
            self.parts = []
        else:
            self.parts = target.split(':')

    def __iter__(self):
        for part in self.parts:
            yield part

    def match(self, obj):
        """
        Returns
            bool: it matches
        """
        path, frag = [], obj
        for part in self.parts:
            path.append(part)
            if isinstance(frag, dict):
                try:
                    frag = frag[part]
                except KeyError:
                    return False
            elif isinstance(frag, (list, tuple)):
                frag = part in frag
            elif isinstance(frag, str):
                frag = frag == part
            else:
                return False
        return True if frag else False

    def read(self, obj):
        """
        Returns
            object: fragment
        """
        path, frag = [], obj
        for part in self.parts:
            path.append(part)
            if isinstance(frag, dict):
                try:
                    frag = frag[part]
                except KeyError as error:
                    raise NotFound(':'.join(path)) from error
            elif isinstance(frag, (list, tuple)):
                try:
                    frag = frag[int(part)]
                except IndexError as error:
                    raise NotFound(':'.join(path)) from error
                except ValueError as error:
                    raise WrongType(':'.join(path)) from error
            else:
                raise NotFound(':'.join(path))
        return frag

    def write(self, obj, value, merge=False):
        """
        Returns
            object: full copy of new obj
        """
        full = deepcopy(obj)
        frag = full
        parts, last = self.parts[:-1], self.parts[-1]
        for part in parts:
            if isinstance(frag, dict):
                frag = frag[part]
            elif isinstance(frag, (list, tuple)):
                frag = frag[int(part)]

        if isinstance(frag, dict):
            if last in frag and merge:
                frag[last].update(value)
            else:
                frag[last] = value
        elif isinstance(frag, list):
            if last == '-':
                frag.append(value)
            else:
                frag[int(last)] = value

        return full

    def delete(self, obj):
        """
        Returns
            object: full copy of new obj
        """
        full = deepcopy(obj)
        frag = full
        parts, last = self.parts[:-1], self.parts[-1]
        for part in parts:
            if isinstance(frag, dict):
                frag = frag[part]
            elif isinstance(frag, (list, tuple)):
                frag = frag[int(part)]

        if isinstance(frag, dict):
            frag.pop(last)
        elif isinstance(frag, list):
            if last == '-':
                frag.pop()
            else:
                frag.pop(int(last))

        return full
