# -*- coding: utf-8 -*-

from django.db import models
from django.utils.translation import ugettext_lazy as _

from feincms.translations import TranslatedObjectMixin, Translation, TranslatedObjectManager

PERSON_CATEGORIES = (
    ('0', _("0")),
    ('1', _("1")),
)


class Person(models.Model, TranslatedObjectMixin):

    """
    Model of a team member.
    """
    title_prefix = models.CharField(
        max_length=127, blank=True, verbose_name=u"Titul před jménem", help_text=u"Například: Ing.")
    first_name = models.CharField(
        max_length=127, verbose_name=u"Jméno", help_text=u"Například: Martin")
    last_name = models.CharField(
        max_length=127, verbose_name=u"Příjmení", help_text=u"Například: Kocourek")
    title_suffix = models.CharField(
        max_length=127, blank=True, verbose_name=u"Titul za jménem", help_text=u"Například: PhD.")
    nick_name = models.SlugField(
        max_length=127, verbose_name=u"Nickname", help_text=u"Například: fanda")

    email = models.EmailField(
        blank=True, verbose_name=u"E-mail", help_text=u"Př.: martin.kocourek@contractis.cz")
    photo = models.ImageField(upload_to="team", blank=True, verbose_name=u"Fotografie",
                              help_text=u"Použijte obrázky ve formátu JPEG, GIF nebo PNG. Obrázky se automaticky zmenší na požadovaný rozměr.")
    category = models.CharField(max_length=127, verbose_name=u"Kategorie",
                                help_text=u"Pro členění na stránce.", default="1", choices=PERSON_CATEGORIES)
    sort_order = models.PositiveIntegerField(verbose_name=u"Pořadí", blank=True, null=True,
                                             help_text=u"Nepovinný údaj pro možnost vlastního řazení. Pokud má více zaměstnanců stejné pořadové číslo, řadí se zaměstnanci abecedně dle příjmení.")
    active = models.BooleanField(default=True, verbose_name=u"Je aktivní?",
                                 help_text=u"Neaktivní karty zaměstnance se nezobrazí na stránce.")

    objects = TranslatedObjectManager()

    class Meta:
        ordering = ['sort_order', 'last_name', ]
        verbose_name = _("Team member")
        verbose_name_plural = _("Team members")

    def full_name(self):
        return u'%s %s %s %s' % (self.title_prefix, self.last_name, self.first_name, self.title_suffix)

    @property
    def display(self):
        return u'%s %s' % (self.first_name, self.last_name)

    def get_absolute_url(self):
        from leonardo.module.web.widget.application.reverse import app_reverse
        return app_reverse(
            'project_team_detail',
            'team.apps.team',
            kwargs={
                'person_nick_name': self.nick_name,
            })

    def __unicode__(self):
        return u'%s %s' % (self.first_name, self.last_name)
        # return u'%s, %s' % (self.last_name, self.first_name)

CONTACT_CHOICES = (
    ("facebook", u"Facebook"),
    ("linkedin", u"LinkedIn"),
    ("twitter", u"Twitter"),
    ("github", u"Github"),
)


class PersonContact(models.Model):

    person = models.ForeignKey("Person", verbose_name=u"person", related_name="contacts")
    engine = models.CharField(
        u"Type", choices=CONTACT_CHOICES, max_length=255, blank=True)
    url = models.URLField(u"url", blank=True)

    def __unicode__(self):
        return self.person.__unicode__()


class PersonTranslation(Translation(Person)):

    """
    Translations for person.
    """
    position = models.CharField(_('position'), max_length=250, blank=True)
    summary = models.TextField(_('top text'), blank=True, null=True)
    description = models.TextField(_('bottom text'), blank=True, null=True)

    class Meta:
        verbose_name = _('text')
        verbose_name_plural = _('texts')

    def __unicode__(self):
        return self.position
