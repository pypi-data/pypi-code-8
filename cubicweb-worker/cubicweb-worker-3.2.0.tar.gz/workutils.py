# copyright 2003-2014 LOGILAB S.A. (Paris, FRANCE), all rights reserved.
# contact http://www.logilab.fr/ -- mailto:contact@logilab.fr
#
# This file is part of CubicWeb tag cube.
#
# CubicWeb is free software: you can redistribute it and/or modify it under the
# terms of the GNU Lesser General Public License as published by the Free
# Software Foundation, either version 2.1 of the License, or (at your option)
# any later version.
#
# CubicWeb is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE.  See the GNU Lesser General Public License for more
# details.
#
# You should have received a copy of the GNU Lesser General Public License along
# with CubicWeb.  If not, see <http://www.gnu.org/licenses/>.

import logging
import os
from datetime import datetime, timedelta
from functools import partial

from cubicweb import ValidationError

logger = logging.getLogger('cubicweb.worker')

def make_worker(cnx):
    worker = cnx.create_entity('CWWorker',
                               last_ping=datetime.utcnow())
    return worker

def worker_ping(repo, eid_dict):
    with repo.internal_cnx() as cnx:
        rset = cnx.execute('SET W last_ping %(tstamp)s WHERE W eid %(eid)s',
                           {'eid': eid_dict['eid'],
                            'tstamp': datetime.utcnow()})
        if not rset:
            logger.warning('The worker %(eid)s apparently died.', eid_dict)
            worker = make_worker(cnx)
            logger.warning('Recreating a new worker (%s)', worker.eid)
            eid_dict['eid'] = worker.eid
        else:
            logger.debug('Worker %s successfully pinged', eid_dict)
        cnx.commit()

def worker_remove_stale_workers(repo, seconds=300):
    with repo.internal_cnx() as cnx:
        rset = cnx.execute(
            'DELETE CWWorker W  WHERE W last_ping < %(tstamp)s',
            {'tstamp': datetime.utcnow() - timedelta(seconds=seconds)})
        cnx.commit()
        if rset:
            logger.warning('Removed %s workers from the DB (%s)',
                           len(rset), rset.rows)

def worker_remove_old_tasks(repo, hours=6):
    with repo.internal_cnx() as cnx:
        cnx.execute('DELETE CWWorkerTask W  WHERE W in_state S,'
                    'S name IN ("task_failed", "task_done"),'
                    'W modification_date < %(tstamp)s',
                    {'tstamp': datetime.now() - timedelta(hours=hours)})
        cnx.commit()

def get_worker(cnx, repo, eid_dict):
    try:
        # clear_caches is required because the worker may have been removed
        # by another instance, in which case we would get the cached entity.
        repo.clear_caches((eid_dict['eid'],))
        worker = cnx.execute('Any W WHERE W eid %(eid)s',
                             eid_dict).get_entity(0, 0)
    except IndexError:
        raise ValueError(eid_dict)
    return worker



def worker_pending_tasks(repo, eid_dict):
    logger.debug('entering worker_pending_tasks for CWWorker eid %(eid)s', eid_dict)
    task, worker = 0, None # None is used as a condition variable
    with repo.internal_cnx() as cnx:
        try:
            if logger.getEffectiveLevel() <= logging.DEBUG:
                rset = cnx.execute(
                    'Any SN,COUNT(T) GROUPBY SN '
                    'WHERE T is CWWorkerTask, T in_state S, S name SN')
                logger.debug('CWWorkerTask: %s', rset.rows)
            worker = get_worker(cnx, repo, eid_dict)
        except ValueError:
            logger.debug(
                'worker_pending_tasks: no worker eid %(eid)s found, '
                'worker_ping will create a new one shortly', eid_dict)
            return

        while task is not None: # while there is job to do and the worker is not too loaded
            task = None
            try:
                task = worker.try_to_acquire_one_task()
                cnx.commit()
                # The work on the task itself must be done in another transaction / session
                if task is not None:
                    logger.info('Performing task %s with worker %s',
                                task.eid, worker.eid)
                    repo.threaded_task(partial(worker.perform_task, task))
            except ValidationError, exc:
                logger.warning('Got validation error while trying to acquire a '
                               'task with worker %s', worker.eid)
                cnx.rollback()
            except Exception, exc: # IntegrityError: but this does look backend dependant
                # need string comparison because of various backends
                if exc.__class__.__name__ != 'IntegrityError':
                    raise # Not the Exception we are looking for. Keep moving.
                logger.warning('Commit failed for worker %s and task %s: %s',
                               worker.eid, task and task.eid, exc)
                logger.warning('This may be due to two workers competing '
                               'for the same task (hence harmless).')
                cnx.rollback()

