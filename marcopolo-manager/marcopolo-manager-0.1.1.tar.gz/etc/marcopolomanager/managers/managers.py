# -*- coding: utf-8 -*-
from __future__ import absolute_import
import sys, logging, time

from tornado.concurrent import Future, run_on_executor

from marcopolo.bindings import marco, polo

from marcopolomanager.marcopolomanager import MarcoPoloManager

class CompilerDiscover(MarcoPoloManager):
    """
    Uses `MarcoPolo <file:///home/martin/TFG/workspaces/discovery/doc/build/html/index.html>`_ 
    through the  :class:`Marco python binding<marcopolo.bindings.marco.Marco>` to
    discover the available `distcc <https://code.google.com/p/distcc/>`_ compilers on the network.
    If successful, it modifies the `/etc/distcc/hosts` with the results.

    This manager is executed with a delay of 10 seconds after startup and reloads every hour.
    """
    @run_on_executor
    def onSetup(self):
        """
        Sends a :py:meth:`Request_for<marcopolo.bindings.marco.Marco.request_for>` message asking for nodes
        with the *compiler* service. If successful, it dumps the results to the '/etc/distcc/hosts file'
        """
        m = marco.Marco()
        while True:
            try:
                nodes = m.request_for("compiler")
                break
            except marco.MarcoTimeOutException:

                time.sleep(1)
                print("Retrying")
        try:
            f = open('/etc/distcc/hosts', 'w')
            for node in nodes:
                f.write(node.address)
                logging.info("Adding compiler %s", node.address)
            f.close()
        except Exception as e:
            logging.warning("Something happened while executing CompilerDiscover: %s" % e)
        return 0
    
    def onStop(self):
        """
        Nothing is done
        """
        pass

    def delay(self):
        """
        Returns 10, the number of seconds to wait
        """
        return 10

    def onReload(self):
        """
        On reload, requests again for the *compiler* service, and dumps
        the results to the hosts file.
        """
        m = marco.Marco()
        while True:
            try:
                nodes = m.request_for("compiler")
                break
            except marco.MarcoTimeOutException:
                time.sleep(1)
                print("Retrying")
        try:
            f = open('/etc/distcc/hosts', 'w')
            for node in nodes:
                f.write(node.address)
            f.close()
        except FileNotFoundException:
            pass
        except Exception as e:
            logging.warning("Unexpected error %s" % e)
    
    def doReload(self):
        """
        Schedules a reload every 3600 seconds (an hour)
        """
        return 3600

    def enable(self):
        return False

class HostnameManager(MarcoPoloManager):
    """
    Includes hostname information in marcopolo
    """

    """By default, disabled"""
    __disable__ = True
    @run_on_executor
    def onSetup(self):
        import socket
        hostname = socket.gethostname()

    def onStop(self):
        pass

    def onReload(self):
        import socket
        hostname = socket.gethostname()

    def doReload(self):
        return 3600
    def enable(self):
        return False

class EnableTomcatManager(MarcoPoloManager):
    __disable__ = True
    @run_on_executor
    def onSetup(self):
        pass

    def onStop(self):
        pass
    def enable(self):
        return False
class EnableHadoopMaster(MarcoPoloManager):
    __disable__ = True
    @run_on_executor
    def onSetup(self):
        pass

    def onStop(self):
        pass
    def enable(self):
        return False
