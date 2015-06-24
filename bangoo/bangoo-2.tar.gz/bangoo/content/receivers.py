# coding: utf-8

from django.utils import timezone

from bangoo.content.models import Content


def menu_created_callback(sender, **kwargs):
    menu = kwargs['menu']

    if menu.plugin != 'bangoo.content':
        return

    #author = kwargs['user']
    content = Content.objects.create(published=timezone.now())

    #content.authors.add(author)

    for menu_trans in menu.translations.all():
        content.translate(menu_trans.language_code)
        content.title = menu_trans.title
        content.url = menu_trans.path
        content.text = ''
        content.save()
