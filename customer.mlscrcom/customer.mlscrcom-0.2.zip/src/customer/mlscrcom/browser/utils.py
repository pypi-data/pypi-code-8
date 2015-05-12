# -*- coding: utf-8 -*-

###############################################################################
#
# Copyright (c) 2011 Propertyshelf, Inc. and its Contributors.
# All Rights Reserved.
#
# This program is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License version 2 as published by the
# Free Software Foundation.
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE. See the GNU General Public License for more
# details.
#
# You should have received a copy of the GNU General Public License along with
# this program; if not, write to the Free Software Foundation, Inc.,
# 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.
#
###############################################################################
"""Custom Browser view to generate JS for customer.mlscrcom."""

from zope.publisher.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from zope.i18n import translate
from customer.mlscrcom.i18n import _


class translations(BrowserView):
    """Generates a JS File with needed translations for searchmask"""

    def __call__(self, REQUEST, RESPONSE):
        RESPONSE.setHeader('Content-Type', 'application/javascript')
        #get all languages in portal
        langs = self.context.portal_languages.portal_languages.getAvailableLanguages().keys()
        #javascript output strings
        js_all_lang = ''
        js_content_array = 'var contents = new Array(); '

        #loop all languages
        for one_lang in langs:
            #Generate a proper js array list string
            if(len(js_all_lang) < 1):
                js_all_lang += '"%s"' % one_lang
            else:
                js_all_lang += ', "%s"' % one_lang
            #generate string for building the js contents array
            js_content_array += 'contents["%s"] = new Array(); ' % one_lang
            js_content_array += 'contents["%s"]["text_UnselectAll"] = "%s"; ' % (one_lang, translate(_(u'searchpage_unselectall', 'unselect all'), 'customer.mlscrcom', target_language=one_lang))
            js_content_array += 'contents["%s"]["text_All"] = "%s"; ' % (one_lang, translate(_(u'searchpage_all', 'All'), 'customer.mlscrcom', target_language=one_lang))
            js_content_array += 'contents["%s"]["text_Selected"] = "%s"; ' % (one_lang, translate(_(u'searchpage_selected', 'Selected'), 'customer.mlscrcom', target_language=one_lang))
            js_content_array += 'contents["%s"]["text_Default"] = "%s"; ' % (one_lang, translate(_(u'searchpage_default', 'Default'), 'customer.mlscrcom', target_language=one_lang))

        js_array = 'var langs = new Array(%s); ' % (js_all_lang)
        js_array += js_content_array
        return js_array


