#!/usr/bin/python
# -*- coding: utf-8 -*-
#-------------------------------------------------------------------------------
# Name:        atddir
# Purpose:     Use of the ATD API for analyzing files in a folder
#
# Author:      Carlos Munoz (carlos_munoz@mcafee.com)
#
# Created:     08/05/2015
# Copyright:   (c) Carlos M 2015
#-------------------------------------------------------------------------------
#
#-------------------------------------------------------------------------------
# Version: V1.0
# Release control:
#                08/05/2015 - First release
#                12/05/2015 - Introducing the quarantine feature
#				 13/05/2015 - Important improvements in terms of logs (recording)
#						      and calculating the list of files not analyzed
#				 15/05/2015 - Creation of basic folder structure separating 
#							  classes for better understanding of the code
#							  Added -foce parameter to force the analisys of 
#							  existing files
#							  Added the date to every entry on the Database for
#							  later comparation in order to allow the re analisys
#							  of files with more than X seconds
#							  Added the delta parameter to re analyze files which
#							  was done before the delta time
#				   			  Added the monitor feature, to monitor in a continuos
#							  loop a folder.
#                17/05/2015 - The vm_id is now None, taking benefict of the new
#							  feature of the class. If it is set to None the 
#							  profile assigned to the user will be used.
#							  If the id is set then the associated profile will
#							  be used.
#							  When it monitor mode now it captures the ctrl-c
#							  signal and end the script not abruptely
#				 25/05/2015 - Two new functionalities are included:
#								- IF ATD reports back that a compress file is 
#								password protected, we change the severity of the
#								file to 666	and the description to: 'File potentially 
#								encrypted - Not analyzed'
#								- Now the solution is able to suport non ascii 
#								characters, aqctually the following codecs are
#								supported: ascii, utf-8 and cp-1252
#									
#-------------------------------------------------------------------------------

# -------------------------------------------------------------------------------
# PROCESO DE CREACION DE REPOSITORIO POR PRIMERA VEZ
#
# mkdir /path/to/your/project
# cd /path/to/your/project
# git init
# git remote add origin https://bit_cmunoz@bitbucket.org/bit_cmunoz/atd_dir.git
#
# PROCESO DE REPLICA EN GIT
#
# git status        --> Muestra el estado de sincronizacion de los distintos archivos
# git add file_name --> Añade un archivo a ser incorporado en la siguiente sincronizacion
# git commit -m "comentario" --> Comentario que queda registrado en bitbucket sobre el commit
# git push -u origin master  --> Sube el archivo al que previamente hemos hecho add a bitbucket
# -------------------------------------------------------------------------------
import threading
import Queue
import os
import hashlib
import sqlite3
import time
import sys
import argparse
import threading
import signal
from atd import atd
from datetime import datetime, timedelta
from Queue import Queue


semaphore = threading.Lock()
mon_pending_files = []
enclosure_queue = None

#***************************************************************************************************************************************************
# The following example of the use of the atd class is quite basic, it just connects to the atd server, uploads a file and return a value from 1-5
# indicating the potential of the file of being malware. This value can be used in third party tools where the integration with the ATD box must
# be done via API.
#***************************************************************************************************************************************************
# In order to integrate the script with third party tools, the script returns the following values:
#    -1 ---> Error connecting to the ATD Server
#    -2 ---> Error uploading file to the ATD Server
#    -3 ---> Analysis failed
#    -4 ---> Error getting report 
#     0 to 5 ---> Severity level (confident of the sample to be malware
#**************************************************************************************************************************************************

