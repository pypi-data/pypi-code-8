"""
A simple module for creating and manipulating a trie

"""


class TriePy(object):
    """
    Data structure class to house the trie

    """
    # A terminator to represent and end of a path
    __TRIE_TERMINATOR = '\0'

    def __init__(self):
        """
        Create an empty trie
        But, since we utilize a dictionary as the
        underlying data structure, we just create an
        empty dictionary.

        :return:
        """
        self.root = {}

    def add_word(self, word):
        """
        Insert a word into a trie

        :param word:
        :return:
        """
        if not word:
            return None
        current_node = self.root
        for char in word:
            current_node = current_node.setdefault(char, {})

        current_node.setdefault(self.__TRIE_TERMINATOR, {"word": word})

    def contains_word(self, word):
        """
        Checks if a path is found in a trie

        :param word:
        :return:
        """
        if not word:
            return False

        current_node = self.root
        for char in word:
            if char in current_node:
                current_node = current_node[char]
            else:
                return False

        # Check if there is a path terminator here since
        # we are at the end of a path
        if self.__TRIE_TERMINATOR in current_node:
            return True
        else:
            return False
