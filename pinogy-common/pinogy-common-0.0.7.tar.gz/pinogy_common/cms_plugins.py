# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.db import models
from django.core.exceptions import ImproperlyConfigured
from django.utils.translation import get_language_from_request

from parler.models import TranslatableModel


class ViewObjectMixin(object):
    """
    This is very similar to Django's own DetailView, but for django CMS plugins.
    What we're doing here, is ultimately providing a `get_object` method that
    introspects the request object to determine which object should be returned.

    Key difference is that the `get_object` method relies on parameters, rather
    than class attributes to do its job. This allows the same methods to work
    for retrieving different objects in the same plugin.

    IMPORTANT NOTE: These method names differ from the CBV methods to prevent
    clobbering existing internal django CMS method names: `get_queryset` and
    `get_object` in particular.
    """

    def get_object_slug_field(self, request=None, slug_field=None):
        """
        Returns the name of the slug field to be used. Override as required for
        more dynamic cases.
        """
        return slug_field

    def get_object_queryset(self, request=None, model=None):
        """
        Get the queryset to look an object up against. May not be called if
        `get_object` is overridden. Override as required for more dynamic cases.
        """
        if model:
            return model.objects.all()
        else:
            raise ImproperlyConfigured("Did not receive a queryset. Pass "
                "`model`, `queryset`, or override get_object_queryset().")

    def get_view_object(self, request, queryset=None, model=None,
                        pk_url_kwarg=None, slug_field="slug",
                        slug_url_kwarg=None):
        """
        Given the paramaters provided, inspect the request object's
        `resolver_match` object to identify the desired type of object, look it
        up from the database and return it.
        """
        if queryset is None:
            queryset = self.get_object_queryset(request, model)

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


class ParlerViewObjectMixin(ViewObjectMixin):
    """
    Very similar to the TranslatableSlugMixin views helper mixin from django-
    parler, this mixin enables ViewObjectPluginMixin to work with Parler-
    translated objects.

    Since CMS Plugins may use this mixin to find objects whose lookup fields
    (slugs) could be translated or not, this mixin may pass control back to
    ViewObjectMixin again if the field it is looking up doesn't appear
    translated.
    """
    def get_language(self, request):
        return get_language_from_request(request)

    def _has_model_field(self, model, field_name):
        try:
            model._meta.get_field_by_name(field_name)
            return True
        except models.FieldDoesNotExist:
            return False

    def get_view_object(self, request, queryset=None, model=None,
                        pk_url_kwarg=None, slug_field="slug",
                        slug_url_kwarg=None):
        """
        Overrides the get_object method of ViewObjectPluginMixin to work with
        translated slugs.
        """

        slug_field = self.get_object_slug_field(request, slug_field)

        # Check that this is a parler.models.TranslatableModel model we're
        # working with. If not, pass control back to this mixin's super class,
        # which can handle non-translated objects fine.

        # TODO: Should also check that this model has a translations property,
        # which "contains" a field whose name matches `slug_field`.
        if not issubclass(model, TranslatableModel):
            return super(ParlerViewObjectMixin, self).get_view_object(request,
                queryset, model, pk_url_kwarg, slug_field, slug_url_kwarg)

        if queryset is None:
            queryset = self.get_object_queryset(request, model)

        if request and request.resolver_match:
            kwargs = request.resolver_match.kwargs
            pk = kwargs.get(pk_url_kwarg, None)
            if pk is not None:
                return super(
                    ParlerViewObjectMixin, self).get_object(request, queryset)
            slug = kwargs.get(slug_url_kwarg, None)
            if slug is not None:
                queryset = queryset.active_translations(
                    language_code=self.get_language(request),
                    **{slug_field: slug})
                return queryset.first()
