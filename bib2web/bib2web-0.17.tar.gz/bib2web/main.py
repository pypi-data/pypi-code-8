# coding=utf-8

from bibtexparser import load, loads, dump, dumps
from bibtexparser.bwriter import BibTexWriter
from bibtexparser.bibdatabase import BibDatabase
from pybtex.database import Person
from merge import merge, add_field, intersect
import ConfigParser
import logging
import logging.config
import glob
import os
from normalize import normalize_title, normalize_year, space_to_underscore, normalize_author
import subprocess
import re
from fuzzywuzzy import process
from time import time, sleep
import gscholar as gs
import random
from mandatory_fields import mandatory
import gui
from glob import iglob
import sys

logger = logging.getLogger(__name__)

logging.config.dictConfig({
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'standard': {
            'format': '%(asctime)s [%(levelname)s] %(name)s %(funcName)s:%(lineno)d: %(message)s'
        },
    },
    'handlers': {
        'default': {
            'level':'ERROR',
            'formatter': 'standard',
            'class':'logging.StreamHandler',
        },
    },
    'loggers': {
        '': {
            'handlers': ['default'],
            'level': 'ERROR',
            'formatter': 'standard',
            'propagate': True
        }
    }
})

writer = BibTexWriter()
writer.contents = ['comments', 'entries']
writer.indent = '  '
writer.order_entries_by = ('ENTRYTYPE', 'author', 'year')

def create_id(t, year, title):
	return str(t) + "_" + str(year) + "_" + str(space_to_underscore(title))

def pdf(pdf_files, shared_pdf, bibtex_folder, bibtex_files, gscholar):
	for pdf in pdf_files:
		txt = re.sub("\W", " ", gs.convert_pdf_to_txt(pdf)).lower()
		#Research determined that the cutting of 35 words gives the 
		#highest accuracy
		words = txt.strip().split()[:35]
		words = " ".join(words)		
		print words
		if gscholar == True:
			bib = load(gs.pdflookup(pdf, all, gs.FORMAT_BIBTEX)[0])
			keys = bib.entries[0].keys()
			matching = [s for s in keys if "pdf" in s]
			if len(matching) - 1 <= 0:
				key = 'pdf'
			else:
				key = 'pdf' + str(len(matching))
			#link = os.symlink(pdf, str(shared_pdf) + str(pdf.split('/')[-1]))
			bib.entries = [add_field(bib.entries[0], key, bib)]
			bibtex(bib.entries, bibtex_folder, bib)
			sleep(random.uniform(1, 2))
		else:
			best_match = process.extractBests(words, bibtex_files, limit=1)
			print best_match
			if best_match:
				bib = best_match[0][0]
				score = best_match[0][1]
				#Research determined that matching score of 45
				#gives the highest accuracy
				if score > 45:
					with open(bib, 'r') as f:
						db = load(f)
					entries = db.entries[0]
					keys = entries.keys()
					matching = [s for s in keys if "pdf" in s]
					if len(matching) - 1 <= 0:
						key = 'pdf'
					else:
						key = 'pdf' + str(len(matching))
					entries = add_field(entries, key, bib)
					with open(bib, 'w') as f:
						f.write(writer._entry_to_bibtex(entries))

#Check wether all mandatory fields are in there
def is_subset(list1, list2):
	intersection = intersect(list1, list2)
	return set(intersection) == set(list2)

#Check wether the bibtex contains the mandatory fields
def check_bibtex(t, keys):
	return is_subset(keys, mandatory[t])

