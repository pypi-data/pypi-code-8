# -*- coding: utf-8 -*-
"""
Created on 2014/11/18

@author: nagai
"""

__author__ = 'nagai'

from plone import api
from Acquisition import aq_inner
from Products.Five.browser import BrowserView
from Products.CMFCore.utils import getToolByName
from ngi.notify.datadog import _
from ngi.notify.datadog import dd_msg_pool
from ngi.notify.datadog.dd import (metric_datadog,
                                   event_datadog)


class CronDatadog(BrowserView):

    def __call__(self):

        context = self.context
        request = context.REQUEST

        #pool data
        global dd_msg_pool
        if dd_msg_pool:
            for x in dd_msg_pool:
                if x['type'] == 'dd_event':
                    event_datadog(
                        x['title'],
                        x['text'],
                        date_happened=x['date_happened'],
                        tags=x['tags']
                    )
                elif x['type'] == 'dd_metric':
                    metric_datadog(
                        x['metric_name'],
                        x['value'],
                        tags=x['tags']
                    )
            dd_msg_pool = []

        #DB size
        metric_name = 'plone.db_info'
        db_name, value = self.db_info()
        db_tags = dict(db_name=db_name)
        metric_datadog(metric_name, value=value, tags=db_tags)

        #Content count by types
        self.content_count()

        return True

    def db_info(self):
        context = aq_inner(self.context)
        cpanel = context.unrestrictedTraverse('/Control_Panel')
        return cpanel.db_name(), float(cpanel.db_size()[0:-1])

    def _content_count(self, portal_type):
        base_query = {}
        portal_catalog = getToolByName(self.context, 'portal_catalog')
        base_query['portal_type'] = portal_type
        results = portal_catalog(base_query)
        return len(results)

    def content_count(self):

        metric_name = 'plone.portal_types'
        context = self.context

        portal_types = getToolByName(context, "portal_types")
        types = portal_types.listContentTypes()
        for t_id in types:
            title = portal_types[t_id].title
            value = self._content_count(t_id)
            tags = dict(portal_type=t_id, title=title)
            metric_datadog(metric_name, value=value, tags=tags, metric_type=u'histogram')