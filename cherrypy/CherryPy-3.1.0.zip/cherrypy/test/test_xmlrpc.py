from cherrypy.test import test
test.prefer_parent_path()
import xmlrpclib

import cherrypy


def setup_server():
    from cherrypy import _cptools
    
    class Root:
        def index(self):
            return "I'm a standard index!"
        index.exposed = True


    class XmlRpc(_cptools.XMLRPCController):
        
        def foo(self):
            return "Hello world!"
        foo.exposed = True
        
        def return_single_item_list(self):
            return [42]
        return_single_item_list.exposed = True
        
        def return_string(self):
            return "here is a string"
        return_string.exposed = True
        
        def return_tuple(self):
            return ('here', 'is', 1, 'tuple')
        return_tuple.exposed = True
        
        def return_dict(self):
            return dict(a=1, b=2, c=3)
        return_dict.exposed = True
        
        def return_composite(self):
            return dict(a=1,z=26), 'hi', ['welcome', 'friend']
        return_composite.exposed = True

        def return_int(self):
            return 42
        return_int.exposed = True

        def return_float(self):
            return 3.14
        return_float.exposed = True

        def return_datetime(self):
            return xmlrpclib.DateTime((2003, 10, 7, 8, 1, 0, 1, 280, -1))
        return_datetime.exposed = True

        def return_boolean(self):
            return True
        return_boolean.exposed = True

        def test_argument_passing(self, num):
            return num * 2
        test_argument_passing.exposed = True

        def test_returning_Fault(self):
            return xmlrpclib.Fault(1, "custom Fault response")
        test_returning_Fault.exposed = True

    root = Root()
    root.xmlrpc = XmlRpc()
    cherrypy.tree.mount(root, config={'/': {
        'request.dispatch': cherrypy.dispatch.XMLRPCDispatcher(),
        }})
    cherrypy.config.update({'environment': 'test_suite'})


class HTTPSTransport(xmlrpclib.SafeTransport):
    """Subclass of SafeTransport to fix sock.recv errors (by using file)."""
    
    def request(self, host, handler, request_body, verbose=0):
        # issue XML-RPC request
        h = self.make_connection(host)
        if verbose:
            h.set_debuglevel(1)
        
        self.send_request(h, handler, request_body)
        self.send_host(h, host)
        self.send_user_agent(h)
        self.send_content(h, request_body)
        
        errcode, errmsg, headers = h.getreply()
        if errcode != 200:
            raise xmlrpclib.ProtocolError(host + handler, errcode, errmsg,
                                          headers)
        
        self.verbose = verbose
        
        # Here's where we differ from the superclass. It says:
        # try:
        #     sock = h._conn.sock
        # except AttributeError:
        #     sock = None
        # return self._parse_response(h.getfile(), sock)
        
        return self.parse_response(h.getfile())


from cherrypy.test import helper

class XmlRpcTest(helper.CPWebCase):
    def testXmlRpc(self):
        
        # load the appropriate xmlrpc proxy
        scheme = "http"
        try:
            scheme = self.harness.scheme
        except AttributeError:
            pass
        
        host = self.HOST
        if host == '0.0.0.0':
            # INADDR_ANY, which should respond on localhost.
            host = "127.0.0.1"
        if host == '::':
            # IN6ADDR_ANY, which should respond on localhost.
            host = "::1"
        
        if scheme == "https":
            url = 'https://%s:%s/xmlrpc/' % (host, self.PORT)
            proxy = xmlrpclib.ServerProxy(url, transport=HTTPSTransport())
        else:
            url = 'http://%s:%s/xmlrpc/' % (host, self.PORT)
            proxy = xmlrpclib.ServerProxy(url)
        
        # begin the tests ...
        self.getPage("/xmlrpc/foo")
        self.assertBody("Hello world!")
        
        self.assertEqual(proxy.return_single_item_list(), [42])
        self.assertNotEqual(proxy.return_single_item_list(), 'one bazillion')
        self.assertEqual(proxy.return_string(), "here is a string")
        self.assertEqual(proxy.return_tuple(), list(('here', 'is', 1, 'tuple')))
        self.assertEqual(proxy.return_dict(), {'a': 1, 'c': 3, 'b': 2})
        self.assertEqual(proxy.return_composite(),
                         [{'a': 1, 'z': 26}, 'hi', ['welcome', 'friend']])
        self.assertEqual(proxy.return_int(), 42)
        self.assertEqual(proxy.return_float(), 3.14)
        self.assertEqual(proxy.return_datetime(),
                         xmlrpclib.DateTime((2003, 10, 7, 8, 1, 0, 1, 280, -1)))
        self.assertEqual(proxy.return_boolean(), True)
        self.assertEqual(proxy.test_argument_passing(22), 22 * 2)
        
        # Test an error in the page handler (should raise an xmlrpclib.Fault)
        try:
            proxy.test_argument_passing({})
        except Exception, x:
            self.assertEqual(x.__class__, xmlrpclib.Fault)
            self.assertEqual(x.faultString, ("unsupported operand type(s) "
                                             "for *: 'dict' and 'int'"))
        else:
            self.fail("Expected xmlrpclib.Fault")
        
        # http://www.cherrypy.org/ticket/533
        # if a method is not found, an xmlrpclib.Fault should be raised
        try:
            proxy.non_method()
        except Exception, x:
            self.assertEqual(x.__class__, xmlrpclib.Fault)
            self.assertEqual(x.faultString, 'method "non_method" is not supported')
        else:
            self.fail("Expected xmlrpclib.Fault")
        
        # Test returning a Fault from the page handler.
        try:
            proxy.test_returning_Fault()
        except Exception, x:
            self.assertEqual(x.__class__, xmlrpclib.Fault)
            self.assertEqual(x.faultString, ("custom Fault response"))
        else:
            self.fail("Expected xmlrpclib.Fault")


if __name__ == '__main__':
    setup_server()
    helper.testmain()

