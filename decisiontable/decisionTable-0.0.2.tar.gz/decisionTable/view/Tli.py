"""
Tli : Terminal line interface module
"""

class Tli(object):
    """
    Main class module
    """
    
    @staticmethod
    def showErrors(title,errors = []): 
        """
        Will parse the errors array and raise pretty value error string.
        
        Attributes:
            title(str): Title of errors.
            errors (array of str): Error info description.
        
        Raise:
            ValueError: Always
        """
        raise ValueError(title+'\n'+('='*30)+'\n > '+'\n > '.join(errors))