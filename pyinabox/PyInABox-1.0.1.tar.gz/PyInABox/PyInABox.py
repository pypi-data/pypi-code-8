#  PyInABox.py
#  
#  Copyright 2013 Logan Perkins <perkins@pyinabox.alestan.publicvm.com>
#  
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#  
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#  
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#  
#  
#tab-width: 2



import sys,gtk,vte,threading,time

from twisted.python.filepath import FilePath
from twisted.python import log
from twisted.internet import gtk2reactor
gtk2reactor.install()
from twisted.internet import reactor
from nevow.athena import LivePage, LiveElement, expose
from nevow.loaders import xmlfile, xmlstr, htmlfile, htmlstr
from nevow.appserver import NevowSite


sibling = FilePath(__file__).sibling
def Print(*args):
  print args

class PyInABoxElement(LiveElement):
    """
    """

    docFactory = xmlfile(sibling('PyInABox.html').path, 'PyInABoxPattern')

    jsClass = u"pyinabox"

    validSymbols = '0123456789/*-=+.C[]^ d'
    keyCodes={37:gtk.keysyms.Left,
              39:gtk.keysyms.Right,
              38:gtk.keysyms.Up,
              40:gtk.keysyms.Down,
              9:gtk.keysyms.Tab,
              27:gtk.keysyms.Escape,
              46:gtk.keysyms.Delete,
              112:gtk.keysyms.F1,
              113:gtk.keysyms.F2,
              114:gtk.keysyms.F3,
              115:gtk.keysyms.F4,
              116:gtk.keysyms.F5,
              117:gtk.keysyms.F6,
              118:gtk.keysyms.F7,
              119:gtk.keysyms.F8,
              120:gtk.keysyms.F9,
              121:gtk.keysyms.F10,
              122:gtk.keysyms.F11,
              123:gtk.keysyms.F12,
              18:gtk.keysyms.Home,
              35:gtk.keysyms.End,
              45:gtk.keysyms.Insert,
              34:gtk.keysyms.Page_Down,
              33:gtk.keysyms.Page_Up,
              18:gtk.keysyms.Alt_L,
              17:gtk.keysyms.Control_L,
              20:gtk.keysyms.Caps_Lock,
              18:gtk.keysyms.Pause,
              19:gtk.keysyms.Break,
              }
    maskCodes={gtk.keysyms.Control_L:4,
              gtk.keysyms.Alt_L:8
              }
    def __init__(self):

        LiveElement.__init__(self)
        self.Modifiers=[]
        self.Vte=vte.Terminal()
        self.Vte.set_size(80,40)
        self.Vte.fork_command('./Login.sh')
        self.Vte.connect('contents-changed', self.Refresh)
    def keyUp(self, keycode):
        kc=self.keyCodes.get(int(keycode))
        if kc in self.Modifiers:  
          for i in xrange(self.Modifiers.count(kc)):
            self.Modifiers.remove(kc)
        if kc:
          a=gtk.gdk.Event(8);
          a.hardware_keycode=int(kc);
          a.keyval=int(kc);
          self.Vte.emit('button-release-event',a)
    expose(keyUp)
    def keyDown(self, keycode):
        kc=self.keyCodes.get(int(keycode))
        self.Modifiers.append(kc)
        if kc:
          a=gtk.gdk.Event(8);
          a.hardware_keycode=int(kc);
          a.keyval=int(kc);
          v=0
          for i in self.Modifiers:
            v=v | self.maskCodes.get(i,0)
          a.state=gtk.gdk.ModifierType(v)
          if v:
            a.is_modifier=True
          self.Vte.emit('button-press-event',a)
    expose(keyDown)
    def Meta(self, keycode):
        kc=self.keyCodes.get(int(keycode))
        if kc:
          a=gtk.gdk.Event(8);
          a.hardware_keycode=int(kc);
          a.keyval=int(kc);
          v=0
          for i in self.Modifiers:
            v=v | self.maskCodes.get(i,0)
          a.state=gtk.gdk.ModifierType(v)
          if v:
            a.is_modifier=True
          self.Vte.emit('key-press-event',a)

    expose(Meta)
    def Refresh(self,*args):
      self.callRemote('Refresh',unicode(self.Vte.get_text(lambda *a:True)).rstrip('\n'), self.Vte.get_cursor_position()
      )
    expose(Refresh)
    def Process(self, symbol):
      if int(symbol) in [13, 8]:
        if symbol==13:
          symbol=10
        self.Vte.feed_child(chr(symbol))
      else:
        a=gtk.gdk.Event(8)
        a.hardware_keycode=int(symbol);
        a.keyval=int(symbol);
        v=0
        for i in self.Modifiers:
          v=v | self.maskCodes.get(i,0)
        a.state=gtk.gdk.ModifierType(v)
        print a.state
        print v
        print a
        if v:
          a.is_modifier=True
        self.Vte.emit('key-press-event',a)
    expose(Process)

class PyInABoxParentPage(LivePage):
    """
    
    """
    docFactory = xmlfile(sibling('PyInABox.html').path)
    def renderHTTP(self, *args):
            return LivePage.renderHTTP(self, *args)
    def __init__(self, *a, **kw):
        LivePage.__init__(self)
        self.jsModules.mapping[u'pyinabox'] = sibling(
            'PyInABox.js').path


    def render_PyInABox(self, ctx, data):
        """
        
        """
        c = PyInABoxElement()
        

        c.setFragmentParent(self)
        return c
class Parent(PyInABoxParentPage):
        def renderHTTP(self, *args):
                return PyInABoxParentPage()

from twisted.internet import ssl

def main():
    log.startLogging(sys.stdout)
    site = NevowSite(Parent())
    Method="SSL"
    #~ SSLPrivateKey='/etc/CA/myCA/private/server-key-cert.pem'
    #~ SSLCert='/etc/CA/myCA/private/server-key-cert.pem'
    reactor.listenTCP(18081, site)
    #~ reactor.listenSSL(18080, site, contextFactory=ssl.DefaultOpenSSLContextFactory(SSLPrivateKey,SSLCert))
    reactor.run()




try:
  import gtk
except:
  print >> sys.stderr, "You need to install the python gtk bindings"
  sys.exit(1)

# import vte
try:
  import vte
except:
  error = gtk.MessageDialog (None, gtk.DIALOG_MODAL, gtk.MESSAGE_ERROR, gtk.BUTTONS_OK,
    'You need to install python bindings for libvte')
  error.run()
  sys.exit (1)

if __name__ == '__main__':
    main()
