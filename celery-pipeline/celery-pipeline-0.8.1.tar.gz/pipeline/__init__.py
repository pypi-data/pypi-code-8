"""
Pipeline

This package (ab)uses the registry pattern, so it it is critical that
modules using registries are imported as early as possible
"""
__version__ = '0.6'


import pipeline.signals
import pipeline.workspace


#TODO(mikew): Move these from explicit CommndTask subclasses to something
#TODO: more generic, so we don't require python code to implement
#TODO: either of them (or any other shell commands)
#from pipeline.modules import flake8, prospector


from pipeline.modules import debug
#from pipeline.modules import dtcop
#from pipeline.modules import jenkins
#from pipeline.modules import coverage
#from pipeline.modules import karma