def parseargs():
    
	description = 'Sandboxing analysis of files in a folder'
	prog        = 'ATD Folder analysis'
	usage       = 'atddir.py [-h] -u USER -p PASSWORD -atd ATD_IP -path path_to_folder_to_anlyze [-vm profile_id] [-q path_to_quarantine_folder] [force] [-delta seconds] [-monitor]'
    
	epilog      = '''
Examples:

atdcli.py -u admin -p admin -atd 192.168.0.202 -path c:\path [-vm 20] [-q c:\quarantine] [-force] [-delta 86400] [-monitor]
    
    		      '''      
    
	parser = argparse.ArgumentParser(epilog=epilog, usage = usage, prog=prog, description=description, formatter_class=argparse.RawTextHelpFormatter)
    
    
	auth_group = parser.add_argument_group('Authentication parameters')
    
	arg_help = 'User name to connect to the ATD box'
	auth_group.add_argument('-u', required=True, action='store', dest='user', help=arg_help, metavar='  USER')
	arg_help = 'Password to connect to the ATD box'
	auth_group.add_argument('-p', required=True, action='store', dest='password', help=arg_help, metavar='  PASSWORD')
	arg_help = 'IP address of ATD box'
	auth_group.add_argument('-atd', required=True, action='store', dest='atd_ip', help=arg_help, metavar='ATD IP')

	required_group = parser.add_argument_group('Rest of required parameters')

	arg_help = 'Path to folder'
	required_group.add_argument('-path', required=True, action='store', dest='path', help=arg_help, metavar='PATH')


	arg_help = 'vmProfileList number (the ID of the analyzer)'
	parser.add_argument('-vm', default=None, required=False, action='store', dest='vm_id', help=arg_help, metavar='VM ID')
	arg_help = 'Delta value in seconds to re-analyze files - 0 = never'
	parser.add_argument('-delta', default=0, required=False, action='store', dest='delta', help=arg_help, metavar='DELTA TIME')
	arg_help = 'Quarantine folder'
	parser.add_argument('-q', default=None, required=False, action='store', dest='q_path', help=arg_help, metavar='QUARANTINE')
	arg_help = 'Force analisys'
	parser.add_argument('-force', default=False, required=False, action='store_true', dest='force', help=arg_help)
	arg_help = 'Monitor folder mode'
	parser.add_argument('-monitor', default=False, required=False, action='store_true', dest='monitor', help=arg_help)

	parser.add_argument('--version',action='version',version='Carlos Munoz (carlos_munoz@mcafee.com)\n%(prog)s 1.0 (15/05/2015)')
    
	return parser.parse_args()

def get_list_and_hash(path_to_folder):
	'''
	Description: Gets the list and the hash of files of the current folder. 
	This is not a recursive process
	
	Input:       
		     path_to_folder: Path to the folder to get the list of files from
	Output:      

			 returns a list of tuples with the following format (hash_value, file_name, path)
	'''
	list_of_files=[]

	items = os.listdir(path_to_folder)
		
	for item in items:
		if os.path.isfile(path_to_folder+'\\'+item): 
			file_name = item

			try:
				with open(path_to_folder+ '\\' + file_name, 'rb') as myfile:
					hash_value = hashlib.sha256(myfile.read()).hexdigest()
			except Exception as er:
				print 'Error opening file or calculating hash - continuing the process'

			list_of_files.append((hash_value, file_name, path_to_folder))

	return list_of_files

def clean_list(list_of_files, path_to_quarantine_folder, force, delta=0, monitor=False):
	'''
	Description: This procedure gets a dictionary of files and hashes, and checks against a Database if the system already has 
				 reputation about the file. The procedure returns a list with the files that has never been analyze before.
	Input:       
		     list_of_files: List with the format of (hash_value, file_name, path_to_folder)
		     path_to_quarantine_folder : Path to move files in the case of bad reputation
		     force : If True, all the files will be re-analyze
	Output:      

			 This procedure returns a list with the following format (hash_value, file_name, path_to_folder)
	'''
	global semaphore

	db_file    = './database.db'
	clean_list = []

	if os.path.isfile(db_file):
		# The file exist so it is not the first time we run this process on this system and some of the files might be already analyze
		if force: # This command line argument force the system to re analyze the files
			i = 0
			for i in range(len(list_of_files)):
				hash_value = list_of_files[i][0]
				file_name  = list_of_files[i][1]
				path       = list_of_files[i][2]
				clean_list.append((hash_value, file_name, path))		
		else:
			try:
				conn   = sqlite3.connect(db_file)
				cursor = conn.cursor()
			except Exception as er:
				er = 'Error connection to Database - %s'%er
				return (False, er)

			i = 0
			for i in range(len(list_of_files)):
				hash_value = list_of_files[i][0]
				file_name  = list_of_files[i][1]
				path       = list_of_files[i][2]

				try:
					cursor.execute('''SELECT FILE_SEVERITY, LAST_DATE FROM FILES WHERE SHA256 = ?''',(hash_value,))
				except Exception as er:
					er = 'Error querying Database - %s'%er
					return (False, er)
    	    
				value = None
				value = cursor.fetchone()
			
				if value: # Means that the record already exits, so the information is written on an output file
					severity = value[0]
					record_date = datetime.strptime(value[1], '%Y%m%d%H%M%S')

					if int(delta) > 0 and record_date + timedelta(seconds=int(delta)) < datetime.now(): 
						clean_list.append((hash_value, file_name, path))
					else:
						if not monitor: # if monitor mode is enable don't print constantly these messages
							text_to_print = '\n[+] File: %s already analyzed.\n [-] Hash value: %s\n [-] Severity value: %s'%(path + '\\' + file_name, hash_value, severity)
							text_to_log = '%s | %s | %s | %s | File already analyzed\n'%(datetime.strftime(datetime.now(), '%Y/%m/%d %H:%M:%S'), path + '\\' + file_name, hash_value, severity)
							log_entry ('atd_log.log', text_to_print, text_to_log)
									
						# check if quarantine is set		
						value, error_info = quarantine_file(path, path_to_quarantine_folder, file_name, severity )
						if not value:
							print error_info
				
				else: # Means that the record doesn't exits, so it is stored on the pending file for futher analysis
					clean_list.append((hash_value, file_name, path))

			conn.close()
		
	else:
		# this is the first time we run the script on this system. Or the database file does not exits
		value = create_database(db_file)
		if value[0] != True:
			return (False, value)

		i = 0

		for i in range(len(list_of_files)):
			hash_value = list_of_files[i][0]
			file_name  = list_of_files[i][1]
			path       = list_of_files[i][2]
			clean_list.append((hash_value, file_name, path))		

	return (clean_list)

