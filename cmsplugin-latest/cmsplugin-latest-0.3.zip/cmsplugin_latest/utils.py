
from django.apps import apps as django_apps
from django.contrib.admin import site

from django.core.exceptions import AppRegistryNotReady

import logging, pprint
logger = logging.getLogger('cmsplugin_latest')

def get_models():
    """ Get a list of all model names reigstered for the current site.
    """
    return site._registry.keys()

def get_model_name(app_model):
    """ Get the short name (e.g. 'user') for the model.
    """
    return app_model._meta.model_name

def get_model_title(app_model):
    """ Get the human-readable title (e.g. 'User') for the model.
    """
    return app_model._meta.verbose_name.title()
    
def get_model_choices():
    """ Get a list of choices for the model. This will be yielded as a list
    of tuples, where each tuple is a model name and model title.
    """
    yield ('', '')
    for app_model in get_models():
        yield (get_model_name(app_model), get_model_title(app_model))

def get_fields_for_model(model):
    """ Get a list of fields for this model.
    """
    if not model:
        yield None
    logger.debug("Fields for model %s:"%model)
    for f in model._meta.local_fields:
        logger.debug("\t-%s"%f.attname)
        yield f.attname
    
def get_model_by_name(name):
    """ Given a model name (e.g. 'user'), get the model class.
    """
    for app_model in get_models():
        if (app_model._meta.model_name == name):
            return app_model
    return None
    
def get_model_field_choices(model):
    yield ['', '']
    for f in list(get_fields_for_model(model)):
        yield [unicode(f), unicode(f)]
        
def get_all_available_fields():
    for m in get_models():
        for f in list(get_fields_for_model(m)):
            yield(f)
            
def get_all_available_fields_choices():
    all_fields = list(get_all_available_fields())
    for f in all_fields:
        yield[unicode(f), unicode(f)]
    
def get_model_field_choices_flattened(model):
    choices = list(get_model_field_choices(model))
    logger.debug("Choices: %s"%choices)
    return ';'.join([','.join(i) for i in choices])
