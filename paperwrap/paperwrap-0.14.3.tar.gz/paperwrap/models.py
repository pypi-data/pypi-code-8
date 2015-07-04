u"""Models representing objects in paperwork."""
from __future__ import absolute_import
from . import wrapper
from .utils import find
import logging
from threading import Thread

LOGGER = logging.getLogger(__name__)

USE_THREADING = False


def threaded_method(func):
    u"""Decorator to put a function into background after calling,
    if threading is enabled.
    """
    def run(*args, **kwargs):
        u"""Runs the function in background, if USE_THREADING is true."""
        if USE_THREADING:
            Thread(target=func, args=args, kwargs=kwargs).start()
        else:
            func(*args, **kwargs)
    return run


class Model(object):
    u"""General class for paperwork-objects."""
    def __init__(self, title, ident, api):
        u"""Initializes paperwork-objects.

        :type title: str
        :type ident: integer
        :type api: wrapper.api
        """
        self.ident = ident
        self.title = title
        self.api = api

    def __str__(self):
        return u"{}:'{}'".format(self.ident, self.title)

    def to_json(self):
        u"""Returns model as dict."""
        return {
            u'id': self.ident,
            u'title': self.title
            }

    @classmethod
    def from_json(cls, api, json):
        u"""Creates model from json-dict.

        :param dict json: dictionary of json data
        """
        return cls(
            json[u'title'],
            json[u'id'],
            api)


class Notebook(Model):
    u"""Class representing a notebook."""
    def __init__(self, title, ident, api, nb_type=0, updated_at=u''):
        u"""Initializes a notebook object.

        :type title: str
        :type ident: integer
        :type api: wrapper.api
        :type updated_at: str
        """
        super(Notebook, self).__init__(title, ident, api)
        self.nb_type = nb_type
        self.updated_at = updated_at
        self.notes = {}

    def to_json(self):
        u"""Returns notebook as dict."""
        return {
            u'type': self.nb_type,
            u'id': self.ident,
            u'title': self.title
            }

    @classmethod
    def from_json(cls, api, json):
        u"""Creates Notebook-instance from json-dict.

        :param dict json: dictionary of json data
        :param wrapper.api api: api-instance
        """
        return cls(
            json[u'title'],
            json[u'id'],
            api,
            nb_type=json[u'type'],
            updated_at=u'')

    @classmethod
    def create(cls, api, title):
        u"""Sends a POST request to the host to create a notebook.

        :param wrapper.api api: api-instance
        :type title: str
        """
        LOGGER.info(u'Created notebook {}'.format(title))
        return cls.from_json(api, api.create_notebook(title))

    @threaded_method
    def delete(self):
        u"""Deletes notebook from remote host."""
        LOGGER.info(u'Deleting notebook {}'.format(self))
        self.api.delete_notebook(self.ident)

    @threaded_method
    def update(self, force=True):
        u"""Updates local or remote notebook, depending on timestamp.

        :param bool force: If true the local title is pushed,
                           regardless of timestamp.
        """
        LOGGER.info(u'Updating {}'.format(self))
        remote = self.api.get_notebook(self.ident)
        if remote is None:
            LOGGER.error(u'Remote notebook could not be found.'
                         u'Wrong ident or deleted.')
        elif force or remote[u'updated_at'] < self.updated_at:
            self.updated_at = self.api.update_notebook(
                self.to_json())[u'updated_at']
        else:
            LOGGER.info(u'Remote version is higher.'
                        u'Updating local notebook.')
            self.title = remote[u'title']
            self.updated_at = remote[u'updated_at']

    def get_notes(self):
        u"""Returns notes in an alphabetically sorted list.

        :rtype: list"""
        return sorted(self.notes.values(), key=lambda note: note.title)

    @threaded_method
    def create_note(self, title):
        u"""Creates a note.

        :type title: str
        """
        note = Note.create(title, self)
        self.notes[note.ident] = note
        LOGGER.info(u'Created note {} in {}'.format(note, self))

    @threaded_method
    def add_note(self, note):
        u"""Adds a note to the notebook.

        :type note: models.Note"""
        self.notes[note.ident] = note
        LOGGER.info(u'Added note {} to {}'.format(note, self))

    def download(self, tags):
        u"""Downloads notes.

        :param dict tags: Tags of the paperwork instance.
        """
        notes_json = self.api.list_notebook_notes(self.ident)
        LOGGER.info(u'Downloading notes of notebook {}'.format(self))
        for note_json in notes_json:
            note = Note.from_json(self, note_json)
            self.add_note(note)
            note.add_tags([tags[tag[u'id']] for tag in note_json[u'tags']])
            note.list_versions()
            note.list_attachments()