def create_database(db_file = './database.db'):

	'''
	Description: This procedure creates a database or rename the existing one creating a new one in case it already exits
	Input:       
		     db_file: Name of the databse file with a default value of ./database.db
	Output:      

			 This procedure only returns error control. Tuple of two values True or False and None or the error code
	'''

	if os.path.exists(db_file): # Check if the datafile exists
		try:
			if os.path.exists(db_file + '.old'): os.remove(db_file + '.old')
			os.rename(db_file, db_file + ".old") # rename old file adding .old at the end of the file name
		except Exception as er:
			er = 'Error renaming old database - %s'%er
			return (False, er) # If something goes wrong the function returns a tuple with the value False and the error code

    # Creation of the Database
	try:
		conn = sqlite3.connect(db_file) # Creation of the connection object

		conn.execute('''CREATE TABLE FILES 
                        (SHA256    text PRIMARY KEY NOT NULL,
                         LAST_DATE     text, FILENAME     text, FILE_SEVERITY  int)''')

		
		conn.commit() # Save commit the changes
		conn.close() # Close de the connection after the changes are commited.

	except Exception as er:
		er = 'Error creating database - %s'%er
		return (False, er) # If something goes wrong the function returns a tuple with the value False and the error code.

	return (True, None) # Finally if everything goes fine a tuple with the value of True and None is returned

