from pyramid.scaffolds import PyramidTemplate
from textwrap import dedent

class ConfigTemplate(PyramidTemplate):
    _template_dir = 'templates/config'
    summary = 'Build a basic configuration'
    quiet = True

    def post(self, command, output_dir, vars): # pragma: no cover
        pass

    def out(self, msg):
        pass




