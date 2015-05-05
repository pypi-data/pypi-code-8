import time
import pickle
import logging
from threading import Thread
from datetime import datetime, timedelta


class BaseResultBackend(object):

    def add_task(self, task):
        raise NotImplementedError

    def delete_task(self, task):
        raise NotImplementedError

    def update_task(self, task):
        raise NotImplementedError

    def get_task(self, task_id):
        raise NotImplementedError

    def cleanup(self, task_result_expires):
        raise NotImplementedError

    def get_tasks(self, **kwargs):
        raise NotImplementedError

    def setup(self, **kwargs):
        logging.info(u"Setting up result backend")

    def terminate(self):
        logging.info(u"Terminating result backend")


class DummyResultBackend(BaseResultBackend):

    def add_task(self, task):
        pass

    def delete_task(self, task):
        pass

    def update_task(self, task):
        pass

    def get_task(self, task_id):
        pass

    def cleanup(self, task_result_expires):
        pass

    def get_tasks(self, **kwargs):
        return []

    def setup(self, **kwargs):
        super(DummyResultBackend, self).setup(**kwargs)

    def terminate(self):
        super(DummyResultBackend, self).terminate()


class RedisResultBackend(BaseResultBackend):
    task_prefix = 'omnomnom_task_'
    # by default task expire after 1 day
    expires_after = 3600 * 24

    def __init__(self, host='localhost', port=6379, db=0):
        import redis
        self.r = redis.StrictRedis(host=host, port=port, db=db)

    def add_task(self, task):
        self.r.set(
            '{0}{1}'.format(self.task_prefix, task.task_id),
            pickle.dumps(task)
        )

    def delete_task(self, task):
        self.r.delete(
            '{0}{1}'.format(self.task_prefix, task.task_id)
        )

    def update_task(self, task):
        self.r.set(
            '{0}{1}'.format(self.task_prefix, task.task_id),
            pickle.dumps(task)
        )

    def get_task(self, task_id):
        return pickle.loads(
            self.r.get('{0}{1}'.format(self.task_prefix, task_id))
        )

    def get_tasks(self, **kwargs):
        from redis.exceptions import ResponseError
        match = kwargs.pop('match', '{0}*'.format(self.task_prefix))

        try:
            for key in self.r.scan_iter(match=match):
                yield (key, pickle.loads(self.r.get(key)))
        except ResponseError:
            for key in self.r.keys(pattern=match):
                yield (key, pickle.loads(self.r.get(key)))

    def cleanup(self, task_result_expires):
        now = datetime.now()
        cleaned_tasks = 0

        for key in self.r.keys('{0}*'.format(self.task_prefix)):
            task = self.get_task(
                key.replace('{0}'.format(self.task_prefix), '')
            )
            if task.has_finished:
                if task.completed_at < (now - timedelta(seconds=task_result_expires)):
                    cleaned_tasks += 1
                    self.delete_task(task)

        return cleaned_tasks

    def setup(self, **kwargs):
        super(RedisResultBackend, self).setup(**kwargs)
        self.monitor_thread_signal = True
        self.monitor_thread = Thread(target=self.monitor_tasks)
        self.monitor_thread.start()

    def monitor_tasks(self):
        elapsed, step = 0, 1

        while self.monitor_thread_signal:
            if self.expires_after <= elapsed:
                cleaned = self.cleanup(self.expires_after)
                logging.debug(u"Results Cleanup: {0} tasks.".format(cleaned))
                elapsed = 0
            time.sleep(1)
            elapsed += step

    def terminate(self):
        super(RedisResultBackend, self).terminate()
        self.monitor_thread_signal = False