
class Tag(object):

    """A label that is added to Element for grouping

    Args:
        name: The name of the tag
        value: The value of the tag

    """

    def __init__(self, name, value=None):
        self.name = name
        self.value = value
