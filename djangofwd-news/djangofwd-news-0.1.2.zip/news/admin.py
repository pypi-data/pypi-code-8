from django.contrib import admin

# Models
from news.app.news.models import News, Category, Tag, Author, Gallery, Attachment

# Translation
from modeltranslation.admin import TranslationAdmin


class GalleryInline(admin.TabularInline):
    model = Gallery
    prepopulated_fields = {'slug': ('title',)}
    extra = 0


class AttachmentInline(admin.TabularInline):
    model = Attachment
    prepopulated_fields = {'slug': ('name',)}
    extra = 0


class NewsAdmin(TranslationAdmin):
    inlines = (GalleryInline, AttachmentInline)
    list_display = ('title', 'author', 'category', 'published',)
    list_editable = ('category', 'published',)
    prepopulated_fields = {'slug': ('title',)}
admin.site.register(News, NewsAdmin)


class CategoryAdmin(TranslationAdmin):
    list_display = ('name',)
    prepopulated_fields = {'slug': ('name',)}
admin.site.register(Category, CategoryAdmin)


class TagAdmin(TranslationAdmin):
    list_display = ('name',)
    prepopulated_fields = {'slug': ('name',)}
admin.site.register(Tag, TagAdmin)


class AuthorAdmin(admin.ModelAdmin):
    list_display = ('name',)
    prepopulated_fields = {'slug': ('name',)}
admin.site.register(Author, AuthorAdmin)


