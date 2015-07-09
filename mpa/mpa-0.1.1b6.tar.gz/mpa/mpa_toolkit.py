"""
MPA TOOKIT
AUTHOR: YUHANG WANG
DATE:  06/18/2015
"""
#================================================
# Use Python 3 compatibility
#================================================
from __future__ import print_function, division
#------------------------------------------------
import re
import pyparsing
#------------------------------------------------

def get_array_item_i_safely(user_input, i):
	"""
	If input is a list, then return its item i 
	If not, then just return user_input 
	"""
	if isinstance(user_input, (list, tuple)):
		return user_input[i]
	else:
		return user_input

def is_list_tuple(input):
	"""
	Check whether input is a list/tuple
	:param input: input 
	"""
	if isinstance(input, list): 
		return True 
	elif isinstance(input, tuple): 
		return True 
	else:
		return False  

def is_multidimensional_list_tuple(input):
	"""
	Check whether input list is multidimensional 
	:param input: input
	"""
	# check whether input is actually a list or not 
	if not is_list_tuple(input): return False 

	if is_list_tuple(input[0]): 
		return True
	else:
		return False

def is_string(input):
	"""
	Check whether input is a string: plain string or unicode 
	ref: http://stackoverflow.com/questions/1303243/how-to-find-out-if-a-python-object-a-string
	"""
	return isinstance(input,basestring)

def is_convertible_to_list(input):
	"""
	Check whether an input string is convertible to a list
	"""
	if type(input) is str:
		return (re.match(r"\(.+\)", input) is not None)
	else:
		return False

def string_to_bool_or_not(input):
	"""
	Convert a numerical value to boolean
	Convention: "True" => True
				"False" => False
				otherwise the original string is returned
	:param str input: either "YES" or "NO"
	"""
	# only proceed when the input type is "str"
	if not is_string(input): return input 

	if input == "True":
		return True
	elif input == "False":
		return False
	else:
		return input

def string_to_number_or_not(input):
	"""
	Convert a string to integer | float number 
	:param str input: input data
	:return: either a number or the original input 
	"""
	# only proceed when the input type is "str"
	if type(input) is not str: return input 

	if re.match(r"^[-]?\d+$", input):
		return int(float(input))
	elif re.match(r"^[-]?\d*\.\d*$", input):
		return float(input)
	else:
		return input

def string_to_None_or_not(input):
	"""
	Convert string "None" to python type 'None'
	"""
	# only proceed when the input type is "str"
	if type(input) is not str: return input 

	if re.match(r"^None$", input):
		return None 
	else:
		return input

def to_boolean_list_or_not(my_input):
	"""
	convert every element in a list to numerical values if possible
	If not, keep the original value 
	"""	
	output = []	
	if type(my_input) is list:
		for item in my_input:
			output.append(to_boolean_list_or_not(item))
		return output
	else:
		return string_to_bool_or_not(my_input)


def to_numerical_list_or_not(my_input):
	"""
	convert every element in a list to numerical values if possible
	If not, keep the original value 
	"""	
	output = []	
	if type(my_input) is list:
		for item in my_input:
			output.append(to_numerical_list_or_not(item))
		return output
	else:
		return string_to_number_or_not(my_input)

def string_to_tuple_or_not(input):
	"""
	convert string to a list 
	"""
	# anything within the quoted string will be preserved
	quoted_string_definition = pyparsing.QuotedString('"', escChar='\\')
	separator = pyparsing.Suppress(',')
	content = pyparsing.Word(pyparsing.alphas+":-[]_^%$#@!"+pyparsing.nums+'.') | separator
	parens = pyparsing.nestedExpr(opener='(', closer=')', content=content, ignoreExpr=quoted_string_definition)

	list_result = parens.parseString(input).asList()[0]
	list_result = to_boolean_list_or_not(list_result)
	list_result = to_numerical_list_or_not(list_result)
	list_result = tuple(list_result)
	return list_result

def transform_string_to_python_data_type(input_string):
	"""
	Transform a string to proper python data type
	:param str input_string: input string 
	:return: either a proper data type or the original string 
	"""
	output = input_string
	if is_convertible_to_list(output):
		output = string_to_tuple_or_not(output)
	output = string_to_None_or_not(output)
	output = string_to_number_or_not(output)
	output = string_to_number_or_not(output)
	output = string_to_bool_or_not(output)
	return output

def return_smaller(input_1, input_2):
	"""
	Compare two inputs and return the smaller one 
	If one of them is None, return the other input 
	:param number input_1: input 1
	:param number input_2: input 2
	:return: number 
	"""
	if input_1 is None: return input_2
	if input_2 is None: return input_1
	if input_1 > input_2:
		return input_2
	else:
		return input_1

def return_bigger(input_1, input_2):
	"""
	Compare two inputs and return the bigger one 
	If one of them is None, return the other input 
	:param number input_1: input 1
	:param number input_2: input 2
	:return: number 
	"""
	if input_1 is None: return input_2
	if input_2 is None: return input_1
	if input_1 > input_2:
		return input_1
	else:
		return input_2

def initialize_a_2d_array_with_None(n_rows, n_columns):
	"""
	Return a 2D array (python list of lists) initialized with None 
	:param int n_rows: number of rows 
	:param int n_columns: number of columns 
	:return: python list of lists 
	"""

	#----------------------------------------------------------------------------------------------
	# make a 2D array to store the global min/max for each figure axis
	#----------------------------------------------------------------------------------------------
	array2d = []
	for i_row in range(0,n_rows):
		array2d.append([])
		for i_column in range(0, n_columns):
			array2d[i_row].append(None)
	return array2d

