from __future__ import absolute_import
import celery


from bq.core.model import DBSession


class SATask(celery.Task):
    """An abstract Celery Task that ensures that the connection the the
    database is closed on task completion"""
    abstract = True

    def after_return(self, status, retval, task_id, args, kwargs, einfo):
        DBSession.remove()
