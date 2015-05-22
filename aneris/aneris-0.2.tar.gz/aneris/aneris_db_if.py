import os.path
import pickle

#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#

class aneris_db_if(object):
	
	task_data_file_name = os.path.expanduser("~")+"/.aneris_task_data.p"
	worker_calendar_exception_data_file_name = os.path.expanduser("~")+"/.aneris_worker_calendar_exception_data.p"

#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#

	def write_task_data(self, task_data):
		with open(self.task_data_file_name, "wb") as task_data_write_fp:
			pickle.dump(task_data, task_data_write_fp)
			
	def read_task_data(self):
		if(os.path.exists(self.task_data_file_name) == True):
			with open(self.task_data_file_name, "rb") as task_data_read_fp:
				task_data = pickle.load(task_data_read_fp)
		else:
			task_data = []

		return(task_data)

#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#
		
	def write_worker_calendar_exception_data(self, worker_calendar_exception_data):
		with open(self.worker_calendar_exception_data_file_name, "wb") as worker_calendar_exception_data_write_fp:
			pickle.dump(worker_calendar_exception_data, worker_calendar_exception_data_write_fp)

			
	def read_worker_calendar_exception_data(self):
		if(os.path.exists(self.worker_calendar_exception_data_file_name) == True):
			with open(self.worker_calendar_exception_data_file_name, "rb") as worker_calendar_exception_data_read_fp:
				worker_calendar_exception_data = pickle.load(worker_calendar_exception_data_read_fp)
		else:
			worker_calendar_exception_data = {}
			
		return(worker_calendar_exception_data)
		