def upload_to_atd(thread_id, q, atd_ip, atd_user, atd_pass, vm_id, q_path):
	global semaphore
	global mon_pending_files


	# Modification included for BCP they want to check if file is protected with password Ex. zip protected file
	# ***************************************************************************************************************
	password_protected = False
	# ***************************************************************************************************************
	
	while True:
		value = q.get()
		file_hash = value[0]
		file_name = value[1]
		path_to_folder = value[2]
		
		# Create the ATD object and connect to it
		try:
			myatd = atd.atd(atd_ip)
		except:
			myatd = atd(atd_ip)
		error_control, data = myatd.connect(atd_user, atd_pass)
    
		if error_control == 0:
			print data
			q.task_done
			sys.exit(-1)

		error_control, data = myatd.upload_file(path_to_folder + '\\' + file_name, vm_id)
		if error_control == 0:
			print data
			myatd.disconnect()
			q.task_done()
			sys.exit(-2)

		jobId  = data['jobId']
		taskId = data['taskId']

		text_to_print = '\n[+] %s \n [-] Uploading file %s\n [-] Hash value: %s '%(datetime.strftime(datetime.now(), '%Y/%m/%d %H:%M:%S'), path_to_folder + '\\' + file_name, file_hash)
		text_to_log = '%s | %s | %s | %s | Uploading file\n'%(datetime.strftime(datetime.now(), '%Y/%m/%d %H:%M:%S'), path_to_folder + '\\' + file_name, file_hash, '')
		log_entry ('atd_log.log', text_to_print, text_to_log)

		# Check status before requesting the report
		while True:
			error_control, data = myatd.check_status(taskId)
			if error_control == 4 or error_control == 3:
				# Waiting for 30 seconds
				time.sleep(30)
			elif error_control == -1:
				print data			
				myatd.disconnect()
				q.task_done()
				sys.exit(-3)
			else: #Analysis done
				#Analysis done
				break	
			

		# Getting Report information	
		while True:
			error_control, data = myatd.get_report(jobId)
		
			if error_control == 0:
				print '\n',data
				myatd.disconnect()
				q.task_done()
				sys.exit(-4)

			if error_control == 3:
				print '\n',data
				myatd.disconnect()
				q.task_done()
				sys.exit(0)


			if error_control == 1:


				# Modification included for XXX they want to check if file is protected with password Ex. zip protected file
				# ***************************************************************************************************************
				try:
					if data['Summary']['OSversion'] == 'invalid password': 
						password_protected = True					
				except Exception as er:
					# Osversion not assinged
					pass
				# *****************************************************************************************************************
				

				severity = data['Summary']['Verdict']['Severity']
				try:
					description = data['Summary']['Verdict']['Description']
				except Exception as er:
					description = "Not provided"

				# Modification included for XXX who wants to check if file is protected with password Ex. zip protected file
				# ***************************************************************************************************************
				if password_protected:
					severity = '666'
					description = 'File potentially encrypted - Not analyzed'
				# *****************************************************************************************************************
				break
			# error_control = 29
			time.sleep(30)

		# Version 0.1.3 supports other codecs aditional to ASCII so now I need to encode that information before to log or present it
		text_to_print = '\n[+] File: %s\n [-] Hash value: %s\n [-] Analisys result value: %s\n [-] Description: %s'%(path_to_folder + '\\' + file_name, file_hash, severity.encode('ascii','ignore'), description.encode('ascii','ignore'))
		text_to_log = '%s | %s | %s | %s | New annalisys perform - %s\n'%(datetime.strftime(datetime.now(), '%Y/%m/%d %H:%M:%S'), path_to_folder + '\\' + file_name, file_hash, severity.encode('ascii','ignore'), description.encode('ascii','ignore'))
		# ***************************************************************************************************************************

		log_entry ('atd_log.log', text_to_print, text_to_log)


		# check if quarantine is set		
		value, error_info = quarantine_file(path_to_folder, q_path, file_name, severity )
		if not value:
			print error_info

		myatd.disconnect()

		# As version 0.1.3 support multiple codecs before to store te information on the Database the coded is decoded, version 0.1.3 supports three codecs utf8, cp1252 and ascii
		codecs=['utf8', 'cp1252','ascii']
		for i in codecs:
			try:
				file_name = file_name.decode(i)
				break
			except:
				pass
		# *************************************************************************************************************************************************************************
		
		semaphore.acquire()
		control_error, error = insert_into_db(file_name, file_hash, severity)
		# Once we know that the analyze proces has ended the entry is remove from the global list so the master thread will not upload it again
		# unless the force of the delta parameter is on.
		if file_hash in mon_pending_files:
			mon_pending_files.remove(file_hash)
		semaphore.release()

		q.task_done()

def quarantine_file(actual_path, new_path, file_name, severity):
	'''
	Description: Qurantine a file 
	Input:       
		     actual_path: Actual location of the file
		     new_path   : New location of the file
		     severity   : Criticity of the file according with ATD
	Output:      

			 This procedure only returns error control. Tuple of two values True or False and None or the error code
	'''
	global semaphore
	if int(severity) > 2 and new_path != None:
		new_path = new_path + '\\' + file_name
		actual_path = actual_path + '\\' + file_name

		try:
			os.rename(actual_path, new_path)
		except Exception as er:
			description = 'Quarantine operation Error: %s'%er
			return (False, description)

		text_to_print = '\n[+] File: %s\n [-] Moved to quarantine folder.'%(actual_path )
		text_to_log = '%s | %s | %s | %s | Moved to quarantine folder - %s\n'%(datetime.strftime(datetime.now(), '%Y/%m/%d %H:%M:%S'), actual_path, '','', new_path)
		log_entry ('atd_log.log', text_to_print, text_to_log)

		return (True, 'Quarantine operation sucessful')

	return (True, 'Threshold for quarantine not reached or quarantine option not activated')

