u"""Wrapper for paperwork API.

License: MIT
Author: Nelo Wallus, http://github.com/ntnn
"""

from __future__ import with_statement
from __future__ import absolute_import
import logging
import json
import requests
from base64 import b64encode
from io import open

LOGGER = logging.getLogger(__name__)

__version__ = u'0.14.3'
API_VERSION = u'/api/v1/'
DEFAULT_AGENT = u'paperwrap api wrapper v{}'.format(__version__)

API_PATH = {
    u'notebooks':      u'notebooks',
    u'notebook':       u'notebooks/{}',
    u'notes':          u'notebooks/{}/notes',
    u'note':           u'notebooks/{}/notes/{}',
    u'move':           u'notebooks/{}/notes/{}/move/{}',
    u'versions':       u'notebooks/{}/notes/{}/versions',
    u'version':        u'notebooks/{}/notes/{}/versions/{}',
    u'attachments':    u'notebooks/{}/notes/{}/versions/{}/attachments',
    u'attachment':     u'notebooks/{}/notes/{}/versions/{}/attachments/{}',
    u'attachment_raw': u'notebooks/{}/notes/{}/versions/{}/attachments/{}/raw',
    u'tags':           u'tags',
    u'tag':            u'tags/{}',
    u'tagged':         u'tagged/{}',
    u'search':         u'search/{}',
    u'i18n':           u'i18n',
    u'i18nkey':        u'i18n/{}'
    }


def b64(string):
    u"""Returns given string as base64 hash-string.

    :type string: str
    :rtype: str
    """
    return b64encode(string.encode(u'UTF-8')).decode(u'ASCII')


def concatenate_ids(coll):
    u"""Concatenates a collection of dicts ID's.

    :type coll: collection of dicts
    :rtype: string
    """
    return u','.join([unicode(item[u'id']) for item in coll])


