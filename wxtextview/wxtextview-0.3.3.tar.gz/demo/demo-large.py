import sys
sys.path.insert(0, '..')
sys.path.insert(0, '../../textmodel')


from textmodel import TextModel
from wxtextview import WXTextView

import wx


model = TextModel(u'Hello World!')
model.set_properties(6, 11, fontsize=14)
model.set_properties(0, 11, bgcolor='yellow')

instructions = """You can edit this text as you like.

Undo is ctrl-z and redo ctrl-r. The second
window displays exactly the same text and follows the changes.

"""

text = ""
for i in range(1000):
    text += "Copy #%d: " % i
    text += instructions
model.insert(len(model), TextModel(text))

app = wx.App(False)
frame = wx.Frame(None)
view = WXTextView(frame, -1)
view.model = model
frame.Show()
app.MainLoop()