def insert_into_db(fname, file_hash, severity):
	db_file = './database.db'
	current_date = datetime.now()
	current_date_str = datetime.strftime(current_date, '%Y%m%d%H%M%S')
	
	try:
		conn   = sqlite3.connect(db_file)
		cursor = conn.cursor()
	except Exception as er:
		print 'Error in SQL connection - %s'%er
		return (False, er)

	# In case the record already exists (example: force parameter set) instead of an insert we have to do an update
	try:
		cursor.execute('''SELECT * FROM FILES WHERE SHA256 = ?''',(file_hash,))
	except Exception as er:
		er = 'Error querying Database - %s'%er
		return (False, er)
    	    
	value = None
	value = cursor.fetchone()
			
	if value: # Means that the record already exits, so we have to update the information
		try:
			cursor.execute('''UPDATE FILES SET LAST_DATE=?, FILENAME=?, FILE_SEVERITY=? WHERE SHA256 = ?''', \
            	              (current_date_str, fname, int(severity), file_hash))
		except Exception as er:
			print 'Error in UPDATE operation - %s'%er
			return (False, er)
	else:
		try:
			cursor.execute('''INSERT INTO FILES(SHA256, LAST_DATE, FILENAME, FILE_SEVERITY) 
        	                  VALUES (?,?,?,?)''', \

            	              (file_hash, current_date_str, fname, int(severity)))
		except Exception as er:
			print 'Error in INSERT operation - %s'%er
			return (False, er)

	try:
		conn.commit()
	except Exception as er:
		print 'Error in COMMIT operation - %s'%er
		return (False, er)

	conn.close()
	return (True, 'Insert done')

def log_entry(log_file, text_to_print, text_to_log):

	global semaphore

	semaphore.acquire()
	
	print text_to_print
	with open(log_file, "a") as mylogfile:
		mylogfile.write(text_to_log)
	
	semaphore.release()

def handler_signal(s, f):
	global enclosure_queue
	print '\n[+] Interruption detected, wating for threads to join'
	enclosure_queue.join()	
	sys.exit()

def main():
	global mon_pending_files
	global enclosure_queue
	
	options = parseargs()

	number_of_threads = 10
	enclosure_queue = Queue()

	if options.monitor: # Requesting monitor mode
		print '\n[+] Monitor mode enabled - Press Ctrl C to exit'
		# Set up some threads to fetch the enclosures
		threads = []
		for i in range(number_of_threads):
			worker = threading.Thread(target=upload_to_atd, args=(i, enclosure_queue, options.atd_ip, options.user, options.password, options.vm_id, options.q_path))
			threads.append(worker)
			worker.setDaemon(True)
			worker.start()

		signal.signal(signal.SIGINT, handler_signal)

		while True:
			list_of_files = get_list_and_hash(options.path) # gets the list of files and their hashes
			final_list = clean_list(list_of_files, options.q_path, options.force, options.delta, options.monitor) # clean the list so we get a clean list with the name and hash of the files to analyze

			if final_list: #If there are files to analyze
				# Read the final_list and put the values into the queue
				i = 0
				for i in range(len(final_list)):
					hash_value = final_list[i][0]
					file_name  = final_list[i][1]
					path       = final_list[i][2]

					if hash_value not in mon_pending_files:
						# When modo monitor is activated we need to inform to the master thread that we are waiting for the results
						# because the master thread checks for new files every 10 seconds and can upload the same file multiple times
						semaphore.acquire()
						mon_pending_files.append(hash_value)
						semaphore.release()
						enclosure_queue.put((hash_value, file_name, path)) # tuple with the following format (hash_value, file_name, path_to_folder)		
			final_list = []
			time.sleep(10)
	else: 

		list_of_files = get_list_and_hash(options.path) # gets the list of files and their hashes

		if not list_of_files:
			print '\n[+] There are not files in this folder - Exiting'
			sys.exit()

		final_list = clean_list(list_of_files, options.q_path, options.force, options.delta) # clean the list so we get a file atd_pending_list with the name and hash of the files to analyze

		if not final_list:
			print '\n[+] All files in this folder were previously analyzed - Exiting'
			sys.exit()

		# Set up some threads to fetch the enclosures
		for i in range(number_of_threads):
			worker = threading.Thread(target=upload_to_atd, args=(i, enclosure_queue, options.atd_ip, options.user, options.password, options.vm_id, options.q_path))
			worker.setDaemon(True)
			worker.start()

		# Read the final_list and put the values into the queue
		i = 0
		for i in range(len(final_list)):
			hash_value = final_list[i][0]
			file_name  = final_list[i][1]
			path       = final_list[i][2]

			enclosure_queue.put((hash_value, file_name, path)) # tuple with the following format (hash_value, file_name, path_to_folder)
		
		# Main thread waiting for the queue and the threads to end to get empty
		enclosure_queue.join()

			
if __name__ == '__main__':
	tic = datetime.now()
	main()
	toc = datetime.now()
	print '\nElapse time: ', toc-tic
	