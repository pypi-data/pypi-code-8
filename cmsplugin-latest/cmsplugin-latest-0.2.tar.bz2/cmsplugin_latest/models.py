from cms.models.pluginmodel import CMSPlugin
from django.conf import settings
from django.core.exceptions import FieldError

from django.db import models
from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

from cmsplugin_latest.utils import *

from django import forms
import django

import logging, pprint
logger = logging.getLogger('cmsplugin_latest')

class Latest(CMSPlugin):
    
    def __init__(self, *args, **kwargs):
        super(Latest, self).__init__(*args, **kwargs)
        
    def save(self, *args, **kwargs):
        logger.debug("Saving %s"%self)
        instance = super(Latest, self).save(*args, **kwargs)
        return instance
    
    def copy_relations(self, oldinstance):
        logger.debug("Copying relation %s"%type(oldinstance))
        for order_by in oldinstance.order_by.all():
            # instance.pk = None; instance.pk.save() is the slightly odd but
            # standard Django way of copying a saved model instance
            logger.debug("Copying relation to %s"%order_by)
            order_by.pk = None
            order_by.plugin = self
            order_by.save()
            logger.info("Successfully saved %s"%order_by)
        
    def __unicode__(self):
        return unicode(self.__class__.__name__ +
            ' [' + ','.join([str(s) for s in self.orderby_set.all() ]) + ']')

    def get_latest(self):
        """ Get all the OrderBys for this latest. Return an OrderByProxy
        instance, which will convert the model CharField to an actual model
        instance.
        """
        for orderby in self.orderby_set.all():
            ModelClass = get_model_by_name(orderby.model)
            
            # If we don't catch this error we'll be locked out.
            object_set = ModelClass.objects.all().order_by(orderby.field)
            
            proxies = []
                
            try:
                for o in object_set:
                    logger.debug("Yielding OrderByProxy(%s, %s)"%(o,
                                                        orderby.template))
                    proxies.append(OrderByProxy(o, orderby.template))
            except FieldError as e:
                logger.error(e)
                return
            #proxies.sort()
            return proxies
            
class JSAttachedCharField(models.CharField):
    
    def __init__(self, *args, **kwargs):
        self.js_callbacks = kwargs.pop('js_callbacks', None)
        if not self.js_callbacks:
            pass
            #logger.error("js_callbacks is null!")
        super(JSAttachedCharField, self).__init__(*args, **kwargs)
    
    def formfield(self, *args, **kwargs):
        field = super(JSAttachedCharField, self).formfield(*args, **kwargs)
        field.widget.attrs.update(self.js_callbacks)
        return field

class OrderByProxy(object):
    def __init__(self, instance, template):
        self.instance = instance
        self.template = template
        
    #def __unicode__(self):
        #return "%s <%s>"%(type(self.instance), self.template)
    
    #def __str__(self):
        #return unicode(self)

class OrderBy(models.Model):
    
    model = JSAttachedCharField(max_length=100,
        choices=get_model_choices(),
        js_callbacks = {
            'onChange' : 'updateFieldField(this)',
        },
        default='')
        
    field = models.CharField(max_length=100,
        choices=get_all_available_fields_choices(),
        default='',
        help_text=_("The 'order by' field to determine "+
            "the latest entries."))

    template = models.CharField(max_length=200,
            choices=getattr(settings, 'CMSPLUGIN_LATEST_TEMPLATES', []),
            help_text=_("What will be rendered on the page."))
            
    latest = models.ForeignKey(Latest)
    
    def __init__(self, *args, **kwargs):
        super(OrderBy, self).__init__(*args, **kwargs)
        #logger.debug("Creating OrderBy!")
        
    def __unicode__(self):
        if self.field:
            return '%s (order by "%s")'%(self.model, self.field)
        return '<%s %s>'%(self.__class__.__name__, self.model)
        
    #def save(self, *args, **kwargs):
        #logger.debug("Saving %s"%self)
        #instance = super(OrderBy, self).save(*args, **kwargs)
        #return instance
    
    #def __lt__(self, other):
        #f_self = getattr(self.model, self.field)
        #f_other = getattr(other.model, other.field)
        #return f_self < f_other
    
    #def __eq__(self, other):
        #f_self = getattr(self.model, self.field)
        #f_other = getattr(other.model, other.field)
        #return f_self == f_other
    
    #def __gt__(self, other):
        #return not self.__lt__(other)
    
class LatestInline(admin.TabularInline):
        
    model = OrderBy
    fk_name = 'latest'
    extra = 1
    
    def __init__(self, *args, **kwargs):
        super(LatestInline, self).__init__(*args, **kwargs)
        #logger.info("Created a new %s"%(type(self)))
        
    #def save_model(self, request, obj, form, change):
        # TODO
