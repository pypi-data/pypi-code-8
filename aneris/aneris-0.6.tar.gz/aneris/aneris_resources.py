import datetime
import curses

from aneris.aneris_workers import workers, work_days

#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#

class aneris_resources(object):

	def __init__(self, db_if):
		self.m_db_if = db_if
		self.m_worker_calendar_exceptions = db_if.read_worker_calendar_exception_data()
		self.m_worker_cursor_index = 0
		self.m_worker_cursor = list(workers.keys())[self.m_worker_cursor_index]
		self.m_day_cursor = datetime.date.today()
		
#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#

	def render(self, window, active):
		height, width = window.getmaxyx()

		window.clear()
		
		if(active == True):
			for y in range(0, height):
				window.addstr(y, 0, " ", curses.A_REVERSE|curses.color_pair(7))
			window.addstr(3, 1, ">>", curses.A_BOLD|curses.A_REVERSE|curses.color_pair(7))

		window.addstr(0, 2, "worker: {0}".format(self.m_worker_cursor), curses.A_BOLD|curses.color_pair(3))
		for x in range(0, len("worker: {0}".format(self.m_worker_cursor))):
			window.addstr(1, x+2, "=", curses.A_BOLD|curses.color_pair(3))

		y=3
		for i in range(0, height-3):
			day = self.m_day_cursor+datetime.timedelta(days=i)
			week_day = work_days[day.weekday()]
			if(day.weekday() in range(5, 7)):
				window.addstr(y, 4, "{0}\t {1}: {2} hours".format(week_day, day, self.get_committed_hours(self.m_worker_cursor, day)), curses.A_BOLD|curses.color_pair(4))
			else:
				window.addstr(y, 4, "{0}\t {1}: {2} hours".format(week_day, day, self.get_committed_hours(self.m_worker_cursor, day)), curses.color_pair(3))
			y += 1
			
#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#

	def key_next_worker(self):
		self.m_worker_cursor_index += 1
		if(self.m_worker_cursor_index == len(workers)):
			self.m_worker_cursor_index = 0
		self.m_worker_cursor = list(workers.keys())[self.m_worker_cursor_index]

	def key_next_day(self):
		self.m_day_cursor += datetime.timedelta(days=1)
		
	def key_previous_day(self):
		if(self.m_day_cursor > datetime.date.today()):
			self.m_day_cursor -= datetime.timedelta(days=1)

	def key_increment(self):
		self.m_worker_calendar_exceptions[self.m_day_cursor][self.m_worker_cursor] = self.get_worker_calendar_exception(self.m_worker_cursor, self.m_day_cursor)+1

	def key_decrement(self):
		self.m_worker_calendar_exceptions[self.m_day_cursor][self.m_worker_cursor] = self.get_worker_calendar_exception(self.m_worker_cursor, self.m_day_cursor)-1

#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#
	
	def get_worker_calendar_exception(self, worker, day):
		if((day in self.m_worker_calendar_exceptions) == False):
			self.m_worker_calendar_exceptions[day] = {}
			
		if((worker in self.m_worker_calendar_exceptions[day]) == False):
			self.m_worker_calendar_exceptions[day][worker] = self.get_default_committed_hours(worker, day)

		return(self.m_worker_calendar_exceptions[day][worker])

	def get_default_committed_hours(self, worker, day):
		week_day = work_days[day.weekday()]
		week_number = ((day-workers[worker]["default_committed_hours_start_date"]).days//7)
		
		if((week_day in workers[worker]["default_committed_hours"]) == True):
			default_committed_hours = workers[worker]["default_committed_hours"][week_day][week_number%len(workers[worker]["default_committed_hours"][week_day])]
		else:
			default_committed_hours = 0
			
		return(default_committed_hours)

	def get_committed_hours(self, worker, day):
		committed_hours = self.get_default_committed_hours(worker, day)
		
		if((day in self.m_worker_calendar_exceptions) == True):
			if((worker in self.m_worker_calendar_exceptions[day]) == True):
				committed_hours = self.m_worker_calendar_exceptions[day][worker]

		return(committed_hours)

	def hours_work_2_completion_day(self, hours_work):
		day=datetime.date.today()
		
		while(hours_work > 0):
			day += datetime.timedelta(days=1)
		
			for worker in workers:
				hours_work -= self.get_committed_hours(worker, day)
		
		return(day)
		
#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#

	def save(self):
		for day in list(self.m_worker_calendar_exceptions.keys()):
			if(day<datetime.date.today()):
				del self.m_worker_calendar_exceptions[day]

		self.m_db_if.write_worker_calendar_exception_data(self.m_worker_calendar_exceptions)
