import logging
import re

from django.core.exceptions import ObjectDoesNotExist
from django.core.management.base import BaseCommand, CommandError

from mirrors.models import Component, ComponentAttribute, ComponentRevision

from mirrors_publisher.exceptions import UnpublishedAttributeError
from mirrors_publisher.filters import ContentFilter
from mirrors_publisher.models import PublishReceipt

LOGGER = logging.getLogger(__name__)


class Command(BaseCommand):
    args = '<component slug> <year> <month>'
    help = 'Publish the given component'

    can_import_settings = True
    requires_system_checks = True

    def _get_filters(self, component):
        """Get all of the filters that should be applied to this particular
        :class:`Component`.

        :param component: the component
        :type component: :class:`Component`
        :rtype: `list`
        """
        useable_filters = []
        schema_name = component.schema_name
        content_type = component.content_type

        for filter in ContentFilter.__subclasses__():
            schemas = [re.compile(r) for r in filter.schema_names]
            content_types = [re.compile(r) for r in filter.content_types]

            if len([x for x in schemas if x.match(schema_name)]) == 0:
                # if none of the schema regexps in this filter match the
                # component, skip to the next filter
                continue

            if len([x for x in content_types if x.match(content_type)]) == 0:
                # as above, but for the content types
                continue

            useable_filters.append(filter())

        if len(useable_filters) == 0:
            # if no specialized filters exist for this component, just use the
            # generic one
            useable_filters.append(ContentFilter())

        return useable_filters

    def _publish_dependency_check(self, component):
        """Check to see if all of the :class:`Component`'s attributes have been
        published. Otherwise raise an :class:UnpublishedAttributeError.

        :param component: the component to check
        :type component: :class:`Component`

        :raises: :class:`UnpublishedAttributeError`
        :raises: :class:`ObjectDoesNotExist`"""
        # before publishing, ensure that all the component's
        # attributes have also been published
        component_attrs = component.attributes.values_list('pk', flat=True)
        attrs_receipts = PublishReceipt.objects.filter(pk__in=component_attrs)

        for attr_pk in component_attrs:
            if attr_pk not in attrs_receipts:
                attr = ComponentAttribute.objects.get(pk=attr_pk)
                raise UnpublishedAttributeError(missing_attribute=attr)

    def handle(self, *args, **kwargs):
        if len(args) != 3:
            raise CommandError('three arguments expected: slug year month')

        slug = args[0]
        try:
            year = int(args[1])
            month = int(args[2])

            if year < 0 or month < 0:
                raise ValueError()
        except ValueError:
            raise CommandError('year and month must be valid integers')

        try:
            component = Component.objects.get(slug=slug,
                                              year=year,
                                              month=month)
        except ObjectDoesNotExist:
            raise CommandError('the component does not exist')

        try:
            self._publish_dependency_check(component)
        except ObjectDoesNotExist as ex_odne:
            # we should log this exception and then just pass it along because
            # something very weird and bad happened
            self.stdout.write('Unable to get component attribute!')
            raise ex_odne
        except UnpublishedAttributeError as ex_uae:
            raise CommandError(
                "Unable to publish because component publishing dependencies "
                "have not been met: attribute {} not yet published".format(
                    ex_uae.missing_attribute.name))

        filters = self._get_filters(component)
        for f in filters:
            f.apply(component)

        try:
            cur_rev = component.revisions.order_by('-version').first()
        except ComponentRevision.DoesNotExist:
            raise CommandError('Unable to get component\'s current revision')

        PublishReceipt.objects.create(component=component, revision=cur_rev)
