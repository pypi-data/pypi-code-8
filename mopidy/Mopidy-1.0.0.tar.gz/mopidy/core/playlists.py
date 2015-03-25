from __future__ import absolute_import, unicode_literals

import logging
import urlparse

import pykka

from mopidy.core import listener
from mopidy.models import Playlist
from mopidy.utils.deprecation import deprecated_property


logger = logging.getLogger(__name__)


class PlaylistsController(object):
    pykka_traversable = True

    def __init__(self, backends, core):
        self.backends = backends
        self.core = core

    def as_list(self):
        """
        Get a list of the currently available playlists.

        Returns a list of :class:`~mopidy.models.Ref` objects referring to the
        playlists. In other words, no information about the playlists' content
        is given.

        :rtype: list of :class:`mopidy.models.Ref`

        .. versionadded:: 1.0
        """
        futures = {
            b.actor_ref.actor_class.__name__: b.playlists.as_list()
            for b in set(self.backends.with_playlists.values())}

        results = []
        for backend_name, future in futures.items():
            try:
                results.extend(future.get())
            except NotImplementedError:
                logger.warning(
                    '%s does not implement playlists.as_list(). '
                    'Please upgrade it.', backend_name)

        return results

    def get_items(self, uri):
        """
        Get the items in a playlist specified by ``uri``.

        Returns a list of :class:`~mopidy.models.Ref` objects referring to the
        playlist's items.

        If a playlist with the given ``uri`` doesn't exist, it returns
        :class:`None`.

        :rtype: list of :class:`mopidy.models.Ref`, or :class:`None`

        .. versionadded:: 1.0
        """
        uri_scheme = urlparse.urlparse(uri).scheme
        backend = self.backends.with_playlists.get(uri_scheme, None)
        if backend:
            return backend.playlists.get_items(uri).get()

    def get_playlists(self, include_tracks=True):
        """
        Get the available playlists.

        :rtype: list of :class:`mopidy.models.Playlist`

        .. versionchanged:: 1.0
            If you call the method with ``include_tracks=False``, the
            :attr:`~mopidy.models.Playlist.last_modified` field of the returned
            playlists is no longer set.

        .. deprecated:: 1.0
            Use :meth:`as_list` and :meth:`get_items` instead.
        """
        playlist_refs = self.as_list()

        if include_tracks:
            playlists = {r.uri: self.lookup(r.uri) for r in playlist_refs}
            # Use the playlist name from as_list() because it knows about any
            # playlist folder hierarchy, which lookup() does not.
            return [
                playlists[r.uri].copy(name=r.name)
                for r in playlist_refs if playlists[r.uri] is not None]
        else:
            return [
                Playlist(uri=r.uri, name=r.name) for r in playlist_refs]

    playlists = deprecated_property(get_playlists)
    """
    .. deprecated:: 1.0
        Use :meth:`as_list` and :meth:`get_items` instead.
    """

    def create(self, name, uri_scheme=None):
        """
        Create a new playlist.

        If ``uri_scheme`` matches an URI scheme handled by a current backend,
        that backend is asked to create the playlist. If ``uri_scheme`` is
        :class:`None` or doesn't match a current backend, the first backend is
        asked to create the playlist.

        All new playlists must be created by calling this method, and **not**
        by creating new instances of :class:`mopidy.models.Playlist`.

        :param name: name of the new playlist
        :type name: string
        :param uri_scheme: use the backend matching the URI scheme
        :type uri_scheme: string
        :rtype: :class:`mopidy.models.Playlist`
        """
        if uri_scheme in self.backends.with_playlists:
            backend = self.backends.with_playlists[uri_scheme]
        else:
            # TODO: this fallback looks suspicious
            backend = list(self.backends.with_playlists.values())[0]
        playlist = backend.playlists.create(name).get()
        listener.CoreListener.send('playlist_changed', playlist=playlist)
        return playlist

    def delete(self, uri):
        """
        Delete playlist identified by the URI.

        If the URI doesn't match the URI schemes handled by the current
        backends, nothing happens.

        :param uri: URI of the playlist to delete
        :type uri: string
        """
        uri_scheme = urlparse.urlparse(uri).scheme
        backend = self.backends.with_playlists.get(uri_scheme, None)
        if backend:
            backend.playlists.delete(uri).get()

    def filter(self, criteria=None, **kwargs):
        """
        Filter playlists by the given criterias.

        Examples::

            # Returns track with name 'a'
            filter({'name': 'a'})
            filter(name='a')

            # Returns track with URI 'xyz'
            filter({'uri': 'xyz'})
            filter(uri='xyz')

            # Returns track with name 'a' and URI 'xyz'
            filter({'name': 'a', 'uri': 'xyz'})
            filter(name='a', uri='xyz')

        :param criteria: one or more criteria to match by
        :type criteria: dict
        :rtype: list of :class:`mopidy.models.Playlist`

        .. deprecated:: 1.0
            Use :meth:`as_list` and filter yourself.
        """
        criteria = criteria or kwargs
        matches = self.playlists
        for (key, value) in criteria.iteritems():
            matches = filter(lambda p: getattr(p, key) == value, matches)
        return matches

    def lookup(self, uri):
        """
        Lookup playlist with given URI in both the set of playlists and in any
        other playlist sources. Returns :class:`None` if not found.

        :param uri: playlist URI
        :type uri: string
        :rtype: :class:`mopidy.models.Playlist` or :class:`None`
        """
        uri_scheme = urlparse.urlparse(uri).scheme
        backend = self.backends.with_playlists.get(uri_scheme, None)
        if backend:
            return backend.playlists.lookup(uri).get()
        else:
            return None

    def refresh(self, uri_scheme=None):
        """
        Refresh the playlists in :attr:`playlists`.

        If ``uri_scheme`` is :class:`None`, all backends are asked to refresh.
        If ``uri_scheme`` is an URI scheme handled by a backend, only that
        backend is asked to refresh. If ``uri_scheme`` doesn't match any
        current backend, nothing happens.

        :param uri_scheme: limit to the backend matching the URI scheme
        :type uri_scheme: string
        """
        if uri_scheme is None:
            futures = [b.playlists.refresh()
                       for b in self.backends.with_playlists.values()]
            pykka.get_all(futures)
            listener.CoreListener.send('playlists_loaded')
        else:
            backend = self.backends.with_playlists.get(uri_scheme, None)
            if backend:
                backend.playlists.refresh().get()
                listener.CoreListener.send('playlists_loaded')

    def save(self, playlist):
        """
        Save the playlist.

        For a playlist to be saveable, it must have the ``uri`` attribute set.
        You must not set the ``uri`` atribute yourself, but use playlist
        objects returned by :meth:`create` or retrieved from :attr:`playlists`,
        which will always give you saveable playlists.

        The method returns the saved playlist. The return playlist may differ
        from the saved playlist. E.g. if the playlist name was changed, the
        returned playlist may have a different URI. The caller of this method
        must throw away the playlist sent to this method, and use the
        returned playlist instead.

        If the playlist's URI isn't set or doesn't match the URI scheme of a
        current backend, nothing is done and :class:`None` is returned.

        :param playlist: the playlist
        :type playlist: :class:`mopidy.models.Playlist`
        :rtype: :class:`mopidy.models.Playlist` or :class:`None`
        """
        if playlist.uri is None:
            return
        uri_scheme = urlparse.urlparse(playlist.uri).scheme
        backend = self.backends.with_playlists.get(uri_scheme, None)
        if backend:
            playlist = backend.playlists.save(playlist).get()
            listener.CoreListener.send('playlist_changed', playlist=playlist)
            return playlist
