#!/usr/bin/python
# .+
# .context    : RunTask, coherent time task scheduler
# .title      : RunTask, coherent time task scheduler
# .kind	      : python source
# .author     : Fabrizio Pollastri
# .site	      : Torino - Italy
# .creation   :	7-Feb-2015
# .copyright  :	(c) 2015 Fabrizio Pollastri
# .license    : GNU General Public License (see below)
#
# This file is part of "RunTask, Coherent Time Task Scheduler".
#
# RunTask is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as
# published by the Free Software Foundation, either version 3 of
# the License, or (at your option) any later version.
#
# RunTask is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this software. If not, see <http://www.gnu.org/licenses/>.
#
# .-


#### import required modules

import math as mt      # mathematical support
import operator as op  # itemgetter
import threading as tg # multiple thread of run
import time as tm      # time support


#### define global variables

__version__ = '0.4.0'
__author__ = 'Fabrizio Pollastri <f.pollastri@inrim.it>'


#### classes

class RunTask:
    """ Implements a coherent time task scheduler. The scheduling time used
    by RunTask is computed from the system time multiplying it by the *speed*
    factor (float) and setting *epoch* (float, unit: second) as the beginning
    of time. The result is quantized by *tick* value (float, unit: second) to
    obtain the scheduling time.
    """

    def __init__(self,speed=1.0,epoch=0.0,tick=1.):

        # save arguments
        self.speed = speed
        self.epoch = epoch
        self.tick = tick

        # save system time base value
        self.systime_base = tm.time()

        # times (unix time floats)
        self.runtime = None

        # init timing arguments
        self.timing_args = None

        # task list and run list
        self.tasks = {}
        self.tasks_run_count = {}
        self.torun = []

        # root task
        def root_task(self):

            # run until terminate
            while True:
                # run all tasks
                self._time()
                self._run()
                # if run list is empty, terminate
                if not self.torun:
                    return
                # wait until next run time comes
                self._time()
                if self.root_task_run.wait(self.torun[0][1] - self.time):
                    return

        # prepare thread for root task
        self.root_task = tg.Thread(target=root_task,args=(self,))
        self.root_task_run = tg.Event()


    def _time(self):
        """ Update the current scheduling time. """

        # presume the same time speed of system time
        self.time = tm.time()
        # if the required time speed is the same of system time ...
        if self.speed == 1.0:
            # if epoch != 0.0, set absolute start of time.
            if self.epoch:
                self.time = self.time() - self.systime_base + self.epoch
        # if time speed is different from system time speed, compute a new 
        # time, starting at self.epoch and flowing whith the given speed.
        else:
            self.time = self.speed * (self.time - self.systime_base) \
                + self.epoch
        # runtime is quantized by tick value
        self.runtime = self.time - mt.fmod(self.time,self.tick)


    def _run(self):
        """ Exec tasks that have reached time to run. """

        # run each task that has reached its run time
        runned = 0
        for self.task_id, self.task_runtime in self.torun:
            # if current task has reached the run time ...
            if self.task_runtime <= self.runtime:
                target,args,kargs,timing,timing_args,worker = \
                    self.tasks[self.task_id]
                if args:
                    if kargs:
                        target(*args,**kargs)
                    else:
                        target(*args)
                else:
                    if kargs:
                        target(**kargs)
                    else:
                        target()
                next_run_time = next(timing)
                # if task has a next run, queue it
                if next_run_time:
                    self.torun.append((self.task_id,next_run_time))
                # count the tasks that are runned
                runned = runned + 1
            # the rest of tasks has not reached the run time, exit run loop.
            else:
                break

        # sort future runs by run ascending time
        if self.torun:
            self.torun = sorted(self.torun[runned:],key=op.itemgetter(1))


    def start(self,join=False):
        """ Start execution of registered tasks. If *join* is False, *start*
        returns immediately to the calling program. If *join* is True, *start*
        returns only when *stop* is called by a registered task. """

        # update current time
        self._time()

        # put all tasks on the run list, computing the first run time.
        for self.task_id,(task,args,kargs,timing,timing_args,worker) \
            in self.tasks.iteritems():
	    self.torun.append((self.task_id,next(timing)))

        # sort run list by ascending runtime
	self.torun = sorted(self.torun,key=op.itemgetter(1))

        # start thread
        self.root_task.start()

        # if required join thread
	if join:
           self.root_task.join()


    def stop(self):
	""" Stop execution of registered tasks. """

	self.root_task_run.set()
        self.root_task.join()


    def task(self,target=None,args=(),kargs={},timing=None,worker=None):
        """ Register a task to be run.

          **target**: callable, a function, a class method, the task to be run.

          **args**: list/tuple, function positional arguments.

          **kargs**: dictionary, function keyword arguments.

          **timing**: a call to one of the timing methods, periodic, etc.

          **worker**: at present, not used.

        All times are in unix format, a float whose units are seconds from the
        beginning of epoch. 
        """

        # save task and its parameters to the tasks list
        self.task_id = len(self.tasks)
        self.tasks[self.task_id] =(target,args,kargs,timing,next(timing),worker)

        # init numbering of each task run
        self.tasks_run_count[self.task_id] = 1

        return self.task_id


    def task_info(self):
        """ Return current task information.

        Return pattern (**id**, **runtime**, **run_count**, **task_args**)

          **id**: integer, the task identifier, it is the order of registration
          starting from zero. 

          **runtime**: float, the nominal task run time.

          **run_count**: integer, number of current run, first run is #1.

          **task_args**: tuple, all args saved by task method, (*target,
          args, kargs, timing, timing_args, worker*). **timing_args** is the
          tuple of the arguments given to the timing method specified in the
          task method call.
        """

        return self.task_id, self.task_runtime, \
            self.tasks_run_count[self.task_id], self.tasks[self.task_id]


    def runs_left(self):
        """ Return the number of runs left excluding the current one.
        If the task is run forever, return -1 . """

        timing =  self.tasks[self.task_id][3].__name__
        if timing == 'aligned':
            runs = self.tasks[self.task_id][4][2]
        elif timing is 'now':
            runs = self.tasks[self.task_id][4][1]
        elif timing is 'uniform':
            runs = self.tasks[self.task_id][4][2]
        else:
            assert False, 'invalid timing argument: ' + str(timing)
        # if task loops forever, return -1
        if runs == -1:
            return runs
        # otherwise, return the runs left.
        else:
            return runs - self.tasks_run_count[self.task_id]


    def aligned(self,period=1.0,phase=0.0,runs=-1):
        """ Timing generator. Set a periodic timing. The timing period can
        be aligned to a reference time. The task execution can be a single
        shot, a given number of times or forever.

          **period**: float (seconds) or tuple (numerator seconds,
          denominator seconds), time elapse between task runs.
          If tuple, the period is a fractional number: the first is the
          numerator, the second is the denominator.

          **phase**: float (seconds), the time offset from which an integer
          number of *periods* are added to obtain the next task run time.

          **runs**: integer, number of task runs. If -1, run task forever.

        The first task run happens when the RunTask time reaches the
        next integer multiple of **period** plus **phase**. 
        """

        # return the next run time aligned to an integer multiple of period.
        def next_runtime():
            # computation for fractional period
            if type(period) is tuple:
                period1 = float(period[0]) / period[1]
                return self.runtime + period1 \
                    - mt.fmod(mt.fmod(self.runtime,period[0]),period1) + phase
            # computation for float/int period
            else:
                return self.runtime+period-mt.fmod(self.runtime,period)+phase

        # first call: return arguments
        yield (period,phase,runs)
 
        # second call: return the first run time.
	yield next_runtime()

        # subsequent calls: the next run time.
        while True:

            # count run
            self.tasks_run_count[self.task_id] += 1

            # if task has a next run, queue it and return the num of runs left
            if self.tasks_run_count[self.task_id] - runs:
                yield next_runtime()
            # no next run, return zero
            else:
                yield 0


    def now(self,period=1.0,runs=-1):
        """ Timing generator. Set a periodic timing with immediate start.
        The task execution can be a single shot, a given
        number of times or forever.

          **period**: float (seconds) or tuple (numerator seconds,
          denominator seconds), time elapse between task runs.
          If tuple, the period is a fractional number: the first is the
          numerator, the second is the denominator.

          **runs**: integer, number of task runs. If -1, run task forever.

        Task run is aligned with a multiple of time tick.
        """

        # first call: return arguments
        yield (period,runs)
 
        # second call: return the first run time.
	start = self.runtime
	yield self.runtime

        # subsequent calls: the next run time.
        while True:

            # count run
            self.tasks_run_count[self.task_id] += 1

            # if task has a next run, queue it and return the num of runs left
            if self.tasks_run_count[self.task_id] - runs:
                # computation for fractional period
                if type(period) is tuple:
                    period1 = float(period[0]) / period[1]
                    yield self.runtime + period1 \
                        - mt.fmod(mt.fmod(self.runtime-start,period[0]),period1)
                # computation for float/int period
                else:
                    yield  self.runtime+period-mt.fmod(
                        self.runtime - start,period)
            # no next run, return zero
            else:
                yield 0


    def uniform(self,period_min=1.0,period_max=10.0,runs=-1):
        """ Timing generator. Set an execution timing aligned to the first
        period and repeat period with a random unform distribution between
        *period_min* and *period_max*. The task execution can be a single
        shot, a given number of times or forever.

          **period_min**: float (seconds), minimum of period execution time.

          **period_max**: float (seconds), maximum of period execution time.

          **runs**: integer, number of task runs. If -1, run task forever.

        Task run is aligned with a multiple of time tick.
        """

        import random as rd

        # first call: return arguments
        yield (period_min,period_max,runs)
 
        # second call: return the first run time.
        period = rd.uniform(period_min,period_max)
	yield self.runtime + period - mt.fmod(self.runtime,period)

        # subsequent calls: the next run time.
        while True:

            # count run
            self.tasks_run_count[self.task_id] += 1

            # if task has a next run, queue it and return the num of runs left
            if self.tasks_run_count[self.task_id] - runs:
	        yield self.task_runtime + rd.uniform(period_min,period_max)
            # no next run, return zero
            else:
                yield 0

#### END
