#
# -*- coding: utf-8 -*-

"""
Module yogosyu
~~~~~~~~~~~~~~
The Sphinx extension to provide yomigana to glossary.

:copyright: © 2011-2015 by Suzumizaki-Kimitaka(only for additional works)
:license: 2-clause BSD.

This is the extension for `Sphinx <http://sphinx-doc.org/>`_ to add the
:code:`yogosyu` directive used to replace :code:`glossary`.

The :code:`yogosyu` directive can sort the terms by the order given from
the user(document writer). Especially to support the language like
Japanese, :code:`:yomimark:` option is exist and make the way adding the
reading(shows how to read) to each term. 

This module depends on the module `sortorder
<https://pypi.python.org/pypi/sortorder>`_. The document of the module
shows how to make your own order for the languages you want.

:code:`yomimark` can be one of
:code:`single_char_or_whitespace_or_unicode`.
the acceptable words are defined in
:mod:`docutils.parsers.rst.directives` as follows:

- one of the words: tab space
- any single unicode character except white-spaces
- the character itself, or the code point represented by:

  - the decimal number
  - the hexadecimal number prefixed x, \\x, U+, u, or \\u
  - XML style like &#x262E;

The every term is splited by yomimark. 1st is the term itself,
2nd is treated as Yomigana(how to read). Currently 3rd and
followers are simply ignored, but using this way, the 'mono ruby' may be
supported for the future. (see HTML ruby module for example.)

Not all the entry have to give yomigana. When yomigana is not
assigned, the name of the entry is used to sort.

yomigana itself is currently not shown in output HTML files.
They're only used to sort.
"""

from docutils.parsers.rst import directives
from docutils.statemachine import ViewList
from docutils import nodes
from sphinx.util.compat import Directive
from sphinx import addnodes

_sort_order_obj = None # Place Holder, and internal only.

def make_termnodes_from_paragraph_node(env, node_and_yomi, new_id=None):
    """helper function of :meth:`Yogosyu.run`

    :param tuple node_and_yomi: the entry
    :param str_or_unicode_or_None new_id: give the id if you already made.
    
    Copied from :mod:`sphinx.domains.std`, modified 2 blocks and the 2nd parameter.
    """
    # The next line is added from 'sphinx/domains/std.py'.
    node, yomi = node_and_yomi
    
    gloss_entries = env.temp_data.setdefault('gloss_entries', set())
    objects = env.domaindata['std']['objects']

    termtext = node.astext()
    if new_id is None:
        new_id = 'term-' + nodes.make_id(termtext)
    if new_id in gloss_entries:
        new_id = 'term-' + str(len(gloss_entries))
    gloss_entries.add(new_id)
    
    # The next line is differ from 'sphinx/domains/std.py',
    # new_id -> (new_id, yomi)
    objects['term', termtext.lower()] = env.docname, (new_id, yomi)

    # add an index entry too
    indexnode = addnodes.index()
    indexnode['entries'] = [('single', termtext, new_id, 'main')]
    new_termnodes = []
    new_termnodes.append(indexnode)
    new_termnodes.extend(node.children)
    new_termnodes.append(addnodes.termsep())
    for termnode in new_termnodes:
        termnode.source, termnode.line = node.source, node.line

    return new_id, termtext, new_termnodes


def make_term_from_paragraph_node(termnodes, ids):
    """Copied function of :meth:`sphinx.domains.std.term_from_paragraph_node`
    
    Currently, no lines are modified.
    Called from :meth:`Yogosyu.run`.
    """
    # make a single "term" node with all the terms, separated by termsep
    # nodes (remove the dangling trailing separator)
    term = nodes.term('', '', *termnodes[:-1])
    term.source, term.line = termnodes[0].source, termnodes[0].line
    term.rawsource = term.astext()
    term['ids'].extend(ids)
    term['names'].extend(ids)
    return term


