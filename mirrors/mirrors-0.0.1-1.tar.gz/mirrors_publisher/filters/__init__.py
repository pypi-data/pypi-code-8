import datetime
import json
import os

from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from django.utils.timezone import utc

from mirrors.serializers import ComponentSerializer
from mirrors.serializers import ComponentWithDataSerializer

from mirrors_publisher import backend_adapters
from mirrors_publisher.models import PublishReceipt


class ContentFilter(object):
    """Base class for filters.

    The variable ``component_types`` is list of regular expressions as strings
    that match the schemas that your plugin should operate on. Similarly,
    ``content_types`` will match the content types of the objects that your
    filter can be applied to.

    .. warning :: When you subclass this class you *must* remember to call
                  ``super().__init__(..)`` or else the plugin will not properly
                  register itself with the application.
    """
    schema_names = []
    content_types = []

    def __init__(self, *args, **kwargs):
        self.args = args
        self.kwargs = kwargs

    def apply(self, component):
        """The basic behavior of a filter - do nothing other than copy the data
        and the metadata using a :class:`BackendAdapter` to push it out to its
        final destination.

        :param component: the component
        :type component: :class:`Component`
        """

        data = component.binary_data

        adapter = backend_adapters.get_adapter()
        rel_path = os.path.join("{0:04d}".format(component.year),
                                "{0:02d}".format(component.month),
                                component.slug)

        if data is None:
            c_metadata = ComponentSerializer(component).data
        else:
            c_metadata = ComponentWithDataSerializer(component).data
            adapter.put(os.path.join(rel_path, 'data'), data)

        try:
            # Attempt to fetch the dateline
            receipt_qs = PublishReceipt.objects.filter(component=component)
            receipt = receipt_qs.order_by('publish_datetime').first()
            dateline = receipt.publish_datetime
        except ObjectDoesNotExist:
            # If we can't find a receipt for this component, then that means
            # this is the first time this has been published.
            dateline = datetime.datetime.utcnow().replace(tzinfo=utc)
        finally:
            c_metadata['dateline'] = dateline.strftime(
                settings.REST_FRAMEWORK['DATETIME_FORMAT'])

        adapter.put(os.path.join(rel_path, 'index.json'),
                    bytes(json.dumps(c_metadata), 'UTF-8'))
