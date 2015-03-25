import newrelic.api.web_transaction
import newrelic.api.in_function

def instrument_cherrypy_wsgiserver_wsgiserver2(module):

    def wrap_wsgi_application_entry_point(server, bind_addr, application,
            *args, **kwargs):
        application = newrelic.api.web_transaction.WSGIApplicationWrapper(
                application)
        args = [server, bind_addr, application] + list(args)
        return (args, kwargs)

    newrelic.api.in_function.wrap_in_function(module,
            'CherryPyWSGIServer.__init__',
            wrap_wsgi_application_entry_point)
