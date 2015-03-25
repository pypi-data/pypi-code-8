from __future__ import absolute_import, unicode_literals

import unittest

import mock

from mopidy import backend, core
from mopidy.models import Playlist, Ref, Track


class PlaylistsTest(unittest.TestCase):
    def setUp(self):  # noqa: N802
        self.plr1a = Ref.playlist(name='A', uri='dummy1:pl:a')
        self.plr1b = Ref.playlist(name='B', uri='dummy1:pl:b')
        self.plr2a = Ref.playlist(name='A', uri='dummy2:pl:a')
        self.plr2b = Ref.playlist(name='B', uri='dummy2:pl:b')

        self.pl1a = Playlist(name='A', tracks=[Track(uri='dummy1:t:a')])
        self.pl1b = Playlist(name='B', tracks=[Track(uri='dummy1:t:b')])
        self.pl2a = Playlist(name='A', tracks=[Track(uri='dummy2:t:a')])
        self.pl2b = Playlist(name='B', tracks=[Track(uri='dummy2:t:b')])

        self.sp1 = mock.Mock(spec=backend.PlaylistsProvider)
        self.sp1.as_list.return_value.get.return_value = [
            self.plr1a, self.plr1b]
        self.sp1.lookup.return_value.get.side_effect = [self.pl1a, self.pl1b]

        self.sp2 = mock.Mock(spec=backend.PlaylistsProvider)
        self.sp2.as_list.return_value.get.return_value = [
            self.plr2a, self.plr2b]
        self.sp2.lookup.return_value.get.side_effect = [self.pl2a, self.pl2b]

        self.backend1 = mock.Mock()
        self.backend1.actor_ref.actor_class.__name__ = 'Backend1'
        self.backend1.uri_schemes.get.return_value = ['dummy1']
        self.backend1.playlists = self.sp1

        self.backend2 = mock.Mock()
        self.backend2.actor_ref.actor_class.__name__ = 'Backend2'
        self.backend2.uri_schemes.get.return_value = ['dummy2']
        self.backend2.playlists = self.sp2

        # A backend without the optional playlists provider
        self.backend3 = mock.Mock()
        self.backend3.uri_schemes.get.return_value = ['dummy3']
        self.backend3.has_playlists().get.return_value = False
        self.backend3.playlists = None

        self.core = core.Core(mixer=None, backends=[
            self.backend3, self.backend1, self.backend2])

    def test_as_list_combines_result_from_backends(self):
        result = self.core.playlists.as_list()

        self.assertIn(self.plr1a, result)
        self.assertIn(self.plr1b, result)
        self.assertIn(self.plr2a, result)
        self.assertIn(self.plr2b, result)

    def test_as_list_ignores_backends_that_dont_support_it(self):
        self.sp2.as_list.return_value.get.side_effect = NotImplementedError

        result = self.core.playlists.as_list()

        self.assertEqual(len(result), 2)
        self.assertIn(self.plr1a, result)
        self.assertIn(self.plr1b, result)

    def test_get_items_selects_the_matching_backend(self):
        ref = Ref.track()
        self.sp2.get_items.return_value.get.return_value = [ref]

        result = self.core.playlists.get_items('dummy2:pl:a')

        self.assertEqual([ref], result)
        self.assertFalse(self.sp1.get_items.called)
        self.sp2.get_items.assert_called_once_with('dummy2:pl:a')

    def test_get_items_with_unknown_uri_scheme_does_nothing(self):
        result = self.core.playlists.get_items('unknown:a')

        self.assertIsNone(result)
        self.assertFalse(self.sp1.delete.called)
        self.assertFalse(self.sp2.delete.called)

    def test_get_playlists_combines_result_from_backends(self):
        result = self.core.playlists.get_playlists()

        self.assertIn(self.pl1a, result)
        self.assertIn(self.pl1b, result)
        self.assertIn(self.pl2a, result)
        self.assertIn(self.pl2b, result)

    def test_get_playlists_includes_tracks_by_default(self):
        result = self.core.playlists.get_playlists()

        self.assertEqual(result[0].name, 'A')
        self.assertEqual(len(result[0].tracks), 1)
        self.assertEqual(result[1].name, 'B')
        self.assertEqual(len(result[1].tracks), 1)

    def test_get_playlist_can_strip_tracks_from_returned_playlists(self):
        result = self.core.playlists.get_playlists(include_tracks=False)

        self.assertEqual(result[0].name, 'A')
        self.assertEqual(len(result[0].tracks), 0)
        self.assertEqual(result[1].name, 'B')
        self.assertEqual(len(result[1].tracks), 0)

    def test_create_without_uri_scheme_uses_first_backend(self):
        playlist = Playlist()
        self.sp1.create().get.return_value = playlist
        self.sp1.reset_mock()

        result = self.core.playlists.create('foo')

        self.assertEqual(playlist, result)
        self.sp1.create.assert_called_once_with('foo')
        self.assertFalse(self.sp2.create.called)

    def test_create_with_uri_scheme_selects_the_matching_backend(self):
        playlist = Playlist()
        self.sp2.create().get.return_value = playlist
        self.sp2.reset_mock()

        result = self.core.playlists.create('foo', uri_scheme='dummy2')

        self.assertEqual(playlist, result)
        self.assertFalse(self.sp1.create.called)
        self.sp2.create.assert_called_once_with('foo')

    def test_create_with_unsupported_uri_scheme_uses_first_backend(self):
        playlist = Playlist()
        self.sp1.create().get.return_value = playlist
        self.sp1.reset_mock()

        result = self.core.playlists.create('foo', uri_scheme='dummy3')

        self.assertEqual(playlist, result)
        self.sp1.create.assert_called_once_with('foo')
        self.assertFalse(self.sp2.create.called)

    def test_delete_selects_the_dummy1_backend(self):
        self.core.playlists.delete('dummy1:a')

        self.sp1.delete.assert_called_once_with('dummy1:a')
        self.assertFalse(self.sp2.delete.called)

    def test_delete_selects_the_dummy2_backend(self):
        self.core.playlists.delete('dummy2:a')

        self.assertFalse(self.sp1.delete.called)
        self.sp2.delete.assert_called_once_with('dummy2:a')

    def test_delete_with_unknown_uri_scheme_does_nothing(self):
        self.core.playlists.delete('unknown:a')

        self.assertFalse(self.sp1.delete.called)
        self.assertFalse(self.sp2.delete.called)

    def test_delete_ignores_backend_without_playlist_support(self):
        self.core.playlists.delete('dummy3:a')

        self.assertFalse(self.sp1.delete.called)
        self.assertFalse(self.sp2.delete.called)

    def test_filter_returns_matching_playlists(self):
        result = self.core.playlists.filter(name='A')

        self.assertEqual(2, len(result))

    def test_filter_accepts_dict_instead_of_kwargs(self):
        result = self.core.playlists.filter({'name': 'A'})

        self.assertEqual(2, len(result))

    def test_lookup_selects_the_dummy1_backend(self):
        self.core.playlists.lookup('dummy1:a')

        self.sp1.lookup.assert_called_once_with('dummy1:a')
        self.assertFalse(self.sp2.lookup.called)

    def test_lookup_selects_the_dummy2_backend(self):
        self.core.playlists.lookup('dummy2:a')

        self.assertFalse(self.sp1.lookup.called)
        self.sp2.lookup.assert_called_once_with('dummy2:a')

    def test_lookup_track_in_backend_without_playlists_fails(self):
        result = self.core.playlists.lookup('dummy3:a')

        self.assertIsNone(result)
        self.assertFalse(self.sp1.lookup.called)
        self.assertFalse(self.sp2.lookup.called)

    def test_refresh_without_uri_scheme_refreshes_all_backends(self):
        self.core.playlists.refresh()

        self.sp1.refresh.assert_called_once_with()
        self.sp2.refresh.assert_called_once_with()

    def test_refresh_with_uri_scheme_refreshes_matching_backend(self):
        self.core.playlists.refresh(uri_scheme='dummy2')

        self.assertFalse(self.sp1.refresh.called)
        self.sp2.refresh.assert_called_once_with()

    def test_refresh_with_unknown_uri_scheme_refreshes_nothing(self):
        self.core.playlists.refresh(uri_scheme='foobar')

        self.assertFalse(self.sp1.refresh.called)
        self.assertFalse(self.sp2.refresh.called)

    def test_refresh_ignores_backend_without_playlist_support(self):
        self.core.playlists.refresh(uri_scheme='dummy3')

        self.assertFalse(self.sp1.refresh.called)
        self.assertFalse(self.sp2.refresh.called)

    def test_save_selects_the_dummy1_backend(self):
        playlist = Playlist(uri='dummy1:a')
        self.sp1.save().get.return_value = playlist
        self.sp1.reset_mock()

        result = self.core.playlists.save(playlist)

        self.assertEqual(playlist, result)
        self.sp1.save.assert_called_once_with(playlist)
        self.assertFalse(self.sp2.save.called)

    def test_save_selects_the_dummy2_backend(self):
        playlist = Playlist(uri='dummy2:a')
        self.sp2.save().get.return_value = playlist
        self.sp2.reset_mock()

        result = self.core.playlists.save(playlist)

        self.assertEqual(playlist, result)
        self.assertFalse(self.sp1.save.called)
        self.sp2.save.assert_called_once_with(playlist)

    def test_save_does_nothing_if_playlist_uri_is_unset(self):
        result = self.core.playlists.save(Playlist())

        self.assertIsNone(result)
        self.assertFalse(self.sp1.save.called)
        self.assertFalse(self.sp2.save.called)

    def test_save_does_nothing_if_playlist_uri_has_unknown_scheme(self):
        result = self.core.playlists.save(Playlist(uri='foobar:a'))

        self.assertIsNone(result)
        self.assertFalse(self.sp1.save.called)
        self.assertFalse(self.sp2.save.called)

    def test_save_ignores_backend_without_playlist_support(self):
        result = self.core.playlists.save(Playlist(uri='dummy3:a'))

        self.assertIsNone(result)
        self.assertFalse(self.sp1.save.called)
        self.assertFalse(self.sp2.save.called)
