#
# -*- coding: utf-8 -*-

"""
sortorder.__init__.py
~~~~~~~~~~~~~~~~~~~~~

The Sphinx extension to provide sort order.

:copyright: © 2011-2015 by Suzumizaki-Kimitaka(鈴見咲君高)
:license: 2-clause BSD

You can define :file:`sort_order_LANG.py` to give new order for indices
to replace the default order.

Any :file:`sort_order_LANG.py` should have the method
:meth:`get_default_sort_order`
The method should return the object which inherits :class:`SortOrderBase`.
"""

import unicodedata
import string
import sys
import six

class SortOrderBase(object):
    """Base class of any SortOrder-s

    Any sort order classes should inherit this class.
    You can refer :file:`sortorder/xx.py` as the sample implementation.
    You may want to inherit :class:`SortOrderLegacy` or
    :class:`SortOrderLegacyLike` instead of this class.
    """

    def get_string_to_sort(self, entry_name):
        """Return the string for sorting instead of given name

        :param str_or_unicode entry_name: the name of the entry
        :rtype: str(Python 3), unicode(Python 2)
        :return: the internal sort key, should be sortable each other

        All inheriting class may override this function.

        Return the internal sort key refering the given name.
        
        The internal sort key should be sortable with the unicode
        codepoint order. For example, when your indices have the
        group "Etc." or "Symbols", the return value from this function
        should have the group marker character prefix against such 
        entries.
        
        Like above, when unfortunately your grouping cannot unify 
        single range of the unicode codepoint, the return value also
        should have prefix.
        
        You can just return the entry_name if you don't have to give
        internal sort key.
        
        Check the implementation of :class:`SortOrderLegacy`.
        You may want to inherit that class to ignore cases or so.
        """
        return entry_name

    def get_group_name(self, entry_name):
        """Return the group name of the given entry

        :param str_or_unicode entry_name: the name of the entry
        :rtype: str(Python 3), unicode(Python 2)
        :return: the name of the group which the given name belongs to

        Grouping itself should be done by :meth:`get_string_to_sort`
        function.
        See the implementation of :class:`SortOrderLegacy`.
        """
        return entry_name[0]


class SortOrderLegacy(SortOrderBase):
    """Perform sort order given like Sphinx 1.0.7 or prior"""

    def get_string_to_sort(self, entry_name):
        """Return the string for sorting instead of given name
        
        To make the grouping done, making lowercased,
        'NFD' normalization and prepend prefix to symbols.
        """
        lcletters = string.ascii_lowercase + '_'
        lckey = unicodedata.normalize('NFD', entry_name.lower())
        if lckey[0:1] in lcletters:
            return chr(127) + lckey
        return lckey

    def get_group_name(self, entry_name):
        """Return the group name of the given entry

        This class/function gives just only English specific
        sort order. The alphabet is limited only in ascii and
        force all characters NFD normalization.
        """        
        letters = string.ascii_uppercase + '_'
        letter = unicodedata.normalize('NFD', entry_name)[0].upper()
        if letter in letters:
            return letter
        else:
            return 'Symbols'


class SortOrderLegacyLike(SortOrderBase):
    """Base class for lauguages similar to latin."""

    def get_string_to_sort(self, entry_name):
        """Return the string to sort"""
        s = unicodedata.normalize('NFD', entry_name).upper()
        if s[:1] not in self.get_uppercases():
            return u"\uffff" + s
        return s

    def get_group_name(self, entry_name):
        """Return the group name of the given entry"""
        s = self.get_string_to_sort(entry_name)
        if s[0] in self.get_uppercases():
            return s[0]
        return self.etc_form()

    def etc_form(self):
        """Return the word 'etc.' in your language

        Override this.
        """
        return u"Etc."

    def get_uppercases(self):
        """Return uppercased characters used in your language

        Override this.
        """
        return string.ascii_uppercase


def get_default_sort_order(cfg):
    """Return the default sort order of the language given in conf.py

    :param sphinx.config.Config cfg:
       you can give from Sphinx with :code:`app.config`,
       :code:`builder.config` etc.
    :rtype: SortOrderBase
    :return: the object of the class inherits SortOrderBase.
    :seealso: :meth:`get_sort_order`

    Indend to be called by another extensions.
    """
    if isinstance(cfg, str):
        lang = cfg
    else:
        try:
            lang = cfg.language
        except:
            lang = None
    if not lang:
        e = ('sortorder.__init__.py: '
             'Neither the language identifier nor sphinx.config'
             'are not given. using SortOrderLegacy.')
        print (e)
        return SortOrderLegacy()
    try:
        six.exec_('import sort_order_{0} as local_order;'.format(lang), globals())
    except ImportError:
        try:
            six.exec_('import sortorder.{0} as local_order;'.format(lang), globals())
        except ImportError:
            e = ('sortorder.__init__.py: '
                 'both sort_order_{0} and sortorder.{0}'
                 ' not found. using SortOrderLegacy.')
            print (e.format(lang))
            return SortOrderLegacy()
    return local_order.get_default_sort_order(cfg)

def get_sort_order(cfg):
    """Return :class:`SortOrderBase` object depends on given Sphinx configure

    :param sphinx.config.Config cfg:
       you can give from Sphinx with :code:`app.config`,
       :code:`builder.config` etc.
    :rtype: SortOrderBase
    :return: the object of the class inherits SortOrderBase.

    Convenient function of :meth:`get_default_sort_order`.
    Indend to be called by another extensions.
    
    When :code:`cfg.sort_order` has :class:`SortOrderBase`, just return it.
    Otherwise, return :meth:`get_default_sort_order`.
    """
    try:
        r = cfg.sort_order
        try:
            assert isinstance(r, SortOrderBase)
            return r
        except:
           print ('sortorder.__init__.py: '
                  'config "sort_order" should be'
                  'the object of SortOrderBase.') 
    except:
        pass
    return get_default_sort_order(cfg)

def setup(app):
    """Placeholder method called by the Sphinx document generator

    :param sphinx.application.Sphinx app: the object to extend the Sphinx

    Just place holder. do nothing.
    """
    return {'version': '2.0.6', 'parallel_read_safe': False}
    