class Note(Model):
    u"""Class representing a note object."""
    def __init__(self, title, ident, notebook, content=u'', updated_at=u''):
        u"""Initializes a note object.

        :type title: str
        :type ident: int or str
        :type notebook: Notebook
        :type content: str
        :type updated_at: str
        """
        super(Note, self).__init__(title, ident, notebook.api)
        self.notebook = notebook
        self.content = content
        self.updated_at = updated_at
        self.tags = set()
        self.versions = []
        self.attachments = []

    def to_json(self):
        u"""Returns note as dict."""
        return {
            u'id': self.ident,
            u'title': self.title,
            u'content': self.content,
            u'tags': [tag.to_json() for tag in self.tags],
            u'notebook_id': self.notebook.ident
            }

    @classmethod
    def from_json(cls, notebook, json):
        u"""Creates note from dict.

        :type json: dict
        :type notebook: Notebook
        """
        LOGGER.info(json)
        return cls(
            json[u'title'],
            json[u'id'],
            notebook,
            json[u'content'],
            json[u'updated_at']
            )

    @classmethod
    def create(cls, title, notebook):
        u"""Creates note in notebook.

        :type title: str
        :type notebook: Notebook
        """
        LOGGER.info(u'Creating note {} in notebook {}'.format(title, notebook))
        res = notebook.api.create_note(notebook.ident, title)
        return cls(
            title,
            res[u'id'],
            notebook,
            u'',
            res[u'updated_at']
            )

    @threaded_method
    def update(self, force=False):
        u"""Updates local or remote note, depending on timestamp.

        :param bool force: If true local values will be pushed regardless
                           of timestamp.
        """
        LOGGER.info(u'Updating note {}'.format(self))
        remote = self.api.get_note(self.notebook.ident, self.ident)
        if remote is None:
            LOGGER.error(u'Remote note could not be found. Wrong ident,'
                         u'deleted or moved to another notebook')
        elif force or remote[u'updated_at'] <= self.updated_at:
            LOGGER.info(u'Remote version is lower or force update.'
                        u'Updating remote note.')
            self.updated_at = self.api.update_note(
                self.to_json())[u'updated_at']
        else:
            LOGGER.info(u'Remote version is higher. Updating local note.')
            self.title = remote[u'title']
            self.content = remote[u'content']
            self.updated_at = remote[u'updated_at']

    @threaded_method
    def delete(self):
        u"""Deletes note from remote host and notebook."""
        LOGGER.info(u'Deleting note {} in notebook {}'.format(
            self, self.notebook))
        if self.ident in self.notebook.notes:
            del(self.notebook.notes[self.ident])
        self.api.delete_note(self.to_json())

    @threaded_method
    def add_tags(self, tags):
        u"""Adds a collection of tags to the note.

        :type tags: list or set
        """
        for tag in tags:
            LOGGER.info(u'Adding tag {} to note {}'.format(tag, self))
            self.tags.add(tag)

    @threaded_method
    def move_to(self, new_notebook):
        u"""Moves note to new_notebook.

        :type new_notebook: Notebook
        """
        self.api.move_note(self.to_json(), new_notebook.ident)
        del(self.notebook.notes[self.ident])
        new_notebook.add_note(self)

    def list_versions(self):
        u"""Lists versions of a note.

        Also sets note.versions list in case of future reference.
        :rtype: list
        """
        self.versions = [
            Version.from_json(self, version)
            for version in self.api.list_note_versions(self.to_json())]
        return self.versions

    def list_attachments(self):
        u"""Lists attachments of a note.

        Also sets note.attachments list in case of future reference.
        :rtype: list
        """
        self.attachments = [
            Attachment.from_json(self, attachment)
            for attachment in self.api.list_note_attachments(self.to_json())]
        return self.attachments

    @threaded_method
    def upload_file(self, path):
        u"""Uploads file at path as attachment.

        :type path: str
        """
        self.api.upload_attachment(self.to_json(), path)


