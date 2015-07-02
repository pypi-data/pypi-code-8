import os

# Instruction manual
def manuals(modulename):
	this_dir, this_filename = os.path.split(__file__)
	if (modulename).lower() == "models":
		DATA_PATH = os.path.join(this_dir, "help", "models_guide.txt")
		print (open(DATA_PATH).read())

	elif (modulename).lower() == "randgen":
		DATA_PATH = os.path.join(this_dir, "help", "randgen_guide.txt")
		print (open(DATA_PATH).read())

	elif (modulename).lower() == "simevent":
		DATA_PATH = os.path.join(this_dir, "help", "simevent_guide.txt")
		print (open(DATA_PATH).read())

	else:
		print("please use 'models','randgen' or 'simevent' as argument")

	return ""