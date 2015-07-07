#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import with_statement
from tornado.web import addslash, Application, authenticated, asynchronous
from tornado.web import StaticFileHandler, RequestHandler
from tornado import gen
from tornado.httpserver import HTTPServer
from tornado import template, ioloop

from requests_futures.sessions import FuturesSession
from requests.adapters import HTTPAdapter

from passlib.hash import sha256_crypt
from pyjade.ext.tornado import patch_tornado

from marcopolo.bindings import marco, polo
from marcopolo.marco_conf.utils import Node

import os, sys, logging, ssl, socket, threading, sqlite3, time, json
import signal
from threading import Thread
from functools import wraps
from glob import glob

from marcobootstrap.backend import conf
import urllib3.contrib.pyopenssl
urllib3.contrib.pyopenssl.inject_into_urllib3()

templates_dir = None
tar_path = conf.TAR_PATH
bootcode_path = conf.BOOTCODE_PATH
static_path = conf.STATIC_PATH
chosen_bootcode = None
io_loop = None
handlers_files = None
cookie_secret = None
app = None
app_files = None
futures_session = FuturesSession()

class NotCheckingHostnameHTTPAdapter(HTTPAdapter):
    """
    Avoids checking the hostname field of a HTTPS connection
    """
    def cert_verify(self, conn, *args, **kwargs):
        """
        Asserts that the hostname is valid without regard to its value
        """
        super(NotCheckingHostnameHTTPAdapter, self).cert_verify(conn, *args, **kwargs)
        conn.assert_hostname = False

futures_session.mount('https://', NotCheckingHostnameHTTPAdapter())

from django.conf import settings

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': conf.DB_FILE,
    }
}

settings.configure(DATABASES=DATABASES, 
                   ENGINE='django.db.backends.sqlite3', 
                   DATABASE_ENGINE='django.db.backends.sqlite3', 
                   DATABASE_NAME=conf.DB_FILE)
import django

if django.VERSION[:2] > (1,5):
    logging.debug("Performing Django setup")
    django.setup()

from django import forms
from django.db import models
from models import Operation, Configuration



class BaseHandler(RequestHandler):
    """
    An extension of :class:`tornado.web.RequestHandler`
    that decrypts a secure username cookie
    """
    def get_current_user(self):
        return self.get_secure_cookie("user")

class WebHandler(BaseHandler):
    """
    Handles index connections
    """
    @addslash
    def get(self):
        """
        If the user is logged, displays the main interface. Otherwise redirects the user
        to the login window
        """
        if self.get_secure_cookie("user", None) is None:
            self.redirect("/login")

        elif self.get_secure_cookie("user").decode('utf-8') == "admin":
            files = [ os.path.basename(f) for f in glob(os.path.join(tar_path,'*.tar.gz'))]
            
            self.render(os.path.join(templates_dir, "index.jade"), **{"files": files})
        
        else:
            self.redirect("/login/")

class LoginHandler(BaseHandler):
    """
    Handles the login process
    """
    @addslash
    def get(self):
        """
        Displays a login form
        """
        self.render(os.path.join(templates_dir, "login.jade"))

    def post(self):
        """
        Validates the credentials and, if successful, redirects the user to the
        main window. If unsuccessful a message error is displayed.
        """
        user = self.get_argument("user", None)
        password= self.get_argument("password", None)

        if user == conf.ADMIN and sha256_crypt.verify(password, conf.ADMIN_PASS):
            self.set_secure_cookie("user", "admin")
            self.redirect("/")

        else:
            self.set_status(403)
            self.render(os.path.join(templates_dir, "403.jade"))

class LogoutHandler(BaseHandler):
    """
    Handles the exiting process
    """
    @authenticated
    def get(self):
        """
        Removes the user cookie
        """
        self.clear_cookie("user")
        self.redirect(self.get_argument("next", "/"))

class ScheduledHandler(BaseHandler):
    """
    Displays the database information about the scheduled events 
    """
    @addslash
    @authenticated
    def get(self):
        """
        Renders a view with all future scheduled jobs
        """
        operations = Operation.objects.filter(operation_time__gt=float(time.time())).order_by('-operation_time')
        
        for operation in operations:
            operation.operation_time_nonformat = operation.operation_time
            operation.operation_time = time.strftime("%H:%M:%S %b %d %Y",time.gmtime(operation.operation_time))

        self.render(os.path.join(templates_dir, "scheduled.jade"), **{"operations":operations})


