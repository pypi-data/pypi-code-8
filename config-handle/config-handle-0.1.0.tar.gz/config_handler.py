import ConfigParser #imports config file parsing from the python library
import os.path
import re

class Parser(object):
    
    def __init__(self, file_object='file', filename="./CONFIG.txt"):
    	# instantiates a parser
    	self.parser = ConfigParser.RawConfigParser()
    	# parser reads the file from inside the same directory
        if file_object == 'file':
    	    assert self.config_exists(filename), "ERROR: Could not find a configuration file. The file's name should be CONFIG.txt. It should reside in the same directory as the project's files."
    	    self.parser.read(filename)
        if file_object == 'fp':
            self.parser.readfp(filename)

    # returns a setting value as a string given a section and an option
    def get_setting(self, section, option):
    	return self.parser.get(section, option)

    # returns a list of sections
    def sections(self):
    	return self.parser.sections()

    # returns a list of sections that contain the string passed
    def section_search(self, string):
    	pattern = re.compile(string)
    	matches = []
    	for i in self.sections():
    		if pattern.search(i) != None:
    			matches.append(i)
    	return matches

    # return a list of options given a section
    def options(self, section):
    	return self.parser.options(section)

    # return a boolean value indicating whether or not a given section
    # exists in the configuration file
    def has_section(self, section):
    	return self.parser.has_section(section)

    # simple function to talk to the OS and check whether or not a 
    # configuration file exists
    def config_exists(self, file_loc):
        if os.path.exists(file_loc):
            return True
        else:
            return False


