import logging
import sys
from inspect import getdoc

from cmds.bash import bash
from cmds.lint import lint
from cmds.server import listen
from compose.cli.docopt_command import NoSuchCommand
from compose.cli.errors import UserError
from compose.cli.main import parse_doc_section, setup_logging, TopLevelCommand
from compose.project import NoSuchService, ConfigurationError
from compose.service import BuildError
from docker.errors import APIError

log = logging.getLogger(__name__)


class UtilsCommands(TopLevelCommand):
    """
    A wrapper around docker-compose with some extra commands.

    Usage:
        docker-utils [options] [COMMAND] [ARGS...]
        docker-utils -h|--help

    Options:
      -f, --file FILE           Specify an alternate compose file (default: docker-compose.yml)
      -p, --project-name NAME   Specify an alternate project name (default: directory name)
      --verbose                 Show more output
      -v, --version             Print version and exit

    Commands:
        bash      Start a bash prompt in the container *
        lint      Lints the YAML file for common errors *
        listen    Start a server that listens to Docker Hub webhooks *

        build     Build or rebuild services
        help      Get help on a command
        kill      Kill containers
        logs      View output from containers
        port      Print the public port for a port binding
        ps        List containers
        pull      Pulls service images
        restart   Restart services
        rm        Remove stopped containers
        run       Run a one-off command
        scale     Set number of containers for a service
        start     Start services
        stop      Stop services
        up        Create and start containers

    * commands provided by docker-utils
    """

    def bash(self, project, options):
        """
        Enter a bash prompt on a container running this image.

        Usage: bash [options] [SERVICE]
        """
        bash(project, options)

    def listen(self, project, options):
        """
        Start a webserver that listens to Docker Hub webhook events.

        Logs incoming webhook requests and verifies that it belongs to
        this compose project. If it does, it issues a pull to get the latest
        images.

        Usage: listen [options] [HOST] [PORT]
        """
        listen(project, options)

    def lint(self, project, options):
        """
        Lints the docker-compose YAML file for common errors.

        Usage: lint
        """
        lint(self, project, options)


def entry():
    setup_logging()
    try:
        command = UtilsCommands()
        command.sys_dispatch()
    except KeyboardInterrupt:
        log.error("\nAborting.")
        sys.exit(1)
    except (UserError, NoSuchService, ConfigurationError) as e:
        log.error(e.msg)
        sys.exit(1)
    except NoSuchCommand as e:
        log.error("No such command: %s", e.command)
        log.error("")
        log.error("\n".join(parse_doc_section("commands:", getdoc(e.supercommand))))
        sys.exit(1)
    except APIError as e:
        log.error(e.explanation)
        sys.exit(1)
    except BuildError as e:
        log.error("Service '%s' failed to build: %s" % (e.service.name, e.reason))
        sys.exit(1)

if __name__ == "__main__":
    sys.exit(entry())
