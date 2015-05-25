#!/usr/bin/python
# -*- coding: utf-8 -*-
#-------------------------------------------------------------------------------
# Name:        atd
# Purpose:     Use of the ATD API 
#
# Author:      Carlos Munoz (carlos_munoz@mcafee.com)
#-------------------------------------------------------------------------------
#
#-------------------------------------------------------------------------------
# Version: V1.0
# Release control:
#                02/10/2014 - First release
#                29/08/2014 - Small modification to support last version of ATD
#				 22/04/2015 - Added functionality to support multiple VM Profiles
#							  the parameter -vm is added. This parameter must be
#							  follow by the identificator of the VM. in order to
#							  get de id, use chrome to upload manually a file and
#							  using the developer tools check the post message
#							  in the post message the identificator of the vm 
#							  appear.
#				 17/05/2015 - By default vmProfileId is now None, when no value
#							  is passed as parameter the header doesn't include
#							  the parameter so the default vm profile assigned
#							  during the creation of the user is used.
#							  If the parameter is passed the the system will 
#							  the profile indicated
#				 25/05/2014 - The class is now able to handle non ascii characters
#							  included on the file naem
#
# Created:     15/05/2015
# Copyright:   (c) Carlos M 2015
#-------------------------------------------------------------------------------

import requests
import json

requests.packages.urllib3.disable_warnings()

