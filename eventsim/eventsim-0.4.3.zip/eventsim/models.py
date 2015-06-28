import random, math, os
number = random.random()

# Checks in case user hasn't inputted the right information
def errorcheck(outcome, cum_prob):
	''' Error checks for invalid inputs.'''
	last_cum = (cum_prob[-1:])
	last_cum = (''.join(map(str, last_cum)))

	if len(outcome) != len(cum_prob):
		raise ValueError("'prob' arguments must be of same length")

	elif float(last_cum) != 1:
		raise ValueError("last value of 2nd argument must be 1")

# Calculates the probability of an outcome given its cummulative probability
def prob(outcome, cum_prob):
	'''Returns a probability given its cummulative probability'''
	#takes in two lists as arguments

	#error checking
	errorcheck(outcome, cum_prob)

	#----- loops to find probability of each item
	probability = []
	probability.append(cum_prob[0])

	#loops over the cumulative probability
	for item in cum_prob:
		# gets previous index in cum_prob list
		prev_index = cum_prob.index(item) - 1

		if 0 < cum_prob.index(item): 
			occurtimes = (float("%.4f" %(item - cum_prob[prev_index])))
			probability.append(occurtimes)
	return probability

# Generaes a discreteEmp for the given outcome 
def discreteemp(*args):
	'''returns a random number from the outcome list'''
	#--- generating a random number based on discreteemp
	
	emplist = []
	outcome = args[0]
	cum_prob = args[1]
	errorcheck(outcome, cum_prob)

	def twoargs():
		count = 0
		number = random.random()

		while count < len(cum_prob):
			if cum_prob[count] < number <= cum_prob[count+1]:
				return outcome[count+1]
			
			elif 0 <= number <= cum_prob[0]:
			 	return outcome[0]

			count+=1

	if len(args) == 2:
		return twoargs()

	elif len(args) == 3:
		amount = args[2]
		# emplist = []
		increment = 0
		while increment < amount:
			generated = twoargs()
			emplist.append(generated)
			increment +=1
		return emplist

# Calculates the expectation value given its outcome and cummulative probability
def expectval(*args):
	''' returns the expectation value of the outcomes'''

	outcome = args[0]
	cum_prob = args[1]
	probability = prob(outcome, cum_prob)

	expectation, increment = 0,0

	while increment < len(cum_prob):
		expectation += probability[increment] * outcome[increment]
		increment += 1

	if len(args) == 2:
		return expectation

	elif len(args) == 3:
		steps = args[2]
		expectation = float("%.4f" % (expectation * steps))
		return expectation

	else:
		raise valueerror("arguments must be two or three")

# Calculates the estimated variance of the given lists
def estvar(*args):
	'''returns estimated variance of the outcome'''
	#arguments are: [outcomes], [cummulative probabilities], optional: float(steps)]

	outcome = args[0]
	cum_prob = args[1]

	probability = prob(outcome, cum_prob)
	mean = expectval(outcome, cum_prob)

	increment = 0
	occurtimes = 0
	while increment < len(cum_prob):
		occurtimes += probability[increment] * pow((outcome[increment] - mean), 2)
		increment +=1

	if len(args) == 2:
		occurtimes = float("%.4f" % (occurtimes))
		return occurtimes

	elif len(args) == 3:
		steps = args[2]
		occurtimes = float("%.4f" % (occurtimes))
		return occurtimes * steps

	else: 
		raise valueerror("arguments must be two or three")

# Calculates the estimated standard deviation of the given lists
def eststddev(*args):
	''' Returns the estimated standard deviation of the outcome'''
	#arguments are: [outcomes], [cummulative probabilities], optional: float(steps)]
	variance = estvar(*args)
	occurtimes = float("%.4f" % (math.sqrt(variance)))
	return occurtimes

# Calculates the estimated mean of the given lists
def estmean(*args):
	''' Returns the estimated mean of the outcome'''
	#arguments are: [outcomes], [cummulative probabilities], optional: float(steps)]
	occurtimes = float("%.4f" % (expectval(*args)))
	return occurtimes 

def instruct(filename):
	pass
	# if filename == "models":
	# 	print(open(os.path.join("./", 'models_guide.txt')).read())
	# else:
	# 	#print(open("randgen_guide.txt").read())
	# 	print(open(os.path.join("./", 'randgen_guide.txt')).read())

# Instruction manual
def manual(modulename):
	this_dir, this_filename = os.path.split(__file__)
	if (modulename).lower() == "models":
		DATA_PATH = os.path.join(this_dir, "models_guide.txt")
		print (open(DATA_PATH).read())

	elif (modulename).lower() == "randgen":
		DATA_PATH = os.path.join(this_dir, "randgen_guide.txt")
		print (open(DATA_PATH).read())

	else:
		print("please use 'models' or 'randgen' as argument")