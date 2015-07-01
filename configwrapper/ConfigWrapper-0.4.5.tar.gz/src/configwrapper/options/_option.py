class OptionError(Exception):
    def __init__(self, prefix, section, message):
        super(OptionError, self).__init__('[option %s from %s]: %s' %
                                          (prefix, section, message))


