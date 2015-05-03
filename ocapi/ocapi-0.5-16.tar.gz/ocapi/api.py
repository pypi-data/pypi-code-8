#!/usr/bin/env python
# -*- coding:utf-8 -*-
# (c)Ing. Zdenek Dlauhy, Michal Dlauhý, info@dlauhy.cz


"""
ocapi
=====

This is API connector to www.pripravto.cz service for furniture makers. You should
be able to use it to create your custom designs for furniture, download data
and eventually build your partial interface. Connector is built on HTTP GET and
POST methods and it uses your account on service.

Instalation
-----------

For instalation you can download package or install by **pip**. Downloaded you
can just unpack or get from from https://pypi.python.org/pypi/ocapi and install it::

    #download archive
    wget https://bitbucket.org/pripravto/ocapi/get/default.tar.gz
    cd /tmp
    virtualenv test
    source test/bin/activate
    tar -xvf default.tar.gz
    #specify correct name
    cd pripravto....

Instalation::

    python setup.py install

or install by pip::

    pip install ocapi


Quickstart
----------

First you should get your account on **https://pripravto.cz** service, when you will have it
Login normally into service. Then you can start by opening Python console
and importing ocapi::

    import ocapi.api as oc
    import math
    args = {'name':'test2','position':[0,0,0],'size':[1000,1000,1000]}
    #set your own credentials will log error with these use credentials
    prod = oc.CabinetMaker(args, username="test",password="test")
    for i in range(36):
        size = [18,math.sin(math.radians(i*10))*50+80,18]
        rot = [0,0,10+i*2]
        prod.add_element(pos=[i*20,0,0],size=size,rot=rot)
    prod.finish()

This is partial example which will show you base usage of this api. This will create
serries of elements which are sized by sin function and rotated by series of
iteration.

To build something more usefull you can make first base cabinet by just writing down
one function::

    args = {'name':'cabinet2','position':[0,0,0],'size':[600,600,1000]}
    prod.parse_args(args)
    #build our base parts
    prod.add_basic()
    #add doors
    prod.add_doors()
    prod.finish()

After data creation you can also check what kind of data you have created on service
itself and also download images and so on.

Username and password are specified at start of object::

    prod = oc.CabinetMaker(args, username="test",password="test", host="test.pripravto.cz")
    #your username and password is from https://pripravto.cz/register/start

For complete registration process you need your functional e-mail address and fill out
data required by registration. **You should keep your user credentials secret.**
For examples what can be built on this api connector take a look on http://pripravto.cz/en/blog
where we put examples.

More documantation for pripravto service or about this plase see web page or
**oc.CabinetMaker** class.

Development
-----------

You can contact us or raise issues on https://bitbucket.org/pripravto/ocapi
Developmnet is also made on Bitbucket, you can clone repository and start
making chaneges. We also plan to use this api connector to be able to connect
with diffrent applications more quickly and easily.


module for access to oc api

base usecase::

    import ocapi.api as oc
    import math
    args = {'name':'test2','position':[0,0,0],'size':[1000,1000,1000]}
    prod = oc.CabinetMaker(args, username="test",password="test")

    for i in range(36):#count through whole rotation
        size = [18,math.sin(math.radians(i*10))*50+80,18]#change size
        rot = [0,0,10+i*2]#rotate part
        prod.add_element(pos=[i*20,0,0],size=size,rot=rot)
    prod.finish()

"""

import logging
import os
import uuid
import json
import functools
import ocapi.info as info

# patch urllib and httplib
import sys
if sys.version_info <= (3, 0, 0):
    import ocapi.urllibtls as tls

try:
    import httplib
except ImportError:
    import http.client as httplib

try:
    import urllib.parse as urllib
except ImportError:
    import urllib

# use funcs or original
import ocapi.prod_func as funcs

logging.basicConfig(level=0)
log = logging.getLogger(__name__)