def add_callback(future, callback, *args, **kwargs):
    """
    Adds and event to the :class:`IOLoop` instance and binds it to the callback funcion

    :param Future future: A future object where to extract information from
    :param function callback: The callback function
    """
    def _add_callback(future):
        """
        Adds the callback to the :class:`IOLoop`
        """
        if future.cancelled():
            raise RuntimeError

        response = future.result(timeout=0)
        io_loop.add_callback(lambda: callback(response, *args, **kwargs))

    return future.add_done_callback(_add_callback)

class Schedule(BaseHandler):
    """
    Schedules operations to the nodes in the net
    """
    @addslash
    @authenticated
    def post(self):
        """
        Processes a POST request with the operation parameters
        """
        operation = self.get_argument('operation', None)
        schedule_time = self.get_argument('schedule', None)
        
        if operation is None or schedule_time is None:
            self.set_status(400)
            self.finish("Malformed request")
            return
        else:
            schedule_time = float(schedule_time)
        
        nodes = self.get_argument('nodes', None)
        try:
            nodes_list = nodes.split(",")[:-1]
        except Exception as e:
            logging.debug(e)
            self.set_status(400)
            self.finish("Malformed request")
        
        if len(nodes_list) > 0:
            for nodes in nodes_list:
                pass

        logging.debug("I shall schedule a %s on %f for %s" % (operation, schedule_time, ",".join('{}: {}'.format(*k) for k in enumerate(nodes_list))))
        
        for node in nodes_list:
            try:
                socket.inet_aton(node)
                if operation == "reboot":
                    url = "https://"+node+":"+str(conf.SLAVE_PORT)+"/reboot"
                    commands = {"type":"reboot","time":schedule_time}
                elif operation == "update":
                    url = "https://"+node+":"+str(conf.SLAVE_PORT)+"/update"
                    commands = {"type":"update", 
                                "time":schedule_time, 
                                "image": self.get_argument('image', ''), 
                                "bootcode": chosen_bootcode}
                    logging.debug(self.get_argument('image', ''))
                    print(self.get_argument('image', ''))
                logging.debug(url)
                future = futures_session.post(url,
                                            files={},
                                            data=commands,
                                            verify=conf.RECEIVERCERT,
                                            cert=(conf.APPCERT, conf.APPKEY))
                
                add_callback(future=future, callback=self.deployed, node=node)

            except socket.error as se:
                logging.debug(se)

        self.add_to_db(operation, schedule_time, nodes, self.get_argument('image', ''))

    def add_to_db(self, operation_type, schedule_time, hosts, image=None):
        """
        Adds to the database a new operation entry with all the concerning information

        :param str operation_type: An identifier for the kind of operation (reboot, update...)
        :param float schedule_time: A time represented in absolute milliseconds (starting on the epoch) that indicates the time of execution.
        :param list hosts: A list of the hosts where the operation is to be executed on
        :param string image: The OS image (only useful for update and similar operations)
        """
        operation_db = Operation()
        operation_db.operation_type=operation_type
        operation_db.operation_time=schedule_time
        operation_db.image = image
        operation_db.hosts = hosts

        operation_db.save()

            
    def deployed(self, response, node):
        """
        Used as a callback for the POST process
        """
        if(response.status_code != 101):
            logging.debug("Error in node %s" % node)
        else:
            logging.debug("OK for node %s" % node)
            
class CancelHandler(BaseHandler):
    """
    Allows cancellation of an operation which is yet to be done.
    """
    @addslash
    @authenticated
    def post(self):
        """
        Processes a cancellation request
        """
        logging.debug("I shall cancel")
        identifier = self.get_argument('id', None)
        if identifier is None:
            self.set_status(400)
            self.finish("Malformed request")
            return

        try:
            event = Operation.objects.get(pk=identifier)
        except Operation.DoesNotExist:
            self.set_status(404)
            self.finish("Not found")
            return
        logging.debug(event.operation_type)
        for node in event.hosts.split(","):
            if node != ",":
                url_cancel = "https://"+node+":"+str(conf.SLAVE_PORT)+"/cancel"
                commands = {'type':event.operation_type,'time':event.operation_time}
                future = futures_session.post(url_cancel, 
                                                files={}, 
                                                data=commands, 
                                                verify=conf.RECEIVERCERT, 
                                                cert=(conf.APPCERT, conf.APPKEY))
                
                add_callback(future, self.cancel)
        
    
        event.delete()
        self.set_status(200)
        self.finish("Removed")

    def cancel(self, response):
        """
        A simple callback, used for logging and debugging purposes
        """
        logging.debug("Cancel")
        logging.debug(response)

