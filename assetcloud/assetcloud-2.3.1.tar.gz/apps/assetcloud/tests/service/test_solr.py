from .utils import TestCase, create_asset


class IndexTest(TestCase):
    needs_index = True

    def test_create_asset(self):
        for i in range(10):
            create_asset()
