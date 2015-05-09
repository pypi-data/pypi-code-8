class NoSuchTable(Exception):
    pass


class WrongDSN(Exception):
    pass


class WrongNamingColumn(Exception):
    pass


class NonValidRowClassName(Exception):
    def __init__(self, class_name):
        self.class_name = class_name

    def __str__(self):
        return 'NonValidRowClassName: {0}'.format(self.class_name)
