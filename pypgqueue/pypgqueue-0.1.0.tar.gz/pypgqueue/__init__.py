"""A simple job queue built on PostgreSQL's listen/notify functionality."""
import logging
import os
import time
import traceback
from concurrent.futures import ThreadPoolExecutor
from threading import Lock

import arrow
from bidon.data import ModelBase, ModelAccess, transaction
from bidon.data.data_access_core import get_pg_core


_PROJ_ROOT = os.path.dirname(os.path.abspath(__file__))

_JOBS_TN = "job.jobs"
_SZK_TN = "job.serialization_keys"
_PG_CHANNEL_NAME = "job_inserted"
_SLEEP = 1.0

STOP_NEVER = 0x0
STOP_NOW = 0x01
STOP_WHEN_CURRENT_DONE = 0x02
STOP_WHEN_ALL_DONE = 0x04


class Job(ModelBase):
  """Model of a job. Do not create this class directly, use queue_job."""
  table_name = _JOBS_TN
  timestamps = ("created_at", None)
  attrs = dict(
    name=None,
    args=None,
    priority=None,
    serialization_key_id=None,
    started_at=None,
    completed_at=None,
    error_message=None)

  @classmethod
  def build(cls, name, args, serialization_key_id=None, *, priority=0, table_name=_JOBS_TN):
    """Construct a job and set a custom table name."""
    job = cls(name=name, args=args, serialization_key_id=serialization_key_id, priority=priority)
    job.table_name = table_name
    return job


class SerializationKey(ModelBase):
  """Model of a serialization key. No two jobs with the same serialization key will run at the
  same time. Do not create this class directly, use queue_job.
  """
  table_name = _SZK_TN
  timestamps = None
  attrs = dict(key=None, active_job_id=None)

  @classmethod
  def build(cls, key, *, table_name=_SZK_TN):
    """Construct a serialization key and set a custom table name."""
    sz_key = cls(key=key)
    sz_key.table_name = table_name
    return sz_key


def queue_job(data_access, job_name, job_args=None, serialization_key=None, *, priority=0,
              jobs_table_name=_JOBS_TN, serialization_keys_table_name=_SZK_TN):
  """Queues a job for a given connection.

  job_name must be a string that has been registered with the watching PyPGQueue.
  job_args must be an object that psycopg will turn into json (by default, a dict) or None.
  serialization_key is a string, and will instruct the PyPGQueue to not run the job while
    another job with the same serialization key is running. If the job has no limits on when it can
    run, leave serialization_key as None.
  priority allows custom ordering of jobs. A higher priority will make a job run earlier. Jobs with
    the same priority are started in the order they are inserted.

  This method must be called in a transaction if a serialization key is given
  """
  if serialization_key:
    sz_key = data_access.find_model(SerializationKey, dict(key=serialization_key))
    if sz_key is None:
      sz_key = SerializationKey.build(serialization_key, table_name=serialization_keys_table_name)
      data_access.insert_model(sz_key)
    job = Job.build(job_name, job_args, sz_key.id, priority=priority, table_name=jobs_table_name)
    data_access.insert_model(job)
  else:
    sz_key = None
    job = Job.build(job_name, job_args, None, table_name=jobs_table_name)
    data_access.insert_model(job)

  return (job, sz_key)


def _exception_to_message(ex):
  """Converts an exception to a string."""
  if ex is None:
    return None
  ex_message = "Exception Type {0}: {1}".format(type(ex).__name__, ex)
  return ex_message + "\n" + "".join(traceback.format_tb(ex.__traceback__))


def get_ddl():
  """Returns the DDL text that can be used to create the postgres database."""
  with open(os.path.join(_PROJ_ROOT, "ddl.sql")) as rfile:
    return rfile.read()


