from testcase import TestCase
from service_engine import ServiceGroup
from service_engine import ServiceEngine
from saddle_service import Service
from saddle_fixture import Fixture
import cli
import services

def relative_to_module(module, relative_dir):
    import os, sys, inspect
    harness_file = inspect.getfile(sys.modules[module])
    return os.path.dirname(os.path.dirname(os.path.realpath(harness_file)) + relative_dir)
