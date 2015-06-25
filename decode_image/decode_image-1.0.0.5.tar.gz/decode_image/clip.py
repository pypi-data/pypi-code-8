import sys
import os
import platform

class clipboard(object):
	def __init__(self, data=''):
		super(clipboard, self)
		self.data = data
		self.copy()

	def check_call(self, command):
		import subprocess
		try:
			r = subprocess.check_call([str(command)])
			return r
		except:
			return 1

	def copy(self):
		if 'indows' in platform.system():
			try:
				import clipboard
				clipboard.copy(self.data)
				return clipboard.paste()
			except:
				import win32clipboard as w
				import win32con
				w.OpenClipboard()
				w.EmptyClipboard()
				w.SetClipboardData(w.CF_TEXT, self.data)
				return w.GetClipboardData(win32con.CF_TEXT)
		elif 'inux' in platform.system():
			try:
				import clipboard
				clipboard.copy(self.data)
				return clipboard.paste()
			except:
				try:
					check_01 = os.system('which xsel')
					if check_01 != '':
						from subprocess import Popen, PIPE
						p = Popen(['xsel','-pi'], stdin=PIPE)
						p.communicate(input='data')
						return os.popen('xsel').read()
					else:
						return "\tplease install xsel (apt-get xsel) or clipboard (pypi)\n\tOn Windows you must install pywin32 (pypi) or clipboard (pypi)\n"
				except:
					if self.check_call('xsel') == 0:
						from subprocess import Popen, PIPE
						p = Popen(['xsel','-pi'], stdin=PIPE)
						p.communicate(input='data')
						return os.popen('xsel').read()
					else:
						return "\tplease install xsel (apt-get xsel) or clipboard (pypi)\n\tOn Windows you must install pywin32 (pypi) or clipboard (pypi)\n"
		elif 'arwin' in platform.system():
			os.system("echo '%s' | pbcopy" % self.data)
			from AppKit import NSPasteboard
			from LaunchServices import *
			pb = NSPasteboard.generalPasteboard()
			text = pb.stringForType_(kUTTypeUTF8PlainText)
			return text
		else:
			print "\t you not in Windows, Linux or Mac, this support for windows/linux/mac yet"

if __name__ == "__main__":
	c = clipboard(sys.argv[1])
	print "clipboard now with:", c.copy()
