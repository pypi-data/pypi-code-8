"""
docutils_react_docgen
=====================

docutils extension for documenting React modules.
Requires react-docgen
"""

from docutils import statemachine
from docutils.parsers import rst
import subprocess
import yaml


CREATE_META_DATA = 'react-docgen'
MISSING = 'Doc string is missing!'
MODULE_DICT_KEY_EMPHASIS = '*'
MODULE_PROP_EMPHASIS = '**'
MODULE_UNDERLINE_CHARACTER = '-'

default_options = {
        "missing": MISSING,
        "module_dict_key_emphasis": MODULE_DICT_KEY_EMPHASIS,
        "module_prop_emphasis": MODULE_PROP_EMPHASIS,
        "module_underline_character": MODULE_UNDERLINE_CHARACTER,
        "src": '',
        }
        
class Converter(object):

    def __init__(self, options, formatter_class):
        self.options = options
        self.formatter_class = formatter_class
            
    def _get_js_text(self, args):
        cmd = [CREATE_META_DATA] + args.split()
        return subprocess.check_output(cmd, stderr=subprocess.PIPE)

    def run(self, args):
        js_text = self._get_js_text(args)
        rst_text = self.formatter_class(self.options).run(js_text)
        return rst_text

class Formatter(object):

    def __init__(self, options):
        self.options = options
            
    def _make_dict(self, d):
        return '\n'.join(['%s: %s' % (
                self._make_emphasis(
                        key, 
                        self.options["module_dict_key_emphasis"]), 
                (d[key] if d[key] or key != 'description' 
                        else self.options["missing"])) 
                for key in sorted(d.keys())])
                
    def _make_emphasis(self, text, style):
        s = ''
        s += style + text + style
        return s

    def _make_heading(self, text, underline_char):
        s = ''
        s += text + '\n'
        s += underline_char * len(text) + '\n'* 2
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
        s += description if description else self.options["missing"]
        s += '\n' * 2
        return s

    def _make_module_header(self, filename):
        s = ''
        s += self._make_heading(
                filename, 
                self.options["module_underline_character"])
        s += self._make_src_link(filename)
        return s
                
    def _make_module_prop(self, name, prop):
        tab = ' ' * 4
        s = ''
        s += self._make_emphasis(
                name, 
                self.options["module_prop_emphasis"]) + '\n'
        s += tab + self._make_dict(prop).replace('\n', '\n' * 2 + tab) 
        s += '\n' * 2
        return s
        
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
            s += '\n' * 2
            s += '.. _`%s`: %s/%s' % (
                    filename,
                    self.options['src'],
                    filename)
            s += '\n' * 2            
        return s
        
    def run(self, js_text):
        d = yaml.load(js_text)
        s = ''
        for key in sorted(d.keys()):
            s += self._make_module(key, d[key])
        return s

class ReactDocgen(rst.Directive):

    required_arguments = 1
    optional_arguments = 0
    final_argument_whitespace = True
    option_spec = { 
            'src': rst.directives.unchanged,
            }
    option_spec.update(
            {k.lower(): rst.directives.unchanged 
                    for k in default_options.keys()})   
    has_content = False
    formatter_class = Formatter
    
    def run(self):
        args = self.arguments[0]
        options = {}
        options.update(default_options)
        options.update(self.options)
        rst_text = Converter(options, self.formatter_class).run(args)
        tab_size = 8
        include_lines = statemachine.string2lines(
                rst_text, 
                tab_size, 
                convert_whitespace=True)

        self.state_machine.insert_input(include_lines, args)
        return []

rst.directives.register_directive('reactdocgen', ReactDocgen)