def api_generator(save=True):
    """
    function for api generation which creates code
    for base CabinetMaker class. This function can be used only in full OptimCabinet
    framework. It will not work without several other functions::

        import ocapi.api as oc

    """
    klass = """
#!/usr/bin/env python
# -*- coding:utf-8 -*-
# (c)Ing. Zdenek Dlauhy, Michal Dlauhý, info@dlauhy.cz

class CabinetMaker(object):
"""
    funcs_def = """
    def {func}(self, {parameters}):
        '''
        {doc}
        '''
        _loc = locals()
        _loc.pop('self')
        self.custom_action(method='{func}', **_loc)

    """

    def attach_attrs(attrs):
        return ",".join("{}={}".format(k, "'{}'".format(v) if isinstance(v, str) else v) for k, v in sorted(attrs.items()))
    # this import excepts whole optimcabinet
    import initialization as oc
    import webapp.web_products
    # get base data
    doc = webapp.web_products.product_doc_generator(oc.CabinetMaker)
    funcs = webapp.web_products.product_parameters_generator(oc.CabinetMaker, generate=True, make_all=True)
    all_data = {}
    # merge data together
    for key, value in funcs:
        all_data[key] = {'attrs':value}
    for key, value in doc:
        all_data[key]['doc'] = value
    all_funcs_def = {}
    # make function definition
    for key, value in all_data.items():
        all_funcs_def[key] = funcs_def.format(func=key,
                                              parameters=attach_attrs(value['attrs']),
                                              doc=value['doc'])
    # merge whole document and save it
    klass += "".join(v for k, v in all_funcs_def.items())
    if save:
        filename = os.path.abspath(__file__)
        path, filename = os.path.split(filename)
        writer = open("{}/product.py".format(path), "w")
        writer.write(klass)
        writer.close()
    return klass

# import local api of CabinetMaker
try:
    from ocapi.product import CabinetMaker as _CabinetMaker
except ImportError as e:
    log.error(e)
    try:
        api_generator()
    except Exception as ee:
        log.error(ee)
        log.error("Run import again")

def connect(host="pripravto.cz", url="/login", port=443, data=None, method="POST",
            headers=None, debug=None, cookie=None, tls=True):
    """patched url opener based on httplib with TLS support"""
    # patch connection
    if tls:
        conn = httplib.HTTPSConnection(host, port)
    else:
        conn = httplib.HTTPConnection(host, port)
    # get headers, x-www-form-urlendoded is important
    if headers is None:
        headers = {"Content-type": "application/x-www-form-urlencoded",
                   "Accept": "text/plain"}
    if cookie and "Cookie" not in headers:
        headers['Cookie'] = cookie
    conn.request(method, url, data, headers)
    if debug:
        conn.set_debuglevel(level=debug)
    response = conn.getresponse()
    return response


