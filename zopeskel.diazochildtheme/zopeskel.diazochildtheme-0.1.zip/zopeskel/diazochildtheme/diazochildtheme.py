import copy

from zopeskel.plone import BasicZope
from zopeskel.base import get_var
from zopeskel.base import var


class DiazoChildTheme(BasicZope):
    _template_dir = 'templates/diazochildtheme'
    summary = "Diazo Bootstrap Child Theme package with css and js resources. Based on diazotheme.framworks"
    help = """
"""
    category = "Plone Development"
    required_templates = ['basic_namespace']
    use_local_commands = False
    use_cheetah = True
    vars = copy.deepcopy(BasicZope.vars)
    get_var(vars, 'namespace_package').default = 'diazochildtheme'
    get_var(vars, 'package').default = 'example'
    get_var(vars, 'description').default = 'My Diazo ChildTheme Package'
    get_var(vars, 'license_name').default = 'GPL version 2'

    def pre(self, command, output_dir, vars):
        vars['include_doc'] = True
