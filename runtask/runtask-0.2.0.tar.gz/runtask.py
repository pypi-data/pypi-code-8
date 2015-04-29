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

__version__ = '0.2.0'
__author__ = 'Fabrizio Pollastri <f.pollastri@inrim.it>'


#### classes

class RunTask:
    """ Implements a coherent time task scheduler. The scheduling time used
    by RunTask is computed from the system time multiplying it by the *speed*
    factor (float) and adding the *phase* offset (float, unit: second). The
    result is quantized by *tick* value (float, unit: second) to obtain the
    scheduling time.
    """

    def __init__(self,speed=1.0,phase=0.0,tick=1.):

        # save arguments
        self.speed = speed
        self.phase = phase
        self.tick = tick

        # save system time base value
        self.systime_base = tm.time()

        # times (unix time floats)
        self.runtime = None

        # task list and run list
        self.tasks = {}
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
                if self.root_task_run.wait(self.torun[0][1] - self.runtime):
                    return

        # prepare thread for root task
        self.root_task = tg.Thread(target=root_task,args=(self,))
        self.root_task_run = tg.Event()


    def _time(self):
        """ Update the current scheduling time. """

        if self.speed != 1.0:
            self.runtime = self.speed * (tm.time()-self.systime_base)+self.phase
        else:
            self.runtime = tm.time() + self.phase
        self.runtime = self.runtime - mt.fmod(self.runtime,self.tick)


    def _run(self):
        """ Exec tasks that have reached time to run. """

        # run each task that has reached its run time
        runned = 0
        for self.task_id, self.truntime in self.torun:
            if self.truntime <= self.runtime:
                task,args,kargs,period,phase,runs = self.tasks[self.task_id]
                if args:
                    if kargs:
                        task(*args,**kargs)
                    else:
                        task(*args)
                else:
                    if kargs:
                        task(**kargs)
                    else:
                        task()
                
                # if required, do runs count down
                if runs > 0:
                    runs = runs - 1
                    self.tasks[self.task_id] = task,args,kargs,period,phase,runs
                # if task has a next run, queue it.
                if runs:
                    next_run_time = self.runtime + period  \
                        - mt.fmod(self.runtime - phase,period)
                    self.torun.append((self.task_id,next_run_time))
                runned = runned + 1
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
        for task_id,(task,args,kargs,period,phase,count) \
            in self.tasks.iteritems():
            first_run = self.runtime+period-mt.fmod(self.runtime-phase,period)
            self.torun.append((task_id,first_run))

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


    def task(self,task,args,kargs,period,phase=0.0,runs=-1):
        """ Register a task to be run.

          **task**: callable, a function, the task to be run.

          **args**: list/tuple, function positional arguments.

          **kargs**: dictionary, function keyword arguments.

          **period**: float, time elapse between task runs.

          **phase**: float, the time offset from which an integer number
          of *periods* are added to obtain the next task run time.

          **runs**: integer, number of task runs. If -1, run task forever.

        All times are in unix format, a float whose units are seconds from the
        beginning of epoch. 
        """

        # save task to tasks list
        task_id = len(self.tasks)
        self.tasks[task_id] = (task,args,kargs,period,phase,runs)

        return task_id


    def task_info(self):
        """ Return current task information.

        Return pattern (**id**, **runtime**, **runs**)

          **id**: integer, the task identifier, it is the order of registration
          starting from zero. 

          **runtime**: float, the nominal task run time.

          **runs**: integer, number of runs left. If -1, run for ever.
        """

        return self.task_id, self.truntime, self.tasks[self.task_id][5]

#### END
