import logging
import unittest
from threading import Thread
from time import sleep

from bidon.data import ModelAccess
from bidon.data.data_access_core import get_pg_core

import pypgqueue as pq


_CONNECTION_STRING = None


def configure(database_name):
  from psycopg2.extras import Json
  from psycopg2.extensions import register_adapter

  global _CONNECTION_STRING

  _CONNECTION_STRING = "dbname={} user=postgres host=localhost".format(database_name)

  register_adapter(dict, lambda d: Json(d))


def sleep_job(data):
  secs = float(data["seconds"])
  sleep(secs)


def exc_job(data):
  raise Exception("Here's an exception for you")


def get_logger():
  logger = logging.getLogger(__name__)
  logger.setLevel(logging.DEBUG)
  if not logger.handlers:
    handler = logging.StreamHandler()
    handler.setLevel(logging.DEBUG)
    handler.setFormatter(logging.Formatter("%(asctime)s\t%(levelname)s\t%(message)s"))
    logger.addHandler(handler)
  return logger


class PyPGQueueTestCase(unittest.TestCase):
  def setUp(self):
    self.da = ModelAccess(get_pg_core(_CONNECTION_STRING))
    self.da.open(autocommit=True)
    self.da.update("job.serialization_keys", dict(active_job_id=None))
    self._tearDown()
    self._logger = None

  def tearDown(self):
    self._tearDown()

  def _tearDown(self):
    self.da.delete("job.jobs")
    self.da.delete("job.serialization_keys")

  def table_counts(self):
    return (self.da.count("job.jobs"), self.da.count("job.serialization_keys"))

  def test_queue_job(self):
    jc0, skc0 = self.table_counts()
    self.assertEqual(jc0, 0)
    self.assertEqual(skc0, 0)
    pq.queue_job(self.da, "a_job", { "a": 1, "b": 2 })
    pq.queue_job(self.da, "b_job")
    pq.queue_job(self.da, "c_job", { "a": 3, "b": 4 }, "tenant/id")
    pq.queue_job(self.da, "d_job", None, "tenant/id")
    pq.queue_job(self.da, "e_job", None, "another_tenant/id")
    jc1, skc1 = self.table_counts()
    self.assertEqual(jc1, 5)
    self.assertEqual(skc1, 2)

  def test_job_running(self):
    qm = pq.PyPGQueue(_CONNECTION_STRING, workers=2, logger=get_logger())
    qm.register_job_function("sleep_job", sleep_job)
    qm.register_job_function("exc_job", exc_job)

    def start_qm():
      qm.start()

    def queue_jobs():
      sleep(0.1)
      pq.queue_job(self.da, "sleep_job", { "seconds": 2 }, "skey")
      sleep(0.1)
      pq.queue_job(self.da, "sleep_job", { "seconds": 2 }, "skey")
      sleep(0.1)
      pq.queue_job(self.da, "sleep_job", { "seconds": 3 })
      sleep(0.1)
      pq.queue_job(self.da, "exc_job")
      sleep(0.1)
      pq.queue_job(self.da, "bad_job_name")

    sqmt = Thread(target=start_qm)
    qjt = Thread(target=queue_jobs)
    sqmt.start()
    qjt.start()
    sleep(5)
    qm.stop(None, pq.STOP_WHEN_ALL_DONE)
    sqmt.join()
