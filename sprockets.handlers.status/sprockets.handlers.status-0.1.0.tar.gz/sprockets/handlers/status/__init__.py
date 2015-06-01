"""
sprockets.handlers.status

A small handler for reporting application status

"""
import pkg_resources

__version__ = '0.1.0'

UNKNOWN = 'unknown'
MAINTENANCE = 'maintenance'
OK = 'ok'

APPLICATION = UNKNOWN


def set_application(name):
    """Set the application name that is reported in the status.

    :param str name: The application name

    """
    global APPLICATION
    APPLICATION = name


class StatusHandler(object):
    """Implement a status handler endpoint that can be used to get information
    about the current service

    """

    def get(self, *args, **kwargs):
        """Tornado RequestHandler GET request endpoint for reporting status

        :param list args: positional args
        :param  dict kwargs: keyword args

        """
        self.set_status(self._status_response_code())
        self.write(self._status_response())

    def _application_status(self):
        """Extend this method to return application status dynamically.
        If the value returns ``maintenance`` a ``503`` status code will be
        returned for any request to the handler. If the values contains
        anything but ``ok``, a ``500`` status code will be returned by the
        handler.

        :rtype: str

        """
        return getattr(self.application, 'status', 'ok')

    @staticmethod
    def _package_version():
        if APPLICATION == UNKNOWN:
            return UNKNOWN
        try:
            return pkg_resources.get_distribution(APPLICATION).version
        except pkg_resources.DistributionNotFound:
            return UNKNOWN

    def _status_response(self):
        """Return the status payload. Extend this method if you would like
        to inject additional status information into the response.

        For example:

          .. code:: python

            class MyStatusHandle(StatusHandler):

                def status(self):
                    response = super(MyStatusHandler, self).status()
                    response['foo'] = 'bar'
                    return response


        :rtype: dict

        """
        return {
            'application': APPLICATION,
            'status': self._application_status(),
            'version': self._package_version()
        }

    def _status_response_code(self):
        """Return the status code for the request based upon the application
        status.

        :rtype: int

        """
        status = self._application_status()
        if status == OK:
            return 200
        elif status == MAINTENANCE:
            return 503
        return 500
