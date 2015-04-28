from zymbit.commands import Command
from zymbit.provision import Provision


class ProvisionCommand(Command):
    command_name = 'provision'

    @classmethod
    def setup_parser(cls, parser):
        command_parser = super(ProvisionCommand, cls).setup_parser(parser)

        command_parser.add_argument('--api-url')
        command_parser.add_argument('--websocket-url')
        command_parser.add_argument('token')

        return command_parser

    def run(self):
        token = self.args.token
        api_url = self.args.api_url
        websocket_url = self.args.websocket_url

        provision = Provision(token, api_url=api_url, websocket_url=websocket_url)
        provision.run()