class BaseControl(object):
    """
    base object for web api access
    initialize connection to some webservice
    """
    def __init__(self, username='user', password='pass', host="example.cz",
                 port=443, debug=None, connector=connect, filepath="/tmp",
                 tls=True):
        """
        :param username: username of user accessing service
        :type username: str
        :param password: password of user accessing service
        :type password: str
        :param host: base name of domain
        :type host: str
        :param port: port to connect
        :type port: int
        :param debug: set debug level
        :type debug: int or None
        :param connector: set connector function
        :type connector: func
        """
        self.username = username
        self.password = password
        self.host = host
        self.port = port
        self.debug = debug
        self.cookie = None
        self.connector = connector
        self.filepath = filepath
        self.tls = tls

    def login(self, username=None, password=None, url="/login"):
        """base login action"""
        if username is None:
            username = self.username
        if password is None:
            password = self.password
        data = dict(username=username, passwd=password)
        response = self.action(url=url, data=data, method="POST")
        if response.status == 302:
            # get cookie or start app
            headers = self.get_headers(response)
            cookie = headers.get("set-cookie", None)
            if cookie:
                self.cookie = cookie.split(";")[0]
            location = headers.get("location", None)
            if location == "/oc/start":
                # start app
                response = self.action(url=location)
        return response

    def action(self, url, data=None, host=None, method="GET", headers=None,
               convert=None, tls=None, port=None):
        """function which makes action ie. download file and send data"""
        if host is None:
            host = self.host
        if port is None:
            port = self.port
        if tls is None:
            tls = self.tls
        if data:
            if isinstance(data, str):
                pass
            else:
                data = urllib.urlencode(data)
        log.debug("Contacting url {} {} with {}".format(host, url, data))
        response = self.connector(host=host, url=url, port=port, data=data, method=method,
                                  headers=headers, debug=self.debug, cookie=self.cookie,
                                  tls=tls)
        if response.status < 400:
            if convert:
                return convert(response)
            else:
                return response
        else:
            msg = "Error in connecting requested url {}:{}"
            log.error(msg.format(response.reason, response.status))
            return response

    def save_file(self, response, headers=None):
        """save file if response should be file"""
        if headers is None:
            headers = self.get_headers(response)
        if headers.get("content-disposition", False):
            filename = headers["content-disposition"].split("filename=")[-1]
        else:
            filename = str(uuid.uuid4())
        data = response.read()
        filename = "{}/{}".format(self.filepath, filename)
        with open(filename, 'wb') as writer:
            writer.write(data)
            writer.close()
            log.info("File saved to {}".format(filename))
        return data

    def get_headers(self, response):
        """make headers same on Python2 and 3"""
        headers = dict(response.getheaders())
        headers = {key.lower():value for key, value in headers.items()}
        return headers

    def convert(self, response):
        """automated convertor function which when is used in self.action
        changes what will happen with response
        """
        if response.status == 200:
            log.info("Converting data sources")
            headers = self.get_headers(response)
            if headers['content-type'] == 'text/xml':
                try:
                    import inout.optimio
                    return inout.optimio.xml2obj(response.read())
                except ImportError as e:
                    log.error(e)
                    return response
            elif headers['content-type'] == 'text/json':
                return json.loads(response.read().decode("utf-8"))
            elif headers['content-type'] == 'image/svg+xml':
                return self.save_file(response, headers)
            elif headers['content-type'] == 'text/plain':
                text = response.read().decode("utf-8")
                log.warn(text)
                return text
            if headers.get("content-disposition", False):
                return self.save_file(response, headers)
        return response

class Control(BaseControl):

    def other_funcs(self):
        self.action_list = {'commit':'/rev/commit',
                            'new':'/system/new',
                            'save':'/system/savepickle'}
        self.make_funcs(self.action_list)

    def make_funcs(self, actions):
        """make functions based on actions list with partial"""
        import functools
        for key, value in actions.items():
            func = functools.partial(self.action, url=value, convert=self.convert)
            setattr(self, key, func)

    def get_optim(self, name=None, obj_id=None, make_new=False):
        return self.get_optim_calc(template="optimalize", name=name,
                                   obj_id=obj_id, make_new=make_new)

    def get_optim_calc(self, template="optimalize", name=None, obj_id=None, make_new=True):
        if name is None:
            name = self.get_order_name()
        if make_new:
            response = self.action(url="/{}/".format(template))
        if obj_id is None:
            last_calc = self.action(url="/json/{}/orders".format(template), convert=self.convert)
            obj_id = last_calc[name]
        url = "/json/{}/orders/{}/{}".format(template, name, obj_id)
        return self.action(url=url, convert=self.convert)

    def get_calc(self, name=None, obj_id=None, make_new=False):
        return self.get_optim_calc(template="calculation", name=name,
                                   obj_id=obj_id, make_new=make_new)

    def get_order_name(self):
        """get name of opened order"""
        response = self.action(url="/json/sidebar", convert=self.convert)
        return str(response['order'])

    def get_product(self, name=None):
        if name is None:
            name = getattr(self, "name", "untitled")
        return self.action(url="/json/products/{}".format(name), convert=self.convert)

    def get_order(self, name=None):
        if name is None:
            name = self.get_order_name()
        return self.action(url="/json/orders/{}".format(name), convert=self.convert)

    def get_image(self, name=None, order=None, paths=None, typ="product", url=None):
        """get image based on settings"""
        if paths is None:
            paths = {'element':'products/elements',
                     'product':'products',
                     'product_viz':'viz',
                     'optim':'optim',
                     'viz':'viz',
                     'img':'import'}
        if name is None:
            name = self.name
        if order is None:
            order = self.get_order_name()
        if typ == "product":
            name = "{}_{}.svg".format(order, name)
        elif typ == "optim":
            pass
        elif typ == "products_viz":
            name = "{}_{}.jpeg".format(order, name)
        elif typ == "viz":
            name = "{}.jpeg".format(order)
        else:
            raise Exception("Wrong type of requested image")
        if url is None:
            url = "/userdata/{}/{}".format(paths[typ], name)
        image = self.action(url=url, convert=self.convert)
        return image

    def save_products(self):
        response = self.action(url="/system/savepickle")
        response = self.action(url="/rev/commit")


