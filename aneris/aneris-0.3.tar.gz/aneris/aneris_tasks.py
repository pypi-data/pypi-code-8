import curses
import curses.textpad
import datetime

from aneris_db_if import aneris_db_if

#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#

class aneris_tasks(object):
	
	def __init__(self, db_if, resources):
		self.m_db_if = db_if
		self.m_resources = resources
		self.m_tasks = db_if.read_task_data()
		self.m_tasks_visible = True
		self.m_task_cursor=0
		self.m_delete_armed=False

#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#
		
	def render(self, window, active):
		height, width = window.getmaxyx()

		window.clear()
		
		if(active == True):
			for y in range(0, height):
				window.addstr(y, 0, " ", curses.A_REVERSE|curses.color_pair(7))
			window.addstr(3, 1, ">>", curses.A_BOLD|curses.A_REVERSE|curses.color_pair(7))

		window.addstr(0, 2, "work list: {0}".format(str(datetime.date.today())), curses.A_BOLD|curses.color_pair(4))
		for x in range(0, len("work list: {0}".format(str(datetime.date.today())))):
			window.addstr(1, x+2, "=", curses.A_BOLD|curses.color_pair(4))
		
		y = 3
		cumulative_hours_remaining = 0
		for task_index in range(0, len(self.m_tasks)):
			if(y == height):
				break
				
			if(self.m_tasks[task_index]["is_a_project"] == True):
				project_hours_remaining = 0
				for task_jndex in range(task_index+1, len(self.m_tasks)):
					if(self.m_tasks[task_jndex]["is_a_project"] == True):
						break
					else:
						project_hours_remaining += self.m_tasks[task_jndex]["hours_work"]
				
				cumulative_hours_remaining += project_hours_remaining
				
				if(task_index >= self.m_task_cursor):
					project_completion_day = self.m_resources.hours_work_2_completion_day(cumulative_hours_remaining)
				
					if((self.m_delete_armed == True) and (y==3)):
						style=curses.A_BOLD|curses.A_REVERSE|curses.color_pair(5)
					else:
						if(project_completion_day > self.m_tasks[task_index]["deadline"]):
							style=curses.A_BOLD|curses.A_REVERSE|curses.color_pair(1)
						else:
							style=curses.A_BOLD|curses.A_REVERSE|curses.color_pair(2)
				
					if(project_completion_day > self.m_tasks[task_index]["deadline"]):
						window.addstr(y, 4, "{0:3d} h by {1} : exp. {2} : {3} :  ~ LATE! ".format( \
										project_hours_remaining, \
										str(self.m_tasks[task_index]["deadline"]),\
										str(project_completion_day), \
										self.m_tasks[task_index]["text"])[:width-4], style)
					else:
						window.addstr(y, 4, "{0:3d} h by {1} : exp. {2} : {3} :  ~ OK ".format( \
										project_hours_remaining, \
										str(self.m_tasks[task_index]["deadline"]),\
										str(project_completion_day), \
										self.m_tasks[task_index]["text"])[:width-4], style)
					y += 1
				
			else:
				if(task_index >= self.m_task_cursor):
					if((self.m_delete_armed == True) and (y==3)):
						style=curses.A_BOLD|curses.color_pair(5)
					else:
						style=curses.color_pair(7)
						
					if(self.m_tasks_visible == True):
						if((task_index == len(self.m_tasks)-1) or (self.m_tasks[task_index+1]["is_a_project"] == True)):
							window.addch(y, 4, curses.ACS_LLCORNER)
						else:
							window.addch(y, 4, curses.ACS_LTEE)
						window.addstr(y, 5, "{0:3d} h remaining : {1}".format(self.m_tasks[task_index]["hours_work"], self.m_tasks[task_index]["text"])[:width-5], style)
						y += 1

	def get_text(self, edit_window, prompt, init_text):
		height, width = edit_window.getmaxyx()
		edit_window.clear()
		edit_window.addstr(0, 0, ">>", curses.A_BOLD|curses.A_REVERSE|curses.color_pair(7))
		edit_window.addstr(0, 3, prompt, curses.A_BOLD|curses.color_pair(7))
		edit_window.refresh()

		curses.curs_set(1)

		textpad_window = curses.newwin(1, width-(len(prompt)+5), 1, (len(prompt)+5))
		textpad_window.clear()
		textpad_window.addstr(0, 0, init_text)
		new_text = curses.textpad.Textbox(textpad_window, insert_mode=True).edit().strip()
		del textpad_window

		curses.curs_set(0)

		edit_window.clear()
		return(new_text)