class PyPGQueue(object):
  """PyPGQueue is a job queuer that uses PostgreSQL's pubsub functionality to minimize database
  polling. It features job prioritization and serialization.
  """
  # pylint: disable=too-many-instance-attributes

  def __init__(self, connection_string, workers=10, *, logger=None, jobs_table_name=_JOBS_TN,
               serialization_keys_table_name=_SZK_TN):
    self._data_access = ModelAccess(get_pg_core(connection_string))
    self._workers = workers
    self._logger = logger
    self._jobs_table_name = jobs_table_name
    self._serialization_keys_table_name = serialization_keys_table_name
    self._executor = ThreadPoolExecutor(max_workers=workers)
    self._waiting_jobs = 0
    self._running_futures = []
    self._completed_jobs = []
    self._completed_jobs_lock = Lock()
    self._stop_requested = STOP_NEVER
    self._stop_callback = None
    self._job_functions = {}

  def register_job_function(self, name, fxn):
    """Register a function for a job name."""
    if name in self._job_functions:
      raise Exception("A method has already been registered for job name {0}".format(name))
    self._job_functions[name] = fxn

  def job(self, name):
    """A decorator function that calls register_job_function on the decoratee."""
    def decorator(fxn):
      """A decorator to register a function as a job."""
      self.register_job_function(name, fxn)
      return fxn
    return decorator

  def start(self):
    """Start the job queuer."""
    self._data_access.open(autocommit=True)
    self._loop()

  def stop(self, callback=None, stop_manner=STOP_WHEN_CURRENT_DONE):
    """Request the job queuer to stop."""
    if self._stop_requested == STOP_NEVER:
      self._stop_callback = callback
      self._stop_requested = stop_manner
      self._log("Stop requested")

  def _log(self, message, loglevel=logging.INFO):
    """Log a message if a logger is attached to the instance."""
    if self._logger:
      if isinstance(message, (list, tuple, set)):
        message = "\t".join(str(i) for i in message)
      self._logger.log(loglevel, message)

  def _loop(self):
    """Run the job loop."""
    # pylint: disable=too-many-branches
    self._log("Starting")
    self._waiting_jobs = self._data_access.count(self._jobs_table_name, "started_at is null")
    self._data_access.execute("listen {0};".format(_PG_CHANNEL_NAME))

    # total_jobs_run = 0
    start_new_count = self._waiting_jobs

    while self._stop_requested != STOP_NOW:
      # If STOP_NEVER we will continue to register new jobs
      if self._stop_requested == STOP_NEVER:
        cn = self._data_access.connection
        if not cn.notifies:
          cn.poll()
        if cn.notifies:
          self._log("{0} new notifications".format(len(cn.notifies)), logging.DEBUG)
          self._waiting_jobs += len(cn.notifies)
          start_new_count += len(cn.notifies)
          cn.notifies.clear()

      # Clean up completed jobs
      with self._completed_jobs_lock:
        start_new_count += len(self._completed_jobs)
        while self._completed_jobs:
          job, sz_key, future = self._completed_jobs.pop()
          self._mark_job_completed(job, sz_key, _exception_to_message(future.exception()))
          self._running_futures.remove(future)

      # At this point start_new_count is the sum of new jobs waiting, plus the number of workers
      # freed up. We need to include freed workers because they may have been blocking serialized
      # jobs that can now be run.

      # If STOP_NEVER or STOP_WHEN_ALL_DONE we will continue to start new jobs
      if self._stop_requested in (STOP_NEVER, STOP_WHEN_ALL_DONE):
        available_workers = self._workers - len(self._running_futures)
        start_new_count = min(start_new_count, available_workers, self._waiting_jobs)

        while start_new_count > 0:
          job, sz_key = self._get_next_job()
          if job:
            future = self._start_job(job, sz_key)
            self._running_futures.append(future)
            self._waiting_jobs -= 1
            start_new_count -= 1
            # total_jobs_run += 1
          else:
            self._log("Checked, no available jobs, {0} requested remaining".format(start_new_count))
            start_new_count = 0

      if len(self._running_futures) == 0:
        if self._stop_requested == STOP_WHEN_CURRENT_DONE:
          break
        if self._stop_requested == STOP_WHEN_ALL_DONE and self._waiting_jobs == 0:
          break

      time.sleep(_SLEEP)

    # Cancel any remaining futures. There will only be futures at this point if there were some
    # running when STOP_NOW was requested.
    if self._running_futures:
      for future in self._running_futures:
        future.cancel()
      self._data_access.execute(
        "update {0} set started_at = null " \
        "where started_at is not null and completed_at is null;".format(self._jobs_table_name))
      self._data_access.execute("update {0} set active_job_id = null;".format(
        self._serialization_keys_table_name))

    self._log("Closing")
    self._data_access.close()
    if self._stop_callback:
      self._stop_callback()

  def _mark_job_completed(self, job, sz_key, error_message):
    """Update a job indicating that it was completed, and release its serializaiton key, if any."""
    if error_message:
      self._log(
        ("Error", job.id, job.name, sz_key.key if sz_key else None, "\n" + error_message),
        logging.CRITICAL)
    else:
      self._log(("Finished", job.id, job.name, sz_key.key if sz_key else None))

    job.update(completed_at=arrow.utcnow().datetime, error_message=error_message)
    if sz_key:
      sz_key.active_job_id = None
    self._update_job(job, sz_key)

  def _get_next_job(self):
    """Get the next waiting job that can be run now."""
    j = self._data_access.find(
      "{0} as j left join {1} as k on j.serialization_key_id = k.id".format(
        self._jobs_table_name,
        self._serialization_keys_table_name),
      "j.started_at is null and k.active_job_id is null",
      columns="j.*",
      order_by="j.priority desc, j.created_at asc")

    if not j:
      return (None, None)

    job = Job(j)
    if job.serialization_key_id:
      sz_key = self._data_access.find_model_by_id(SerializationKey, job.serialization_key_id)
    else:
      sz_key = None

    return (job, sz_key)

  def _start_job(self, job, sz_key):
    """Start a job."""
    def fxn():
      """Job starting function, passed to pool."""
      if job.name not in self._job_functions:
        raise KeyError("Bad job name")
      self._job_functions[job.name](job.args)

    job.started_at = arrow.utcnow().datetime
    if sz_key:
      sz_key.active_job_id = job.id

    self._update_job(job, sz_key)
    self._log(("Starting", job.id, job.name, sz_key.key if sz_key else None))

    future_ = self._executor.submit(fxn)
    future_.add_done_callback(lambda future: self._job_finished(job, sz_key, future))
    return future_

  def _job_finished(self, job, sz_key, future):
    """Mark a job as completed."""
    with self._completed_jobs_lock:
      self._completed_jobs.append((job, sz_key, future))

  def _update_job(self, job, sz_key):
    """Update a job and (optionally) a serialization key to indicate that the job has started."""
    if sz_key:
      with transaction(self._data_access):
        self._data_access.update_model(
          job,
          include_keys={"started_at", "completed_at", "error_message"})
        self._data_access.update_model(sz_key, include_keys={"active_job_id"})
    else:
      self._data_access.update_model(
        job,
        include_keys={"started_at", "completed_at", "error_message"})
