# from notsio import cli
from os.path import expanduser
from notsio import __version__
from notsio import cli
from notsio.client import NotsioClient
from pycli_tools.parsers import get_argparser

def help(args, parser, client):
    parser.print_usage()

def main():
    parser = get_argparser(
        default_config=expanduser('~/.notsiorc'),
        version=__version__,
        description='notsio note and bookmark command line utility'
    )
    parser.set_defaults(func=help)

    subparser = parser.add_commands([
        cli.ListBooksCommand(),
        cli.InboxCommand(),
        cli.ListNotesCommand(),
        cli.ShowNotesCommand(),
        cli.CreateNotesCommand(),
        cli.MoveNotesCommand(),
        cli.ModifyNotesCommand(),
        cli.EditNotesCommand(),
        cli.DeleteNotesCommand()
    ])

    args = parser.parse_args()

    client = NotsioClient(
        args.base_url,
        args.username,
        args.password,
        verify=args.verify_ssl
    )
    # defaults['notsio']['editor'] = environ.get('EDITOR', 'vim')
    # defaults['notsio']['pager'] = environ.get('PAGER', 'less')
    # defaults['notsio']['verify_ssl'] = True

    return args.func(args, parser=parser, client=client)

if '__main__' == __name__:
    main()
