import os
from nekbot.core.exceptions import SecurityError, InvalidArgument

__author__ = 'nekmo'

class Node(object):
    def __init__(self, root):
        root = os.path.abspath(root)
        if not os.path.exists(root):
            raise ValueError('Invalid root for %s: "%s"' % (self.__class__.__name__,
                                                            root))
        self.root = root

    def path_not_exist(self, node):
        raise InvalidArgument('The path does not exist.', node)

    def additional_checks(self, node):
        return node

    def __call__(self, node):
        node = os.path.abspath(os.path.join(self.root, node))
        if not node.startswith(self.root):
            raise SecurityError('The path does not belong to the base path.', node)
        if not os.path.exists(node):
            return self.path_not_exist(node)
        return self.additional_checks(node)


class File(Node):
    def additional_checks(self, node):
        if not os.path.isfile(node):
            raise InvalidArgument('The path is not a file.', node)
        return node


class Dir(Node):
    def additional_checks(self, node):
        if not os.path.isdir(node):
            raise InvalidArgument('The path is not a directory.', node)
        return node