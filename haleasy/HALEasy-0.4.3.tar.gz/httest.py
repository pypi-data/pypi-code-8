from haleasy import HALEasy
h = HALEasy('http://haltalk.herokuapp.com/')
s = h.link(rel='http://haltalk.herokuapp.com/rels/signup').follow(method='POST', data={'username': '7654321111121123', 'password': '1234567'})
s.properties()