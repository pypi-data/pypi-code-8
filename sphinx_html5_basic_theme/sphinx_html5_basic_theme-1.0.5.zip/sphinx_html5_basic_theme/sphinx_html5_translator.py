# coding: utf-8

"""Overwrite sphinx.writers.html.HTMLTranslator

or base class docutils.writers.html4css1.HTMLTranslator,
SmartyPantsHTMLTranslator

This file is the extension for the Sphinx document generator.

All the functions here are copied from docutils 0.12 or/
and Sphinx 1.3.1. You can use this file BSD-License.

Fixing work after the copy and writing setup() function
are done by Suzumizaki-Kimitaka, 2015-05-08.
"""

from sphinx.writers.html import HTMLTranslator as BaseTranslator
from sphinx.errors import SphinxError
import docutils.nodes as nodes

#
# utility functions
#

def write_table_tag_open(writer, node,
                         css_clsnam, col1_clsnam, col2_clsnam,
                         end):
    clsnams = "docutils " + css_clsnam + " frame-void rules-none"
    starttag = writer.starttag(node, 'table', CLASS=clsnams)
    writer.body.append(starttag)
    if col1_clsnam == -1:
        return
    c1 = ' class="' + col1_clsnam + '"' if col1_clsnam else ''
    c2 = ' class="' + col2_clsnam + '"' if col2_clsnam else ''
    writer.body.append('<colgroup><col%(c1)s /><col%(c2)s />'
                       '</colgroup>\n'
                       '<tbody class="valign-top">\n%(end)s' %
                       {'c1': c1, 'c2': c2, 'end': end})

def write_colspecs(writer):
    """

    Copied from docutils.writers.html4css1.HTMLTranslator,
    except the parameter to writer.body.append function.
    """
    width = 0
    for node in writer.colspecs:
        width += node['colwidth']
    for node in writer.colspecs:
        colwidth = int(node['colwidth'] * 100.0 / width + 0.5)
        writer.body.append('<col class="width-%d%%" />\n' % colwidth)
    writer.colspecs = []

#
# citation and citation_reference
#

def visit_citation(self, node):
    """

    Copied from docutils.writers.html4css1.HTMLTranslator,
    except attrs of start tag.
    """
    write_table_tag_open(self, node, 'citation', 'label', '', '<tr>')
    self.footnote_backrefs(node)
    
depart_citation = BaseTranslator.depart_citation

def visit_citation_ref(self, node):
    """
    
    Copied from docutils.writers.html4css1.HTMLTranslator,
    except the open braket is omitted and attrs of start tag.
    
    The braket should be defined with style sheet.
    """
    href = '#'
    if 'refid' in node:
        href += node['refid']
    elif 'refname' in node:
        href += self.document.nameids[node['refname']]
    else:
        raise SphinxError('Citation reference missing.')
    self.body.append(self.starttag(
        node, 'a', CLASS='citation-reference', href=href))

def depart_citation_ref(self, node):
    """
    
    Copied from docutils.writers.html4css1.HTMLTranslator,
    except the close braket is omitted.
    
    The braket should be defined with style sheet.
    """
    self.body.append('</a>')

#
# docinfo
#

def visit_docinfo(self, node):
    """

    Copied from docutils.writers.html4css1.HTMLTranslator,
    except attrs of start tag.
    """
    self.context.append(len(self.body))
    write_table_tag_open(self, node, 'docinfo',
                         'docinfo-name', 'docinfo-content', '')
    self.in_docinfo = True

depart_docinfo = BaseTranslator.depart_docinfo

#
# field list
#

def visit_field_list(self, node):
    """

    Copied from both docutils.writers.html4css1.HTMLTranslator and
    sphinx.writer.html.HTMLTranslator,
    except attrs of start tag.
    """
    # this comes from sphinx.writer.html.HTMLTranslator
    self._fieldlist_row_index = 0
    
    # remains come from douctils.writers.html4css1.HTMLTranslator
    self.context.append((self.compact_field_list, self.compact_p))
    self.compact_p = None
    if 'compact' in node['classes']:
        self.compact_field_list = True
    elif (self.settings.compact_field_lists
          and 'open' not in node['classes']):
        self.compact_field_list = True
    if self.compact_field_list:
        for field in node:
            field_body = field[-1]
            assert isinstance(field_body, nodes.field_body)
            children = [n for n in field_body
                        if not isinstance(n, nodes.Invisible)]
            if not (len(children) == 0 or
                    len(children) == 1 and
                    isinstance(children[0],
                               (nodes.paragraph, nodes.line_block))):
                self.compact_field_list = False
                break
    write_table_tag_open(self, node,
                         'field-list', 'field-name', 'field-body', '')

