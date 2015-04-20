import pickleshare
import args
import os, glob
from subprocess import *
import tempfile

db = pickleshare.PickleShareDB("~/.grepo")

root = db.get('root', None)

def here_c(args):
	db['root'] = os.getcwd()

def runpeco(input):
	tf = tempfile.NamedTemporaryFile(delete=False)
	tf.write(input)
	tf.close()
	p = Popen(['peco', '-b', '5000000', tf.name], stdout = PIPE)
	out = p.stdout.read()
	os.unlink(tf.name)
	#fin, fout = p.stdin, p.stdout
	#fin.write(input)
	#fin.close()
	
	return out

def parents(pth):
	cur = pth
	while 1:
		c2 = os.path.dirname(cur)
		if c2 == cur:
			return
		cur = c2
		yield cur

def search_str(s, files):
	res = []
	for f in files:
		if s in open(f).read():
			res.append(f)

	return res

def more_info(fname):
	fname = os.path.abspath(fname)
	print fname
	bname = os.path.basename(fname)
	for p in parents(fname):
		look = glob.glob(p + '/*.csproj') + glob.glob(p + '/*.sln')
		found = search_str(bname, look)
		print p, look, found

def peco_and_edit(input):
	lines = runpeco(input).splitlines()
	for l in lines:
		fname, line, text = l.split(':', 2)
		print "pick:", fname
		call(['subl',fname + ':' + line])
		#more_info(fname)


def grep_c(args):
	os.chdir(root)
	out = os.popen('git grep -n ' + args.pattern).read()
	#print out
	db['grepoutput'] = out
	peco_and_edit(out)



def pick_c(args):
	os.chdir(root)
	peco_and_edit(db['grepoutput'])
			

def main():
	args.init()

	args.sub('here', here_c, help = 'Set current dir as prjroot')
	s = args.sub('g', grep_c, help = 'Grep the project')
	s.arg("pattern", type=str)
	args.sub('p', pick_c, help = 'Use peco to quick pick one of the earlier choices')
	args.parse()

def test():
	pick_c(None)

#test()
if __name__ == "__main__":
	main()
