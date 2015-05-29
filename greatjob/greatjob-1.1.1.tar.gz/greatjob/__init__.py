
import os 

main_image = os.path.dirname(os.path.abspath(__file__)) + "/thumbsup.png"
sparkle_image = os.path.dirname(os.path.abspath(__file__)) + "/sparkle.png"

def main():
	# cwd = os.getcwd()
	# os.chdir(os.path.dirname(os.path.abspath(__file__)) + "/proj/")
	# os.system('make clean')
	# os.system('make install')

	os.system("/usr/local/bin/imageleap -i %s -p %s" % (main_image, sparkle_image))