class CabinetMaker(Control, _CabinetMaker):
    """
    import ocapi.api as oc
    import math
    args = {'name':'test2','position':[0,0,0],'size':[1000,1000,1000]}
    prod = oc.CabinetMaker(args, username="test",password="test")
    for i in range(36):#count through whole rotation
        size = [18,math.sin(math.radians(i*10))*50+80,18]#change size
        rot = [0,0,10+i*2]#rotate part
        prod.add_element(pos=[i*20,0,0],size=size,rot=rot)
    prod.finish()
    """
    def __init__(self, args=None, username='user', password='pass', host="test.pripravto.cz",
                 port=443, debug=None, connector=connect, filepath="/tmp",
                 login=True, tls=True):
        BaseControl.__init__(self, username=username, password=password, host=host, port=port,
                             debug=debug, connector=connector, filepath=filepath, tls=tls)
        self.data = []
        self.name = "untitled"
        if args:
            self.parse_args(args)
        if login:
            self.login(username, password)
        # self.make_funcs(funcs.parameters['PRODFUNC'], funcs.parameters['PRODFUNC_HELP'])

    def parse_args(self, params):
        """transform parameters"""
        params = dict(params)
        params['posX'] = params['position'][0]
        params['posY'] = params['position'][1]
        params['posZ'] = params['position'][2]
        params['width'] = params['size'][0]
        params['depth'] = params['size'][1]
        params['height'] = params['size'][2]
        params['selectFunction'] = "empty"
        self.name = params.get('name', "untitled")
        params.pop('position')
        params.pop('size')
        self.data = self.data + list(params.items())
        self.data.append(('productParam', params))

    def custom_action(self, method="name", **kwargs):
        """custom action to save data"""
        self.data.append((method, kwargs))

    def finish(self):
        """send all data to server and create object"""
        name = self.name
        response = self.action(url="/products/create", data=urllib.urlencode(self.data), method='POST')
        log.info("To create new item use func parse_args")
        self.data = []
        response = self.action(url="/json/products/{}".format(name), convert=self.convert)
        return response

    def make_funcs(self, actions, docs):
        """create all functions so it should be possible to use it as cabinet maker"""
        for key, value in actions:
            func = functools.partial(self.custom_action, method=key, **value)
            setattr(self, key, func)
        for key, value in docs:
            func = getattr(self, key)
            func.__doc__ = value


if __name__ == "__main__" :
    # api_generator()
    # import ocapi.api as oc
    import math
    def test_local():
        args = {'name':'test2', 'position':[0, 0, 0], 'size':[1000, 1000, 1000]}
        prod = CabinetMaker(args, host="localhost", port=2000, tls=False, login=False)
        for i in range(36):  # count through whole rotation
            size = [18, math.sin(math.radians(i * 10)) * 50 + 80, 18]  # change size
            rot = [0, 0, 10 + i * 2]  # rotate part
            prod.add_element(pos=[i * 20, 0, 0], size=size, rot=rot)
        print(prod.finish())
        print(prod.get_image())

    def test_normal():
        args = {'name':'test2', 'position':[0, 0, 0], 'size':[1000, 1000, 1000]}
        prod = CabinetMaker(args, username="useroc1", password="oc1user1piff")
        for i in range(36):  # count through whole rotation
            size = [18, math.sin(math.radians(i * 10)) * 50 + 80, 18]  # change size
            rot = [0, 0, 10 + i * 2]  # rotate part
            prod.add_element(pos=[i * 20, 0, 0], size=size, rot=rot)
        print(prod.finish())
        print(prod.get_image())
    test_normal()
