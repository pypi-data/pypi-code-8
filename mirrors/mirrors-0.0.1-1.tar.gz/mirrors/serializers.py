import json
import logging

from django.contrib.auth.models import User

from rest_framework import serializers
from mirrors.models import Component
from mirrors.models import ComponentLock
from mirrors.models import ComponentAttribute
from mirrors.models import ComponentRevision


LOGGER = logging.getLogger(__name__)


class WritableSerializerMethodField(serializers.SerializerMethodField):
    """A field that gets and sets its value by calling a method on the serializer
    it's attached to.
    """

    def __init__(self, get_method_name, set_method_name, *args, **kwargs):
        self.read_only = False
        self.get_method_name = get_method_name
        self.method_name = get_method_name
        self.set_method_name = set_method_name
        self.required = kwargs.pop('required', False)

        super().__init__(get_method_name,
                         *args,
                         **kwargs)

    def field_from_native(self, data, files, field_name, into):
        return getattr(self.parent, self.set_method_name)(data,
                                                          files,
                                                          field_name,
                                                          into)


class JSONSerializerField(serializers.CharField):
    """A serializer field that contains a JSON object."""

    def to_native(self, value):
        """Convert the value of the field from a JSON-encoded string into a
        Python `dict`, if it is a `str`.
        """

        if isinstance(value, dict):
            return value
        else:
            return json.loads(value)

    def from_native(self, data):
        """Convert a Python `dict` into a JSON-encoded string so that it can
        be stored in the database.
        """

        if isinstance(data, dict):
            return json.dumps(data)

        return data


class ComponentSerializer(serializers.ModelSerializer):
    """Used for turning a JSON blob into a :class:`mirrors.models.Component`
    object, and back again.
    """

    created_at = serializers.DateTimeField(read_only=True)
    updated_at = serializers.DateTimeField(read_only=True)
    revisions = serializers.RelatedField(many=True, read_only=True)
    attributes = serializers.SerializerMethodField('_get_attributes')
    metadata = WritableSerializerMethodField('_get_metadata',
                                             '_set_metadata')

    _version = None
    # this is used to store the metadata that gets submitted as part of the
    # post process so that we can save it the correct way by overriding
    _metadata = None

    class Meta:
        model = Component
        fields = ('slug', 'metadata', 'content_type', 'created_at',
                  'updated_at', 'schema_name', 'revisions', 'attributes')

    def __init__(self, *args, **kwargs):
        self._version = kwargs.pop('version', None)
        super().__init__(*args, **kwargs)

    def save_object(self, obj, **kwargs):
        """Save the data in this object to the database, including any metadata
        that may have been passed to it through ``__init__()``.

        :param obj: the object we want to commit to the database
        :type obj: :class:`ComponentSerializer`
        """
        super().save_object(obj, **kwargs)

        if self._metadata is not None:
            self.object.new_revision(metadata=self._metadata)
            self._metadata = None

    def restore_object(self, attrs, instance=None):
        """Given a dictionary of deserialized field values, either update an existing
        model instance, or create a new model instance.

        :param attrs: the the key/value pairs (generally made by loading a JSON
                      blob from the client) that represent the fields of a
                      ``Component`` object
        :type attrs: dict

        :param instance: an optional instance of a ``Component``. If this is
                         set, then the values of `attrs` will be used update
                         it, rather than to create a new ``Component``.
        :type instance: :class:`mirrors.models.Component`
        :rtype: :class:`mirrors.models.Component`

        """
        if instance is not None:
            instance.content_type = attrs.get('content_type',
                                              instance.content_type)
            instance.schema_name = attrs.get('schema_name',
                                             instance.schema_name)
            return instance

        return Component(**attrs)

    def transform_metadata(self, obj, val):
        """Transform the contents of `metadata` from a string into a dict.

        :param obj: reference to an instance of ``CompenentSerializer``
        :type obj: :py:class:`CompenentSerializer`
        :param val: the current value of `metadata`
        :type val: str or dict

        :rtype: dict

        """
        if isinstance(val, str):
            return json.loads(val)
        else:
            return val

    def _get_metadata(self, obj):
        if obj is None:
            return {}

        try:
            if self._version is not None and self._version != 0:
                return obj.metadata_at_version(self._version)
            else:
                return obj.metadata
        except IndexError as e:
            if str(e) == 'No such version':
                return {}

    def _set_metadata(self, data, *args, **kwargs):
        if 'metadata' in data:
            self.validate_metadata(data, 'metadata')
            self._metadata = data['metadata']

    def validate_metadata(self, attrs, source):
        if source not in attrs:
            return attrs

        if not isinstance(attrs[source], dict):
            try:
                attrs[source] = json.loads(attrs[source])
            except Exception:
                raise serializers.ValidationError("This field must be a JSON "
                                                  "object")

        return attrs

    def _get_attributes(self, obj):
        result = {}
        # not all DB backends support DISTINCT ON, so just get a flat list of
        # all the attributes' names, then turn them into a set and then back
        # into a list so that we remove all of the dupes
        attribute_names = list(set(obj.attributes.values_list('name',
                                                              flat=True)))

        for n in attribute_names:
            attr = obj.get_attribute(n)

            if isinstance(attr, list):
                result[n] = [ComponentSerializer(a).data for a in attr]
            elif attr is None:
                result[n] = None
            else:
                result[n] = ComponentSerializer(attr).data

        return result


