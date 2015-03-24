from cherrypy.test import test
test.prefer_parent_path()

import cherrypy

def setup_server():
    
    def check(username, password):
        # Dummy check_username_and_password function
        if username != 'login' or password != 'password':
            return u'Wrong login/password'
    
    class Test:
        
        _cp_config = {'tools.sessions.on': True,
                      'tools.session_auth.on': True,
                      'tools.session_auth.check_username_and_password': check,
                      }
        
        def index(self):
            return "Hi, you are logged in"
        index.exposed = True
    
    cherrypy.tree.mount(Test())
    cherrypy.config.update({'environment': 'test_suite'})


from cherrypy.test import helper


class SessionAuthenticateTest(helper.CPWebCase):
    
    def testSessionAuthenticate(self):
        # request a page and check for login form
        self.getPage('/')
        self.assertInBody('<form method="post" action="do_login">')
        
        # setup credentials
        login_body = 'username=login&password=password&from_page=/'
        
        # attempt a login
        self.getPage('/do_login', method='POST', body=login_body)
        self.assertStatus((302, 303))
        
        # get the page now that we are logged in
        self.getPage('/', self.cookies)
        self.assertBody('Hi, you are logged in')
        
        # do a logout
        self.getPage('/do_logout', self.cookies)
        self.assertStatus((302, 303))
        
        # verify we are logged out
        self.getPage('/', self.cookies)
        self.assertInBody('<form method="post" action="do_login">')


if __name__ == "__main__":
    setup_server()
    helper.testmain()

