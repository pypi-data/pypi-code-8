#
# -*- encoding: utf-8 -*-

"""
sortorder.ru.py
~~~~~~~~~~~~~~~
The order definition to sort Russian words.

:copyright: © 2011-2015 by Suzumizaki-Kimitaka(鈴見咲君高).
:license: 2-clause BSD

Please check working correctly and fix if we need!
"""

import sortorder
import string

class SortOrderRu(sortorder.SortOrderLegacyLike):
    def etc_form(self):
        return u"Другой"

    def get_uppercases(self):
        return u"АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ"

def get_default_sort_order(cfg):
    """Return the sort order object defined in this module
    
    :param sphinx.config.Config cfg:
       you can give from Sphinx with :code:`app.config`,
       :code:`builder.config` etc.
    :rtype: SortOrderRu
    :return: the object of the class inherits SortOrderBase.

    Indend to be called by :meth:`sortorder.get_default_sort_order`.
    """
    return SortOrderRu()

def setup(app):
    """Extend the Sphinx as we want, called from the Sphinx

    :param sphinx.application.Sphinx app: the object to add builder or something.
    :rtype: None
    :return: None
    """
    sortorder.setup(app)
    app.add_config_value('sort_order', SortOrderRu(), 'env')