class atd():

	def __init__(self,atdserver):
		'''
		Description: Constructor
		Input:       IP address of ATD Server
		Output:      No Output
		'''
		self.atdserver  = atdserver
		self.session	= ''
		self.userId     = ''
		self.matdver	= ''

		self.sessionhdr = {}
		
	def connect(self, user, password):
		'''
		Description: Connection method, stablish a connection to the ATD server and populates all 
			     self variables of the constructor
		Input:       User and password
		Output:      Two possible values: 
			     (0, error_info): Unsucessful connection, error_info contain the cause of the error
			     (1, 'Connection sucessful): Sucessful connection
		'''
		authheader = {
				'Accept': 'application/vnd.ve.v1.0+json',
				'Content-Type': 'application/json',
				'VE-SDK-API': '%s'%self.b64(user,password)
			     }

		url = 'https://%s/php/session.php'%self.atdserver

		try:
			r = requests.get(url, headers = authheader, verify=False)	
		except Exception as e:
			error_info = 'Error connecting to ATD:\n %s'%e
			return (0, error_info)

		if r.status_code == 200:
			server_info = json.loads(r.content)
			if server_info['success'] == True:
				self.session = server_info['results']['session']
				self.userId  = server_info['results']['userId']
				self.matdver = server_info['results']['matdVersion']
				self.sessionhdr = {
				  'Accept': 'application/vnd.ve.v1.0+json',
				  'Content-Type': 'application/json',
				  'VE-SDK-API': '%s'%self.b64(self.session, self.userId)
			         }
			else:
				error_info = 'Connection unsucessful'
				return (0, error_info)
		else:
			error_info = 'Error conecting to ATD, Status Code: %d'%r.status_code
			return(0, error_info)
		
		return(1, 'Connection sucessful')
		
	def disconnect(self):
		'''
		Description: Disconnection method.
		Input:       No input
		Output:      Two possible values: 
			     (0, error_info): Unsucessful disconnection, error_info contain the cause of the error
			     (1, 'Disconnection sucessful): Sucessful disconnection
		'''	
		url = 'https://%s/php/session.php'%self.atdserver
		
		try:
			r = requests.delete(url, headers = self.sessionhdr, verify=False)
		except Exception as e:
			error_info = 'Error disconnecting from ATD:\n %s'%e
			return (0, error_info)
		if r.status_code == 200:
			server_info = json.loads(r.content)

			if server_info['success'] == True:
				return(1,'Disconnection successful')
			else:
				error_info = 'Error disconecting from ATD - Check credentials or content type header'
				return(0, error_info)
		else:
			error_info = 'Error disconnection from ATD, Status Code: %d'%r.status_code
			return(0, error_info)

	def heartbeat(self):
		'''
		Description: Hearbeat value
		Input:       No input
		Output:      Two possible values: 
			     (0, error_info): Error getting heartbeat value
			     (1, heartbeat_value): Heartbeat value
		'''	
		url = 'https://%s/php/heartbeat.php'%self.atdserver

		try:
			r = requests.get(url, headers = self.sessionhdr, verify=False)
		except Exception as e:
			error_info = 'Error getting heartbeat:\n%s'%e
			return(0, error_info)

		if r.status_code == 200:
			server_info = json.loads(r.content)

			if server_info['success'] == True:
				return (1, server_info['results']['heartBeat'])

			else:
				error_info = 'Error getting heartbeat, check credentials or content type header'
				return (0, error_info)
		else:
			error_info = 'Error getting heartbeat, status code: %d'%r.status_code
			return (0, error_info)

	def force_decode(self, string, codecs=['utf8', 'cp1252','ascii']):
		'''
		Description: Internal function that receives a string and try to decode it using different codecs
		Input:       
			     string: String to decode
			     codecs: List of possible codecs

		Output:      Two possible values: 

			     (0, 'codecs not valid'): The funciton is not able to find the coded used to coded the string
			     (1, string_decoded): Tuple with a positive value and the decoded string
		'''
		for i in codecs:
			try:
				return (1, string.decode(i))
			except:
				pass
		return (0, 'codecs not valid')

	def upload_file(self, filetosubmit, vmProfileList=None, numVmProfiles=1, overrideOS=0):
		'''
		Description: Upload procedure, uploads a file to the ATD server for inspection
		Input:       
			     filetosubmit:  Path to the file to be submitted
			     vmProfileList: ATD Profile ID for inspection
			     numVMProfiles: Value not used in this version (3.60.XX)
 			     overrideOS:    Value not used in this version (3.60.XX)

		Output:      Two possible values: 

			     (0, error_info): Unsucessful procedure
			     (1, {'jobID':'xxx','taskId':'xxx','file':'xxx','md5':'xxx','size':'xxx':'mimeType':'xxx'}): Sucessful upload
		'''
		'''
		Notes: The documentation is not clear (at least in my opinion), about how to build this method
		I finally used Chrome inspector to understand the header and information sent to the ATD server
		when manually upload a file for inspection.
		vmProfileList is the ID of the profile to be used for inspection, however in my tests always
		the default profile associated to the user is the one used, I have not been able to change the
		profile.
		'''		
		url = 'https://%s/php/fileupload.php'%self.atdserver

		if vmProfileList:
			postdata = {'data':'{"data":{"overrideOS": "%d","vmProfileList":"%s","numVmProfiles":"%s"}}'%(overrideOS,vmProfileList,numVmProfiles)}
		else:
			postdata = {'data':'{"data":{"overrideOS": "%d","numVmProfiles":"%s"}}'%(overrideOS,numVmProfiles)}

		# According with changes on 25 of May, now the system is able to decode files with non ascii characters ************************************
		value, data = self.force_decode(self.get_filename(filetosubmit)) # This call returns an unicode (not coded) string for further manipulation
		if value:
			datatosubmit = data.encode('ascii','replace') # This function replace non ascci characters used on the name of the file
		# ******************************************************************************************************************************************

		try:
			files = {'amas_filename': (datatosubmit, open(filetosubmit, 'rb'))} # The ATD upload header expects the amas_file name in ascci
		except Exception as e:
			error_info = 'Upload method: Error opening file: %s'%e
			return(0, error_info)			

		custom_header = {
			 'Accept': 'application/vnd.ve.v1.0+json',
			 'VE-SDK-API': '%s'%self.b64(self.session, self.userId)
			 }
		
		try:
			r = requests.post(url, postdata, headers = custom_header, files=files, verify=False)

		except Exception as e:
			error_info = 'Error submitting file to ATD:\n%s'%e
			return(0, error_info)

		if r.status_code == 200:
			server_info = json.loads(r.content)
			if server_info['success'] == True:	
				info = {
					'jobId'   : server_info['subId'],
					'taskId'  : server_info['results'][0]['taskId'],
					'file'    : server_info['results'][0]['file'],
					'md5'     : server_info['results'][0]['md5'],
					'size'    : server_info['results'][0]['size'],
					'mimeType': server_info['mimeType']
					}
				return (1,info)	
			else:
				error_info = 'Upload operation did not return a success value'
				return (0,error_info)
		else:
			error_info = 'Error uploading file, bad credentials or header - status code: %d'%r.status_code
			return (0, error_info)

	def check_status(self, taskId):
		'''
		Description: Check the status of the uploded file to the ATD server for inspection
		Input:       
			     taskId:  ID of the task identifying the inspection operation
		Output:      Possible values: 

			     (0, error_info): Unsucessful procedure
			     (4, 'Sample waiting to be analyzed')
			     (3, 'Sample being analyzed')
			     (-1, 'Analysis failed')

			     (1, {'jobid': 'xxx', 'taskid':'xxx', 'filename':'xxx', 'md5':'xxx','submitTime': 'xxx',
			     'vmProfile':'xxx','vmName':'xxx','vmDesc':'xxx','summaryFiles':'xxx', 'useLogs':'xxx',
			     'asmListing':'xxx','PEInfo':'xxx', 'family':'xxx'})
	
			     (2, {'jobid': 'xxx', 'taskid':'xxx', 'filename':'xxx', 'md5':'xxx','submitTime': 'xxx',
			     'vmProfile':'xxx','vmName':'xxx','vmDesc':'xxx','summaryFiles':'xxx', 'useLogs':'xxx',
			     'asmListing':'xxx','PEInfo':'xxx', 'family':'xxx'})
		'''
		url = 'https://%s/php/samplestatus.php'%self.atdserver

		payload = {'iTaskId':taskId}

		try:
			r = requests.get(url, params=payload, headers=self.sessionhdr, verify=False)
		except Exception as e:
			error_info = 'Can not get status of taskId: %d,\nReturned error: %s '%(taskId,e) 
			return (0, error_info)

		if r.status_code == 200:
			server_info = json.loads(r.content)
			if server_info['success'] == True:
				status = server_info['results']['istate']

				if status == 4: # Sample waiting in the queue to be analyzed
					return (4, 'Sample waiting to be analyzed')
				elif status == 3: # Sample being analyzed
					return (3, 'Sample being analyzed')
				elif status == -1: # Sample failed to be analyzed
					return (-1, 'Analysis failed')
				elif status == 1 or status == 2: # Sample correctly analyzed
					info = {
						'jobid'        : server_info['results']['jobid'],
						'taskid'       : server_info['results']['taskid'],
						'filename'     : server_info['results']['filename'],
						'md5'          : server_info['results']['md5'],
						'submitTime'   : server_info['results']['submitTime'],
						'vmProfile'    : server_info['results']['vmProfile'],
						'vmName'       : server_info['results']['vmName'],
						'vmDesc'       : server_info['results']['vmDesc'],
						'summaryFiles' : server_info['results']['summaryFiles'],
						'useLogs'      : server_info['results']['useLogs'],
						'asmListing'   : server_info['results']['asmListing'],
						'PEInfo'       : server_info['results']['PEInfo'],
						'family'       : server_info['results']['family']
					       }
					return (status, info)
				else:
					error_info = 'Unknown error checking status of taskId: %d'%taskId	
					return (0, error_info)
			else:
				error_info = 'Check status operation did not return a success value'
				return (0,error_info)
		else:
			error_info = 'Error checking status, bad credentials or header - status code: %d'%r.status_code
			return (0, error_info)

	def get_report(self, jobId):
		'''
		Description: Get the final result of the inspection of the sample submitted
		Input:       jobId, identification of the job
		Output:      Possible values: 

			     (0, error_info): Unsucessful procedure
			     (2, 'Result is not ready')
			     (3, 'Report not found, Ex. file not supported')
			     (1, {}): The dic includes all the json report
		'''
	
		url = 'https://%s/php/showreport.php'%self.atdserver

		payload = {'jobId':jobId, 'iType':'json'}

		custom_header = {
			        'Accept': 'application/vnd.ve.v1.0+json',
			        'VE-SDK-API': '%s'%self.b64(self.session, self.userId)
			        }
	
		try:
			r = requests.get(url, params=payload, headers=custom_header, verify=False)
		except Exception as e:
			error_info = 'Can not get report of jobId: %d,\nReturned error: %s '%(jobId,e) 
			return (0, error_info)

		if r.status_code == 400:
			info = 'Inspection not yet finished'
			return(2, info)

		if r.content.split('\n')[0] == 'Result is not ready':
			info = 'Result is not ready'
			return (2, info)
		else:
			if 'report file not found' in r.content.lower():
				server_info = 'Report not found - Ex. file not supported'
				return (3, server_info)
			else:
				server_info = json.loads(r.content)
				return (1, server_info)

	def b64(self, user, password):
		'''
		Description: Internal procedure to get the base64 values used for authentication
		Input:       user and password
		Output:      base64('user:pass'): The dic includes all the json report
		'''
		import base64
		auth_string = user + ':' + password
		return base64.b64encode(auth_string)

	def get_filename(self, filetosubmit):
		'''
		Description: Internal procedure to get the clean filename
		Input:       path to file
		Output:      clean filename
		'''
	
		if filetosubmit.find('/') != -1:
			file = filetosubmit.split('/')[-1]
		else:
			if filetosubmit.find('\\') != -1:
				file = filetosubmit.split('\\')[-1]
			else:
				file = filetosubmit
		return file	