# BibTex controll function, decides if BibTex needs to be merged
# or if it can just be written
def bibtex(entries, db_folder, current_file):

	#Loop through all entries
	for i, entry in enumerate(entries):
		#Get the keys of the entry
		keys = entry.keys()

		# Check wether the entry has the required mandatory fields
		# for it's ENTRYTYPE
		mandatory_fields = check_bibtex(entry['ENTRYTYPE'], keys)
		if not mandatory_fields:
			print "Entry doesn't contain the mandatory fields"
			continue

		#Make sure the values don't have unicode characters, normalize them
		for key in keys:
			entry[key] = str(entry[key].encode('ascii', 'replace'))

		#Try to normalize author to the Person class
		#If it doesn't match the right format the entry will be skipped
		if 'author' in keys:
			authors = entry['author'].split(' and ')
			a = []
			a_failed = False
			for author in authors:
				try:
					a.append(Person(author))
				except:
					print "Author does not have the right format"
					a_failed = True
					break
			#Something wrong with author, skip the entry
			if a_failed == True:
				continue
			entry['author'] = ' and '.join(unicode(person) for person in a)
			entry['author_norm'] = normalize_author(str(entry['author']))

		#Try to normalize editor to the Person class
		#If it doesn't match the right format the entry will be skipped
		if 'editor' in keys:
			editors = entry['editor'].split(' and ')
			e = []
			e_failed = False
			for editor in editors:
				try:
					e.append(Person(author))
				except:
					print "Editor does not have the right format"
					e_failed = True
					break
			#Something wrong with editor, skip the entry
			if e_failed == True:
				continue

			entry['editor'] = ' and '.join(unicode(person) for person in e)
			entry['editor_norm'] = normalize_author(str(entry['editor']))
		
		#Normalize the title and save the normalized title
		if 'title' in keys and not 'title_norm' in keys:
			title_norm = normalize_title(str(entry['title']))
			entry['title_norm'] = str(title_norm)

		#Normalize the year and save the normalized year
		if 'year' in keys and not 'year_norm' in keys and len(entry['year']) > 0:
			year_norm = normalize_year(str(entry['year']))
			entry['year_norm'] = str(year_norm)

		#Normalize the citationkey and overwrite the old one
		if 'ID' in keys:
			citationkey = str(create_id(entry['ENTRYTYPE'], year_norm, title_norm))
			entry['ID'] = str(citationkey)
		else:
			print "No citationkey found, faulty entry, will be skipped"
			continue

		#Create the unique filename
		filename = str(create_id(entry['ENTRYTYPE'], year_norm, title_norm)) + ".bib"
		path = str(db_folder) + str(filename)

		#Check wether the file exists
		exists = os.path.exists(path)

		#File doesn't exist then we can just write
		if exists == False:
			try:
				with open(path, 'w+') as f:
					f.write(writer._entry_to_bibtex(entry))
			except:
				print "There must be something wrong, please check: "
				print current_file
				print "Can't write this file " + str(path)
				continue
			#File does exists, find open the existing one and merge
			#it with the new one
		else:
			with open(path, 'r') as f:
				simular = load(f).entries
				#Write new entry if existing one is empty
				if len(simular) == 0:
					with open(path, 'w') as f:
						f.write(writer._entry_to_bibtex(entry))

				#Only merge with non empty files
				if len(simular) > 0:
					db = merge(entry, simular[0])

			with open(path, 'w') as f:
				#Only merge when the merge has gone right
				if len(db.entries) > 0:
					f.write(writer._entry_to_bibtex(db.entries[0]))

# Recursively search all subdirectory for files of given type t
def dir_to_file_list(dirs, ext):
	for d in dirs:
		#files = [f for dirpath, dirnames, file in os.walk(d) for f in
		#	iglob(os.path.join(next(iglob(dirpath),
         #                        '\\'), "*{}".format(ext)))]
		files = [os.path.join(dirpath, f)
			for dirpath, dirnames, files in os.walk(d)
			for f in files if f.endswith(ext)]
	return files


def search_new(config, shared_bib, graphical, bibtex_files):
	for bib in bibtex_files:
		with open(bib, 'r') as bibtex_file:
			db = load(bibtex_file)
			bibtex(db.entries, shared_bib, bibtex_file)

	if config.get('pdf', 'search_pdf') == True:
		gscholar = config.get('general','google_scholar')
		pdf_files = dir_to_file_list(config.get('pdf', 'directories').split(','), '.pdf')
		bibtex_files_shared = dir_to_file_list(shared_bib.split(','), '.bib')
		shared_pdf = config.get('pdf', 'shared_directory')
		pdf(pdf_files, shared_pdf, shared_bib, bibtex_files_shared, gscholar)

	graphical.update_table()

def main():
	print sys.argv
	if len(sys.argv) < 2:
		print "Please give a config file in the command line"
		print "Example execution: python bib2web settings.conf"
	else:
		print "Using " + str(sys.argv[1]) + " as configuration file."
		graphical = gui.GUI()

		config = ConfigParser.ConfigParser()
		config.read(sys.argv[1])
		extentions = config.get('general', 'bibtex_filetypes').split(',')
		bibtex_files = []
		for ext in extentions:
			bibtex_files.append(dir_to_file_list(config.get('bibtex', 'directories').split(','), ext.strip()))
		bibtex_files = [item for sublist in bibtex_files for item in sublist]
		shared_bib = config.get('bibtex', 'shared_directory')
		graphical.config = config
		graphical.bib_dir = shared_bib
		graphical.bibtex_files = bibtex_files
		graphical.personal_website_bib = config.get('general', 'personal_website_bib')
		graphical.personal_website_html = config.get('general', 'personal_website_html')
		graphical.personal_link = config.get('general', 'personal_link').replace('dl=0', 'raw=1')
		graphical.group_website_bib = config.get('general', 'group_website_bib')
		graphical.group_website_html = config.get('general', 'group_website_html')
		graphical.group_link = config.get('general', 'group_link').replace('dl=0', 'raw=1')

		count = 0
		for f in os.listdir(shared_bib):
			if f.endswith(".bib"):
				graphical.file_list.append(f)
				split = f.split('_')
				split[-1] = split[-1].split('.')[0]
				graphical.tree.insert("", count, values=(split[0], split[1], split[2:]))
				count += 1

		graphical.win.mainloop()

