
from setuptools import setup

try:
    unicode
    def u8(s):
        return s.decode('unicode-escape').encode('utf-8')
except NameError:
    def u8(s):
        return s.encode('utf-8')

setup(name='inlang',
      version='0.1',
      description=u8('A sample python package'),
	  long_description="module to extract Indian states' names according to their respective language codes"
      )

