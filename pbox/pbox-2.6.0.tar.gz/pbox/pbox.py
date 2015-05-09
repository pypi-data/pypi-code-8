#!/usr/bin/env python
# --------------------------------------------------------------------------------------------------------------
#  PBOX makes it easy to handle persistent data using pickle.
# --------------------------------------------------------------------------------------------------------------
from __future__ import print_function
from inspect import stack
import sys, os, codecs

try:
    import json
    import cPickle as pickle
except:
    import pickle

# --------------------------------------------------------------------------------------------------------------
# Declaring global variables:
# --------------------------------------------------------------------------------------------------------------
_data_folder = r'dat'
_data_file = r'datafile.box'
_protocol = pickle.HIGHEST_PROTOCOL
_box_type = r'pickle'

if sys.platform.startswith('win'):
    _slash_char = '\\'
else:
    _slash_char = '/'
    
_separator = '\n{0:2}{1}'.format('|', ('-' * 65))

# --------------------------------------------------------------------------------------------------------------
# pbox class:
# --------------------------------------------------------------------------------------------------------------
class CreateBox(object):
    
    def __init__(self, file = _data_file, folder = _data_folder, protocol = _protocol, type = _box_type):
        ''' Initializes the box intance. Possible arguments are:
            
            Argument                Default Value
            
            * file          =       'datafile.box'
            * folder        =       'dat'
            * protogol      =       'pickle.HIGHEST_PROTOCOL'
            * type          =       'pickle' 
            
            '''
        self.data_file = file
        self.data_folder = folder
        self.protocol = protocol
        self.data_pack = dict()
        self.cache_pack = dict()
        self.box_path = '{}{}'.format(self.data_folder, _slash_char)
        self.box_type = type
        
        
    def __len__(self):
        ''' Count the objects inside the saved data-file. '''
        self._read_data_file
        return len(self.data_pack)

    
    def __iter__(self):
        ''' Iterates objects inside the saved data-file. '''
        self._read_data_file
        if self.data_pack:
            for key in self.data_pack.keys():
                yield {key:self.data_pack[key]}
        
        
    @property    
    def _save_data_file(self):
        ''' This private property saves the objects inside the data-file using
            the type and protocol specified. '''
        if not os.path.exists(self.box_path):
            os.makedirs(self.box_path)
            
        if self.box_type == 'json':
            with codecs.open((self.box_path + self.data_file), 'w', encoding='utf-8') as file:
                json.dump(self.data_pack, file)       
        else:
            with open((self.box_path + self.data_file), 'wb') as file:
                pickle.dump(self.data_pack, file, self.protocol)
                
            
    @property
    def _read_data_file(self):
        ''' This private property loads the objects from the data-file using
            the type and protocol specified. '''
        try:
            if self.box_type == 'json':
                with codecs.open((self.box_path + self.data_file), 'r', encoding='utf-8') as file:
                    self.data_pack = json.load(file)
            else:
                with open((self.box_path + self.data_file), 'rb') as file:
                    self.data_pack = pickle.load(file)
                
        except:
            if os.path.exists((self.box_path + self.data_file)):
                os.remove((self.box_path + self.data_file))
    
    
    def _get_obj_value(self, name):
        ''' This private method searchs the stack for the 
            value of the dumped object represented here by the
            argument 'name', and then return it's value or None. '''
            
        module_obj = stack()[1][0]
        
        while name not in module_obj.f_locals:
            module_obj = module_obj.f_back
            
            if module_obj is None:
                return None
        
        return module_obj.f_locals[name]
        

    def _get_objs(self, *args):
        ''' This private method receives the string representation of the 
            object's names and then returns a dictionary with their names and values. '''
        if args:
            new_objs = dict()
            
            for arg in args:
                if type(arg) == str:
                    obj_value = eval('self._get_obj_value(\'{}\')'.format(arg))
                    
                    if obj_value:
                        new_objs[arg] = obj_value
            
            return new_objs
 
    
    @property        
    def datafile(self):
        ''' This property returns the object's from the data-file as a dictionary and 
            saves any dictionary that is assigned to it inside the data-file. ''' 
        self._read_data_file
        return self.data_pack

    
    @datafile.setter
    def datafile(self, pack):
        ''' This setter runs when a value is assigned to datafile. '''
        if type(pack) == dict:
            self.data_pack = pack
            self._save_data_file
        else:
            title = '\n{0:2}{1}{2}:'.format('|', '[PBOX Module] >> Manually overwriting box ', str(self.data_file))
            message = ( '\n{0:2}TypeError: You can only assign dictionaries to \'datafile\'.'
                       ).format('|')
                       
            sys.stdout.write(title + _separator + message + _separator + '\n\n')
            
            
    @property        
    def cached(self):
        ''' This property returns the object's from the cache as a dictionary and 
            updates the cache with any dictionary that is assigned to it. '''
        return self.cache_pack

    
    @cached.setter
    def cached(self, pack):
        ''' This setter runs when a value is assigned to cached. '''
        if type(pack) == dict:
            self.cache_pack = pack
        else:
            title = '\n{0:2}{1}:'.format('|', '[PBOX Module] >> Manually overwriting cache')
            message = ( '\n{0:2}TypeError: You can only assign dictionaries to \'cached\'.'
                       ).format('|')
                       
            sys.stdout.write(title + _separator + message + _separator + '\n\n')
            

    def dump(self, *args):
        ''' This method dump objects in the data-file. 
            Object names must be passed as strings. '''
        if args:    
            new_objs = self._get_objs(*args)
        
            self._read_data_file
            self.data_pack.update(new_objs)
            
            self._save_data_file
            
             
    def cache(self, *args):
        ''' This method cache objects in the box. 
            Object names must be passed as strings. '''
        if args:
            new_objs = self._get_objs(*args)
            self.cache_pack.update(new_objs)
        
        
    @property   
    def flush(self):
        ''' This methos erases the cache. '''
        self.data_pack = dict()
        self.cache_pack = dict()
        
              
    @property
    def consolidate(self):
        ''' This method pushes the objects from the cache to the data-file. '''
        if not os.path.exists(self.box_path):
            os.makedirs(self.box_path)
        
        self.data_pack.update(self.cache_pack)
           
        with open((self.box_path + self.data_file), 'wb') as file:
            pickle.dump(self.data_pack, file, self.protocol)
            
            
    def pick(self, item = None, cache = False):
        ''' This method pick an object from the cache or data-file. Use cache = True
            agument to pick objects from the cache. '''
        if item and type(item) == str:
            
            if not cache:
                self._read_data_file
                
                title = '\n{0:2}{1}{2}:'.format('|', '[PBOX Module] >> Picking object from box ', str(self.data_file))
                message = ( '\n{0:2}Error: Object \'{1}\' could not be found in the box!'
                            '\n{0:2}'
                            '\n{0:2}Use method \'<BOX_INSTANCE>.list()\' to get a full list of the'
                            '\n{0:2}objects saved in this box.'
                           ).format('|', item)
            
            else:
                title = '\n{0:2}{1}:'.format('|', '[PBOX Module] >> Picking object from {}\'s cache'.format(self.data_file))
                message = ( '\n{0:2}Error: Object \'{1}\' could not be found in the cache!'
                            '\n{0:2}'
                            '\n{0:2}Use method \'<BOX_INSTANCE>.list(cache = True)\' to get a full'
                            '\n{0:2}list of the objects saved in the cache.'
                           ).format('|', item)        
                
            try:
                if not cache:
                    return self.data_pack[item]
                else:
                    return self.cache_pack[item]
                
            except:
                sys.stdout.write(title + _separator + message + _separator + '\n')
    
    
    @property
    def cache_datafile(self):
        ''' This method updates the cache with the objects stored in the data-file. '''
        self._read_data_file
        self.cache_pack = self.data_pack

    
    def remove(self, *args):
        ''' This method remove the objects from the data-file. '''
        if args:
            self._read_data_file
                
            for arg in args:
                if type(arg) == str:
                    
                    if arg in self.data_pack.keys():
                        del self.data_pack[arg]

                    else:
                        title = '\n{0:2}{1}{2}:'.format('|', '[PBOX Module] >> Removing object from box ', str(self.data_file))
                        message = ( '\n{0:2}Error: Object \'{1}\' could not be found!'
                                    '\n{0:2}'
                                    '\n{0:2}Use method \'<BOX_INSTANCE>.list()\' to get a full list of'
                                    '\n{0:2}the objects in this box.'
                                  ).format('|', arg)
                
                        sys.stdout.write(title + _separator + message + _separator + '\n')
            
            self._save_data_file
            
                        
    def list(self, cache = False):
        ''' This method list all objects in the cache or data-file. Use cache = True
            agument to list objects in cache. '''
        if not cache:
            self._read_data_file
            data_source = self.data_pack
            title = '\n{0:2}{1}{2}:'.format('|', '[PBOX Module] >> Listing objects from box ', str(self.data_file))
        
        else:
            data_source = self.cache_pack
            title = '\n{0:2}{1}:'.format('|', '[PBOX Module] >> Listing objects from {}\'s cache'.format(self.data_file))
        
        header = '\n{0:2}{1:<18}{2:<14}{3:<18}{4:<18}'.format('|', '<OBJECT>','>>>', '<VALUE>', '<TYPE>')
        sys.stdout.write(title + _separator + header + _separator)
        
        def format_strs(str):
            char_limit = 15
            if str:
                if len(str) > char_limit:
                    return str[:char_limit - 4] + '...'
                else:
                    return str
        
        if not data_source:
            list_obj = '\n{0:2}{1:<18}{2:<14}{1:<18}{1:<18}'.format('|', '<EMPTY>','>>>')
            sys.stdout.write(list_obj)
        
        else:           
            for obj in sorted(data_source.keys()):
                obj_name = format_strs(str(obj))
                obj_value = format_strs(str(data_source[obj]))
                obj_type = format_strs(str(type(data_source[obj])))
            
                list_obj = '\n{0:2}{1:<18}{2:<14}{3:<18}{4:<18}'.format('|', obj_name,'>>>', obj_value, obj_type)
                sys.stdout.write(list_obj)
    
        sys.stdout.write(_separator + '\n\n')

# --------------------------------------------------------------------------------------------------------------
#  pbox - END
# --------------------------------------------------------------------------------------------------------------
