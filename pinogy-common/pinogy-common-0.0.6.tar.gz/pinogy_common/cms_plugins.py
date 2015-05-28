# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.core.exceptions import ImproperlyConfigured
from django.utils.translation import get_language_from_request


class ViewObjectPluginMixin(object):
    """
    This is very similar to Django's own DetailView, but for django CMS plugins.
    What we're doing here, is ultimately providing a `get_object` method that
    introspects the request object to determine which object should be returned.

    Key difference is that the `get_object` method relies on parameters, rather
    than class attributes to do its job. This allows the same methods to work
    for retrieving different objects in the same plugin.
    """

    def get_object_slug_field(self, request=None, slug_field=None):
        """
        Returns the name of the slug field to be used. Override as required for
        more dynamic cases.
        """
        return slug_field

    def get_queryset(self, request=None, model=None):
        """
        Get the queryset to look an object up against. May not be called if
        `get_object` is overridden.
        """
        if model:
            return model.objects.all()
        else:
            raise ImproperlyConfigured("Did not receive a queryset. Pass "
                "`model`, `queryset`, or override get_queryset().")

    def get_object(self, request, queryset=None, model=None, pk_url_kwarg=None,
                   slug_field="slug", slug_url_kwarg=None):
        if queryset is None:
            queryset = self.get_queryset(request, model)

        if request and request.resolver_match:
            kwargs = request.resolver_match.kwargs
            pk = kwargs.get(self.pk_url_kwarg, None)
            slug = kwargs.get(self.slug_url_kwarg, None)
            if pk is not None:
                queryset = queryset.filter(pk=pk)
                return queryset.first()
            if slug is not None:
                slug_field = self.get_object_slug_field(
                    request, slug_field)
                queryset = queryset.filter(**{"slug": slug_field})
                return queryset.first()
        return None


class TranslatableSlugMixin(object):
    """
    Very similar to the helper mixin from django-parler of the same name, this
    mixin enables ViewObjectPluginMixin to work with Parler-translated objects.
    """
    def get_language(self, request):
        return get_language_from_request(request)

    def get_object(self, request, queryset=None, model=None, pk_url_kwarg=None,
                   slug_field="slug", slug_url_kwarg=None):
        """
        Overrides the get_object method of ViewObjectPluginMixin to work with
        translated slugs.
        """
        if queryset is None:
            queryset = self.get_queryset(request, model)

        if request and request.resolver_match:
            kwargs = request.resolver_match.kwargs
            pk = kwargs.get(pk_url_kwarg, None)
            if pk is not None:
                return super(
                    TranslatableSlugMixin, self).get_object(request, queryset)
            slug = kwargs.get(slug_url_kwarg, None)
            if slug is not None:
                slug_field = self.get_object_slug_field(request, slug_field)
                queryset = queryset.active_translations(
                    language_code=self.get_language(request),
                    **{slug_field: slug})
                return queryset.first()
