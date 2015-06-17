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
import doctest
import mock
import os
import sys
import unittest
import zc.thread

class TestThread(unittest.TestCase):

    def test_default(self):
        with mock.patch('threading.Thread') as Thread:
            @zc.thread.Thread
            def foo():
                return 42

            Thread.call_args[1].pop('target')()
            self.assert_(foo.value == 42 and foo.exception is None)
            Thread.assert_called_with(name='zc.thread.tests.foo',
                                      args=(), kwargs={})
            foo.setDaemon.assert_called_with(True)
            foo.start.assert_called_with()

    @mock.patch('logging.getLogger')
    @mock.patch('traceback.print_exc')
    def test_undecorated_and_exception_return(self, print_exc, getLogger):
        with mock.patch('threading.Thread') as Thread:
            def foo2():
                raise ValueError(42)

            Thread.__name__ = 'Thread'
            t = zc.thread.Thread(foo2)
            Thread.call_args[1].pop('target')()
            Thread.assert_called_with(
                name='zc.thread.tests.foo2', args=(), kwargs=dict())
            t.setDaemon.assert_called_with(True)
            t.start.assert_called_with()
            self.assert_(t.value is None)
            self.assert_(isinstance(t.exception, ValueError))
            self.assert_(t.exception.args == (42,))

            getLogger.assert_called_with('zc.thread.tests.foo2')
            getLogger.return_value.exception.assert_called_with(
                "Exception in %s", "Thread")

            print_exc.assert_called_with()

            t = zc.thread.Thread(foo2, args=(1, 2))
            Thread.call_args[1].pop('target')(1, 2)
            Thread.assert_called_with(name='zc.thread.tests.foo2',
                                      args=(1, 2), kwargs=dict())
            t.setDaemon.assert_called_with(True)
            t.start.assert_called_with()
            self.assert_(t.value is None)
            self.assert_(isinstance(t.exception, TypeError))


    @mock.patch('logging.getLogger')
    @mock.patch('traceback.print_exc')
    @mock.patch('threading.Thread')
    def test_no_exceotion_handling_if_exiting(
        self, Thread, print_exc, getLogger):
        self.assertEqual(zc.thread.exiting, False)
        zc.thread.set_exiting()
        self.assertEqual(zc.thread.exiting, True)

        @zc.thread.Thread
        def foo2():
            raise ValueError(42)
        Thread.call_args[1].pop('target')()
        getLogger.assert_not_called()
        print_exc.assert_not_called()
        zc.thread.exiting = False

    @mock.patch('time.sleep')
    @mock.patch('logging.getLogger')
    @mock.patch('traceback.print_exc')
    @mock.patch('threading.Thread')
    def test_restart(self, Thread, print_exc, getLogger, sleep):
        called = []
        Thread.__name__ = 'Thread'

        @zc.thread.Thread(restart=9)
        def foo2():
            called.append(0)
            if len(called) < 3:
                raise ValueError(42)
            else:
                raise BaseException

        self.assertRaises(BaseException, Thread.call_args[1].pop('target'))
        self.assertEqual(len(called), 3)
        sleep.assert_called_with(9)

    def test_passing_arguments(self):
        with mock.patch('threading.Thread') as Thread:
            @zc.thread.Thread(args=(1, 2), kwargs=dict(a=1), daemon=False,
                              start=False)
            def foo(*a, **k):
                return a, k

            Thread.call_args[1].pop('target')(1, 2, **dict(a=1))
            self.assert_(foo.value == ((1, 2), dict(a=1)))
            Thread.assert_called_with(name='zc.thread.tests.foo',
                                      args=(1, 2), kwargs=dict(a=1))
            foo.setDaemon.assert_called_with(False)
            self.assert_(not foo.start.called)

    def test_Thread_wo_mock(self):
        @zc.thread.Thread
        def foo():
            return 42

        foo.join()
        self.assert_(foo.value == 42)

    def test_Process_w_mock(self):
        with mock.patch('multiprocessing.Process') as Process:

            @zc.thread.Process
            def foo():
                print('foo called')
            Process.call_args[1].pop('target')()
            Process.assert_called_with(name='zc.thread.tests.foo',
                                       args=(), kwargs={})
            self.assert_(foo.daamon)
            foo.start.assert_called_with()
            Process.reset_mock()

            def foo2():
                return 42
            t = zc.thread.Process(foo2)
            Process.call_args[1].pop('target')()
            self.assertEqual(Process.return_value.value, 42)
            Process.assert_called_with(
                name='zc.thread.tests.foo2', args=(), kwargs={})
            self.assert_(t.daamon)
            t.start.assert_called_with()
            Process.reset_mock()

    def test_Process_w_mock2(self):

        with mock.patch('multiprocessing.Process') as Process:

            del Process.return_value.setDaemon

            @zc.thread.Process(daemon=False, start=False, args=(42,),
                               kwargs=dict(a=1))
            def foo3():
                print('foo3 called')
            Process.call_args[1].pop('target')()
            Process.assert_called_with(
                name='zc.thread.tests.foo3', args=(42,), kwargs=dict(a=1))
            self.assert_(not foo3.daemon)
            self.assert_(not foo3.start.called)

    def test_Process_wo_mock(self):
        import multiprocessing
        queue = multiprocessing.Queue()
        zc.thread.Process(run_process, args=(queue,)).join(11)
        self.assert_(queue.get() != os.getpid())

def run_process(queue):
    queue.put(os.getpid())

def test_suite():
    return unittest.makeSuite(TestThread)
