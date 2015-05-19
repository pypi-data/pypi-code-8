from json import dumps as json_dumps
from logging import getLogger
from notsio.utils import VALID_URL
from os import system
from pycli_tools.commands import Command, arg
from sys import stdin
from tempfile import NamedTemporaryFile


log = getLogger(__name__)


class ListBooksCommand(Command):
    '''list all books on the server'''
    name = 'books'

    def run(self, args, parser, client):
        response = client.get_books()
        books = response.json()

        padding = max([len(b['name']) for b in books])

        for book in books:
            print('{name:<{padding}} \t{note_count}'.format(padding=padding, **book))


class InboxCommand(Command):
    '''list all notes in the inbox book on the server'''
    name = 'inbox'

    def run(self, args, parser, client):
        response = client.get_notes(params={'book': 'inbox'})
        data = response.json()

        if len(data['results']) == 0:
            log.warn('Zero inbox :)')
            return 0

        padding = max([len(n['book']) for n in data['results']])

        for note in reversed(data['results']):
            if 'book' not in note:
                note['book'] = ''
            print('{id:<5}\t{book:{padding}}\t{title}'.format(
                padding=padding, **note
            ))


class ListNotesCommand(Command):
    '''search or list notes'''
    name = 'list'

    args = [
        arg('--book',         help='only show notes from this book'),
        arg('--bookmarks',    action='store_true', dest='bookmarks',
                              default=None, help='only show bookmarks'),
        arg('--no-bookmarks', action='store_false', dest='bookmarks',
                              default=None, help='hide bookmarks'),
        arg('search',         nargs='*', help='optionally filter notes'),
    ]

    def run(self, args, parser, client):
        payload = {}

        if args.book:
            payload['book'] = args.book.strip()

        if True == args.bookmarks:
            payload['bookmarks'] = 'true'
        elif False == args.bookmarks:
            payload['bookmarks'] = 'false'

        if args.search:
            payload['search'] = ' '.join(args.search)

        log.debug('Listing notes: %s', payload)
        response = client.get_notes(params=payload)
        data = response.json()

        if len(data['results']) == 0:
            log.warn('No notes found')
            return 1

        padding = max([len(n['book']) for n in data['results']])

        for note in reversed(data['results']):
            if 'book' not in note: note['book'] = ''
            print('{id:<5}\t{book:{padding}}\t{title}'.format(padding=padding, **note))


class ShowNotesCommand(Command):
    '''show a note'''
    name = 'show'

    args = [
        arg('--no-pager', action='store_false', dest='use_pager', help='do not pipe the output to $PAGER'),
        arg('note', help='the id of the note to show'),
    ]

    def run(self, args, parser, client):
        note_id = args.note

        try:
            response = client.get_note(note_id)
        except HTTPError as e:
            log.error(e)
            return 1

        note = response.json()

        text = [
            'title:   {0}'.format(note['title']),
            'created: {0}'.format(note['created']),
            'updated: {0}'.format(note['updated']),
            'book:    {0}'.format(note['book']),
            'link:    {0}'.format(note['link'] or '-')
        ]

        if 'description' in note:
            text += [
                '',
                '-' * 78,
                '',
                '{0}'.format(note['description'])
            ]

        if args.use_pager:
            with NamedTemporaryFile(mode="w", suffix='-notsio') as tmpnote:
                tmpnote.write('\n'.join(text))
                tmpnote.flush()
                system(args.pager + ' ' + tmpnote.name)
        else:
            print('\n'.join(text))


class CreateNotesCommand(Command):
    '''create a new note'''
    name = 'create'

    args = [
        arg('--book', help='the book this note should be part of (defaults to `inbox`)'),
        arg('--link', help='a valid url to store with this note'),
        arg('title', help='the title for this note'),
    ]

    def run(self, args, parser, client):
        data = {
            'title': args.title
        }

        if args.book:
            data['book'] = args.book
        else:
            data['book'] = 'inbox'

        if args.link:
            data['link'] = args.link
        elif VALID_URL.match(args.title):
            data['link'] = args.title

        if not stdin.isatty():
            data['description'] = stdin.read().strip()

        try:
            response = client.post_notes(data=json_dumps(data))
        except HTTPError as e:
            log.error(e)
            log.error(e.response.text)
            log.debug(json_dumps(data))
            return 1

        print('Note saved as %s' % response.json()['id'])


class MoveNotesCommand(Command):
    '''move one or more notes to another book'''
    name = 'move-to'

    args = [
        arg('book', help='the name of the destination book'),
        arg('note', nargs='+', help='one or more id\'s of notes to move'),
    ]

    def run(self, args, parser, client):
        for note in args.note:
            response = client.patch_note(note, data={'book': args.book})
            print('{0}\t{1}'.format(note, response))


class ModifyNotesCommand(Command):
    '''
    change one or more note attributes

    if the [file] argument is not specified /dev/stdin will be read and used
    instead.

    if there is no input on /dev/stdin the body of the note is not changed.
    '''
    name = 'modify'

    args = [
        arg('--title', help='the title for this note'),
        arg('--book',  help='the book this note should be part of'),
        arg('--link',  help='a valid url to store with this note'),
        arg('note',    help='the id of the note to edit'),
        arg('file',    default=None, nargs='?',
                       help='set the note to the content of this file'),
    ]

    def run(self, args, parser, client):
        data = {}

        if args.book:
            data['book'] = args.book
        if args.link:
            data['link'] = args.link
        if args.title:
            data['title'] = args.title

        if args.file:
            data['description'] = open(args.file, 'r').read().strip()
        elif not stdin.isatty():
            data['description'] = stdin.read().strip()

        if not data:
            log.error('No modifications supplied')
            return 1

        log.debug(data)
        response = client.patch_note(args.note, data=data)
        print(response)


class EditNotesCommand(Command):
    '''edit a note in your favorite $EDITOR'''
    name = 'edit'

    args = [
        arg('note', help='the id of the note to edit')
    ]

    def run(self, args, parser, client):
        response = client.get_note(args.note)
        note_before = response.json()

        with NamedTemporaryFile(mode="w", suffix='-notsio') as tmpnote:
            tmpnote.write(note_before['description'])
            tmpnote.flush()
            system(args.editor.format(note_id=args.note) + ' ' + tmpnote.name)
            current_description = open(tmpnote.name).read()

        response = client.get_note(args.note)
        note_after = response.json()

        if note_after['description'].strip() == current_description.strip():
            log.info('Note already synced with notsio. Ignoring.')
        else:
            response = client.patch_note(args.note,
                                   data={'description': current_description})
            print(response)

        return 0


class DeleteNotesCommand(Command):
    '''delete one or more notes'''
    name = 'delete'

    args = [
        arg('note', nargs='+', help='one or more id\'s of notes to remove'),
    ]

    def run(self, args, parser, client):
        for note in args.note:
            try:
                response = client.delete_note(note)
            except HTTPError as e:
                response = e.response
            print('Delete {}:\t{}'.format(note, response))
