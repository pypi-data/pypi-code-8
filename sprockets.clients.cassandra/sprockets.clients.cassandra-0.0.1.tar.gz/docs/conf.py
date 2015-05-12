# -*- coding: utf-8 -*-
import sphinx_rtd_theme
import sprockets.clients.cassandra

project = 'sprockets.clients.cassandra'
copyright = 'AWeber Communications, Inc.'
version = sprockets.clients.cassandra.__version__
release = '.'.join(str(v) for v in sprockets.clients.cassandra.version_info)

needs_sphinx = '1.0'
extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.intersphinx',
    'sphinx.ext.viewcode',
]

templates_path = []
source_suffix = '.rst'
source_encoding = 'utf-8-sig'
master_doc = 'index'
exclude_patterns = []
pygments_style = 'sphinx'
html_theme = 'sphinx_rtd_theme'
html_theme_path = [sphinx_rtd_theme.get_html_theme_path()]
html_static_path = []

intersphinx_mapping = {
    'python': ('http://docs.python.org/3/', None),
}
