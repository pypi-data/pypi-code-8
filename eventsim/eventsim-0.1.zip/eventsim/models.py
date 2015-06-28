import random, math
number = random.random()

# Checks in case user hasn't inputted the right information
def errorcheck(outcome, cum_prob):
	last_cum = (cum_prob[-1:])
	last_cum = (''.join(map(str, last_cum)))

	if len(outcome) != len(cum_prob):
		raise ValueError("'prob' arguments must be of same length")

	elif float(last_cum) != 1:
		raise ValueError("last value of 2nd argument must be 1")

# Calculates the probability of an outcome given its cummulative probability
def prob(outcome, cum_prob):
	'''generates a probability based on its given cummulative probability'''
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
	'''generates an outcome based on the given cummulative probability'''
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
	'''arguments are: [outcomes], [cummulative probabilities], optional: float(steps)]'''

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
		return expectation * steps

	else:
		raise valueerror("arguments must be two or three")

# Calculates the estimated variance of the given lists
def estvar(*args):
	'''arguments are: [outcomes], [cummulative probabilities], optional: float(steps)]'''
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
	'''arguments are: [outcomes], [cummulative probabilities], optional: float(steps)]'''
	variance = estvar(*args)
	occurtimes = float("%.4f" % (math.sqrt(variance)))
	return occurtimes

# Calculates the estimated mean of the given lists
def estmean(*args):
	'''arguments are: [outcomes], [cummulative probabilities], optional: float(steps)]'''
	occurtimes = float("%.4f" % (expectval(*args)))
	return occurtimes 

