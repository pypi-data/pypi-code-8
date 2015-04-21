"""
TODO: add comments
"""
from commands import Command


class CreateCommand(Command):

    def add_parser(self, subparsers):
        super(CreateCommand, self).add_parser(subparsers)
        parser = subparsers.add_parser("create",
                                       help="Create tow project in current directory")
        parser.add_argument("project_name", type="string",
                            help="name of tow project", dest="project_name")

    def command(self, namespace, args):
        pass
