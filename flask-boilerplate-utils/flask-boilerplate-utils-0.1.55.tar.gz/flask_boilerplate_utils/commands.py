from flask.ext.script import Option, Manager, Command

# Manager Factory.
def MainManager(app, tests_module=None, **kwargs):
    """
    A factory which creates a flask-script manager and configure it for use
    with the boilerplate. 

    :param kwargs: keyword arguments to send to flask-script's Manager
                   class initialiser
    """

    manager = Manager(app,**kwargs)
    manager.add_command('server', Run(app))
    manager.add_command('meinheld', Host(app))
    if tests_module:
        tests_command = Test(app)
        tests_command.tests_module = tests_module
        manager.add_command('test', tests_command)

    return manager


class BaseCommand(Command):
    """
    Base command class which comes with the default options
    """

    option_list = (Option('--config', '-c', dest='config', nargs=1, action='store', help='Provide'\
            'a configuation class defined in config.'),)

    def __init__(self, app):
        super(Command, self).__init__()
        self.app = app


class Run(BaseCommand):
    "Run the Flask Builtin Server (Not for production)"

    option_list = (
        Option('--hostname', '-h', dest='hostname', default=None, type=str),
        Option('--port', '-p', dest='port', default=None, type=int),
        Option('--no-debug', '-n', dest='debug', default=True, action='store_false'),       
    ) + BaseCommand.option_list

    def run(self, port, hostname, debug, config, **kwargs):
        if port is None:
            port = self.app.config.setdefault('LISTEN_PORT', 8000)
        if hostname is None:
            hostname = self.app.config.setdefault('LISTEN_HOST', '127.0.0.1')

        self.app.run(debug=debug, host=hostname, port=port)

class Test(BaseCommand):
    def run(self, **kwargs):
        import unittest
        suite = unittest.TestLoader().loadTestsFromModule(self.tests_module)
        unittest.TextTestRunner(verbosity=2).run(suite)

class Host(BaseCommand):
    """
    Run a Web Server for Hosting using meinheld.
    """

    option_list = (
        Option('--hostname', '-h', dest='hostname', default='0.0.0.0', type=str),
        Option('--port', '-p', dest='port', default=8000, type=int),
    ) + BaseCommand.option_list
    def run(self, port, hostname, **kwargs):
        if port is None:
            port = self.app.config.setdefault('LISTEN_PORT', 8000)
        if hostname is None:
            hostname = self.app.config.setdefault('LISTEN_HOST', '127.0.0.1')

        from meinheld import server, patch
        patch.patch_all()
        print(" - Running Hosting Server using Meinheld")
        print(" - http://%s:%s/" % (hostname, port))
        server.listen((hostname, port))
        server.run(self.app)
