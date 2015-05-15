import sys

from cmds.bash import bash
from cmds.status import status
from compose.cli.main import setup_logging, TopLevelCommand


class UtilsCommands(TopLevelCommand):
    """
    A wrapper around docker compose with some extra commands.

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
        Enter a bash prompt on the service. The container must be running.

        Usage: bash [options] [SERVICE]
        """
        bash(project, options)

    def status(self, project, options):
        """
        Show a status console.

        Usage: bash [options]
        """
        status(project, options)


def entry():
    setup_logging()
    command = UtilsCommands()
    command.sys_dispatch()


if __name__ == "__main__":
    sys.exit(entry())
