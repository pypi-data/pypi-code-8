#!/usr/bin/python3

import time
import curses
import datetime

from aneris_tasks import aneris_tasks
from aneris_resources import aneris_resources
from aneris_db_if import aneris_db_if

#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#

def main_ui(stdscr):

	curses.init_pair(1, curses.COLOR_RED, curses.COLOR_BLACK)
	curses.init_pair(2, curses.COLOR_GREEN, curses.COLOR_BLACK)
	curses.init_pair(3, curses.COLOR_YELLOW, curses.COLOR_BLACK)
	curses.init_pair(4, curses.COLOR_BLUE, curses.COLOR_BLACK)
	curses.init_pair(5, curses.COLOR_MAGENTA, curses.COLOR_BLACK)
	curses.init_pair(6, curses.COLOR_CYAN, curses.COLOR_BLACK)
	curses.init_pair(7, curses.COLOR_WHITE, curses.COLOR_BLACK)
	
	curses.curs_set(0)

	db_if=aneris_db_if()
	resources=aneris_resources(db_if)
	tasks=aneris_tasks(db_if, resources)
	
	tasks_window_active = True
	resources_window_active = False

	while True:

		#paint screen
		try:
			stdscr.clear()
			height, width = stdscr.getmaxyx()

			edit_window = curses.newwin(1, width-2, 1, 1)
			tasks_window = curses.newwin((height-5)>>1, width-2, 3, 1)
			resources_window = curses.newwin((height-5)>>1, width-2, ((height-5)>>1)+4, 1)
			
			tasks.render(tasks_window, tasks_window_active)
			resources.render(resources_window, resources_window_active)
			
			stdscr.refresh()
			tasks_window.refresh()
			resources_window.refresh()
		except curses.error:
			pass
		
		#catch key input
		key=stdscr.getch()

		if key == curses.KEY_UP:
			if(tasks_window_active == True):
				tasks.key_previous_task()
			if(resources_window_active == True):
				resources.key_previous_day()
		elif key == curses.KEY_DOWN:
			if(tasks_window_active == True):
				tasks.key_next_task()
			if(resources_window_active == True):
				resources.key_next_day()

		elif key == curses.KEY_LEFT or key == ord('q'):
			break

		elif key == curses.KEY_RIGHT or key == ord('\n'):
			if(tasks_window_active == True):
				tasks.key_select(edit_window)

		elif key == ord('+'):
			if(tasks_window_active == True):
				tasks.key_increment()
			if(resources_window_active == True):
				resources.key_increment()
				
		elif key == ord('-'):
			if(tasks_window_active == True):
				tasks.key_decrement()
			if(resources_window_active == True):
				resources.key_decrement()

		elif key == ord(' '):
			if(tasks_window_active == True):
				tasks.key_toggle_task_visibility()
			if(resources_window_active == True):
				resources.key_next_worker()

		elif key == ord('a'):
			if(tasks_window_active == True):
				tasks.key_add_task(edit_window)
		elif key == ord('A'):
			if(tasks_window_active == True):
				tasks.key_add_project(edit_window)
		elif key == ord('r') or key == curses.KEY_BACKSPACE:
			if(tasks_window_active == True):
				tasks.key_remove_task()

		elif key == ord('\t'):
			tasks_window_active = not tasks_window_active
			resources_window_active = not resources_window_active

		elif key == ord('s'):
			try:
				edit_window.clear()
				edit_window.addstr(0, 0, "saved at {0}".format(datetime.datetime.now()), curses.color_pair(2))
				edit_window.refresh()
			except curses.error:
				pass
			tasks.save()
			resources.save()
			time.sleep(1)

		elif key == ord('h') or key == ord('?'):
			try:
				stdscr.clear()
				stdscr.addstr(1, 1, "aneris usage:", curses.A_BOLD|curses.color_pair(5))
				stdscr.addstr(2, 1, "=============", curses.A_BOLD|curses.color_pair(5))

				stdscr.addstr(4, 1, "tab          : toggle active panel", curses.A_BOLD|curses.color_pair(5))

				stdscr.addstr(6, 1, "cursor up    : previous task/day", curses.A_BOLD|curses.color_pair(5))
				stdscr.addstr(7, 1, "cursor down  : next task/day", curses.A_BOLD|curses.color_pair(5))
				stdscr.addstr(8, 1, "cursor left  : exit tp", curses.A_BOLD|curses.color_pair(5))
				stdscr.addstr(9, 1, "cursor right : edit project/task", curses.A_BOLD|curses.color_pair(5))

				stdscr.addstr(11, 1, "space        : toggle task visibility/next worker", curses.A_BOLD|curses.color_pair(5))

				stdscr.addstr(13, 1, "+            : increment project priority/task hours/hours committed", curses.A_BOLD|curses.color_pair(5))
				stdscr.addstr(14, 1, "-            : decrement project priority/task hours/hours committed", curses.A_BOLD|curses.color_pair(5))

				if(height > 20):
					stdscr.addstr(16, 1, "A            : add project", curses.A_BOLD|curses.color_pair(5))
					stdscr.addstr(17, 1, "a            : add task", curses.A_BOLD|curses.color_pair(5))
					stdscr.addstr(18, 1, "r            : remove project/task", curses.A_BOLD|curses.color_pair(5))

					stdscr.addstr(20, 1, "s            : save data", curses.A_BOLD|curses.color_pair(5))
				key=stdscr.getch()
			except curses.error:
				pass

		del edit_window
		del tasks_window
		del resources_window

	try:
		edit_window.clear()
		edit_window.addstr(0, 0, "saved at {0}".format(datetime.datetime.now()), curses.color_pair(2))
		edit_window.refresh()
	except curses.error:
		pass
	tasks.save()
	resources.save()
	time.sleep(1)

#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#
			
curses.wrapper(main_ui)

