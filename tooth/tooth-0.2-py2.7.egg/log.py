__author__ = 'Tom James Holub'


import sys
import pprint
import traceback
import string
import os
import datetime
import json
import thread
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from .config import Config


config = Config()
ACCESSDIR = config.get('path', 'access')
ERRORDIR = config.get('path', 'error')
EXCEPTIONDIR = config.get('path', 'exception')
SLASH = '/' if config.get('environment', 'os') == 'unix' else '\\'
DEBUG_EMAIL_FAILED = ERRORDIR + "DEBUG_EMAIL_FAILED"
MAX_SIMILAR_ERRORS_SAVED = 50


def access(identifiers, function, request, response, source='REQUEST'):

	if "success" in response.keys():
		filename = "anonymous" if not identifiers else '_'.join(map(str, identifiers))
		filepath = "%s%s.log" % (ACCESSDIR, filename)
	else:
		filepath = "%s%s.log" % (ERRORDIR, 'error')

	with open(filepath, "a") as myfile:
		try:
			json_request = json.dumps(request)
		except TypeError:
			json_request = "not serializabke, keys: %s" % (','.join(request.keys()))

		myfile.write("[%s %s] %s ---------- %s\n" % (source, function, json.dumps(response), json_request))


def format_directory_name(unformatted):
	valid_chars = "-_.() %s%s" % (string.ascii_letters, string.digits)
	sanitized = ''.join(c for c in unformatted if c in valid_chars)
	return 'E_' + sanitized.replace(' ', '_')[:100] + SLASH


def exception(dump=[], stdout=''):
	content = [
		'############################################',
		'# Stack Trace ##############################',
		'############################################',
		''
	]
	exc_type, exc_value, exc_traceback = sys.exc_info()
	if exc_type is None:
		return None

	try:
		if type(dump) == list:
			dump.append(exc_value.data)
		elif type(dump) == dict:
			dump['exception'] = exc_value.data
		elif dump is None:
			dump = {'exception': exc_value.data}
	except AttributeError:
		pass
	content += traceback.format_exception(exc_type, exc_value, exc_traceback)
	content += ['', '#############', '# Data ######', '#############', '']
	content += [pprint.pformat(dump)]
	content += ['', '', '#############', '# Stdout ####', '#############', '']
	content += [str(stdout)]

	exception_log_dir = format_directory_name(str(exc_type.__name__) + '___' + str(exc_value))

	if not os.path.exists(EXCEPTIONDIR + exception_log_dir):
		os.makedirs(EXCEPTIONDIR + exception_log_dir)
		if not config.get('environment', 'debug', bool):
			send_email_notification('New unhandled exception (' + str(exc_type.__name__) + ': ' + str(exc_value)[:100] + ')', content)

	do_save = len(os.listdir(EXCEPTIONDIR + exception_log_dir)) < MAX_SIMILAR_ERRORS_SAVED
	now = datetime.datetime.now()
	file_name = now.strftime("exception_%Y-%m-%d_%H-%M-%S-") + str(now.microsecond).zfill(6) + ".log"
	if do_save:
		sys.stderr.write("!!! Exception -> " + exception_log_dir + file_name + "\n")
		with open(EXCEPTIONDIR + exception_log_dir + file_name, "w") as myfile:
			myfile.write("\n".join(content))
	else:
		sys.stderr.write("!!! Exception (not saved, above 50) -> " + exception_log_dir + "\n")

	return exception_log_dir + file_name


def send_email_notification(subject, body):
	send_through_gmail(subject, "<br/>".join(body).replace(' ', '&nbsp;').replace('\n', '<br/>'))


def set_debug_email_failed_flag(exception=None):
	try:
		with open(DEBUG_EMAIL_FAILED, "w") as myfile:
			myfile.write(str(exception))
	except Exception, err:
		print exception
		print err


def send_through_gmail(subject, body):
	try:
		smtpserver = smtplib.SMTP("smtp.gmail.com", 587)
		smtpserver.ehlo()
		smtpserver.starttls()
		smtpserver.login(config.get('gmail', 'email'), config.get('gmail', 'password'))
		email_message_html = body
		msg = MIMEMultipart('alternative')
		msg['Subject'] = subject
		msg['From'] = "Vincent Python <%s>" % config.get('gmail', 'email')
		msg['To'] = "%s <%s>" % ('awesome hackers', config.get('environment', 'debug_email'))
		# Record the MIME types of both parts - text/plain and text/html.
		part1 = MIMEText(email_message_html, 'plain')
		part2 = MIMEText(email_message_html, 'html')
		msg.attach(part1)
		msg.attach(part2)
		smtpserver.sendmail(msg['From'], msg['To'], msg.as_string())
		smtpserver.close()
	# except (smtplib.SMTPAuthenticationError, smtplib.SMTPConnectError, socket.gaierror), err:
	# 	set_debug_email_failed_flag(failed=True, exception=err)
	except Exception, err:
		set_debug_email_failed_flag(exception=err)


class ThreadStdout:

	def __init__(self):
		self.thread_specific_outputs = {}
		self.MAIN_THREAD = thread.get_ident()

	def write(self, value):
		if thread.get_ident() != self.MAIN_THREAD:  # put all children threads stdouts into a separate storage
			if thread.get_ident() not in self.thread_specific_outputs:
				self.thread_specific_outputs[thread.get_ident()] = value
			else:
				self.thread_specific_outputs[thread.get_ident()] += value
		else:  # print all main thread stdouts the normal way
			sys.__stdout__.write(value)

	def flush(self):
		sys.__stdout__.flush()

	def clean(self):
		if thread.get_ident() in self.thread_specific_outputs:
			del self.thread_specific_outputs[thread.get_ident()]

	def get(self):
		return self.thread_specific_outputs[thread.get_ident()]
