from django.db import models
from django.db.models.fields.related import ManyToManyField
from django.db.models.loading import get_model
from django.utils import importlib
from django import forms
from assetcloud import app_settings


def metadata_form(metadata_model):

    class MetaDataForm(forms.ModelForm):
        class Meta:
            model = metadata_model
            exclude = ["asset"]

    return MetaDataForm


def get_class_from_string(class_path):
    module_name, class_name = class_path.rsplit(".", 1)
    module = importlib.import_module(module_name)
    return getattr(module, class_name)


def get_metadata_model_and_form_classes(asset_metadata_model):

    if isinstance(asset_metadata_model, tuple):
        model_class_path, form_class_path = asset_metadata_model
    else:
        model_class_path = asset_metadata_model
        form_class_path = None

    model_class = get_model(*model_class_path.split('.', 1))
    if form_class_path is not None:
        form_class = get_class_from_string(form_class_path)
    else:
        form_class = metadata_form(model_class)

    return model_class, form_class


def get_asset_metadata(asset):

    metadata = []

    for asset_metadata_model in app_settings.ASSET_METADATA_MODELS:
        metadata_model, metadata_form = get_metadata_model_and_form_classes(asset_metadata_model)
        metadata_model_instance = get_asset_metadata_for_metadata_model(asset, metadata_model)
        for field_name in metadata_model_instance._meta.get_all_field_names():
            if field_name not in ['asset', 'id']:
                field = metadata_model_instance._meta.get_field(field_name)

                if type(field) == ManyToManyField:
                    related_models = getattr(metadata_model_instance, field.name).all()
                    value = ", ".join([str(related_model) for related_model in related_models])
                else:
                    value = getattr(metadata_model_instance, field.name)

                metadata.append(
                    {
                        'label': field.verbose_name,
                        'name': field.name,
                        'value': value
                    })

    return metadata


def get_asset_metadata_for_metadata_model(asset, metadata_model):
    try:
        return metadata_model.objects.get(asset=asset)
    except metadata_model.DoesNotExist:
        return metadata_model(asset=asset)


class MetadataMeta(object):

    create_on_save = False

    def __init__(self, opts):
        if opts:
            for key, value in opts.__dict__.iteritems():
                setattr(self, key, value)


class MetadataMetaclass(models.base.ModelBase):
    """
    Optional Metaclass for Metadata models
    """

    def __new__(mcs, name, bases, attrs):
        new = super(MetadataMetaclass, mcs).__new__(mcs, name, bases, attrs)
        metadata_meta = attrs.pop('MetadataMeta', None)
        setattr(new, '_metadata_meta', MetadataMeta(metadata_meta))
        return new


class BaseMetadataModel(models.Model):
    """
    Optional Metaclass for Metadata models
    """
    __metaclass__ = MetadataMetaclass

    class Meta:
        abstract = True
