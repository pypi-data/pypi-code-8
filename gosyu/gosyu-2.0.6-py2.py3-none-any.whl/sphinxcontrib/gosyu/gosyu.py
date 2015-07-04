#!python
# -*- encoding: utf-8 -*-


"""
Module gosyu
~~~~~~~~~~~~
The Sphinx extension to provide yomigana to glossary.

:copyright: © 2011-2015 by Suzumizaki-Kimitaka(only for additional works)
:license: 2-clause BSD.

This is the extension for `Sphinx <http://sphinx-doc.org/>`_ to add the
:code:`gosyu` directive used to replace :code:`glossary`.

The :code:`gosyu` directive can sort the terms by the order given from
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

from sphinx import addnodes
from sphinx.util.nodes import nodes
from sphinx.domains import Index, Domain, ObjType
from sphinx.directives import ObjectDescription, directives
from docutils.statemachine import ViewList

_sort_order_obj = None # Place Holder, and internal only.


# ========================================================
# Helper functions
# ========================================================

def make_termnodes_from_paragraph_node(env, domain_obj, node, yomi):
    """helper function of :meth:`GosyuDirective.run`

    :param Sphinx.BuildEnvironment env: current build environment
    :param dict domain_obj:
       reference to the dict of the termtext and corresponding
       informations(docname, id_used_for_anchor, yomigana) 
    :param docutils.nodes.paragraph node: the node represents the term
    :param str_or_unicode yomi: the string shows how to read or the term itself
    :rtype: list
    :return: the list of :class:`docutils.Node`
    
    Copied from :mod:`sphinx.domains.std` and modified.
    Called from :meth:`GosyuDirective.run`.
    """
    gosyu_entries = env.temp_data.setdefault('gosyu_entries', set())
    prefix = env.config['gosyu_anchor_prefix']

    termtext = node.astext()
    new_id = prefix + (nodes.make_id(termtext) or u'etc')
    if new_id in gosyu_entries:
        new_id += str(len(gosyu_entries))
    gosyu_entries.add(new_id)
    
    domain_obj[termtext] = env.docname, new_id, yomi

    # Because we don't want to make entries on 'genindex.html',
    # new_termnodes below doesn't contain the object 'node.index'.
    new_termnodes = []
    new_termnodes.extend(node.children)
    new_termnodes.append(addnodes.termsep())
    for termnode in new_termnodes:
        termnode.source, termnode.line = node.source, node.line

    return new_id, termtext, new_termnodes

def make_term_from_paragraph_node(termnodes, ids):
    """Copied function of :meth:`sphinx.domains.std.term_from_paragraph_node`
    
    Currently, no lines are modified.
    Called from :meth:`GosyuDirective.run`.
    """
    # make a single "term" node with all the terms, separated by termsep
    # nodes (remove the dangling trailing separator)
    term = nodes.term('', '', *termnodes[:-1])
    term.source, term.line = termnodes[0].source, termnodes[0].line
    term.rawsource = term.astext()
    term['ids'].extend(ids)
    term['names'].extend(ids)
    return term

# ========================================================
# Inheriting Directive class
# ========================================================

class GosyuDirective(ObjectDescription):
    """Yomigana featured version of sphinx.domains.std.Glossary

    The option :code:`yomimark` is added.
    """
    has_content = True
    required_arguments = 0
    optional_arguments = 0
    final_argument_whitespace = False
    option_spec = {
        'sorted': directives.flag,
        'yomimark': directives.single_char_or_whitespace_or_unicode
    }

    domainname = None #: can be '' which need to be distinguished with None.
 
    def run(self):
        """Inherit ObjectDescription.run, called by docutils

        Base codes are copied from :class:`sphinx.domains.std.Glossary`.
        """
        if self.domainname is None:
            if ':' in self.name:
                self.domainname, self.objtype = self.name.split(':', 1)
            else:
                self.domainname, self.objtype = '', self.name

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
                            2, 'gosyu term must be preceded by empty line',
                            source=source, line=lineno))
                    entries.append(([(line, source, lineno)], ViewList()))
                    in_definition = False
                # second term and following
                else:
                    if was_empty:
                        messages.append(self.state.reporter.system_message(
                            2, 'gosyu terms must not be separated by empty '
                            'lines', source=source, line=lineno))
                    if entries:
                        entries[-1][0].append((line, source, lineno))
                    else:
                        messages.append(self.state.reporter.system_message(
                            2, 'gosyu seems to be misformatted, check '
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
                        2, 'gosyu seems to be misformatted, check '
                    'indentation', source=source, line=lineno))
            was_empty = False

        # 
        yomimark = self.options.get('yomimark', None)
        d_objs = env.domaindata[self.domainname].setdefault('gosyu_indices', {})

        # now, parse all the entries into a big definition list
        items = []
        for terms, definition in entries:
            termtexts = []
            termnodes = []
            system_messages = []
            ids = []
            yomi1st = line1st = ''
            for line, source, lineno in terms:
                if not line1st:
                    line1st = line
                yomi = line
                if yomimark:
                    line_and_yomi = line.split(yomimark)
                    line = line_and_yomi[0]
                    if len(line_and_yomi) > 1:
                        yomi = line_and_yomi[1]
                        if not yomi1st:
                            yomi1st, line1st = yomi, line
                # parse the term with inline markup
                res = self.state.inline_text(line, lineno)
                system_messages.extend(res[1])

                # get a text-only representation of the term and register it
                # as a cross-reference target
                tmp = nodes.paragraph('', '', *res[0])
                tmp.source = source
                tmp.line = lineno
                new_id, termtext, new_termnodes = \
                    make_termnodes_from_paragraph_node(env, d_objs, tmp, yomi)
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
                          yomi1st or line1st))

        if 'sorted' in self.options:
            items.sort(key=lambda x:
                       _sort_order_obj.get_string_to_sort(x[2]))

        dlist = nodes.definition_list()
        dlist['classes'].append('gosyu')
        dlist.extend(item[1] for item in items)
        node += dlist
        return messages + [node]

# ========================================================
# Inheriting sphinx.domains.Index class
# ========================================================

class GosyuIndex(Index):
    """Index representation class supports yomigana(how to read)
    
    Pick the terms declared with :class:`GosyuDirective`
    (:code:`.. gosyu::`) and make the :file:`std-gosyu.html`.
    
    Support 2 options, :code:`gosyu_shortname` and :code:`gosyu_localname`
    given in :file:`conf.py`.
    """
    
    name = 'gosyu'
    localname = shortname = 'gosyu_dummy' #: overwritten  by __init__()
    
    def __init__(self, *args, **kwargs):
        super(GosyuIndex, self).__init__(*args, **kwargs)
        
        # During HTML generation these values pick from class,
        # not from instance so we have a little hack the system
        cls = self.__class__
        cls.shortname = self.domain.env.config['gosyu_shortname']
        cls.localname = self.domain.env.config['gosyu_localname']
    
    def generate(self, docnames=None):
        domaindata = self.domain.env.domaindata[self.domain.name]
        if 'gosyu_indices' not in domaindata:
            return [], False
        items = []
        for key, values in domaindata['gosyu_indices'].items():
            items.append((key, values))
        items.sort(key=lambda x: _sort_order_obj.get_string_to_sort(x[1][2]))
        groups = []
        prevHeading = ''
        for termtext, (docname, anchor, yomi) in items:
            heading = _sort_order_obj.get_group_name(yomi)
            if prevHeading != heading:
                g = list()
                groups.append([heading, g])
                prevHeading = heading
            g.append((termtext, 0, docname, anchor, None, u'', u''))
        return groups, False

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
        print ('gosyu.py: Using SortOrderLegacy.')

def setup(app):
    """Extend the Sphinx as we want, called from the Sphinx

    :param sphinx.application.Sphinx app: the object to add builder or something.
    """
    app.add_index_to_domain('std', GosyuIndex)
    app.add_directive_to_domain('std', 'gosyu', GosyuDirective)
    app.add_config_value('gosyu_shortname', u'用語集', True)
    app.add_config_value('gosyu_localname', u'用語集', True)
    
    # the default value should be ASCII, the anchor string can be written with
    # Non-Unicode.
    app.add_config_value('gosyu_anchor_prefix', u'yogo_', True)
    
    app.connect('builder-inited', determine_sort_order)
    app.setup_extension('sortorder')
    return {'version': '2.0.6', 'parallel_read_safe': False}
