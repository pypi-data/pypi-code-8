import yaml
from django.db import models
from django.dispatch import receiver
from django.db.models import signals as model_signals
from django.utils.translation import ugettext_lazy as _
from django.template import loader

try:
    from django.template.backends.django import DjangoTemplates
    TEMPLATE_ENGINE = DjangoTemplates
except ImportError:  # Django < 1.8
    TEMPLATE_ENGINE = None


class Template(models.Model):

    slug = models.CharField(_(u"slug"), max_length=255, unique=True)
    data = models.TextField(_(u"content"))
    specs = models.TextField(_(u"specification"), default="")

    class Meta:
        verbose_name = _(u'template')
        verbose_name_plural = _(u'templates')

    def __unicode__(self):
        return self.slug

    def get_context_specs(self):
        return yaml.load(self.specs)['context']


@receiver(model_signals.post_save, sender=Template)
def on_save_template_invalidate_loader_cache(**kwargs):
    if TEMPLATE_ENGINE is None:
        from django.template.loader import template_source_loaders
        if not template_source_loaders:
            return
        loaders = template_source_loaders
    else:
        for engine in loader.engines.all():
            if not isinstance(engine, DjangoTemplates):
                return
            loaders = engine.engine.template_loaders

    for template_loader in loaders:
        template_loader.reset()
