from zope import schema
from zope.interface import Interface
from z3c.form import interfaces
from z3c.form.interfaces import IFileWidget
from zope.interface import alsoProvides
from plone.directives import form
from plone.autoform.interfaces import IFormFieldProvider
from medialog.controlpanel.interfaces import IMedialogControlpanelSettingsProvider

from collective.z3cform.datagridfield import DataGridFieldFactory 
from collective.z3cform.datagridfield.registry import DictRow

 

from zope.i18nmessageid import MessageFactory

_ = MessageFactory('medialog.dexterityview')


class IDexterityViewLayer(Interface):
    """A layer specific to medialog.dexterityview
        """

class IContentPair(form.Schema):
    content_type = schema.ASCIILine(
        title=_(u'content_type', 'Content type'), 
        required=False
    )
        
    image_scale = schema.Choice(
        title=_(u"imagesize", default=u"image Size"),
        vocabulary = 'medialog.dexterityview.ImageSizeVocabulary',
        required = True,
        description=_(u"help_imagesize",
            default=u"Set  size for image")
    )
    
    block_fields = schema.ASCIILine(
        title=_(u'block_fields', 'Fields to block'),
        required=False
    )
    


class IDexterityViewSettings(form.Schema):
    """Adds settings to medialog.controlpanel
        """
    form.fieldset(
        'dexterity_view',
        label=_(u'Dexterity View'),
            fields=[
                    'content_pairs',
            ],
    )
    
    form.widget(content_pairs=DataGridFieldFactory)
    content_pairs = schema.List(
        title = _(u"content_pairs", 
            default=u"Content type and fields blocked"),
        value_type=DictRow(schema=IContentPair),
    )
    
                
alsoProvides(IDexterityViewSettings, IMedialogControlpanelSettingsProvider)


