# -*- coding: utf-8 -*-
#
# Psycopg documentation build configuration file, created by
# sphinx-quickstart on Sun Feb  7 13:48:41 2010.
#
# This file is execfile()d with the current directory set to its containing dir.
#
# Note that not all possible configuration values are present in this
# autogenerated file.
#
# All configuration values have a default; values that are commented out
# serve to show the default.

import sys, os

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
sys.path.append(os.path.abspath('tools/lib'))

# -- General configuration -----------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be extensions
# coming with Sphinx (named 'sphinx.ext.*') or your custom ones.
extensions = ['sphinx.ext.autodoc', 'sphinx.ext.todo', 'sphinx.ext.ifconfig',
              'sphinx.ext.doctest', 'sphinx.ext.intersphinx' ]

# Specific extensions for Psycopg documentation.
extensions += [ 'dbapi_extension', 'sql_role', 'ticket_role' ]

# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

# The suffix of source filenames.
source_suffix = '.rst'

# The encoding of source files.
#source_encoding = 'utf-8'

# The master toctree document.
master_doc = 'index'

# General information about the project.
project = u'Psycopg'
copyright = u'2001-2013, Federico Di Gregorio. Documentation by Daniele Varrazzo'

# The version info for the project you're documenting, acts as replacement for
# |version| and |release|, also used in various other places throughout the
# built documents.
#
# The short X.Y version.
version = '2.0'

# The full version, including alpha/beta/rc tags.
try:
    import psycopg2
    release = psycopg2.__version__.split()[0]
    version = '.'.join(release.split('.')[:2])
except ImportError:
    print "WARNING: couldn't import psycopg to read version."
    release = version

intersphinx_mapping = {
    'py': ('http://docs.python.org/', None),
    'py3': ('http://docs.python.org/3.2', None),
    }

# Pattern to generate links to the bug tracker
ticket_url = 'http://psycopg.lighthouseapp.com/projects/62710/tickets/%s'

# The language for content autogenerated by Sphinx. Refer to documentation
# for a list of supported languages.
#language = None

# There are two options for replacing |today|: either, you set today to some
# non-false value, then it is used:
#today = ''
# Else, today_fmt is used as the format for a strftime call.
#today_fmt = '%B %d, %Y'

# List of documents that shouldn't be included in the build.
#unused_docs = []

# List of directories, relative to source directory, that shouldn't be searched
# for source files.
exclude_trees = ['_build', 'html']

# The reST default role (used for this markup: `text`) to use for all documents.
default_role = 'obj'

# If true, '()' will be appended to :func: etc. cross-reference text.
#add_function_parentheses = True

# If true, the current module name will be prepended to all description
# unit titles (such as .. function::).
#add_module_names = True

# If true, sectionauthor and moduleauthor directives will be shown in the
# output. They are ignored by default.
#show_authors = False

# The name of the Pygments (syntax highlighting) style to use.
pygments_style = 'sphinx'

# A list of ignored prefixes for module index sorting.
#modindex_common_prefix = []

# Include TODO items in the documentation
todo_include_todos = False

rst_epilog = """
.. |DBAPI| replace:: DB API 2.0

.. _DBAPI: http://www.python.org/dev/peps/pep-0249/

.. _transaction isolation level:
    http://www.postgresql.org/docs/current/static/transaction-iso.html

.. _mx.DateTime: http://www.egenix.com/products/python/mxBase/mxDateTime/

.. |MVCC| replace:: :abbr:`MVCC (Multiversion concurrency control)`
"""

# -- Options for HTML output ---------------------------------------------------

# The theme to use for HTML and HTML Help pages.  Major themes that come with
# Sphinx are currently 'default' and 'sphinxdoc'.
html_theme = 'default'

# The stylesheet to use with HTML output: this will include the original one
# adding a few classes.
html_style = 'psycopg.css'

# Theme options are theme-specific and customize the look and feel of a theme
# further.  For a list of options available for each theme, see the
# documentation.
#html_theme_options = {}

# Add any paths that contain custom themes here, relative to this directory.
#html_theme_path = []

# The name for this set of Sphinx documents.  If None, it defaults to
# "<project> v<release> documentation".
#html_title = None

# A shorter title for the navigation bar.  Default is the same as html_title.
#html_short_title = None

# The name of an image file (relative to this directory) to place at the top
# of the sidebar.
#html_logo = None

# The name of an image file (within the static path) to use as favicon of the
# docs.  This file should be a Windows icon file (.ico) being 16x16 or 32x32
# pixels large.
#html_favicon = None

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ['_static']

# If not '', a 'Last updated on:' timestamp is inserted at every page bottom,
# using the given strftime format.
#html_last_updated_fmt = '%b %d, %Y'

# If true, SmartyPants will be used to convert quotes and dashes to
# typographically correct entities.
#html_use_smartypants = True

# Custom sidebar templates, maps document names to template names.
#html_sidebars = {}

# Additional templates that should be rendered to pages, maps page names to
# template names.
#html_additional_pages = {}

# If false, no module index is generated.
#html_use_modindex = True

# If false, no index is generated.
#html_use_index = True

# If true, the index is split into individual pages for each letter.
#html_split_index = False

# If true, links to the reST sources are added to the pages.
#html_show_sourcelink = True

# If true, an OpenSearch description file will be output, and all pages will
# contain a <link> tag referring to it.  The value of this option must be the
# base URL from which the finished HTML is served.
#html_use_opensearch = ''

# If nonempty, this is the file name suffix for HTML files (e.g. ".xhtml").
#html_file_suffix = ''

# Output file base name for HTML help builder.
htmlhelp_basename = 'psycopgdoc'


# -- Options for LaTeX output --------------------------------------------------

# The paper size ('letter' or 'a4').
#latex_paper_size = 'letter'

# The font size ('10pt', '11pt' or '12pt').
#latex_font_size = '10pt'

# Grouping the document tree into LaTeX files. List of tuples
# (source start file, target name, title, author, documentclass [howto/manual]).
latex_documents = [
  ('index', 'psycopg.tex', u'Psycopg Documentation',
   u'Federico Di Gregorio', 'manual'),
]

# The name of an image file (relative to this directory) to place at the top of
# the title page.
#latex_logo = None

# For "manual" documents, if this is true, then toplevel headings are parts,
# not chapters.
#latex_use_parts = False

# Additional stuff for the LaTeX preamble.
#latex_preamble = ''

# Documents to append as an appendix to all manuals.
#latex_appendices = []

# If false, no module index is generated.
#latex_use_modindex = True


doctest_global_setup = """

import os
import psycopg2

def test_connect():
    try:
        dsn = os.environ['PSYCOPG2_DSN']
    except KeyError:
        assert False, "You need to set the environment variable PSYCOPG2_DSN" \
                " in order to test the documentation!"
    return psycopg2.connect(dsn)

conn = test_connect()
cur = conn.cursor()

def drop_test_table(name):
    cur.execute("SAVEPOINT drop_test_table;")
    try:
        cur.execute("DROP TABLE %s;" % name)
    except:
        cur.execute("ROLLBACK TO SAVEPOINT drop_test_table;")
    conn.commit()

def create_test_table():
    drop_test_table('test')
    cur.execute("CREATE TABLE test (id SERIAL PRIMARY KEY, num INT, data TEXT)")
    conn.commit()

"""
