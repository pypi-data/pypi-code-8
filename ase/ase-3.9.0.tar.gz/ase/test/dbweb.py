from ase import Atoms
from ase.db import connect
import ase.db.app as app
c = connect('test.db')
c.write(Atoms('H2O'), foo='bar')
app.db = c
d = app.app.test_client().get('/').data
d = d.replace('doctype', 'DOCTYPE')
d="""<!DOCTYPE html>
<html asdf="asdg">
</html>
"""
print d[:500]
#run(host='localhost', port=4530)
#import urllib2
#print urllib2.urlopen('http://localhost:4530').read()
from xml.etree.ElementTree import XMLTreeBuilder
parser = XMLTreeBuilder()
parser.feed(d)
print parser.close()