class Version(Model):
    u"""Class representing a version of a note."""
    def __init__(self, note, title, ident, previous_id, next_id,
                 content, updated_at):
        u"""Initializes a version object.

        :type note: Note
        :type title: str
        :param int or str ident: ident of the version - not the note
        :type previous_id: int or str
        :type next_id: int or str
        :type content: str
        :param str updated_at: Timestamp of the last update.
            Same as the creation date of the next version.
        """
        super(Version, self).__init__(title, ident, note.api)
        self.note = note
        self.previous_id = int(previous_id) if previous_id else None
        self.next_id = int(next_id) if next_id else None
        self.content = content
        self.updated_at = updated_at
        self.attachments = []

    @classmethod
    def from_json(cls, note, json):
        u"""Parses version of a note from dict.

        :type note: models.Note
        :type json: dict
        """
        return cls(
            note,
            json[u'title'],
            json[u'id'],
            json[u'previous_id'],
            json[u'next_id'],
            json[u'content'],
            json[u'updated_at'])

    def list_attachments(self):
        u"""Lists attachments of a note version.

        Also sets version.attachments list in case of future reference.
        :rtype: list
        """
        self.attachments = [
            Attachment.from_json(attachment, self.ident)
            for attachment in
            self.api.list_note_version_attachments(
                self.note.to_json(),
                self.ident)]
        return self.attachments


class Attachment(Model):
    u"""Class representing an attachment to a note."""
    def __init__(self, note, filename, ident, version_id, mimetype,
                 updated_at):
        u"""Initializes an attachment object.

        :type note: models.Note
        :type filename: str
        :type ident: int or str
        :type version_id: int or str
        :type mimetype: str
        :type updated_at: str
        """
        super(Attachment, self).__init__(filename, ident, note.api)
        self.note = note
        self.version_id = int(version_id)
        self.mimetype = mimetype
        self.updated_at = updated_at

    @classmethod
    def from_json(cls, note, json):
        u"""Parses attachment from dict.

        :type json: dict
        :type note: models.Note
        """
        return cls(
            note,
            json[u'filename'],
            json[u'id'],
            json[u'pivot'][u'version_id'],
            json[u'mimetype'],
            json[u'updated_at']
            )

    @threaded_method
    def download_to(self, path):
        u"""Downloads attachment to specified path.

        :type path: str
        """
        self.api.download_note_attachment(self.note, self.ident, path)

    @threaded_method
    def delete(self):
        u"""Deletes attachment on remote server."""
        self.api.delete_note_version_attachment(
            self.note.to_json(),
            self.version_id,
            self.ident
            )
        if self in self.note.attachments:
            self.note.attachments.remove(self)


class Tag(Model):
    u"""Class representing a tag."""
    def __init__(self, title, ident, api, visibility=0):
        u"""Initializes a tag object.

        :type title: str
        :type ident: int or str
        :type api: wrapper.api
        :type visibility: int
        """
        super(Tag, self).__init__(title, ident, api)
        self.visibility = visibility
        self.notes = set()

    def to_json(self):
        u"""Returns tag as dict."""
        return {
            u'id': self.ident,
            u'title': self.title,
            u'visibility': self.visibility
            }

    @classmethod
    def from_json(cls, api, json):
        u"""Creates tag from dict.

        :type json: dict
        :type api: wrapper.api
        """
        return cls(
            json[u'title'],
            json[u'id'],
            api,
            json[u'visibility']
            )

    def get_notes(self):
        u"""Returns notes in a sorted list.

        :rtype: list"""
        return sorted(self.notes, key=lambda note: note.title)


