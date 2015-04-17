# Translations
from modeltranslation.translator import translator, TranslationOptions

# models
from news.app.news.models import News, Category, Tag, Gallery, Attachment


class GalleryTranslation(TranslationOptions):
    fields = ('title', 'slug',)
translator.register(Gallery, GalleryTranslation)


class AttachmentTranslation(TranslationOptions):
    fields = ('name', 'slug',)
translator.register(Attachment, AttachmentTranslation)


class NewsTranslation(TranslationOptions):
    fields = ('title', 'slug', 'summary', 'content',)
translator.register(News, NewsTranslation)


class CategoryTranslation(TranslationOptions):
    fields = ('name', 'slug',)
translator.register(Category, CategoryTranslation)


class TagTranslation(TranslationOptions):
    fields = ('name', 'slug',)
translator.register(Tag, TagTranslation)