def run_async(func):
    """
    A simple wrapper that allows a blocking function to work inside the tornado IOLoop
    :param function func: The blocking function
    :returns: An async_func callable
    """
    @wraps(func)
    def async_func(*args, **kwargs):
        """
        Wraps the funcionality of the non-blocking behaviour (basically, it creates a thread using the standard Python thread API)
        """
        func_hl = Thread(target = func, args = args, kwargs = kwargs)
        func_hl.start()
        return func_hl

    return async_func

#See: http://stackoverflow.com/a/15952516/2628463
#See: http://lbolla.info/blog/2013/01/22/blocking-tornado
@run_async
def longwait(callback):
    """
    Performs a Marco request
    """
    m = marco.Marco()
    nodes = m.request_for("marco-bootstrap-slave")
    callback(json.dumps([n.address for n in nodes]))

class MarcoDetect(BaseHandler):
    """
    Detect all nodes in the network 
    """
    @authenticated
    @asynchronous
    @gen.coroutine
    def get(self):
        """
        Performs the Marco operation and returns the result as a JSON-formatted string
        :returns: A JSON formated string with the node information
        """
        response = yield gen.Task(longwait)

        self.write(response)
        self.finish()


class RemoveHandler(BaseHandler):
    """
    Removes an OS image
    """
    @authenticated
    def post(self):
        """
        Processes the request and removes the OS image
        """
        file_name = self.get_argument('file', None)
        if file_name is None:
            self.set_status(404)
            self.finish("Not found")
        else:
            files = [ os.path.basename(f) for f in glob(tar_path+'/*.tar.gz')]

            if file_name in files:
                os.remove(os.path.join(tar_path, file_name));
                self.set_status(200)
                self.finish("Removed!")
            else:
                self.set_status(404)
                self.finish("Not found")

class BootcodeHandler(BaseHandler):
    """
    Handles the bootcodes available
    """
    @authenticated
    def get(self):
        """
        Returns the list of bootcodes
        """
        files = [os.path.basename(f) for f in glob(bootcode_path+'/*.zip')]
        self.render(os.path.join(templates_dir, "bootcode.jade"), **{"files": files, "chosen_bootcode": chosen_bootcode})

    @authenticated
    def post(self):
        """
        Updates the chosen bootcode
        """
        new_bootcode = self.get_argument("file", None)
        if new_bootcode is None or new_bootcode not in [os.path.basename(f) for f in glob(bootcode_path+'/*.zip')]:
            self.set_status(409)
            self.finish("There is no such bootcode")
        else:
            chosen_bootcode = new_bootcode
            try:
                c = Configuration.objects.get(pk=1)
            except Configuration.DoesNotExist as d:
                c = Configuration()

            c.bootcode = chosen_bootcode
            c.save()

def shutdown():
    logging.info("Stopping gracefully")
    try:
        polo.Polo().unpublish_service(conf.SERVICE_NAME)
    except Exception as e:
        logging.warning(e)
    io_loop.stop()

def sigint_handler(signal, frame):
    io_loop.add_callback(shutdown)

signal.signal(signal.SIGINT, sigint_handler)

def choose_bootcode():
    global chosen_bootcode
    try:
        chosen = [os.path.basename(f) for f in glob(bootcode_path+'/*.zip')][0]
    except IndexError:
        logging.error("There is not bootcode!")
        sys.stderr.write("There is no bootcode!\n")
        shutdown()
        sys.exit(1)

    chosen_bootcode = chosen
    try:
        c = Configuration.objects.get(pk=1)
        chosen_bootcode = c.bootcode
    except Configuration.DoesNotExist as d:
        c = Configuration(bootcode=chosen_bootcode)
        c.save()

