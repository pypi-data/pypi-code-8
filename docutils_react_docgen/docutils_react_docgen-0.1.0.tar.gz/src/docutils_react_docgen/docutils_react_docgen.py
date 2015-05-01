"""
docutils_react_docgen
=====================

docutils extension for documenting React modules.
Requires react-docgen
"""

from docutils import statemachine
from docutils.parsers import rst
import json
import os
import subprocess

REACT_DOCGEN = 'react-docgen'

MODULE_DESCRIPTION_MISSING = 'Module doc string is missing!'

MODULE_PROP_DESCRIPTION_MISSING = 'Property doc string is missing!'

MODULE_UNDERLINE_CHARACTER = '-'

TAB_SIZE = 4

DEFAULT_OPTIONS = {
    'use_commonjs_module_name':         True,
    'module_description_missing':       MODULE_DESCRIPTION_MISSING,
    'module_prop_description_missing':  MODULE_PROP_DESCRIPTION_MISSING,
    'module_underline_character':       MODULE_UNDERLINE_CHARACTER,
    'src':                              '',
    'tab_size':                         TAB_SIZE,
}


def find_package(dirname):
    """find commonjs package for given directory.
    Starts from `dirname` and recurses up the directory tree 
    looking for bower.json or package.json.

    Returns a tuple (dirname, package)

    dirname
        The directory the .json file was found in.

    package
        A dict loaded from the .json file.  
        Its keys are the module filenames.
    """
    if dirname:
        bower_json = os.path.join(dirname, 'bower.json')
        if os.path.exists(bower_json):
            with open(bower_json, 'r') as f:
                return dirname, json.load(f)
        package_json = os.path.join(dirname, 'package.json')
        if os.path.exists(package_json):
            with open(package_json, 'r') as f:
                return dirname, json.load(f)
        next_dirname = os.path.dirname(dirname)
        if next_dirname != dirname:
            return find_package(next_dirname)
    return None, None


def get_dirname(doc_dict, options):
    return (os.path.dirname(doc_dict.keys()[0]) 
            if options['use_commonjs_module_name'] and doc_dict 
            else '')
    
def react_docgen(args, react_docgen=REACT_DOCGEN):
    """ Execute ``react-docgen`` with the given arguments. 
    `args` is a string which may contain spaces.
    
    returns the output of `react_docgen` as a dict whose items are
     
    string
        module filename 

    dict
        module metadata
    """
    cmd = [react_docgen] + args.split()
    return json.loads(subprocess.check_output(cmd, stderr=subprocess.PIPE))


def react_doc_to_rst(doc_dict, options, formatter_class):
    """ Convert `doc_dict`, the react-docgen output dict
    to a string of ReStructuredText,
    according to the `options` and using the `formatter_class`
    """
    dirname = get_dirname(doc_dict, options)
    formatter = formatter_class(options, dirname)
    return formatter.run(doc_dict)


class Formatter(object):
    """ Formatter(options, dirname).run(doc_dict) returns a string.
    
    options
        a dict of options.

    dirname
        the directory to search for the CommonJS package 
        if the use_commonjs_module_name option is True
    
    doc_dict
        a dict of react-docgen module metadata 
    """

    def __init__(self, options, dirname):
        self.options = options
        self.tab = ' ' * self.options['tab_size']
        package_dirname, package = find_package(dirname)
        if package_dirname:
            self.package_dirname_len = len(package_dirname)
            self.package_name = package['name']
        else: 
            self.package_dirname_len = 0

    def _get_module_name(self, filename):
        if self.package_dirname_len:
            module_name = '%s%s' % (
                    self.package_name,
                    filename[self.package_dirname_len:])
            if module_name.endswith('.js'):
                module_name = module_name[:-3]
        else:
            module_name = filename
        return module_name

    def _make_definition(self, term, term_definition):
        definition = '\n'.join(self.tab + line 
                for line in term_definition.split('\n'))
        return term + '\n' + definition

    def _make_emphasis(self, text, style):
        s = ''
        s += style + text + style
        return s

    def _make_heading(self, text, underline_char):
        s = ''
        s += text + '\n'
        s += underline_char * len(text) + '\n\n'
        return s

    def _make_module(self, filename, module_blob):
        s = ''
        s += self._make_module_header(filename)
        s += self._make_module_description(module_blob)
        s += self._make_module_props(module_blob)
        return s

    def _make_module_description(self, module_blob):
        s = ''
        description = module_blob.get('description', '')
        s += description if description else self.options[
                'module_description_missing']
        s += '\n\n'
        return s

    def _make_module_header(self, filename):
        module_name = self._get_module_name(filename)
        s = ''
        s += self._make_heading(
                module_name,
                self.options['module_underline_character'])
        s += self._make_src_link(filename)
        return s

    def _make_module_prop_name(self, name, prop):
        args = []
        #print prop
        if prop.get('required'):
            args.append('required')
        if prop.get('defaultValue'):
            args.append('default = ``%s``' % prop['defaultValue']['value'])
        if args:
            return '%s (%s)' % (name, ', '.join(args))
        else:
            return name

    def _make_module_prop(self, name, prop):
        return self._make_definition(
                self._make_module_prop_name(name, prop),
                self._make_module_prop_description(prop)) + '\n\n'

    def _make_module_prop_description(self, prop):
        return prop.get(
                'description', 
                self.options['module_prop_description_missing'])

    def _make_module_props(self, module_blob):
        s = ''
        props = module_blob.get('props', {})
        for key in sorted(props.keys()):
            s += self._make_module_prop(key, props[key])
        return s

    def _make_src_link(self, filename):
        s = ''
        if self.options['src']:
            s += '`%s`_' % filename
            s += '\n\n'
            s += '.. _`%s`: %s/%s' % (
                    filename,
                    self.options['src'],
                    filename)
            s += '\n\n'
        return s

    def run(self, doc_dict):
        return ''.join(self._make_module(k, d) 
                for k, d in sorted(doc_dict.items()))


class ReactDocgen(rst.Directive):
    """ Docutils Directive which calls the react-docgen executable.
    """

    required_arguments = 1
    optional_arguments = 0
    final_argument_whitespace = True
    option_spec = {'src': rst.directives.unchanged}
    option_spec.update(
            {k.lower(): rst.directives.unchanged
                    for k in DEFAULT_OPTIONS.keys()})
    has_content = False
    formatter_class = Formatter

    def run(self):
        args = self.arguments[0]
        options = {}
        options.update(DEFAULT_OPTIONS)
        options.update(self.options)
        doc_dict = react_docgen(args)
        rst = react_doc_to_rst(doc_dict, options, self.formatter_class)
        tab_size = options['tab_size']
        include_lines = statemachine.string2lines(
                rst,
                tab_size,
                convert_whitespace=True)
        self.state_machine.insert_input(include_lines, '')
        return []

rst.directives.register_directive('reactdocgen', ReactDocgen)

