from django.db import models
from hvad.models import TranslatableModel, TranslatedFields, TranslationManager
from jsonfield import JSONField
from .debug import WrongMenuFormatException
from django.conf import settings
from django.template.defaultfilters import slugify
from mptt.models import MPTTModel, TreeForeignKey
from .noconflict import classmaker
from .signals import menu_created


class MenuManager(TranslationManager):
    def get_queryset(self, *args, **kwargs):
        return super(MenuManager, self).get_queryset(*args, **kwargs)

    def add_menu(self, titles, plugin=None, user=None, **defaults):
        default_locale = settings.LANGUAGE_CODE.split('-')[0]
        try:
            assert default_locale in list(titles.keys())
        except AssertionError:
            raise WrongMenuFormatException('Title keys must contain default locale (%s)' % default_locale)
        try:
            assert plugin in settings.INSTALLED_APPS
        except AssertionError:
            raise WrongMenuFormatException('plugin parameter must be listen in INSTALLED_APPS')
        menu = Menu.objects.create(plugin=plugin, **defaults)
        for lang, title in list(titles.items()):
            menu.translate(lang)
            menu.title = title
            menu.path = '/%s/' % slugify(title)
            if 'parent' in list(defaults.keys()):
                menu.path = defaults['parent'].path + menu.path[1:]
            menu.save()

        menu_created.send(self.__class__, menu=menu, user=user)
        return menu


class Menu(TranslatableModel, MPTTModel, metaclass=classmaker()):
    """
    login_required: Is this menu public accessable
    parent: The parent menu
    plugin: Which apps urlconf to use?
    weight: The weight of the menu item. Items in the same level are ordered by weight
    """
    login_required = models.BooleanField(default=False)
    parent = TreeForeignKey('self', null=True, blank=True, related_name='children')
    plugin = models.CharField(max_length=100, blank=True, null=True)
    weight = models.SmallIntegerField(default=0)
    parameters = JSONField(blank=True, null=True)
    translations = TranslatedFields(
        path = models.CharField(max_length=255),
        title = models.CharField(max_length=100),
        meta = {'unique_together': [('path', 'language_code')]},
    )
    handler = MenuManager()

    def __str__(self):
        return self.title
