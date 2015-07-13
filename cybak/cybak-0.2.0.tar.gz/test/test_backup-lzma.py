import unittest
import tempfile

class ConfigFixture(unittest.TestCase):

    def setUp(self):
        # make a config file object with testable properties
        fil = tempfile.TemporaryFile()
        fil.write('[SECTION1]\ndir1=../\ndir2=~\ndirlist=./zsh_src/,/python')
        
class ConfigTests(ConfigFixture):

    def test_configbhv(self):
       pass  
