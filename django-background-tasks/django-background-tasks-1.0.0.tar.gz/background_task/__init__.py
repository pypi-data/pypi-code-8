__version__ = '1.0.0'


def background(*arg, **kw):
    from .tasks import tasks
    return tasks.background(*arg, **kw)
