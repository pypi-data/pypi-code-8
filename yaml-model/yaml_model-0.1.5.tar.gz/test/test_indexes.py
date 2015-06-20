"""
Test the Model class
"""
from unittest.mock import NonCallableMock, patch

import pytest
import yaml

from yaml_model import IndexValueError, LoadOnAccess, Model


@pytest.mark.usefixtures("cleandir")
class TestIndexes(object):
    """
    Test the index property of LoadOnAccess class
    """
    @pytest.mark.parametrize('slugs', [
        ('justone',),
        ('testslug', 'moretestslug'),
        ('with spaces', 'some more spaces'),
        ('Σ', 'œø', 'åę😀'),
    ])
    @pytest.mark.parametrize('value', [
        'testval', 'spaces val', 'Σval', '😀val',
    ])
    def test_index(self, cleandir, slugs, value):
        """
        Make sure indexes are correctly created, and can be loaded from easily
        """
        class Test(Model):  # pylint:disable=missing-docstring
            slug = None
            test_field = LoadOnAccess(index=True)

            def __init__(self, slug):
                super(Test, self).__init__()
                self.slug = slug

        def create_instance(this_slug):
            """ Create a test instance with the global value """
            obj = Test(this_slug)
            obj.test_field = value
            return obj

        test_create = [create_instance(slug) for slug in slugs]

        assert len(tuple(Test.get_where('test_field', value))) == 0

        for obj in test_create:
            obj.save()

        model_dir = cleandir.join('data', 'tests')

        for obj in test_create:
            expected_file = model_dir.join('%s.yaml' % obj.slug)
            expected_link = model_dir.join(
                '_i_test_field', value, '%s.yaml' % obj.slug
            )

            assert expected_link.check(link=True), "File exists"
            assert expected_link.samefile(expected_file)

        with patch.object(
            Test, '_get_where_indexed',
            wraps=Test._get_where_indexed,
        ) as mock_indexed:
            with patch.object(
                Test, '_get_where_no_index',
                new_callable=NonCallableMock,
            ):
                loaded_list = tuple(Test.get_where('test_field', value))
                assert len(loaded_list) == len(slugs)
                assert mock_indexed.call_count == 1

        assert set([obj.slug for obj in loaded_list]) == set(slugs)

        for obj in loaded_list:
            assert obj.test_field == value

    @pytest.mark.parametrize('field_kwargs', [
        {}, {'index': False},
    ])
    def test_no_index(self, cleandir, field_kwargs):
        """
        Make sure when not indexing fields, the index is not created
        """
        class Test(Model):  # pylint:disable=missing-docstring
            slug = None
            test_field = LoadOnAccess(**field_kwargs)

            def __init__(self, slug):
                super(Test, self).__init__()
                self.slug = slug

        test_create = Test('testslug')
        test_create.test_field = 'testval'
        test_create.save()

        model_dir = cleandir.join('data', 'tests')
        assert len(model_dir.listdir('_i_*')) == 0

    @pytest.mark.parametrize('value', [
        {}, [], (), None,
    ])
    # pylint:disable=unused-argument
    def test_unindexable(self, cleandir, value):
        """
        Some values can't be indexed and should raise an error
        """
        class Test(Model):  # pylint:disable=missing-docstring
            slug = None
            test_field = LoadOnAccess(index=True)

            def __init__(self, slug):
                super(Test, self).__init__()
                self.slug = slug

        test_create = Test('testslug')

        with pytest.raises(IndexValueError):
            test_create.test_field = value

    @pytest.mark.parametrize('value', [
        'abc', 'with spaces', 123, 1.2, 'Σ', 'œø', 'åę😀',
    ])
    # pylint:disable=unused-argument
    def test_get_where_unindexed(self, cleandir, value):
        """
        Get where should still work on unindexed values
        """
        class Test(Model):  # pylint:disable=missing-docstring
            slug = None
            test_field = LoadOnAccess()

            def __init__(self, slug):
                super(Test, self).__init__()
                self.slug = slug

        test_not_value = Test('testslugneg')
        test_not_value.test_field = 'not the value'

        test_create = [Test('testsluga'), Test('testslugb')]
        for obj in test_create:
            obj.test_field = value

        assert len(tuple(Test.get_where('test_field', value))) == 0

        test_not_value.save()
        for obj in test_create:
            obj.save()

        with patch.object(
            Test, '_get_where_no_index',
            wraps=Test._get_where_no_index,
        ) as mock_no_index:
            with patch.object(
                Test, '_get_where_indexed',
                new_callable=NonCallableMock,
            ):
                loaded_list = tuple(Test.get_where('test_field', value))
                assert len(loaded_list) == 2
                assert mock_no_index.call_count == 1

        assert set([obj.slug for obj in loaded_list]) == set(
            ('testsluga', 'testslugb')
        )

    @pytest.mark.parametrize('value', [
        {}, [], (), None,
    ])
    # pylint:disable=unused-argument
    def test_get_where_unindexable(self, cleandir, value):
        """
        Some values can't be indexed and should raise an error
        """
        class Test(Model):  # pylint:disable=missing-docstring
            slug = None
            test_field = LoadOnAccess(index=True)

            def __init__(self, slug):
                super(Test, self).__init__()
                self.slug = slug

        with pytest.raises(IndexValueError):
            tuple(Test.get_where('test_field', value))

    @pytest.mark.parametrize('value', [
        'testval', 'spaces val', 'Σval', '😀val',
    ])
    def test_update_indexes(self, cleandir, value):
        """
        Update indexes using lazy values
        """
        class Test(Model):  # pylint:disable=missing-docstring
            slug = 'testslug'
            test_field = LoadOnAccess(index=True)

            def __init__(self):
                super(Test, self).__init__()

        model_dir = cleandir.join('data', 'tests')
        model_file = model_dir.join('testslug.yaml')
        index_file_real = model_dir.join(
            '_i_test_field', value, 'testslug.yaml',
        )
        index_value_dir_fake = model_dir.join(
            '_i_test_field', 'fake_value',
        )

        model_dir.ensure_dir()
        with model_file.open('w') as handle:
            yaml.dump({'test_field': value}, handle)

        obj = Test()
        obj.update_indexes()

        assert not index_value_dir_fake.check()
        assert index_file_real.check(link=True, file=True)
        assert index_file_real.samefile(model_file)

        obj.test_field = 'fake_value'
        obj.update_indexes()

        assert not index_value_dir_fake.check()
        assert index_file_real.check(link=True, file=True)
        assert index_file_real.samefile(model_file)

    @pytest.mark.parametrize('value', [
        'testval', 'spaces val', 'Σval', '😀val',
    ])
    def test_update_indexes_for_save(self, cleandir, value):
        """
        Update indexes for save (using dirty values)
        """
        class Test(Model):  # pylint:disable=missing-docstring
            slug = 'testslug'
            test_field = LoadOnAccess(index=True)

            def __init__(self):
                super(Test, self).__init__()

        model_dir = cleandir.join('data', 'tests')
        model_file = model_dir.join('testslug.yaml')
        index_value_dir_pre = model_dir.join(
            '_i_test_field', 'preval',
        )
        index_file_pre = index_value_dir_pre.join('testslug.yaml')
        index_value_dir_post = model_dir.join(
            '_i_test_field', value
        )
        index_file_post = index_value_dir_post.join('testslug.yaml')

        model_dir.ensure_dir()
        with model_file.open('w') as handle:
            yaml.dump({'test_field': 'preval'}, handle)

        obj = Test()
        obj.update_indexes()

        assert not index_value_dir_post.check()
        assert index_file_pre.check(link=True, file=True)
        assert index_file_pre.samefile(model_file)

        obj.test_field = value
        obj.update_indexes(for_save=True)

        assert not index_value_dir_pre.check()
        assert index_file_post.check(link=True, file=True)
        assert index_file_post.samefile(model_file)

    @pytest.mark.parametrize('slug', [
        'justone',
        'with spaces', 'some more spaces',
        'Σ', 'œø', 'åę😀',
    ])
    @pytest.mark.parametrize('value_a, value_b', [
        ('testval', 'spaces val'),
        ('Σval', '😀val'),
    ])
    def test_delete_index(self, cleandir, slug, value_a, value_b):
        """ Ensure indexes are deleted when the model is """
        class Test(Model):  # pylint:disable=missing-docstring
            slug = None
            test_field_a = LoadOnAccess(index=True)
            test_field_b = LoadOnAccess(index=True)

            def __init__(self, slug):
                super(Test, self).__init__()
                self.slug = slug

        model = Test(slug)
        model.test_field_a = value_a
        model.test_field_b = value_b
        model.save()

        model_dir = cleandir.join('data', 'tests')
        expected_value_a_dir = model_dir.join('_i_test_field_a', value_a)
        expected_value_b_dir = model_dir.join('_i_test_field_b', value_b)
        expected_link_a = expected_value_a_dir.join('%s.yaml' % slug)
        expected_link_b = expected_value_b_dir.join('%s.yaml' % slug)
        assert expected_link_a.check()
        assert expected_link_b.check()

        model.delete()
        assert not expected_link_a.check()
        assert not expected_link_b.check()
        assert not expected_value_a_dir.check()
        assert not expected_value_b_dir.check()
