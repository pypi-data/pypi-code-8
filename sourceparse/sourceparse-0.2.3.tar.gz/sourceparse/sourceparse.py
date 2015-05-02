"""
a personal adaptation of pyclbr from the standard python lib

http://docutils.sourceforge.net/sandbox/davidg/docutils/readers/python/moduleparser.py
"""

import tokenize
import ast
import re

args_re = re.compile(r'^\s*def \w*\((.*)\):', re.MULTILINE | re.DOTALL)
kwargs_re = re.compile(r'^\s*def \w*\((.*)\):', re.MULTILINE | re.DOTALL)


class CodeChunk(object):
    """ base class to represent a Python source object
    be it a class function or method
    """
    def __init__(self, parser, name, file_name, decorated_from, from_line):
        self.name = name
        self.file = file_name
        self.decorated_from = decorated_from
        self.from_line = from_line
        self.to_line = 0
        self.parser = parser

    @property
    def source(self):
        return self.parser.lines[self.from_line - 1:self.to_line]

    @property
    def decorators(self):
        if self.decorated_from:
            return self.parser.lines[self.decorated_from - 1:self.from_line - 1]
        return []

    def __repr__(self):
        msg = '{0} {1}: from {2} to {3}\n' \
            .format(self.__class__.__name__, self.name, self.from_line, self.to_line)
        if self.decorated_from:
            msg += '    decorated from {0} to {1}' \
                .format(self.decorated_from, self.from_line)
        return msg


class Class(CodeChunk):
    """ Class to represent a Python class.
    """
    def __init__(self, parser, name, file_name, decorated_from, from_line):
        super(Class, self).__init__(parser, name, file_name, decorated_from, from_line)
        self.methods = []

    @property
    def docstring(self):
        first_line = self.source[0]
        indent = len(first_line) - len(first_line.lstrip())
        dedented = [l[indent:] for l in self.source if not l.startswith('#')]
        src = ''.join(dedented)
        parsed = ast.parse(src)
        ast_def = [node for node in parsed.body if isinstance(node, ast.ClassDef)][0]
        doc = ast.get_docstring(ast_def)
        doc = doc if doc is not None else ""
        return doc


class Method(CodeChunk):
    """ class for methods
    """
    @property
    def docstring(self):
        first_line = self.source[0]
        indent = len(first_line) - len(first_line.lstrip())
        dedented = [l[indent:] for l in self.source if not l.startswith('#')]
        src = ''.join(dedented)
        parsed = ast.parse(src)
        ast_def = [node for node in parsed.body if isinstance(node, ast.FunctionDef)][0]
        doc = ast.get_docstring(ast_def)
        doc = doc if doc is not None else ""
        return doc

    def _all_args(self):
        arg_names = []
        kwargs = {}
        src = ''.join(self.source)
        m = args_re.search(src)
        if m is not None:
            args = m.groups()[0]
            for arg_line in args.split('\n'):
                for arg_expr in arg_line.split(','):
                    with_default = arg_expr.split('=')
                    if len(with_default) > 1:
                        kwargs[with_default[0].strip()] = with_default[1].strip()
                    else:
                        arg_names.append(with_default[0].strip())
        if 'self' in arg_names:
            arg_names.remove('self')
        return arg_names, kwargs

    @property
    def args(self):
        """ returns a list of args names
        ['arg1', 'arg2', 'adfd', 'azert']
        """
        return self._all_args()[0]

    @property
    def kwargs(self):
        """ returns a dict of kwarg: default
        {'arg1':'value', 'arg2':'value', }
        """
        return self._all_args()[1]


class Function(Method):
    """ class for module level function
    """
    @property
    def docstring(self):
        src = ''.join(self.source)
        parsed = ast.parse(src)
        ast_def = [node for node in parsed.body
                   if isinstance(node, ast.FunctionDef)][0]
        doc = ast.get_docstring(ast_def)
        doc = doc if doc is not None else ""
        return doc


class CodeCollector(object):

    def __init__(self, filename):
        self.filename = filename
        self.module_objects = []
        self.lines = self._readfile()
        self.linegen = (l for l in self.lines)
        self.parse()

    @property
    def classes(self):
        return filter(lambda x: isinstance(x, Class),
                      self.module_objects)

    @property
    def functions(self):
        return filter(lambda x: isinstance(x, Function),
                      self.module_objects)

    def _readfile(self):
        """  can be overriden for other backends
        """
        with open(self.filename, 'r') as fh:
            return fh.readlines()

    def _lineread(self):
        return self.linegen.next()

    # pylint:disable = too-many-branches
    def parse(self):
        """ parse the code and populate self.module_objects
        """
        token_generator = tokenize.generate_tokens(self._lineread)
        stack = []
        decorated = False
        decorated_from = 0

        for tokentype, token, start, _end, _line in token_generator:

            if tokentype == tokenize.DEDENT:
                lineno, thisindent = start
                # close nested classes and defs
                while stack and stack[-1][1] >= thisindent:
                    previous_obj = stack[-1][0]
                    if previous_obj is not None:
                        previous_obj.to_line = lineno - 1
                    del stack[-1]

            if token == '@':
                tokentype, decorator_name, start = token_generator.next()[0:3]
                if tokentype != tokenize.NAME:
                    continue  # Syntax error
                if not decorated:
                    decorated_from = start[0]  # only the first lineno
                    decorated = True

            elif token == 'class':
                lineno, thisindent = start

                # close previous nested classes and defs
                while stack and stack[-1][1] >= thisindent:
                    del stack[-1]
                tokentype, class_name, start = token_generator.next()[0:3]
                if tokentype != tokenize.NAME:
                    continue  # Syntax error

                cur_class = Class(self, class_name, self.filename, decorated, lineno)
                if decorated:
                    decorated = False
                    cur_class.decorated_from = decorated_from

                if not stack:
                    self.module_objects.append(cur_class)
                stack.append((cur_class, thisindent))

            elif token == 'def':
                lineno, thisindent = start
                # close previous nested classes and defs
                while stack and stack[-1][1] >= thisindent:
                    del stack[-1]
                tokentype, func_name, start = token_generator.next()[0:3]
                if tokentype != tokenize.NAME:
                    continue  # Syntax error
                if stack:
                    cur_class = stack[-1][0]
                    if isinstance(cur_class, Class):
                        # it's a method
                        cur_method = Method(self, func_name,
                                            self.filename, decorated, lineno)
                        if decorated:
                            decorated = False
                            cur_method.decorated_from = decorated_from
                        cur_class.methods.append(cur_method)
                        # Marker for nested fns
                        stack.append((cur_method, thisindent))
                # else it's a nested def
                else:
                    # it's a function
                    cur_function = Function(self, func_name, self.filename, decorated, lineno)
                    if decorated:
                        decorated = False
                        cur_function.decorated_from = decorated_from
                    self.module_objects.append(cur_function)
                    stack.append((cur_function, thisindent))  # Marker for nested fns
