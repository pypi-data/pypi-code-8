import pickle
import logging

from google.appengine.ext import webapp
from google.appengine.ext.deferred.deferred import (
    _DEFAULT_LOG_LEVEL, SingularTaskFailure, PermanentTaskFailure,
)


class BaseTaskHandler(webapp.RequestHandler):
    """This is how TaskHandler should be written"""
    @classmethod
    def runfunc(cls, func, args, kwargs):
        return func(*args, **kwargs)

    @classmethod
    def run(cls, data):
        try:
            func, args, kwds = pickle.loads(data)
        except Exception, e:
            raise PermanentTaskFailure(e)
        else:
            return cls.runfunc(func, args, kwds)

    def run_from_request(self):
        """Default behavior for POST requests to deferred handler."""

        if 'X-AppEngine-TaskName' not in self.request.headers:
            logging.critical(
                'Detected an attempted XSRF attack. The header '
                '"X-AppEngine-Taskname" was not set.'
            )
            self.response.set_status(403)
            return

        in_prod = (
            not self.request.environ.get("SERVER_SOFTWARE").startswith("Devel")
        )
        if in_prod and self.request.environ.get("REMOTE_ADDR") != "0.1.0.2":
            logging.critical(
                'Detected an attempted XSRF attack. This request did '
                'not originate from Task Queue.'
            )
            self.response.set_status(403)
            return


        headers = [
            "%s:%s" % (k, v)
            for k, v in self.request.headers.items()
            if k.lower().startswith("x-appengine-")
        ]
        logging.log(_DEFAULT_LOG_LEVEL, ", ".join(headers))

        self.run(self.request.body)
        
    def post(self):
        try:
            self.run_from_request()
        except SingularTaskFailure:
            logging.debug("Failure executing task, task retry forced")
            self.response.set_status(408)
            return
        except PermanentTaskFailure, e:
            logging.exception("Permanent failure attempting to execute task")


class TaskHandler(BaseTaskHandler):
    @classmethod
    def runfunc(cls, func, args, kwargs):
        logmsg = "Executing task '{name}' with:\nargs: {args}\nkwargs: {kwargs}"
        logmsg = logmsg.format(name=func.__name__, args=args, kwargs=kwargs)
        logging.log(_DEFAULT_LOG_LEVEL, logmsg)
        return super(TaskHandler, cls).runfunc(func, args, kwargs)


application = webapp.WSGIApplication([('.*', TaskHandler)])
