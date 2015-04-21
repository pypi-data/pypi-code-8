from django.db import models
from django.utils.translation import ugettext_lazy as _
from djangocms_text_ckeditor.fields import HTMLField


class Category(models.Model):
    name = models.CharField(_("Name"), max_length=255)
    slug = models.SlugField(_("Slug"), max_length=255)
    published = models.BooleanField(_("Published"), default=False)
    created_at = models.DateTimeField(_("Date created"), auto_now_add=True)
    updated_at = models.DateTimeField(_("Last edited"), auto_now=True)

    def __unicode__(self):
        return "%s" % self.name

    class Meta:
        verbose_name = _(u"Category")
        verbose_name_plural = _(u"Categories")


class Tag(models.Model):
    name = models.CharField(_("Tag name"), default=None, max_length=255)
    slug = models.SlugField(_("Slug"), max_length=255)
    created_at = models.DateTimeField(_("Date created"), auto_now_add=True)
    updated_at = models.DateTimeField(_("Last edited"), auto_now=True)

    def __unicode__(self):
        return "%s" % self.name

    class Meta:
        verbose_name = _(u"Tag")
        verbose_name_plural = _(u"Tags")


class Author(models.Model):
    name = models.CharField(_("Name"), default=None, max_length=255)
    slug = models.SlugField(_("Slug"), max_length=255)
    created_at = models.DateTimeField(_("Date created"), auto_now_add=True)
    updated_at = models.DateTimeField(_("Last edited"), auto_now=True)

    def __unicode__(self):
        return "%s" % self.name

    class Meta:
        verbose_name = _(u"Author")
        verbose_name_plural = _(u"Authors")


class News(models.Model):
    title = models.CharField(_("Title"), max_length=255)
    slug = models.SlugField(_("Slug"), max_length=255)
    author = models.ForeignKey(Author, blank=True, null=True, related_name="authors", verbose_name=_("Author"))
    summary = HTMLField(_("Summary"), blank=True, null=True)
    content = HTMLField(_("Content"), blank=True, null=True)
    category = models.ForeignKey(Category, related_name="news_category", verbose_name="Category")
    tag = models.ManyToManyField(Tag, blank=True, null=True, default=None, related_name="news_tags", verbose_name=_("Tag"))
    source_url = models.URLField(_("Source url"), blank=True, null=True)
    highlight = models.BooleanField(_("Highlight"), default=False)
    published = models.BooleanField(_("Published"), default=False)
    created_at = models.DateTimeField(_("Date created"), auto_now_add=True)
    updated_at = models.DateTimeField(_("Last edited"), auto_now=True)

    def __unicode__(self):
        return "%s" % self.title

    class Meta:
        verbose_name = _(u"Article")
        verbose_name_plural = _(u"News")


class Gallery(models.Model):
    news = models.ForeignKey(News, blank=True, null=True, default="", related_name="news_gallery", verbose_name=(_("For news")))
    title = models.CharField(_("Title"), default="", max_length=255)
    slug = models.SlugField(_("Slug"), default="", max_length=255)
    image = models.ImageField(_("Image"), blank=True, null=True, upload_to="uploads/news/images/")
    created_at = models.DateTimeField(_("Date created"), auto_now_add=True)
    updated_at = models.DateTimeField(_("Last edited"), auto_now=True)

    def __unicode__(self):
        return "%s" % self.title

    class Meta:
        verbose_name = _(u"Gallery")
        verbose_name_plural = _(u"Galleries")


class Attachment(models.Model):
    news = models.ForeignKey(News, blank=True, null=True, default="", related_name="news_attachments", verbose_name=(_("For news")))
    name = models.CharField(_("Name"), default="", max_length=255)
    slug = models.SlugField(_("Slug"), default="", max_length=255)
    attachment = models.FileField(_("File"), blank=True, null=True, upload_to="uploads/news/files/")
    created_at = models.DateTimeField(_("Date created"), auto_now_add=True)
    updated_at = models.DateTimeField(_("Last edited"), auto_now=True)

    def __unicode__(self):
        return "%s" % self.name

    class Meta:
        verbose_name = _(u"Attachment")
        verbose_name_plural = _(u"Attachments")