import sys
import time

import tornado.web
import tornado.wsgi
import tornado.ioloop

from tprofile import ProfileMeta

class BaseHandler(tornado.web.RequestHandler):
    """this is base class of all handlers"""
    __metaclass__ = ProfileMeta

class MainHandler(BaseHandler):
    def block(self, n):
        time.sleep(n)

    def get(self):
        self.block(1)
        self.write("this is get.\n")
        self.block(0.8)

app = tornado.wsgi.WSGIApplication([
            (r"/test/profile", MainHandler),
        ])

if __name__ == "__main__":
    port = 9876
    if len(sys.argv) > 1:
        port = int(sys.argv[1])
    app.listen(port)
    tornado.ioloop.IOLoop.instance().start()

