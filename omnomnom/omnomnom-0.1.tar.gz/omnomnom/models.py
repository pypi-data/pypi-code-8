import uuid
import json
from datetime import datetime

from nanomsg import Socket


class Pip(Socket):

    def send_json(self, msg, flags=0, **kwargs):
        msg = json.dumps(msg, **kwargs).encode('utf8')
        self.send(msg, flags)

    def recv_json(self, buf=None, flags=0):
        msg = self.recv(buf, flags)
        return json.loads(msg)


class Task(object):

    class Status:
        SENT = 'sent'
        PROCESSING = 'processing'
        FINISHED = 'finished'
        FAILED = 'failed'

    def __init__(self, *args, **kwargs):
        self.task_name = kwargs.get('task_name')
        self.task_args = kwargs.get('task_args', None) or ()
        self.task_kwargs = kwargs.get('task_kwargs', None) or {}
        self.created_at = kwargs.get('created_at', datetime.now())
        self.completed_at = kwargs.pop('completed_at', None)
        self.failed_at = kwargs.pop('failed_at', None)
        self.task_id = kwargs.get('task_id', uuid.uuid4().hex)
        self.status = kwargs.get('status', Task.Status.SENT)
        self.result = kwargs.get('result', None)
        self.failure_reason = kwargs.pop('failure_reason', None)

    @classmethod
    def from_task_data(cls, data):
        return Task(**data)

    @property
    def has_finished(self):
        status_list = [Task.Status.FINISHED]
        return self.status in status_list

    def finalize(self):
        self.status = Task.Status.FINISHED
        self.completed_at = datetime.now()

    def failure(self, reason):
        self.status = Task.Status.FAILED
        self.failed_at = datetime.now()
        self.failure_reason = reason

    def get_info(self):
        return {
            'id': self.task_id,
            'name': self.task_name,
            'args': self.task_args,
            'kwargs': self.task_kwargs
        }

    def to_json(self):
        return {
            'task_id': self.task_id,
            'task_name': self.task_name,
            'task_args': self.task_args,
            'task_kwargs': self.task_kwargs,
            'created_at': str(self.created_at),
            'status': self.status
        }


class Executable(object):

    def __call__(self, *args, **kwargs):
        # Executable receives service instance in kwargs
        pass


class Message(object):

    def __init__(self, executable, args, kwargs, *a, **kw):
        self.executable = executable
        self.args = args if args else ()
        self.kwargs = kwargs if kwargs else {}