class RedirectHandler(RequestHandler):
    """
    Redirects all request to the secure port
    """
    def get(self):
        """
        Redirects all requests to the secure port
        """
        self.redirect("https://%s:%s%s" 
            % ((self.request.host).replace(":"+str(conf.NON_SECURE_BACKEND_PORT), ""), 
                conf.BACKEND_PORT, self.request.uri), permanent=True
            )

def main(args=None):
    """
    Starts the connection to the database, starts the logging facilities and creates the server
    """
    global io_loop, templates_dir, tar_path, static_path, handlers, futures_session
    
    patch_tornado()

    templates_dir = conf.TEMPLATES_DIR

    if not os.path.exists(tar_path):
        os.makedirs(tar_path)

    if not os.path.exists(bootcode_path):
        os.makedirs(bootcode_path)


    io_loop = ioloop.IOLoop.instance()
    handlers=[
        (r'/bootcode/?', BootcodeHandler),
        (r'/removetar/?', RemoveHandler),
        (r'/nodes/?', MarcoDetect),
        (r'/cancel/?', CancelHandler),
        (r'/schedule/', Schedule),
        (r'/scheduled/?', ScheduledHandler),
        (r'/logout/?', LogoutHandler),
        (r'/login/?', LoginHandler),
        (r'/', WebHandler),
        
    ]

    nonsecure_handlers = [
        (r'/.*', RedirectHandler)
    ]

    handlers_files = [
        (r'/tar/(.*)', StaticFileHandler, {'path': tar_path}),
        (r'/bootcode/download/(.*)', StaticFileHandler, {'path': bootcode_path})
    ]
    try:
        with open(conf.COOKIE_SECRET_FILE, 'r') as secret_file:
            cookie_secret = secret_file.read()
    except EnvironmentError as e:
        logging.error(e)
        sys.exit(1)

    settings = {
        "debug": True,
        "static_path": static_path,
        "cookie_secret": cookie_secret,
        "login_url": "/login/"
    }

    app = Application(handlers, **settings)
    app_files = Application(handlers_files, **settings)
    nonsecure_app = Application(nonsecure_handlers)


    conn = sqlite3.connect(conf.DB_FILE)
    c = conn.cursor()

    create_table_operation = 'create table if not exists operation (id INTEGER PRIMARY KEY, operation_type varchar(30) not null, operation_time REAL, hosts varchar(1000) not null, image varchar(50))'
    create_table_configuration = 'create table if not exists configuration (id INTEGER PRIMARY KEY, bootcode varchar(60) not null)'
    
    c.execute(create_table_operation)
    c.execute(create_table_configuration)

    conn.commit()
    
    choose_bootcode()

    httpServer = HTTPServer(app, ssl_options={"certfile":conf.APPCERT, 
                                              "keyfile":conf.APPKEY
                                              })

    httpServer.listen(conf.BACKEND_PORT)
    use_ssl = True
    
    if use_ssl:
        httpserverFiles = HTTPServer(app_files, ssl_options={
                                            "certfile":conf.APPCERT, 
                                            "keyfile":conf.APPKEY,
                                            "cert_reqs": ssl.CERT_REQUIRED,
                                            "ca_certs": conf.APPCERT
                                        })
    else:
        httpserverFiles = HTTPServer(app_files)
    httpserverFiles.listen(conf.BACKEND_FILES_PORT)

    nonsecure_app.listen(conf.NON_SECURE_BACKEND_PORT)
    if not os.path.exists('/var/log/marcopolo'):
        os.makedirs('/var/log/marcopolo')

    logging.basicConfig(filename=conf.LOG_FILE,
                        level=logging.DEBUG)

    logging.debug("Publishing service")
    while True:
        try:
            polo.Polo().publish_service(conf.SERVICE_NAME, root=True)
            break
        except polo.PoloInternalException as e:
            logging.warning(e)
            time.sleep(1)
        except polo.PoloException as i:
            logging.warning(i)
            break
        except Exception as e:
            logging.warning(e)
            time.sleep(1)

    logging.info('Starting marco-bootstrap-backend on port 1346. Files on port 1345')
    
    io_loop.start()

if __name__ == "__main__":
    main(sys.argv[1:])
