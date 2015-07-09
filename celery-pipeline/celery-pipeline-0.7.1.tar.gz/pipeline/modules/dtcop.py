from pipeline.actions import action, TaskResult
from pipeline.tasks import TaskResult
from pipeline.command import CommandResult
import logging
logger = logging.getLogger(__name__)

class DT2Cop(object):

    def __init__(self, diff):
        self.diff = diff.decode('utf-8')
        self.new_classes = []
        self.new_methods = []

    def get_all_new_classes_from_file_diff(self, file_diff):
        """
        Calls get new methods
        """
        for i, line in enumerate(file_diff.split('+class')):
            if i == 0:
                continue
            else:
                new_class = '{}{}'.format('class', line)
                self.new_classes.append(new_class)
                self.get_all_new_methods_from_new_class(new_class)

    def get_all_new_methods_from_new_class(self, new_class):
        for i, method in enumerate(new_class.split('+    def')):
            if i == 0:
                continue
            new_method = '{}{}'.format('def', method)
            self.new_methods.append(new_method)

    def get_all_files_from_diff(self):
        # There is one index per file in the diff
        logger.critical(type(self.diff))
        files_diff = self.diff.split('index')
        for myfile in files_diff:
            self.get_all_new_classes_from_file_diff(myfile)

    def check_print_statements(self):
        """
        Diffs should not have any print statements.
        """
        # TODO use regex so method names that have print are not accounted for
        if 'print' in self.diff:
            msg = 'Print Violation. DT2COP id: {}'.format('BP13')
            return msg
        return ''

    def check_setup_teardown(self):
        """
        SetUp and TearDown methods must call super
        """
        for method in self.new_methods:
            if method.startswith('def setUp') or method.startswith('def tearDown'):
                if not 'super(' in method:
                    msg = 'Did not call super on test setUp() or tearDown(): DT2COP_ID: {}'
                    return msg.format('CT03')
        return ''

    def check_dunder_init(self):
        """
        Do not override dunder init if just calling super
        """
        for method in self.new_methods:
            if method.startswith('def __init__'):
                method = method.replace('+', '')
                method = method.split('\n')
                method = [x for x in method if x]  #filter(None, method)
                # Check if we are just overriding init
                if len(method) == 2:
                    if method[1].strip().startswith('super('):
                        msg = 'Do not override dunder init if just calling super. DT2COP_ID: {}'.format('CC01')
                        return msg
        return ''

    def check_manager_log_explicit_context(self):
        """
        self.log DOES NOT need an explicit context to be passed
        """
        for method in self.new_methods:
            if method.startswith('def DT20COP_lo'):
                method = method.replace('+', '')
                method = method.split('\n')
                method = [x for x in method if x]  #filter(None, method)
                for line in method:
                    if line.strip().startswith('self.log'):
                        if 'extra=self.context':
                            msg = 'self.log DOES NOT need an explicit context to be passed: DT2COP_ID: {}'.format('CT05')
                            return msg
        return ''

    def check_use_of_with_statement_with_get_manager(self):
        """
        Do not use with statement with getManager
        """
        for method in self.new_methods:
            if 'with getManager' in method:
                msg = 'Do not use with statement with getManager, DT2COP_ID: {}'.format('BP05')
                return msg
        return ''

    def check_use_of_dt_requests(self):
        """
        Use dt_requests module for all HTTP communication
        """
        if 'import requests' in self.diff:
            msg = 'Use dt_requests instead of requests. DT2COP_ID: {}'.format('BP08')
            return msg
        return ''

    def check_simplejson_import(self):
        if 'import json' in self.diff:
            msg = 'Use simplejson instead of json. DT2COP_ID: {}'.format('PL01')
            return msg
        return ''

    def run(self):
        output = []
        # Make sure we call `get_all_files_from_diff`
        self.get_all_files_from_diff()
        output.append(self.check_setup_teardown())
        output.append(self.check_print_statements())
        output.append(self.check_dunder_init())
        output.append(self.check_simplejson_import())
        output.append(self.check_use_of_dt_requests())
        output.append(self.check_use_of_with_statement_with_get_manager())
        output.append(self.check_manager_log_explicit_context())
        logger.critical(output)
        return '\n'.join(output)


@action(name='dtcop')
def dtcop(self, retval, source):
    """Run dtcop ona pull request"""
    output = DT2Cop(source.diff).run()
    return CommandResult(True, output=output)
