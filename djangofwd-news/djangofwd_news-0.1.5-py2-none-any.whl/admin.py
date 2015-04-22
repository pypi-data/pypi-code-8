from django.contrib import admin

# Models
from models import News, Category, Tag, Author, Gallery, Attachment

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
    list_display = ('title', 'author', 'category', 'highlight', 'published',)
    list_editable = ('category','highlight', 'published',)
    prepopulated_fields = {'slug': ('title',)}
    list_filter = ('published', 'category', 'created_at',)
    search_fields = ['title', 'category__name', 'author__name',]
admin.site.register(News, NewsAdmin)


class CategoryAdmin(TranslationAdmin):
    list_display = ( 'name', 'id',)
    readonly_fields = ('id',)
    prepopulated_fields = {'slug': ('name',)}
    list_filter = ('published', 'created_at',)
    search_fields = ['name',]
admin.site.register(Category, CategoryAdmin)


class TagAdmin(TranslationAdmin):
    list_display = ('name',)
    prepopulated_fields = {'slug': ('name',)}
    list_filter = ('created_at',)
    search_fields = ['name',]
admin.site.register(Tag, TagAdmin)


class AuthorAdmin(admin.ModelAdmin):
    list_display = ('name',)
    prepopulated_fields = {'slug': ('name',)}
    list_filter = ('created_at',)
    search_fields = ['name',]
admin.site.register(Author, AuthorAdmin)


