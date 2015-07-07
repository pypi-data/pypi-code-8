#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import os
import atexit
from signal import SIGTERM
from time import sleep
import logging


class daemon:

    """
    A generic daemon class.

    Usage: subclass the Daemon class and override the run() method
    """
    def __init__(self, name, rundir='/var/run', stdin='/dev/null', stdout='/dev/null', stderr='/dev/null'):

        # Run outside of python environment
        self.rundir = rundir
        self.stdin = stdin
        self.stdout = stdout
        self.stderr = stderr
        self.pidfile = '%s/%s.pid' % (rundir, name)
        self.name = name

        logging.debug("Sysproc init called")

    def daemonize(self):
        """
        do the UNIX double-fork magic, see Stevens' "Advanced
        Programming in the UNIX Environment" for details (ISBN 0201563177)
        http://www.erlenstar.demon.co.uk/unix/faq_2.html#SEC16
        """

        logging.debug("Beginning Daemon Process")
        logging.debug("Pidfile is [%s]", self.pidfile)

        try:
            logging.debug("Forking child from parent.")
            pid = os.fork()
            if pid > 0:
                # exit first parent
                sys.exit(0)
        except OSError as e:
            logging.fatal("fork #1 failed: %d (%s)\n" % (e.errno, e.strerror))
            sys.exit(1)

        # decouple from parent environment
        try:
            if not os.path.exists(self.rundir):
                os.makedirs(self.rundir)
        except Exception, e:
            logging.exception(e)
            raise e
        try:
            os.chdir(self.rundir)
            logging.debug('Set environment to [%s]', self.rundir)
        except Exception as e:
            logging.fatal(
                "Unable to set running directory [%s]", self.rundir)

        logging.debug(
            "Running directory set [%s]", self.rundir)

        os.setsid()

        logging.debug("SID Set")

        os.umask(0)
        logging.debug("Mask Set")

        # do second fork
        try:
            pid = os.fork()
            if pid > 0:
                # exit from second parent
                logging.debug("Second Fork Complete.")
                sys.exit(0)
        except OSError as e:
            logging.fatal("fork #2 failed: %d (%s)\n" % (e.errno, e.strerror))
            sys.exit(1)

        # redirect standard file descriptors
        sys.stdout.flush()
        sys.stderr.flush()
        si = file(self.stdin, 'r')
        so = file(self.stdout, 'a+')
        se = file(self.stderr, 'a+', 0)
        os.dup2(si.fileno(), sys.stdin.fileno())
        os.dup2(so.fileno(), sys.stdout.fileno())
        os.dup2(se.fileno(), sys.stderr.fileno())

        logging.debug("Flush Complete")

        # write pidfile
        try:
            atexit.register(self.delpid)
            pid = str(os.getpid())
            logging.debug(self.pidfile)
            file(self.pidfile, 'w+').write("%s\n" % pid)
        except Exception as e:
            logging.error(
                "Cannot Write Pid File [%s]. Error: [%s]", self.pidfile, e)
            exit(1)

        logging.debug("Pid is [%s]", pid)

    def delpid(self):
        os.remove(self.pidfile)

    def start(self):
        """
        Start the daemon
        """

        # Check for a pidfile to see if the daemon already runs
        try:
            pf = file(self.pidfile, 'r')
            pid = int(pf.read().strip())
            pf.close()
        except IOError:
            logging.info(
                "No PID file [%s]. Will Continue.", self.pidfile)
            pid = None

        if pid:
            sys.stdout.write("%s already running\n" % self.name)
            sys.exit(1)

        # Start the daemon
        sys.stdout.write("Starting %s\n" % self.name)
        self.daemonize()
        self.run()

    def stop(self):
        """
        Stop the daemon
        """
        # Get the pid from the pidfile
        try:
            pf = file(self.pidfile, 'r')
            pid = int(pf.read().strip())
            pf.close()
            logging.debug("PIDFILE [%s] found" % pf)
        except IOError:
            pid = None
            logging.fatal('NO PID FILE FOUND')
        if not pid:
            sys.stderr.write("%s not running\n" % self.name)
            return  # not an error in a restart

        # Try killing the daemon process
        try:
            sys.stdout.write("Stopping %s" % self.name)
            while True:
                sys.stdout.write(".")
                os.kill(pid, SIGTERM)
                sleep(0.1)
        except OSError as err:
            err = str(err)
            if err.find("No such process") > 0:
                if os.path.exists(self.pidfile):
                    os.remove(self.pidfile)
            else:
                sys.exit(1)
        sys.stdout.write("\n%s stopped\n" % self.name)

    def restart(self):
        """
        Restart the daemon
        """
        self.stop()
        self.start()

    def run(self):
        """
        You should override this method when you subclass Daemon.
        It will be called after the process has been
        daemonized by start() or restart().
        """
