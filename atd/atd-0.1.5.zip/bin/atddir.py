#!/usr/bin/python
# -*- coding: utf-8 -*-
#-------------------------------------------------------------------------------
# Name:        atddir
# Purpose:     Use of the ATD API for analyzing files in a folder or to monitor
#			   files in a folder
#
# Author:      Carlos Munoz (charly.munoz@gmail.com)
#
# Created:     11 Of June 2015
# Copyright:   (c) Carlos M 2015
#-------------------------------------------------------------------------------
#
#-------------------------------------------------------------------------------
# Version: V.0.1.5
#-------------------------------------------------------------------------------

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

def parseargs():
    
	description = 'Sandboxing analysis of files in a folder'
	prog        = 'ATD Folder analysis'
	usage       = 'atddir.py [-h] -u USER -p PASSWORD -atd ATD_IP -path path_to_folder_or_file_to_analyze [-vm profile_id] [-q path_to_quarantine_folder] [force] [-delta seconds] [-monitor]'
    
	epilog      = '''

Examples:

1.)

atddir.py -u admin -p admin -atd 192.168.0.202 -path c:\path 

Analyze the content of the folder c:\path, sending the files to the ATD box using the default profile

2.-)

atddir.py -u admin -p admin -atd 192.168.0.202 -path \\path\filename.pdf -vm 20

Analyze the file in the share \\path\filename.pdf, sending it to the ATD box using the profile with the ID 20

3.-)

atddir.py -u admin -p admin -atd 192.168.0.202 -path c:/path/malware -vm 20 -q c:\quarantine -monitor

Analyze the folder c:/path/malware in monitor mode if the file is supicious (>=3) it will be moved to quarantine

4.-)

atddir.py -u admin -p admin -atd 192.168.0.202 -path c:/path/malware -vm 20 -q c:\quarantine -monitor -delta 86400

Same as before but in this case if the files has not been re-analyze in 86400 seconds they will be re-analyze

5.-)

atddir.py -u admin -p admin -atd 192.168.0.202 -path \\path\\filename.pdf -vm 20 -force

Even if the file filename.pdf has been already analyzed, so it is cache locally the -force paramete forces the re-analisys of the file    
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

def get_filename_path(filetosubmit):
	'''
	Description: Internal procedure to get a clean filename and a path 
				 
	Input:       path to file
	Output:      tuple with the clean filename and the path
	'''
	
	if filetosubmit.find(os.sep) != -1:
		file = filetosubmit.split(os.sep)[-1]
	else:
		file = filetosubmit

	path = filetosubmit.split(file)[0]

	# If filetosubmit only includes de filename without the path use curdir instead
	if path == '':
		return (file, os.curdir)

	return (file, path[:-1]) # Return the path except the last directory bar

def get_list_and_hash(path_to_folder):
	'''
	Description: Gets the list and the hash of files of the current folder. 
				 It supports the case where path_to_folder points to a final file
				 This is not a recursive process, so it doesn't look into internal folders
	
	Input:       
		     	 path_to_folder: Path to the folder to get the list of files from
	Output:      

			 	 returns a list of tuples with the following format [(hash_value, file_name, path)]
	'''
	list_of_files=[]

	if os.path.isfile(path_to_folder):
		path_to_file = path_to_folder 
		try:
			with open(path_to_file, 'rb') as myfile:
				hash_value = hashlib.md5(myfile.read()).hexdigest().upper()
		except Exception as er:
			print 'Error opening file: %s or calculating hash - Check path and file size'%path_to_file
			sys.exit()
		
		file_name, path_to_folder = get_filename_path(path_to_file)
		list_of_files.append((hash_value, file_name, path_to_folder))

	else:

		try :
			items = os.listdir(path_to_folder)
		except Exception as er: 
			print 'Error getting the list of files - Check path'
			sys.exit()
		
		for item in items:
			if os.path.isfile(path_to_folder+os.sep+item): 
				file_name = item

				try:
					with open(path_to_folder + os.sep + file_name, 'rb') as myfile:
						hash_value = hashlib.md5(myfile.read()).hexdigest().upper()
				except Exception as er:
					print 'Error opening file: %s or calculating hash - continuing the process'%file_name

				list_of_files.append((hash_value, file_name, path_to_folder))

	return list_of_files

def clean_list(list_of_files, path_to_quarantine_folder, force, delta=0, monitor=False):
	'''
	Description: This procedure gets a list of files, path and hashes, and checks against a Database if the system already 
				 has reputation about the file. The procedure returns a list with the files that has never been analyze before.
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
		# The database file exists so this is not the first time we run this process on this system and some of the files might be already analyzed
		if force: # This command line argument force the system to re analyze the files
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
				er = 'Error connecting to the Database - %s'%er
				sys.exit()

			for i in range(len(list_of_files)):
				hash_value = list_of_files[i][0]
				file_name  = list_of_files[i][1]
				path       = list_of_files[i][2]

				try:
					cursor.execute('''SELECT FILE_SEVERITY, LAST_DATE FROM FILES WHERE MD5 = ?''',(hash_value,))
				except Exception as er:
					er = 'Error querying Database - %s'%er
					sys.exit()
    	    
				value = None
				value = cursor.fetchone()
			
				if value: # Means that the record already exits, so the information is written on an output file
					severity = value[0]
					record_date = datetime.strptime(value[1], '%Y%m%d%H%M%S')

					if int(delta) > 0 and record_date + timedelta(seconds=int(delta)) < datetime.now(): 
						clean_list.append((hash_value, file_name, path))
					else:
						if not monitor: # if monitor mode is enable don't print constantly these messages
							text_to_print = '\n[+] File: %s already analyzed.\n [-] Hash value: %s\n [-] Severity value: %s'%(path + os.sep + file_name, hash_value, severity)
							text_to_log = '%s | %s | %s | %s | File already analyzed\n'%(datetime.strftime(datetime.now(), '%Y/%m/%d %H:%M:%S'), path + os.sep + file_name, hash_value, severity)
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
			print value[1]
			sys.exit()
			
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
                        (MD5           text PRIMARY KEY NOT NULL,
                         LAST_DATE     text, FILENAME     text, FILE_SEVERITY  int)''')

		
		conn.commit() # Save commit the changes
		conn.close() # Close de the connection after the changes are commited.

	except Exception as er:
		er = 'Error creating database - %s'%er
		return (False, er) # If something goes wrong the function returns a tuple with the value False and the error code.

	return (True, None) # Finally if everything goes fine a tuple with the value of True and None is returned

def check_status(jobId, taskId, myatd):

	'''
	Description: This procedure check the severity and the description of a JobId once it has been uploades to ATD
	Input:       
		     	 jobId: Id of the job to check severity and description
	Output:      

				 (error_control,(severity, description) where error control is 1
				 (error_control, (data,)) where error control is 0, -1, 3 and data is the cause of the error
	'''

	status = False 

	if taskId == -1: # it is a zip file
		error_control, taskLists = myatd.taskIdList(jobId)

		if error_control != 1 or len(taskLists) == 0: # There isn't any task associated to this job
			status = False # If there are not task associated, then go to the report without checking status
			status_severity = 'No tasks assigned to this jobId'
		else:
			status = True
	else:
		status = True

	if status:

		while True:
			error_control, data = myatd.check_status(jobId)
			if error_control == 2 or error_control == 3:
				# Waiting for 30 seconds
				time.sleep(30)
			elif error_control == -1 or error_control == 0:
				return (error_control, data)								
			else: #Analysis done
				status_severity = str(data['severity'])
				break

	while True:
		error_control, data = myatd.get_report(jobId)

		if error_control == 0 or error_control == 3: # 0 error, 3 report not found
			return (error_control, data)

		if error_control == 1:
			report_severity = data['Summary']['Verdict']['Severity']

			try:
				report_description = data['Summary']['Verdict']['Description']
			except Exception as er:
				report_description = "Not provided"
		
			try:
				report_notes = data['Summary']['OSversion']						
			except Exception as er:
				report_notes = "Not provided"
								
			break

		time.sleep(10)

	if report_notes == "Blacklist":
		report_severity = '5'
		report_notes    = 'File already in Blacklist, assuming severity 5'
	elif report_notes == "invalid password":
		report_severity = '3'
		report_notes    = 'Protected compressed file with unknown password, assuming severity 3'

	return (1, {'status_severity': status_severity, 'report_severity': report_severity, 'report_description': report_description, 'report_notes': report_notes})



def upload_to_atd(thread_id, q, atd_ip, atd_user, atd_pass, vm_id, q_path):

	'''
	Description: This procedure uploads a file to the ATD server
	Input:       
		     	 thread_id --> Not used
		     	 q         --> Queue used to communicate with threads
		     	 atd_ip    --> IP Address of the ATD server
		     	 atd_user  --> Username to logon to the ATD server
		     	 atd_pass  --> Password to logon to the ATD server
		     	 vm_id	   --> Profile identificator to check the object against
		     	 q_path	   --> Path to quratine to move infected files to
	Output:      

				 Nothing
	'''
	global semaphore
	global mon_pending_files


	while True:
		value = q.get()
		file_hash = value[0]
		file_name = value[1]
		path_to_folder = value[2]
		
		# Create the ATD object
		# *********************************************************************
		try:
			myatd = atd.atd(atd_ip)
		except:
			myatd = atd(atd_ip)
		# *********************************************************************

		# Connect to the ATD object
		# *********************************************************************
		error_control, data = myatd.connect(atd_user, atd_pass)
    
		if error_control == 0:
			print data
			q.task_done
			sys.exit()
		# *********************************************************************

		# Check if file is White or Blacklisted
		# *********************************************************************
		error_control, data = myatd.isBlackorWhiteListed(file_hash) 
		# *********************************************************************


		if data != 'w' and data != 'b': # File not whitelisted or Blacklisted

			# Upload the file to ATD
			# *********************************************************************************
			error_control, data = myatd.upload_file(path_to_folder + os.sep + file_name, vm_id)
			if error_control == 0:
				print data
				myatd.disconnect()
				q.task_done()
				sys.exit()
			# *********************************************************************************

			jobId  = data['jobId']
			taskId = data['taskId'] 

			text_to_print = '\n[+] %s \n [-] Uploading file %s\n [-] Hash value: %s '%(datetime.strftime(datetime.now(), '%Y/%m/%d %H:%M:%S'), path_to_folder + os.sep + file_name, file_hash)
			text_to_log = '%s | %s | %s | %s | Uploading file\n'%(datetime.strftime(datetime.now(), '%Y/%m/%d %H:%M:%S'), path_to_folder + os.sep + file_name, file_hash, '')
			log_entry ('atd_log.log', text_to_print, text_to_log)

			# Check status of the uploaded file
			# *********************************************************************************
			
			error_control, data = check_status(jobId, taskId, myatd)
			
			if not error_control: # if something goes wrong getting the status of the jobId
				print data
				myatd.disconnect()
				q.task_done()				

			else: 

				status_severity    = data['status_severity']
				report_severity    = data['report_severity']
				report_description = data['report_description']
				report_notes       = data['report_notes']

				
				text_to_print = '\n[+] File: %s\n [-] Hash value: %s\n [-] Status result value: %s\n [-] Report result value: %s\n [-] Report Description: %s\n [-] Report Notes: %s'%(path_to_folder + os.sep + file_name, file_hash, status_severity.encode('ascii','ignore'), report_severity.encode('ascii','ignore'), report_description.encode('ascii','ignore'), report_notes.encode('ascii','ignore'))
				text_to_log = '%s | %s | %s | %s | New analisys perform - %s\n'%(datetime.strftime(datetime.now(), '%Y/%m/%d %H:%M:%S'), path_to_folder + os.sep + file_name, file_hash, report_severity.encode('ascii','ignore'), report_description.encode('ascii','ignore'))
			# *********************************************************************************

		else: # File already white or blacklisted
			if data == 'w': # File whitelisted
				severity = 0
				report_severity = severity

				description = 'File previously Whitelisted'
				text_to_print = '\n[+] File: %s\n [-] Hash value: %s\n [-] Analisys result value: %s\n [-] Description: %s'%(path_to_folder + os.sep + file_name, file_hash, severity, description)
				text_to_log = '%s | %s | %s | %s | New analisys perform - %s\n'%(datetime.strftime(datetime.now(), '%Y/%m/%d %H:%M:%S'), path_to_folder + os.sep + file_name, file_hash, severity, description)

			elif data == 'b': # File Blacklisted
				severity = 5
				report_severity = severity

				description = 'File previously Blacklisted'
				text_to_print = '\n[+] File: %s\n [-] Hash value: %s\n [-] Analisys result value: %s\n [-] Description: %s'%(path_to_folder + os.sep + file_name, file_hash, severity, description)
				text_to_log = '%s | %s | %s | %s | New analisys perform - %s\n'%(datetime.strftime(datetime.now(), '%Y/%m/%d %H:%M:%S'), path_to_folder + os.sep + file_name, file_hash, severity, description)

		log_entry ('atd_log.log', text_to_print, text_to_log)


		# check if quarantine is set
		# *************************************************************************************
		value, error_info = quarantine_file(path_to_folder, q_path, file_name, report_severity )
		if not value:
			print error_info
		# *************************************************************************************

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
		control_error, error = insert_into_db(file_name, file_hash, report_severity)
		if not control_error:
			print error
		# Once we know that the analyze proces has ended the entry is remove from the global list so the master thread will not upload it again
		# unless the force of the delta parameter is on.
		if file_hash in mon_pending_files:
			mon_pending_files.remove(file_hash)
		semaphore.release()

		q.task_done()

def quarantine_file(actual_path, new_path, file_name, severity):
	
	'''
	Description: Quarantine a file 
	Input:       
		     	 actual_path: Actual location of the file
		     	 new_path   : New location of the file
		     	 severity   : Severity of the file according with ATD
	Output:      

			 	 This procedure only returns error control. Tuple of two values True or False and None or the error code
	'''
	global semaphore
	if int(severity) > 2 and new_path != None:
		new_path = new_path + os.sep + file_name
		actual_path = actual_path + os.sep + file_name

		if os.path.exists(new_path): # Check if the file exists
			try:
				if os.path.exists(new_path + '.old'): 
					os.remove(new_path + '.old')
				os.rename(new_path, new_path + ".old") # rename old file adding .old at the end of the file name
			except Exception as er:
				description = 'Error deleting or renaming existing file in quarantine: %s'%er
				return (False, er) # If something goes wrong the function returns a tuple with the value False and the error code
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

	'''
	Description: Insert file information into the local cache (Database)
	Input:       
		     	 fname 		: Name of the file to insert
		     	 file_hash  : Hash of the file to insert
		     	 severity   : Severity of the file according with ATD
	Output:      

			 	 This procedure only returns error control. Tuple of two values (True, 'Insert Done') or (False, error_description)
	'''

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
		cursor.execute('''SELECT * FROM FILES WHERE MD5 = ?''',(file_hash,))
	except Exception as er:
		er = 'Error querying Database - %s'%er
		return (False, er)
    	    
	value = None
	value = cursor.fetchone()
			
	if value: # Means that the record already exits, so we have to update the information
		try:
			cursor.execute('''UPDATE FILES SET LAST_DATE=?, FILENAME=?, FILE_SEVERITY=? WHERE MD5 = ?''', \
            	              (current_date_str, fname, int(severity), file_hash))
		except Exception as er:
			er = 'Error in UPDATE operation - %s'%er
			return (False, er)
	else:
		try:
			cursor.execute('''INSERT INTO FILES(MD5, LAST_DATE, FILENAME, FILE_SEVERITY) 
        	                  VALUES (?,?,?,?)''', \

            	              (file_hash, current_date_str, fname, int(severity)))
		except Exception as er:
			er =  'Error in INSERT operation - %s'%er
			return (False, er)

	try:
		conn.commit()
	except Exception as er:
		er =  'Error in COMMIT operation - %s'%er
		return (False, er)

	conn.close()
	return (True, 'Insert done')

def log_entry(log_file, text_to_print, text_to_log):

	'''
	Description: Procedure in charge of writing into the console or into the log file
	Input:       
		     	 log_file	    : Filename of the log to write the information into
		     	 text_to_print  : Text we want to output in the console
		     	 text_to_log    : Text we want to log into the log file
	Output:      

			 	 Nothing
	'''
	
	global semaphore

	semaphore.acquire()
	
	print text_to_print
	with open(log_file, "a") as mylogfile:
		mylogfile.write(text_to_log)
	
	semaphore.release()

def handler_signal(s, f):

	'''
	Description: Procedure that will be executed when the user press CTRL+C in monitor mode.
				 It forces the threads to finish and exit from the program
	Input:       
		     	 s: internal value of the function not used
		     	 f: internal value of the function not used
	Output:      

			 	 Nothing
	'''

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
			final_list = clean_list(list_of_files, options.q_path, options.force, options.delta, options.monitor) # clean the list

			if final_list: #If there are files to analyze
				# Read the final_list and put the values into the queue
				for i in range(len(final_list)):
					hash_value = final_list[i][0]
					file_name  = final_list[i][1]
					path       = final_list[i][2]

					if hash_value not in mon_pending_files:
						# When monitor mode is activated we need to inform to the master thread that we are waiting for the results
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
	