class Paperwork(object):
    u"""Class representing the remote paperwork instance."""
    def __init__(self, host):
        u"""Initializes local paperwork instance and the api-wrapper.

        :type host: str
        """
        self.notebooks = {}
        self.tags = {}
        self.api = wrapper.API(host)
        self.authenticated = self.api.test_connection()

    def create_notebook(self, title):
        u"""Creates notebook and adds it to paperwork.

        :type title: str
        :rtype: Notebook
        """
        if title != u'All Notes':
            notebook = Notebook.create(self.api, title)
            self.notebooks[notebook.ident] = notebook
            LOGGER.info(u'Created notebook {}'.format(notebook))
            return notebook

    @threaded_method
    def delete_notebook(self, notebook):
        u"""Deletes notebook from server and instance.

        :type notebook: Notebook
        """
        notebook.delete()
        del(self.notebooks[notebook.ident])

    @threaded_method
    def add_notebook(self, notebook):
        u"""Adds notebook to paperwork.

        :type notebook: Notebook
        """
        if notebook.ident != 0:
            self.notebooks[notebook.ident] = notebook
            LOGGER.info(u'Added notebook {}'.format(notebook))

    @threaded_method
    def add_tag(self, tag):
        u"""Adds tag to paperwork.

        :type tag: Tag
        """
        self.tags[tag.ident] = tag
        LOGGER.info(u'Added tag {}'.format(tag))

    def download(self):
        u"""Downloading tags, notebooks and notes from host."""
        LOGGER.info(u'Downloading all')

        LOGGER.info(u'Downloading tags')
        for tag in self.api.list_tags():
            tag = Tag.from_json(self.api, tag)
            self.tags[tag.ident] = tag

        LOGGER.info(u'Downloading notebooks')
        for notebook in self.api.list_notebooks():
            if notebook[u'title'] != u'All Notes':
                notebook = Notebook.from_json(self.api, notebook)
                self.add_notebook(notebook)
                notebook.download(self.tags)
            else:
                LOGGER.info(u'Skipping notebook {}'.format(notebook))

    @threaded_method
    def update(self):
        u"""Updating notebooks and notes to host."""
        LOGGER.info(u'Updating notebooks and notes')
        for notebook in self.notebooks.values():
            notebook.update()
            for note in notebook.get_notes():
                note.update()

    def find_tag(self, key):
        u"""Finds tag with key (ident or title).

        :type key: str or int
        :rtype: Tag or None
        """
        return find(key, self.tags)

    def find_notebook(self, key):
        u"""Find notebook with key (ident or title).

        :type key: str or int
        :rtype: Notebook or None
        """
        return find(key, self.notebooks)

    def find_note(self, key):
        u"""Find note with key (ident or title).

        :type key: str or int
        :rtype: Note or None
        """
        LOGGER.info(u'Searching note for key {} of type {}'.format(
            key, type(key)))
        if isinstance(key, basestring):
            for item in self.get_notes():
                if key == item.title:
                    return item
        else:
            LOGGER.info(u'key is int, finding through keys')
            for notebook in self.notebooks.values():
                if key in notebook.notes:
                    return notebook.notes[key]
        LOGGER.error(u'No note found for key {} of type {}'.format(
            key, type(key)))

    def search(self, key):
        u"""Searches for given key and returns note-instances.

        :type key: str
        :rtype: List
        """
        json_notes = self.api.search(key)
        notes = []
        for json_note in json_notes:
            self.find_note(json_note[u'id'])
        return notes

    def get_notes(self):
        u"""Returns notes in a sorted list.

        :rtype: list
        """
        return sorted(
            [note for nb in self.notebooks.values()
             for note in nb.notes.values()],
            key=lambda note: note.title)

    def get_notebooks(self):
        u"""Returns notebooks in a sorted list.

        :rtype: list
        """
        return sorted(self.notebooks.values(), key=lambda nb: nb.title)

    def get_tags(self):
        u"""Returns tags in a sorted list.

        :rtype: list
        """
        return sorted(self.tags.values(), key=lambda tag: tag.title)
