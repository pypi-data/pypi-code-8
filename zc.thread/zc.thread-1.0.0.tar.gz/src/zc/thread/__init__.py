##############################################################################
#
# Copyright (c) Zope Foundation and Contributors.
# All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.0 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
#
##############################################################################

import atexit

exiting = False

@atexit.register
def set_exiting():
    global exiting
    exiting = True

def _options(daemon=True, start=True, args=(), kwargs=None, restart=False):
    return daemon, start, args, kwargs or {}, restart

def _Thread(class_, func, options):
    daemon, start, args, kwargs, restart = _options(**options)

    name = "%s.%s" % (getattr(func, '__module__', None),
                      getattr(func, '__name__', None))

    def run(*args, **kw):
        while 1:
            try:
                v = func(*args, **kw)
                thread.value = v
                return
            except Exception as v:
                thread.exception = v
                if exiting:
                    return
                import logging
                logging.getLogger(name).exception(
                    'Exception in %s', class_.__name__)
                import traceback
                traceback.print_exc()
                if not restart:
                    return
                import time
                time.sleep(restart)

    thread = class_(target=run, name=name, args=args, kwargs=kwargs)

    if hasattr(thread, 'setDaemon'):
        thread.setDaemon(daemon)
    else:
        thread.daemon = daemon
    thread.value = thread.exception = None
    if start:
        thread.start()
    return thread


def Thread(func=None, **options):
    """Create and (typically) start a thread

    If no function is passed, then a decorator function is
    returned. Typical usage is::

       @zc.thread.Thread
       def mythreadfunc():
           ...

       ...

       mythread.join()

    Options:

        deamon=True
           Thread daemon flag. Set to false to cause process exit to
           block until the thread has exited.

        start=True
           True to automatically start the thread.

        args=()
           Positional arguments to pass to the thread function.

        kwargs={}
           keyword arguments to pass to the thread function.

    """
    if func is None:
        return lambda f: Thread(f, **options)
    import threading
    return _Thread(threading.Thread, func, options)

def Process(func=None, **options):
    """Create and (typically) start a multiprocessing process

    If no function is passed, then a decorator function is
    returned. Typical usage is::

       @zc.thread.Process
       def mythreadfunc():
           ...

       ...

       mythread.join()

    Options:

        deamon=True
           Process daemon flag. Set to false to cause process exit to
           block until the process has exited.

        start=True
           True to automatically start the process.

        args=()
           Positional arguments to pass to the process function.

        kwargs={}
           keyword arguments to pass to the process function.

    """
    if func is None:
        return lambda f: Process(f, **options)
    import multiprocessing
    return _Thread(multiprocessing.Process, func, options)
