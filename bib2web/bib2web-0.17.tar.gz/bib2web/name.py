# coding=utf-8

from nameparser import HumanName
from bibtexparser.customization import *

class Name():
	def __init__(self, first=None, middle=None, last=None, titles=None):
		self.first = first
		self.middle = middle
		self.last = last
		self.titles = titles

	def __repr__(self):
		return "<Name first:%s middle:%s last:%s titles:%s>" % (self.first, self.middle, self.last, self.titles)

	#Original function is bibtexparser's, I only added some more contraints
	def getnames(self, names, names_norm):
		"""Make people names as surname, firstnames
		or surname, initials. Should eventually combine up the two.
		:param names: a list of names
		:type names: list
		:returns: list -- Correctly formated names
		"""
		tidynames = []
		result = ""
		print names
		print names_norm
		for i, namestring in enumerate(names):
			print namestring
			if len(namestring.split()) < 2:
				#print str(namestring) + " cannot be parsed"
				tidynames.append(Name(None, None, namestring, None))
				continue
			foundMiddle = False
			last = []
			middle = []
			titles = []
			firsts = []
			namestring = namestring.strip()
			left_curly_index = right_curly_index = comma_index = -1
			if len(namestring) < 1:
				continue
			print names_norm[i][0]
			if '{' in names_norm[i][0] and '}' in names_norm[i][0]:
				left_curly_index = namestring.find('{')
				right_curly_index = namestring.find('}')
				comma_index = namestring.find(',')
				print left_curly_index
				print right_curly_index
				print comma_index
			if ',' in namestring:
				namesplit = namestring.split(',')
				if len(namesplit) == 2:
					#print "ALS HET GOED IS KOMEN WE HIER!"
					"""
					tussenvoegsel(s) Achternaam/Achternamen, Voornamen/Initialen 
					"""
					if left_curly_index < comma_index:
						middle = namesplit[0]
						#print middle
						while not middle[len(middle) - 1].islower():
							middle.pop()
						last = namestring.split('{')[1].split('}')[0].split()
						firsts = [i.strip() for i in namesplit[1].split()]
					elif left_curly_index > comma_index:
						last = namesplit[0].strip().split()
						firsts = namestring.split('{')[1].split('}')[0].split()
					else:
						last = namesplit[0].split()
						firsts = namesplit[1].split()
					if len(middle) == 0:
						for i, name in enumerate(last):
							if name.islower():
								middle.append(last.pop(i))
						middle = middle[::-1] #Reverse the list!
				if len(namesplit) == 3:
					"""
					tussenvoegsel(s) Achternaam/Achternamen, Titel(s), Voornamen/Initialen
					"""
					if left_curly_index < comma_index and left_curly_index >= 0:
						middle = namesplit[0]
						while not middle[len(middle) - 1].islower():
							middle.pop()
						last = namestring.split('{')[1].split('}')[0].split()
						firsts = [i.strip() for i in namesplit[2].split()]
					elif left_curly_index > comma_index and left_curly_index >= 0:
						last = namesplit[0].strip().split()
						firsts = namestring.split('{')[1].split('}')[0].split()
					else:
						firsts = namesplit[2].split()
						last = namesplit[0].split()
					for i, name in enumerate(last):
						if name.islower():
							middle.append(last.pop(i))
					middle = middle[::-1] #Reverse the list!
					titles.append(namesplit[1].strip())
			else:
				"""
				Voornamen/Initialen tussenvoegsel(s) Achternaam/Achternamen
				"""
				print "Voornamen/Initialen tussenvoegsel(s) Achternaam/Achternamen"
				namesplit = namestring.split()
				for item in namesplit:
					if item.islower():
						foundMiddle = True
				if left_curly_index == 0 and right_curly_index > 0:
					print "dit is niet goed"
					firsts = namestring.split('{')[1].split('}')[0].split()
					last = namesplit[right_curly_index + 1:].split()
				elif left_curly_index > 0 and right_curly_index > 0:
					print "dit is goed"
					last = namestring.split('{')[1].split('}')[0].split()
					firsts = namestring[:left_curly_index - 1].split()
				else:
					print "in de else"
					if foundMiddle == True:
						while not namesplit[len(namesplit) - 1].islower():
							last.append(namesplit.pop())
						last = last[::-1] #Reverse the list!
					else:
						last = [namesplit.pop()]
				if foundMiddle == True:
					#print namesplit
					while namesplit[len(namesplit) - 1].islower():
						middle.append(namesplit.pop())
					middle = middle[::-1] #Reverse the list!
				if len(firsts) == 0:
					firsts = [i.replace('.', '. ').strip() for i in namesplit]
			#print "first: " + str(firsts)
			#print "middle: " + str(middle)
			#print "last: " + str(last)
			#print "titles: " + str(titles)
			tidynames.append(Name(firsts, middle, last, titles))
			result += " ".join(middle) + " " + " ".join(last) + ", " + " ".join(firsts)
		return result