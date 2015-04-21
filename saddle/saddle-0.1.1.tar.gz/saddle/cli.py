"""Command line interface to saddle."""
from clip import App, ClipExit, arg, opt, echo
from search import Search
from runner import Runner
import os
import sys
import signal

app = App()
OPTIONS = None


@app.main(description='Functional test runner.')
@opt('-d', '--directory', default=os.getcwd(), name='directory', help='Directory to search in.')
@opt('-p', '--python', default=sys.executable, name='pythonpath', help="Which python path to run tests with.")
def saddle(**kwargs):
    """Parse global options."""
    def signal_handler(signal, frame):
        """Catch ctrl-C and SIGTERM and don't spew stack trace."""
        echo("")

    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)

    global OPTIONS
    OPTIONS = kwargs


@saddle.subcommand(description='Run single test')
@arg('name', required=True, help='File name, module name or simply part of the name of a test.')
@opt('-r', '--repeat', default=1, help='Number of times to run the test. Report % success and failure.')
@opt('-w', '--watch', nargs=1, default='', required=False, help='Run the test and watch for changes to the code using specified builder.')
def test(name, repeat, watch):
    """Run a single test."""
    search = Search(OPTIONS['directory'], name)
    search.run()
    if search.none():
        echo("""No tests found matching : "{0}". \n""".format(name))
        sys.exit(1)
    elif search.just_one():
        runner = Runner(OPTIONS['pythonpath'], search.just_one())

        if watch: # For some reason, clip.py returns this instead of True if the opt is specified
            builder.watch(watch, runner)
            sys.exit(0)

        if repeat == 1:
            echo("Running test {0}".format(runner.module_name))
            passed = runner.runonce()
            sys.exit(0) if passed else sys.exit(1)
        else:
            echo("Running test {0}, {1} times.".format(runner.module_name, repeat))
            pass_rate = runner.multiple(repeat)
            echo("Pass rate : {0}%".format(pass_rate))
            sys.exit(0)
    else:
        type_of_matches, matches = search.matching()
        echo("Multiple {0} test matches found:\n".format(type_of_matches))
        for match in matches:
            echo(" * {0}".format(match))
        sys.exit(1)

#@saddle.subcommand(description='Run test group')
#@opt('-t', '--tag', name='onlytag', help='Only run tests matching this tag.')
#@opt('-d', '--dir', name='onlydir', help='Only run tests in this directory.')
#@opt('-p', '--part', default='1/1', help='Run only a portion of the tests. 1/2 and 2/2 will run the first 50% and last 50% respectively.', name='part')
#@opt('-r', '--repeat', default=5, help='Number of times to repeat running failed tests until accepting the result.', name='repeat')
#def group(onlytag, onlydir, part, repeat):
    #echo('Run a group of tests.')
    #sys.exit(1)

#@saddle.subcommand(description='Rebuild environment to run a test.')
#@arg('name', required=True)
#def build(name):
    #echo('Tail a test's logs.')


#@saddle.subcommand(description='Cloud tests.')
#@arg('name', required=True)
#def cloud(name):
    #echo('Run cloud tests.')

#@saddle.subcommand(description='Tail a test's logs.')
#opt('-s', '--service', help='Which service to tail')
#opt('-l', '--lines', default=80, help='Number of lines to print before tailing live.')
#def tail(name):
    #echo('Tail a test's logs.')


#@saddle.subcommand(description='Run service engine alone.')
#@arg('name', required=True)
#def serviceengine(name):
    #echo('Determine which commit caused a test to break.')

#@saddle.subcommand(description='Determine which commit caused the bug (only works on git).')
#@arg('name', required=True)
#def bisect(name):
    #echo('Determine which commit caused a test to break.')

#@saddle.subcommand(description='Run (h)top listing all services currently running.')
#def top():
    #echo('Run process manager listing all of the services.')

#@saddle.subcommand(description='Subtest.')
#def subtest():
    #echo('Run shorter versions of long running tests.')

#@saddle.subcommand(description='Lint your test suite.')
#def lint():
    #echo('Lint your test suite.')

#@saddle.subcommand(description='List tags in suite.')
#@opt('-o', '--output', default='csv', name='output')
#def tags():
    #echo('List tags.')

def run():
    try:
        app.run()
    except ClipExit:
        pass

if __name__ == '__main__':
    run()