class ComponentWithDataSerializer(ComponentSerializer):
    """This is the exact same thing as a :py:class:`ComponentSerializer` but with
    the added presence of the data_uri field, which is the URI that corresponds
    to the component's binary data.
    """
    data_uri = serializers.URLField(read_only=True)

    class Meta:
        model = Component
        fields = ('slug', 'metadata', 'content_type', 'created_at',
                  'updated_at', 'schema_name', 'revisions', 'data_uri',
                  'attributes')


class AutocompleteComponentSerializer(serializers.ModelSerializer):
    """This is a sort of stripped down version of the
    :py:class:`ComponentSerializer` designed to have only the data necessary
    for use with autocomplete text boxes.
    """
    data_uri = serializers.URLField(read_only=True)
    metadata = JSONSerializerField(source='current_metadata')

    class Meta:
        model = Component
        fields = ('slug', 'data_uri', 'metadata')


class ComponentAttributeSerializer(serializers.ModelSerializer):
    parent = serializers.SlugRelatedField(slug_field='slug')
    child = WritableSerializerMethodField('_get_child_field',
                                          '_set_child_field',
                                          required=True)
    weight = serializers.IntegerField(required=False)
    name = serializers.SlugField()

    _child = None

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    class Meta:
        model = ComponentAttribute
        fields = ('parent', 'child', 'name', 'weight')

    def _get_child_field(self, obj):
        if obj.child is None and obj.weight > -1:
            return []
        if obj.child is None and obj.weight == -1:
            return None
        else:
            return obj.child.slug

    def _set_child_field(self, data, *args, **kwargs):
        if 'child' in data:
            self._child = data['child']

    def save_object(self, obj, **kwargs):
        """Save the data in this object to the database.

        :param obj: the object to save to the database
        :type obj: :class:`ComponentAttributeSerializer`

        """
        if (self._child is None and
           (self.object is None or self.object.child is None)):
            raise serializers.ValidationError('Child must be set')

        super().save_object(obj, **kwargs)

        if self._child is not None:
            child_obj = Component.objects.get(slug=self._child)
            self.object.child = child_obj
            self._child = None

    def restore_object(self, attrs, instance=None):
        """Given a dictionary of deserialized field values, either update an existing
        model instance, or create a new model instance.

        :param attrs: the the key/value pairs (generally made by loading a JSON
                      blob from the client) that represent the fields of a
                      ``ComponentAttribute`` object
        :type attrs: dict

        :param instance: an optional instance of a ``ComponentAttribute``. If
                         this is set, then the values of `attrs` will be used
                         update it, rather than to create a new
                         ``ComponentAttribute``.
        :type instance: :class:`mirrors.models.ComponentAttribute`
        :rtype: :class:`mirrors.models.ComponentAttribute`

        """
        if instance is not None:
            instance.child = attrs.get('child', instance.child)
            instance.weight = attrs.get('weight', instance.weight)

            return instance

        if self._child is not None:
            attrs['child'] = Component.objects.get(slug=self._child)

        return ComponentAttribute(**attrs)


class ComponentRevisionSerializer(serializers.ModelSerializer):
    version = serializers.IntegerField(read_only=True)
    change_date = serializers.DateTimeField(read_only=True,
                                            source='created_at')
    change_types = serializers.SerializerMethodField('_get_change_types')

    class Meta:
        model = ComponentRevision
        fields = ('version', 'change_date', 'change_types')

    def _get_change_types(self, obj):
        changes = []

        if obj.data is not None:
            changes.append('data')

        if obj.metadata is not None:
            changes.append('metadata')

        return changes


class ComponentLockSerializer(serializers.ModelSerializer):
    locked = serializers.SerializerMethodField('return_true')
    locked_by = serializers.SlugRelatedField(read_only=True,
                                             slug_field='username')

    class Meta:
        model = ComponentLock
        fields = ('locked', 'locked_by', 'locked_at', 'lock_ends_at',)

    def return_true(self, obj):
        return True


class UserSerializer(serializers.ModelSerializer):
    username = serializers.SerializerMethodField('_get_username')
    is_authenticated = serializers.SerializerMethodField('_is_authenticated')
    full_name = serializers.SerializerMethodField('_get_full_name')
    email = serializers.SerializerMethodField('_get_email')

    class Meta:
        model = User
        fields = ('username', 'full_name', 'email', 'is_authenticated')

    def _get_username(self, obj):
        if obj.is_authenticated():
            return obj.get_username()
        else:
            return ''

    def _get_full_name(self, obj):
        if obj.is_authenticated():
            return obj.get_full_name()
        else:
            return ''

    def _get_email(self, obj):
        if obj.is_authenticated():
            return obj.email
        else:
            return ''

    def _is_authenticated(self, obj):
        return obj.is_authenticated()
