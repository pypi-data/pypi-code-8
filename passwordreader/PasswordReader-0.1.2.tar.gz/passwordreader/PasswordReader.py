'''
Tool for getting password from various sources
'''

__all__ = ["readPassword"]


class PasswordReaderModule(object):
    '''
    Abstract class for PasswordReader modules
    '''

    def readPassword(self):
        '''
        Override this method in custom module.
        Returns:
          String with password or None
        '''
        return None


def readPassword(*modules):
    '''
    Iterate over PasswordReaderModule modules
    and perform readPassword() function
    until one returns non-None value.
    '''
    for module in modules:
        modulePassword = module.readPassword()
        if modulePassword:
            return modulePassword
