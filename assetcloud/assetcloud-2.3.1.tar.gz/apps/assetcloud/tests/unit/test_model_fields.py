from assetcloud.models import NullableCharField, DomainPartValidator, ReservedDomainValidator
from .utils import UnitTestCase
from django.core.exceptions import ValidationError


class ModelFieldTests(UnitTestCase):
    def assertToPython(self, given, expected):
        field = NullableCharField()
        self.assertEqual(field.to_python(given), expected)

    def assertDbPrepValue(self, given, expected):
        field = NullableCharField()
        self.assertEqual(field.get_db_prep_value(given), expected)

    def test_nullable_char_field_preserves_values(self):
        self.assertToPython("test", "test")
        self.assertDbPrepValue("test", "test")

    def test_nullable_char_field_converts_to_null(self):
        self.assertDbPrepValue("", None)
        self.assertDbPrepValue(None, None)
        self.assertDbPrepValue('0', '0')

    def test_nullable_char_field_converts_from_null(self):
        self.assertToPython("", "")
        self.assertToPython(None, "")
        self.assertToPython('0', '0')


class DomainValidatorTests(UnitTestCase):
    def setUp(self):
        super(DomainValidatorTests, self).setUp()
        self.validators = [DomainPartValidator(), ReservedDomainValidator()]

    def assertAccepted(self, value):
        try:
            for validator in self.validators:
                validator(value)
        except ValidationError:
            self.fail('%s unexpectedly rejected' % value)

    def assertRejected(self, value):
        error_raised = False
        for validator in self.validators:
            try:
                validator(value)
            except ValidationError:
                error_raised = True
        if not error_raised:
            self.fail('%s did not raise validation error' % value)

    def test_domain_part_validator_accepts(self):
        self.assertAccepted('a')
        self.assertAccepted('6')
        self.assertAccepted('a12381Dds2')
        self.assertAccepted('aA2a-a2dd53d')
        self.assertAccepted('a-aa23fds')
        self.assertAccepted('a-a')
        self.assertAccepted('1-2')

    def test_domain_part_validator_reject(self):
        self.assertRejected(None)
        self.assertRejected('')
        self.assertRejected('-')
        self.assertRejected('.')
        self.assertRejected('-a')
        self.assertRejected('a-')
        self.assertRejected('-2')
        self.assertRejected('5-')
        self.assertRejected('a.')
        self.assertRejected('.b')
        self.assertRejected('a.b')

    def test_reserved_domain_validator(self):
        for sub in ReservedDomainValidator.reserved:
            self.assertRejected(sub)