depart_field_list = BaseTranslator.depart_field_list

#
# footnote and footnote_reference
#

def visit_footnote(self, node):
    """

    Copied from docutils.writers.html4css1.HTMLTranslator,
    except attrs of start tag.
    """
    write_table_tag_open(self, node, 'footnote', 'label', '', '<tr>')
    self.footnote_backrefs(node)
    
depart_footnote = BaseTranslator.depart_footnote

def visit_footnote_ref(self, node):
    """open a-element of the link to footnote
    
    Copied from docutils.writers.html4css1.HTMLTranslator,
    but ignores self.settings.footnote_references.

    The braket, font-size and text-decoration should be defined with style sheet.
    """
    href = '#' + node['refid']
    self.context.append('') ### do because depart_footnote_ref calls context.pop()
    
    self.body.append(self.starttag(node, 'a',
                                   CLASS='footnote-reference',
                                   href=href).strip())

depart_footnote_ref = BaseTranslator.depart_footnote_reference

def visit_label(self, node):
    """
    
    Copied from docutils.writers.html4css1.HTMLTranslator,
    except the open braket is omitted.
    
    The braket should be defined with style sheet.
    """
    self.body.append(self.starttag(node, 'td', '%s' % self.context.pop(),
                                   CLASS='label'))

def depart_label(self, node):
    """
    
    Copied from docutils.writers.html4css1.HTMLTranslator,
    except the close braket is omitted.
    
    The braket should be defined with style sheet.
    """
    self.body.append('%s</td><td>%s' % (self.context.pop(), self.context.pop()))

#
# option list
#

def visit_option_list(self, node):
    """

    Copied from docutils.writers.html4css1.HTMLTranslator,
    but all processes are replaced by write_table_tag_open().
    """
    write_table_tag_open(self, node, 'option-list', 'option', 'description', '')

depart_option_list = BaseTranslator.depart_option_list

#
# table
#

def visit_table(self, node):
    """

    Copied from both docutils.writers.html4css1.HTMLTranslator and
    sphinx.writer.html.HTMLTranslator,
    except attrs of start tag.
    """

    # this comes from sphinx.writer.html.HTMLTranslator
    self._table_row_index = 0
    
    # remains come from douctils.writers.html4css1.HTMLTranslator
    # 'docutils' class is added by write_table_tag_open().
    self.context.append(self.compact_p)
    self.compact_p = True
    classes = self.settings.table_style.strip() + " border-1"
    
    write_table_tag_open(self, node, classes, -1, '', '')

depart_table = BaseTranslator.depart_table

def visit_thead(self, node):
    """

    Copied from docutils.writers.html4css1.HTMLTranslator,
    except calling replaced write_colspecs() and attrs of start tag.
    """
    write_colspecs(self) ### the function is defined in this file.
    self.body.append(self.context.pop()) # '</colgroup>\n'
    # There may or may not be a <thead>; this is for <tbody> to use:
    self.context.append('')
    self.body.append(self.starttag(node, 'thead', CLASS='valign-bottom'))

depart_thead = BaseTranslator.depart_thead

def visit_tbody(self, node):
    """

    Copied from docutils.writers.html4css1.HTMLTranslator,
    except calling replaced write_colspecs() and attrs of start tag.
    """
    write_colspecs(self) ### the function is defined in this file.
    self.body.append(self.context.pop()) # '</colgroup>\n' or ''
    self.body.append(self.starttag(node, 'tbody', CLASS='valign-top'))

depart_tbody = BaseTranslator.depart_tbody

#
# setup function
#

def setup(app):
    """overwrite HTMLTranslator. Called from Sphinx"""
    app.add_node(nodes.citation, html=(visit_citation, depart_citation))
    app.add_node(nodes.citation_reference,
                 html=(visit_citation_ref, depart_citation_ref))
    app.add_node(nodes.docinfo, html=(visit_docinfo, depart_docinfo))
    app.add_node(nodes.field_list, html=(visit_field_list, depart_field_list))
    app.add_node(nodes.footnote, html=(visit_footnote, depart_footnote))
    app.add_node(nodes.footnote_reference,
                 html=(visit_footnote_ref, depart_footnote_ref))
    app.add_node(nodes.label, html=(visit_label, depart_label))
    app.add_node(nodes.table, html=(visit_table, depart_table))
    app.add_node(nodes.thead, html=(visit_thead, depart_thead))
    app.add_node(nodes.tbody, html=(visit_tbody, depart_tbody))
    
    return {'version': '1.0.5'}
