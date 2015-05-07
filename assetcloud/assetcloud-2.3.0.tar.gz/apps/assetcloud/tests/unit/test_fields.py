from assetcloud.fields import SpacesAllowedTagField
from .utils import UnitTestCase
import datetime


def tag_field_test(fn):
    def decorated_fn(self, *args, **kwargs):
        ret = fn(self, *args, **kwargs)
        self.assertSetEqual(set(self.field(required=False).clean(self.given)),
                            set(self.expected))
        return ret
    return decorated_fn


class TagFieldTests(UnitTestCase):
    @tag_field_test
    def test_spaces_allowed_tag_field(self):
        self.field = SpacesAllowedTagField
        self.given = "a b c"
        self.expected = ['a b c']

    @tag_field_test
    def test_spaces_allowed_tag_field_with_comma(self):
        self.field = SpacesAllowedTagField
        self.given = "a,b c"
        self.expected = ['a', 'b c']

    @tag_field_test
    def test_spaces_allowed_tag_field_with_none(self):
        self.field = SpacesAllowedTagField
        self.given = None
        self.expected = []

    @tag_field_test
    def test_spaces_allowed_tag_field_with_invalid(self):
        self.field = SpacesAllowedTagField
        self.given = datetime.datetime.now()
        self.expected = str(self.given).split(' ')

    @tag_field_test
    def test_spaces_allowed_tag_field_case_is_preserved(self):
        self.field = SpacesAllowedTagField
        self.given = "a B C"
        self.expected = ['a B C']