#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#

	def key_next_task(self):
		self.m_delete_armed=False
		if(self.m_task_cursor < len(self.m_tasks)):
			self.m_task_cursor += 1
			if(self.m_tasks_visible == False):
				while((self.m_task_cursor < len(self.m_tasks)) and (self.m_tasks[self.m_task_cursor]["is_a_project"] == False)):
					self.m_task_cursor += 1

	def key_previous_task(self):
		self.m_delete_armed=False
		if(self.m_task_cursor > 0):
			self.m_task_cursor -= 1
			if(self.m_tasks_visible == False):
				while((self.m_task_cursor > 0) and (self.m_tasks[self.m_task_cursor]["is_a_project"] == False)):
					self.m_task_cursor -= 1
				
	def key_toggle_task_visibility(self):
		self.m_delete_armed=False
		self.m_tasks_visible = not self.m_tasks_visible

#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#

	def key_increment(self):
		self.m_delete_armed=False
		if(self.m_task_cursor < len(self.m_tasks)):
			if(self.m_tasks[self.m_task_cursor]["is_a_project"] == False):
				self.m_tasks[self.m_task_cursor]["hours_work"] += 1
			else:
				project_indices = [ i for i, task in enumerate(self.m_tasks) if task["is_a_project"] == True ]
				project_index_cursor = project_indices.index(self.m_task_cursor)
				if(project_index_cursor > 0):
					project_indices.append(len(self.m_tasks))
				
					a=project_indices[project_index_cursor-1]
					b=project_indices[project_index_cursor]
					c=project_indices[project_index_cursor+1]
					
					self.m_tasks[b:c], self.m_tasks[a:a] = [], self.m_tasks[b:c]

	def key_decrement(self):
		self.m_delete_armed=False
		if(self.m_task_cursor < len(self.m_tasks)):
			if(self.m_tasks[self.m_task_cursor]["is_a_project"] == False):
				if(self.m_tasks[self.m_task_cursor]["hours_work"] > 0):
					self.m_tasks[self.m_task_cursor]["hours_work"] -= 1
			else:
				project_indices = [ i for i, task in enumerate(self.m_tasks) if task["is_a_project"] == True ]
				project_index_cursor = project_indices.index(self.m_task_cursor)
				if(project_index_cursor < len(project_indices)-1):
					project_indices.append(len(self.m_tasks))
					
					a=project_indices[project_index_cursor]
					b=project_indices[project_index_cursor+1]
					c=project_indices[project_index_cursor+2]
					
					self.m_tasks[b:c], self.m_tasks[a:a] = [], self.m_tasks[b:c]

#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#

	def key_add_project(self, edit_window):
		self.m_delete_armed=False
		self.m_tasks.insert(self.m_task_cursor, {})
		self.m_tasks[self.m_task_cursor]["text"] = ""
		self.m_tasks[self.m_task_cursor]["is_a_project"] = True
		self.m_tasks[self.m_task_cursor]["deadline"] = datetime.date.today()
		self.key_select(edit_window)
	
	def key_add_task(self, edit_window):
		if((self.m_task_cursor < len(self.m_tasks)) and (self.m_tasks[self.m_task_cursor]["is_a_project"] == True)):
			self.m_delete_armed=False
			self.m_task_cursor += 1

			self.m_tasks.insert(self.m_task_cursor, {})
			self.m_tasks[self.m_task_cursor]["text"] = ""
			self.m_tasks[self.m_task_cursor]["is_a_project"] = False
			self.m_tasks[self.m_task_cursor]["hours_work"] = 0
			self.key_select(edit_window)
			self.m_task_cursor -= 1
			
	def key_remove_task(self):
		if(self.m_task_cursor < len(self.m_tasks)):
			if((self.m_task_cursor > 0) or (len(self.m_tasks) == 1) or (self.m_tasks[self.m_task_cursor+1]["is_a_project"] == True)):
				if(self.m_delete_armed == False):
					self.m_delete_armed=True
				else:
					self.m_delete_armed=False
					del self.m_tasks[self.m_task_cursor]

#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#

	def key_select(self, edit_window):
		self.m_delete_armed=False
		
		if(self.m_tasks[self.m_task_cursor]["is_a_project"] == True):
			self.m_tasks[self.m_task_cursor]["text"] = self.get_text(edit_window, "project:", self.m_tasks[self.m_task_cursor]["text"])
			deadline_str=self.get_text(edit_window, "project deadline (yyyy-mm-dd):", str(self.m_tasks[self.m_task_cursor]["deadline"]))
			try:
				self.m_tasks[self.m_task_cursor]["deadline"] = datetime.datetime.strptime(deadline_str, "%Y-%m-%d").date()
			except ValueError:
				self.m_tasks[self.m_task_cursor]["deadline"] = datetime.date.today()
			
		else:
			self.m_tasks[self.m_task_cursor]["text"] = self.get_text(edit_window, "task:", self.m_tasks[self.m_task_cursor]["text"])
			hours_work_str=self.get_text(edit_window, "hours work:", str(self.m_tasks[self.m_task_cursor]["hours_work"]))
			try:
				self.m_tasks[self.m_task_cursor]["hours_work"] = int(hours_work_str)
			except ValueError:
				self.m_tasks[self.m_task_cursor]["hours_work"] = 0
		

#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#

	def save(self):
		self.m_db_if.write_task_data(self.m_tasks)

