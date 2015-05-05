import logging

from concurrent.futures import ThreadPoolExecutor

from omnomnom import models
from omnomnom import utils


class BasicHandler(object):

    def __init__(self, result_backend, *args, **kwargs):
        self.result_backend = result_backend

    def run_task(self, task, func, args, kwargs):
        result = func(*args, **kwargs)
        task.result = result
        task.finalize()
        self.result_backend.update_task(task)

    def handle_failed(self, task, e):
        task.failure(reason=str(e))
        self.result_backend.update_task(task)

    def process_task(self, task):
        try:
            func = utils.get_func(task.task_name)
            task.status = models.Task.Status.PROCESSING
            self.result_backend.add_task(task)
            self.run_task(
                task=task, func=func,
                args=task.task_args, kwargs=task.task_kwargs
            )
        except Exception as e:
            logging.error(e)
            self.handle_failed(task=task, e=e)

    def close(self):
        pass


class FuturesHandler(BasicHandler):
    DEFAULT_WORKER_NUM = 4
    WAIT_FOR_RESOURCES = False

    def __init__(self, *args, **kwargs):
        super(FuturesHandler, self).__init__(*args, **kwargs)
        max_workers = kwargs.get('max_workers', self.DEFAULT_WORKER_NUM)
        self.executor = ThreadPoolExecutor(max_workers=max_workers)
        msg = (
            u"Initialized Futures Handler "
            u"that uses ThreadPoolExecutor with {0} workers"
        )
        logging.debug(msg.format(max_workers))

    def handle_failed(self, task, e):
        pass

    def _update_task(self, future, task):
        e = future.exception()
        if not e:
            task.result = future.result()
            task.finalize()
            self.result_backend.update_task(task)
        else:
            task.failure(reason=str(e))
            self.result_backend.update_task(task)

    def run_task(self, task, func, args, kwargs):
        future = self.executor.submit(
            func, *args, **kwargs
        )
        future.add_done_callback(lambda f: self._update_task(f, task))

    def close(self):
        self.executor.shutdown(wait=self.WAIT_FOR_RESOURCES)