class API(object):
    u"""Class representing the api-wraper."""
    def __init__(self, host, user_agent=DEFAULT_AGENT):
        u"""Api instance.

        :type host: str
        :type user_agent: str
        """
        self.headers = {u'User-Agent': user_agent}
        self.host = host if u'http://' in host else u'http://' + host

    def test_connection(self):
        u"""Tests connection.  Returns false if connection fails.

        :rtype: bool
        """
        if self.get(u'notebooks'):
            return True
        else:
            return False

    def request(self, method, keyword, *ids, **data):
        u"""Sends a request to the host and returns the parsed json data
        if successfull.

        :type method: str
        :type keyword: str
        :rtype: dict or None
        """
        uri = self.host + API_VERSION + API_PATH[keyword].format(*ids)

        if data:
            self.headers[u'Content-Type'] = u'application/json'
            data = json.dumps(data)

        LOGGER.info(
            u'{} request to {}:\ndata: {}\nheaders: {}'.format(
                method, uri, data, self.headers))

        res = requests.request(
            method,
            uri,
            data=data,
            headers=self.headers,
            verify=False).text

        if keyword == u'attachment_raw':
            return res

        json_res = json.loads(res)
        if json_res[u'success'] is False:
            LOGGER.error(u'Unsuccessful request: {}'.format(
                json_res[u'errors']))
        else:
            return json_res[u'response']

    def get(self, keyword, *ids):
        u"""Convenience wrapper for GET request.

        :type keyword: str
        :rtype: dict or list or None
        """
        return self.request(u'get', keyword, *ids)

    def post(self, data, keyword, *ids):
        u"""Convenience wrapper for POST request.

        :type data: dict
        :type keyword: str
        :rtype: dict or list or None
        """
        return self.request(u'post', keyword, *ids, **data)

    def put(self, data, keyword, *ids):
        u"""Convenience wrapper for PUT request.

        :type data: dict
        :type keyword: str
        :rtype: dict or list or None
        """
        return self.request(u'put', keyword, *ids, **data)

    def delete(self, keyword, *ids):
        u"""Convenience wrapper for DELETE request.

        :type keyword: str
        :rtype: dict or list or None
        """
        return self.request(u'delete', keyword, *ids)

    def list_notebooks(self):
        u"""Return all notebooks in a list.

        :rtype: list
        """
        return self.get(u'notebooks')

    def create_notebook(self, title):
        u"""Create new notebook with title.

        :type title: str
        :rtype: dict
        """
        return self.post(
            {u'type': 0, u'title': title, u'shortcut': u''},
            u'notebooks')

    def get_notebook(self, notebook_id):
        u"""Returns notebook.

        :type notebook_id: int
        :rtype: dict
        """
        return self.get(u'notebook', notebook_id)

    def update_notebook(self, notebook):
        u"""Updates notebook.

        :type notebook: dict
        :rtype: dict
        """
        return self.put(notebook, u'notebook', notebook[u'id'])

    def delete_notebook(self, notebook_id):
        u"""Deletes notebook and all containing notes.

        :type notebook_id: int
        :rtype: dict
        """
        return self.delete(u'notebook', notebook_id)

    def list_notebook_notes(self, notebook_id):
        u"""Returns notes in notebook in a list.

        :type notebook_id: int
        :rtype: list
        """
        return self.get(u'notes', notebook_id)

    def create_note(self, notebook_id, note_title, content=u''):
        u"""Creates note with note_title in notebook.

        :type notebook_id: int
        :type note_title: str
        :type content: str
        :rtype: dict
        """
        content_preview = content[:15] if len(content) >= 15 else content
        return self.post(
            {u'title': note_title,
             u'content': content,
             u'content_preview': content_preview},
            u'notes',
            notebook_id)

    def get_note(self, notebook_id, note_id):
        u"""Returns note with note_id from notebook with notebook_id.

        :type notebook_id: int
        :type note_id: int
        :rtype: dict
        """
        return self.get_notes(notebook_id, [note_id])

    def get_notes(self, notebook_id, note_ids):
        u"""Returns note with note_id from notebook with notebook_id.

        :type notebook_id: int
        :type note_ids: list or set or tuple
        :rtype: list
        """
        return self.get(
            u'note',
            notebook_id,
            u','.join([unicode(note_id) for note_id in note_ids]))

    def update_note(self, note):
        u"""Update note.

        :type note: models.Note
        :rtype: dict
        """
        return self.put(note, u'note', note[u'notebook_id'], note[u'id'])

    def delete_note(self, note):
        u"""Delete note.

        :type note: dict
        :rtype: dict
        """
        return self.delete_notes([note])[0]

    def delete_notes(self, notes):
        u"""Delete notes.

        :type note: list
        :rtype: list
        """
        return self.delete(
            u'note',
            notes[0][u'notebook_id'],
            concatenate_ids(notes))

    def move_note(self, note, new_notebook_id):
        u"""Moves note to new_notebook_id.

        :type note: dict
        :type new_notebook_id: int
        :rtype: dict
        """
        return self.move_notes([note], new_notebook_id)[0]

    def move_notes(self, notes, new_notebook_id):
        u"""Moves notes to new_notebook_id.

        :type notes: list
        :type new_notebook_id: int
        :rtype: list
        """
        return self.get(
            u'move',
            notes[0][u'notebook_id'],
            concatenate_ids(notes),
            new_notebook_id)

    def list_note_versions(self, note):
        u"""Returns a list of versions of given note.

        :type note: dict
        :rtype: list
        """
        return self.list_notes_versions([note])

    def list_notes_versions(self, notes):
        u"""Returns lists of versions of given notes.

        :type notes: list
        :rtype: list
        """
        return self.get(
            u'versions',
            notes[0][u'notebook_id'],
            concatenate_ids(notes))

    def get_note_version(self, note, version_id):
        u"""Returns version with version_id of note.

        :type note: dict
        :type version_id: int
        :rtype: dict
        """
        return self.get(u'version', note[u'notebook_id'], note[u'id'], version_id)

    def list_note_attachments(self, note):
        u"""List attachments of note.

        :type note: dict
        :rtype: list
        """
        return self.list_note_version_attachments(note, 0)

    def list_note_version_attachments(self, note, version_id):
        u"""List attachments of a note belonging to a specific version.

        :type note: dict
        :type version_id: int
        :rtype: list
        """
        return self.get(
            u'attachments',
            note[u'notebook_id'],
            note[u'id'],
            version_id)

    def get_note_attachment(self, note, attachment_id):
        u"""Returns info about attachment with attachment_id of note.

        :type note: dict
        :type attachment_id: int
        :rtype: dict
        """
        return self.get_note_version_attachment(note, 0, attachment_id)

    def get_note_version_attachment(self, note, version_id, attachment_id):
        u"""Returns info about attachment with attachment_id of note version.

        :type note: dict
        :type version_id: int
        :type attachment_id: int
        :rtype: dict
        """
        return self.get(
            u'attachment',
            note[u'notebook_id'],
            note[u'id'],
            version_id,
            attachment_id)

    def download_note_attachment(self, note, attachment_id, path):
        u"""Downloads attachment to specified path.

        Returns true in case of success, false otherwise.
        :type note: dict
        :type attachment_id: int
        :type path: str
        :rtype: bool
        """
        return self.download_note_version_attachment(
            note,
            0,
            attachment_id,
            path)

    def download_note_version_attachment(
            self,
            note,
            version_id,
            attachment_id,
            path):
        u"""Downloads attachment of note version to specified path.

        Returns true in case of success, false otherwise.
        :type note: dict
        :type version_id: int
        :type attachment_id: int
        :type path: str
        :rtype: bool
        """
        attachment = self.get(
            u'attachment_raw',
            note[u'notebook_id'],
            note[u'id'],
            version_id,
            attachment_id)
        try:
            with open(path, u'wb') as f:
                f.write(attachment)
            return True
        except IOError, ioerror:
            LOGGER.error(ioerror)
        return False

    def delete_note_attachment(self, note, attachment_id):
        u"""Deletes attachment with attachment_id on note.

        :type note: dict
        :type attachment_id: int
        :rtype: dict
        """
        return self.delete_note_version_attachment(note, 0, attachment_id)

    def delete_note_version_attachment(self, note, version_id, attachment_id):
        u"""Deletes attachment with attachment_id on note.

        :type note: dict
        :type version_id: int
        :type attachment_id: int
        :rtype: dict
        """
        return self.delete(
            u'attachment',
            note[u'notebook_id'],
            note[u'id'],
            version_id,
            attachment_id)

    def upload_attachment(self, note, path):
        u"""Uploads an attachment.

        :type note: dict
        :type path: str
        :rtype: dict
        """
        LOGGER.info(u'Uploading file at {} to {}'.format(path, note))
        return requests.post(
            self.host + API_VERSION + API_PATH[u'attachments'].format(
                note[u'notebook_id'],
                note[u'id'],
                0),
            files={u'file': open(path, u'rb')},
            headers=self.headers)

    def list_tags(self):
        u"""Returns all tags.

        :rtype: list
        """
        return self.get(u'tags')

    def get_tag(self, tag_id):
        u"""Returns tag with tag_id.

        :type tag_id: int
        :rtype: dict
        """
        return self.get(u'tag', tag_id)

    def list_tagged(self, tag_id):
        u"""Returns notes tagged with tag.

        :type tag_id: int
        :rtype: list
        """
        return self.get(u'tagged', tag_id)

    def search(self, keyword):
        u"""Search for notes containing given keyword.

        :type keyword: str
        :rtype: list
        """
        return self.get(u'search', b64(keyword))

    def i18n(self, keyword=None):
        u"""Returns either the full i18n dict or the requested word.

        :type keyword: str
        :rtype: list or str
        """
        if keyword:
            return self.get(u'i18nkey', keyword)
        return self.get(u'i18n')
