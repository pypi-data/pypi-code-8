#
# -*- encoding: utf-8 -*-

"""
sortorder.el.py
~~~~~~~~~~~~~~~
The order definition to sort (Modern) Greek words.

:copyright: © 2011-2015 by Suzumizaki-Kimitaka(鈴見咲君高).
:license: 2-clause BSD

Please check working correctly and fix if we need!
"""

import sortorder
import string

class SortOrderEl(sortorder.SortOrderLegacyLike):
    def etc_form(self):
        return u"Άλλο"

    def get_uppercases(self):
        return u"ΑΒΓΔΕΖΗΘΙΚΛΜΝΞΟΠΡΣΤΥΦΧΩ"

def get_default_sort_order(cfg):
    """Return the sort order object defined in this module
    
    :param sphinx.config.Config cfg:
       you can give from Sphinx with :code:`app.config`,
       :code:`builder.config` etc.
    :rtype: SortOrderEl
    :return: the object of the class inherits SortOrderBase.

    Indend to be called by :meth:`sortorder.get_default_sort_order`.
    """
    return SortOrderEl()

def setup(app):
    """Extend the Sphinx as we want, called from the Sphinx

    :param sphinx.application.Sphinx app: the object to add builder or something.
    :rtype: None
    :return: None
    """
    sortorder.setup(app)
    app.add_config_value('sort_order', SortOrderEl(), 'env')
