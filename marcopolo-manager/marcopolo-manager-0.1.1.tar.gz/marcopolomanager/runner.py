#!/usr/bin/env python
"""
Using an IOLoop instance all the onSetup jobs on loading are executed 
and the the onReload functionality is scheduled.

By default, the runner loads all the MarcoManager-inherited classes defined 
in the modules inside the ``/etc/marcopolomanager/managers`` directory.
To include other file, just import it in the runner.py file or modify the path in the 
configuration file.

The runner uses standard UNIX signals to reload the application and gracefully stop
 all the managers using SIGUSR1 to schedule functionality.
"""
from __future__ import absolute_import
import signal, logging
import sys, os
import inspect

import tornado.ioloop
import tornado.concurrent

from marcopolomanager import conf
from marcopolomanager.marcopolomanager import MarcoPoloManager

sys.path.insert(0, conf.MANAGERS_DIR)
from managers import *

io_loop = tornado.ioloop.IOLoop.instance()

def sigterm_handler(signum, frame):
    """
    Triggers the onStop event and then stops the IOLoop
    """
    for manager in manager_instances:
        manager.onStop()
    logging.info("Stopping runner")
    io_loop.stop()
    sys.exit(0)

def sigusr1_handler(signum, frame):
    """
    Handles the USR1 signal, used for reloading the services
    """
    signal.signal(signal.SIGUSR1, signal.SIG_IGN)
    for manager in manager_instances:
        manager.onReload()
    logging.info("Reloading runner")
    signal.signal(signal.SIGUSR1, sigusr1_handler)


classes = []
manager_instances = []
names = []
for name, obj in [(name, obj) for name, obj in \
    inspect.getmembers(sys.modules[__name__]) \
    if issubclass(obj.__class__, MarcoPoloManager.__class__) \
    and name not in ["Future", "ABCMeta", "MarcoPoloManager"]]:
    classes.append(obj)
    names.append(name)



def log(future):
    """
    Gets the result of a future and logs it.
    """
    result = future.result()
    if result is not None:
        logging.info(future.result())


def main(argv=None):  
    """
    Starts the daemon and service units.
    Initializes the runfile and logs and then starts the IOLoop
    """
    for manager_instance in [m for m in classes if m.__disable__ == False]:
        manager_instances.append(manager_instance())

    signal.signal(signal.SIGTERM, sigterm_handler)
    signal.signal(signal.SIGUSR1, sigusr1_handler)
    signal.signal(signal.SIGINT, sigterm_handler)
    #signal.signal(signal.SIGHUP, signal.SIG_IGN)
    
    for manager in manager_instances:
        if manager.enable():
            io_loop.call_later(manager.delay(), 
                               io_loop.add_future, 
                               manager.onSetup(), 
                               log)
            
            doReload = int(manager.doReload()) * 1000
            if doReload != False:
                tornado.ioloop.PeriodicCallback(manager.onReload, doReload).start()
    
    if not os.path.exists(conf.LOGDIR):
        os.makedirs(conf.LOGDIR)
    
    logging.basicConfig(filename=os.path.join(conf.LOGDIR, conf.LOGFILE),
                        level=conf.DEBUG_LEVEL)
    
    logging.info("Starting runner with the services %s" % u', '.join(names))
    
    io_loop.start()

if __name__ == "__main__":
    main(sys.argv[1:])
