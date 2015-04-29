from django.test import TestCase
from uuidstore.tests.models import (
    ModelWithDenormalisedCharField,
    ModelWithDenormalisedUUIDField,
    ModelWithDetatchedUUID,
    ModelWithMonkeyPatchedUUID,
    )
from uuidstore.models import ObjectUUID
import uuid


class SimpleTestClient(TestCase):

    def _validate(self, model):

        # Create the test object
        obj = model.objects.create(title='Test')

        # Try to retrieve the related uuidstore object
        stored = ObjectUUID.objects.get_for_instance(obj)

        # We're talking about the same object?
        self.assertEqual(obj, stored.content_object)

        try:
            id = uuid.UUID(stored.uuid)  # noqa
        except ValueError:
            msg = "'{}' is not a valid UUID.".format(stored.uuid)
            self.fail(msg)
        return obj, stored

    def test_model_with_detatched_uuid(self):
        self._validate(ModelWithDetatchedUUID)

    def test_model_with_monkey_patched_uuid(self):
        obj, stored = self._validate(ModelWithMonkeyPatchedUUID)

        # ... and it matches the one on the object?
        self.assertEqual(stored.uuid, obj.uuid)

    def test_model_with_denormalised_charfield(self):
        obj, stored = self._validate(ModelWithDenormalisedCharField)

        # ... and it matches the one on the object?
        self.assertEqual(stored.uuid, obj.uuid)

    def test_model_with_denormalised_uuidfield(self):
        obj, stored = self._validate(ModelWithDenormalisedUUIDField)

        # ... and it matches the one on the object?
        self.assertEqual(stored.uuid, obj.uuid)
