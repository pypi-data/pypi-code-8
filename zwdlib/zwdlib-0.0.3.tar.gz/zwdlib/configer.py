# -*- coding: utf-8 -*-
from ConfigParser import ConfigParser, NoOptionError
import os
class Configer(object, ConfigParser):
    '''
    [default_section]
    int_attr = 20
    string_attr = aaa.com.cn
    float_attr = 2.1
    eval_string = 60*60
    '''
    DEFAULT_SECTION = "default_section"
    
    _instances = {}
    
#     def __new__(cls, *args, **kwargs):
    def __new__(cls, filename="config.ini"):
#         filename = (args or kwargs.values())[0] 
        if not cls._instances.get(filename):
            cls._instances[filename] = super(Configer, cls).__new__(
                                cls, filename)
        return cls._instances.get(filename)
    
    def __init__(self, filename="config.ini"):
        '''
        >>> cfg1 = Configer(None)
        >>> cfg2 = Configer(None)
        >>> id(cfg1) == id(cfg2)
        True
        '''
        ConfigParser.__init__(self)
        self.filename = filename
        self.reload()
    
    def load_docstring(self):
        import StringIO
        self.readfp(StringIO.StringIO('\n'.join([line.strip() for line in self.__class__.__doc__.splitlines()])))
        return self
    
    def reload(self):
        '''
        >>> cfg = Configer("config.ini") # doctest: +IGNORE_EXCEPTION_DETAIL
        Traceback (most recent call last):  
        IOError: config.ini
        '''
        if self.filename:
            if not os.path.exists(self.filename):
                raise IOError, self.filename
            self.read(self.filename)
        if not self.has_section(Configer.DEFAULT_SECTION):
            self.add_section(Configer.DEFAULT_SECTION)
    
    def reset(self):
        for section in self.sections():
            self.remove_section(section)
        self.add_section(Configer.DEFAULT_SECTION)
    
    def save(self):
        fp = open(self.filename,"w")
        self.write(fp)
        fp.close()
    
    def set(self,option,value,section=None):
        if not section:
            section = Configer.DEFAULT_SECTION
        ConfigParser.set(self,section,option,str(value))
    
    def get(self,option,section=None):
        if not section:
            section = Configer.DEFAULT_SECTION
        try:
            return ConfigParser.get(self,section,option)
        except NoOptionError:
            return ""
    
    def __getattr__(self, name):
        '''
        >>> cfg = Configer(None).load_docstring()
        >>> cfg.int_attr
        20
        >>> cfg.float_attr
        2.1
        >>> cfg.string_attr
        'aaa.com.cn'
        >>> cfg.eval_string
        3600
        '''
        v = self.get(name)
        try:
            return eval(v)
        except:
            pass
        return v
    
if __name__ == "__main__":
    import doctest
    doctest.testmod(verbose=True, report=True)
