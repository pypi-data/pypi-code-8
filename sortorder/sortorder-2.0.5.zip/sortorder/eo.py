#
# -*- encoding: utf-8 -*-

"""
sortorder.eo.py
~~~~~~~~~~~~~~~
The order definition to sort Esperanto words.

:copyright: © 2011-2015 by Suzumizaki-Kimitaka(鈴見咲君高).
:license: 2-clause BSD

The language `esperanto` has 6 diacritical marked
alphabet. C^, G^, H^, J^, S^ and U with breve.

These characters ordered just after non marked chars,
such as C, G, H, J, S and U.
"""

import sortorder
import string

class SortOrderEo(sortorder.SortOrderBase):
    """The sort order for Esperanto

    Q, W, X and Y are not used as Esperanto words, but
    some acronym may be used without translating for
    Esperanto.
    """
    eo_uppercases = u"ĈĜĤĴŜŬ"
    diacriticalmark_target = u"CGHJSU"
    eo_alluppercases = string.ascii_uppercase + eo_uppercases

    def get_string_to_sort(self, entry_name):
        s = entry_name.upper()
        s = ''.join((self.insert_space_or_hat(x) for x in s))
        if s[:1] not in self.eo_alluppercases:
            return u"\uffff" + s
        return s

    def get_group_name(self, entry_name):
        s = self.get_string_to_sort(entry_name)
        if s[0] in self.eo_alluppercases:
            if s[1] == u" ":
                return s[0]
            idx = self.diacriticalmark_target.find(s[0])
            return self.eo_uppercases[idx]
        return u"Malalfabetoj"

    def insert_space_or_hat(self, c):
        """Return sortable string as Esperanto word.
        
        :param str_or_unicode c: the character, means len(c) == 1
        :rtype: str(Python 3) or unicode(Python 2)
        :return: converted string used for sorting
        
        The parameter c sholud be a character, means len(c) == 1.
        Return value is string which length is 2.
        This function returns U^ for Ŭ, used internal only.
        """
        idx = self.eo_uppercases.find(c)
        return c+u" " if idx==-1 else self.diacriticalmark_target[idx]+u"^"

def get_default_sort_order(cfg):
    """Return the sort order object defined in this module
    
    :param sphinx.config.Config cfg:
       you can give from Sphinx with :code:`app.config`,
       :code:`builder.config` etc.
    :rtype: SortOrderEo
    :return: the object of the class inherits SortOrderBase.

    Indend to be called by :meth:`sortorder.get_default_sort_order`.
    """
    return SortOrderEo()

def setup(app):
    """Extend the Sphinx as we want, called from the Sphinx

    :param sphinx.application.Sphinx app: the object to add builder or something.
    :rtype: None
    :return: None
    """
    sortorder.setup(app)
    app.add_config_value('sort_order', SortOrderEo(), 'env')
