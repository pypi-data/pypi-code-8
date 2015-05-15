import curses
import time
from operator import attrgetter


def main(screen, project, options):
    begin_x = 20; begin_y = 7
    height = 5; width = 40
    win = curses.newwin(height, width, begin_y, begin_x)

    screen.addstr(0, 0, 'docker ps')
    screen.addstr(1, 0, '---------')

    containers = sorted(
        project.containers(stopped=True) +
        project.containers(one_off=True),
        key=attrgetter('name')
    )

    for k, container in enumerate(containers):
        string = (
            container.name + ' ' + container.human_readable_state)
        screen.addstr(k+2, 0, string)

    screen.refresh()
    time.sleep(3)


def status(project, options):
    curses.wrapper(main, project, options)
