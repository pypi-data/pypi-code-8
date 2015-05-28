import time
# For debug mode when adding a space
space = 'Spaaaaaaaaaaaaaaace added'
# The usagetext
usagetext = ''' 
Usage: python Encry.py (-e, -d, -f) (message/file) (-d, -r, key) (outputfile[optional])

for help see python Encry.py --help'''
#what to print with an unexpected error
unknownerror = 'Unexpected Error'
#when someone ****s up the arguments
argserror = 'Error, Invalid args'
# _____ has been changed to:
changefrom = 'Has been Changed to:'
# Outputted to file
outputted = 'Outputted to file'
# The version text
version = 'Version 1.3! More O:+Nu-gUYu]#bYn6,bfg+gJ]gIjn]s;fnf)J -ness'
# When done encrypting/decrypting a file
donetext = 'Done!'
# When Giving the entry number
entrynumtext = 'Your Entry Number: '
# this is for a special easter egg with --quit
def quit():
	r = random.randint(1, 50)
	if r == 43:
		print "Don't be a quitter!"
		print "I'm not letting you quit"
		time.sleep(1)
		print "jk just do --quit again"
		sys.exit()
# The helptext
Helptext = '''	Welcome to Encry.py
	
	This program Encrypts messages.
	It can also be used to decrypt.
	Options include:
	--version    	: Prints the version number and exits
	--help		: Prints this help and exits
	--usage	 	: Prints the correct input methods
	--reset	 	: Erases all data in the output file
	--display   	: Prints everything in the output file
	--entry (n) 	: Decrypts the given entry from the output file
	--setup	(-J) 	: Will create/reset the settings, and output file
	--settings  	: Shows the path to settings.py for editing
	--quit	  	: will quit the program
	'''
#change commands too? send me your ideas