class Yogosyu(Directive):
    """Yomigana featured version of sphinx.domains.std.Glossary

    Directive to create a glossary with cross-reference targets for :term:
    roles. The option :code:`yomimark` is added.

    The base class is :class:`docutils.parsers.rst.Directive`.
    The option parser is defined in the module
    :mod:`docutils.parsers.rst.directives`.
    """
    has_content = True
    required_arguments = 0
    optional_arguments = 0
    final_argument_whitespace = False
    option_spec = {
        'sorted': directives.flag,
        # 'yomimark' is added against 'Glossary' directive.
        'yomimark': directives.single_char_or_whitespace_or_unicode
    }
 
    def run(self):
        """Inherit sphinx.util.compatDerective.run

        Base codes are copied from the module
        :mod:`sphinx.domains.std.Glossary`.
        """
        env = self.state.document.settings.env
        node = addnodes.glossary()
        node.document = self.state.document

        # This directive implements a custom format of the reST definition list
        # that allows multiple lines of terms before the definition.  This is
        # easy to parse since we know that the contents of the glossary *must
        # be* a definition list.

        # first, collect single entries
        entries = []
        in_definition = True
        was_empty = True
        messages = []
        for line, (source, lineno) in zip(self.content, self.content.items):
            # empty line -> add to last definition
            if not line:
                if in_definition and entries:
                    entries[-1][1].append('', source, lineno)
                was_empty = True
                continue
            # unindented line -> a term
            if line and not line[0].isspace():
                # enable comments
                if line.startswith('.. '):
                    continue
                # first term of definition
                if in_definition:
                    if not was_empty:
                        messages.append(self.state.reporter.system_message(
                            2, 'glossary term must be preceded by empty line',
                            source=source, line=lineno))
                    entries.append(([(line, source, lineno)], ViewList()))
                    in_definition = False
                # second term and following
                else:
                    if was_empty:
                        messages.append(self.state.reporter.system_message(
                            2, 'glossary terms must not be separated by empty '
                            'lines', source=source, line=lineno))
                    if entries:
                        entries[-1][0].append((line, source, lineno))
                    else:
                        messages.append(self.state.reporter.system_message(
                            2, 'glossary seems to be misformatted, check '
                        'indentation', source=source, line=lineno))
            else:
                if not in_definition:
                    # first line of definition, determines indentation
                    in_definition = True
                    indent_len = len(line) - len(line.lstrip())
                if entries:
                    entries[-1][1].append(line[indent_len:], source, lineno)
                else:
                    messages.append(self.state.reporter.system_message(
                        2, 'glossary seems to be misformatted, check '
                    'indentation', source=source, line=lineno))
            was_empty = False

        # now, parse all the entries into a big definition list
        items = []
        for terms, definition in entries:
            termtexts = []
            termnodes = []
            system_messages = []
            ids = []
            for line, source, lineno in terms:
                # split yomi from entry name
                yomi = line
                if 'yomimark' in self.options:
                    yomimark = self.options['yomimark']
                    line_and_yomi = line.split(yomimark)
                    line = line_and_yomi[0].rstrip()
                    if len(line_and_yomi) > 1:
                        yomi = line_and_yomi[1].lstrip()
                # parse the term with inline markup
                res = self.state.inline_text(line, lineno)
                system_messages.extend(res[1])

                # get a text-only representation of the term and register it
                # as a cross-reference target
                tmp = nodes.paragraph('', '', *res[0])
                tmp.source = source
                tmp.line = lineno
                new_id, termtext, new_termnodes = \
                        make_termnodes_from_paragraph_node(env, (tmp, yomi))
                ids.append(new_id)
                termtexts.append(termtext)
                termnodes.extend(new_termnodes)

            term = make_term_from_paragraph_node(termnodes, ids)
            term += system_messages

            defnode = nodes.definition()
            if definition:
                self.state.nested_parse(definition, definition.items[0][1],
                                        defnode)
                tmp.source = source
                tmp.line = lineno
            items.append((termtexts,
                          nodes.definition_list_item('', term, defnode),
                          yomi))

        if 'sorted' in self.options:
            items.sort(key=lambda x:
                       _sort_order_obj.get_string_to_sort(x[2]))

        dlist = nodes.definition_list()
        dlist['classes'].append('glossary')
        dlist.extend(item[1] for item in items)
        node += dlist
        return messages + [node]

# ========================================================
# Hacking functions
# ========================================================

def wrap_make_refnode(org_method):
    """

    Defined to override :func:`sphinx.util.nodes.make_refnode`.
    """
    
    def my_make_refnode(
            builder, fromdocname, todocname, targetid, child, title=None):
        if isinstance(targetid, tuple):
            targetid = targetid[0]
        return org_method(
            builder, fromdocname, todocname, targetid, child, title=None)
    
    return my_make_refnode

def my_domains_std_StandardDomain_get_objects(self):
    """

    Defined to override :meth:`sphinx.domains.std.StandardDomain.get_objects`.
    """
    for (prog, option), info in self.data['progoptions'].items():
        info_1 = info[1][0] if isinstance(info[1], tuple) else info[1]
        yield (option, option, 'option', info[0], info_1, 1)
    for (type, name), info in self.data['objects'].items():
        info_1 = info[1][0] if isinstance(info[1], tuple) else info[1]
        yield (name, name, type, info[0], info_1,
               self.object_types[type].attrs['searchprio'])
    for name, info in self.data['labels'].items():
        info_1 = info[1][0] if isinstance(info[1], tuple) else info[1]
        yield (name, info[2], 'label', info[0], info_1, -1)

# ========================================================
# Initializing functions
# ========================================================

def determine_sort_order(app):
    """Determine sort order used in this module

    :param sphinx.config.Config cfg:
       you can give from Sphinx with :code:`app.config`,
       :code:`builder.config` etc.
    :rtype: None
    :return: None
    """
    global _sort_order_obj
    import sortorder
    _sort_order_obj = sortorder.get_sort_order(app.config)
    if _sort_order_obj.__class__ == sortorder.SortOrderLegacy:
        print ('yogosyu.py: Using SortOrderLegacy.')
    return

def setup(app):
    """Extend the Sphinx as we want, called from the Sphinx

    :param sphinx.application.Sphinx app: the object to add builder or something.
    """
    app.add_directive('yogosyu', Yogosyu)
    app.add_directive(u'用語集', Yogosyu) # 'yogosyu' written in original.
    app.connect('builder-inited', determine_sort_order)
    app.setup_extension('sortorder')

    # make sure import sphinx.util.nodes first, because
    # domains.std refers make_refnode by using the form
    # 'from sphinx.util.nodes import make_refnode'
    import sphinx.util.nodes
    sphinx.util.nodes.make_refnode = wrap_make_refnode(sphinx.util.nodes.make_refnode)
    import sphinx.domains.std
    sphinx.domains.std.make_refnode = wrap_make_refnode(sphinx.util.nodes.make_refnode)
    sphinx.domains.std.StandardDomain.get_objects = my_domains_std_StandardDomain_get_objects
    return {'version': '2.0.5', 'parallel_read_safe': False}
