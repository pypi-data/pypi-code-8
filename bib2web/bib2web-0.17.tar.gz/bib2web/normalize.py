# coding=utf-8

from bibtexparser import load, loads
from bibtexparser.bibdatabase import BibDatabase
from bibtexparser.bparser import BibTexParser
import re
import unicodedata
import latexcodec
import string
#import merge

#Normalize a string to ascii, this does not clear the string of all non-
#alphanumeric characters
def to_ascii(s):
	#http://www.peterbe.com/plog/unicode-to-ascii
   return unicodedata.normalize('NFKD', s).encode('ascii', 'ignore').lower()

#Delete all non-alphanumeric characters and lower the whole string
def remove_non_alphanumeric(str):
	return re.sub(r'[^a-zA-Z0-9 ]+', '', str).lower()

def only_letters(str):
	return re.sub(r'[^a-zA-Z]+', '', str).lower()

def only_letters_spaces_comma(str):
	return re.sub(r'[^a-zA-Z, ]+', '', str)

#Make sure all the escaped chars are escaped again, otherwise chars like
# '\t' are interpreted in stead of found by regex
def escape_str(str):
	escaped = str.encode('string_escape')
	return escaped

#Get all the latex tags in the string
def get_latex(str):
	pattern = r'\\\w+'
	return re.findall(pattern, str)

def dash_to_space(str):
	result = re.sub(r'-|/', ' ', str)
	return result

def multiple_spaces(str):
	result = re.sub(r'[ ]{2,}', ' ', str)
	return result

def find_latex_in_name(name):
	escaped = escape_str(name).strip()
	tags = get_latex(escaped)
	for tag in tags:
		if len(tag.decode('string_escape').decode('latex')) != -1:
			escaped = escaped.replace(tag, '')
	decoded_latex = escaped.decode('latex')

#Normalizing the string to ascii and non-alphanumeric only
def normalize_title(str):
	no_newline = str.replace('\n', ' ').replace('\r', '')
	#print "escaping"
	escaped = escape_str(no_newline).strip()
	#print "remove spaces"
	no_multiple_spaces = multiple_spaces(escaped)
	#print "remove dashes"
	no_dashes = dash_to_space(no_multiple_spaces)
	#print "checking for latex"
	tags = get_latex(no_dashes)
	for tag in tags:
		# if length is not 1, the unicode equivalent is not found
		if len(tag.decode('string_escape').decode('latex')) != 1:
			no_dashes = no_dashes.replace(tag, '')
	#print "remove non existing latex"
	decoded_latex = no_dashes.decode('latex')
	#print "all ascii"
	ascii_only = to_ascii(decoded_latex)
	return remove_non_alphanumeric(ascii_only)

def space_to_underscore(str):
	result = re.sub(r'[ ]', '_', str)
	return result

#Delete everything that is not a number
def normalize_number(number):
	return re.sub(r'\D+', '', number)

#Sometimes year has a other field as well, because of parsing error
def normalize_year(year):
	#print "normalizing year: " + str(year)
	if len(year) > 4:
		year = year[:4]
	return str(year)


#Normalize month from abbreviation to full month name
def normalize_month(month):
	abbr = ['jan', 'feb', 'mar', 'apr', 'may', 'jun', \
			'jul', 'aug', 'sep', 'oct' ,'nov', 'dec']
	months = ['January', 'February', 'March', 'April', \
			 'May', 'June',	'July', 'August', 'September',
			 'October' ,'November', 'December']
	if only_letters(month) in abbr:
		return months[abbr.index(only_letters(month))]

	return month

def normalize_author(author):
	no_newline = author.replace('\n', ' ').replace('\r', '')
	#print "escaping"
	escaped = escape_str(no_newline).strip()
	#print "remove spaces"
	no_multiple_spaces = multiple_spaces(escaped)
	#print "remove dashes"
	no_dashes = dash_to_space(no_multiple_spaces)
	#print "checking for latex"
	tags = get_latex(no_dashes)
	for tag in tags:
		# if length is not 1, the unicode equivalent is not found
		if len(tag.decode('string_escape').decode('latex')) != 1:
			no_dashes = no_dashes.replace(tag, '')
	#print "remove non existing latex"
	decoded_latex = no_dashes.decode('latex')
	#print "all ascii"
	author_norm = only_letters_spaces_comma(decoded_latex)
	#print "author_norm: " + str(author_norm)
  	
  	return author_norm


