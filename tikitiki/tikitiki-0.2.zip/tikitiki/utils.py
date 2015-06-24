try:
	import Tkinter as tk
except:
	import tkinter as tk
import types

'''
enables/disables the state of a widget and its child widgets 
'''
def set_widget_state(widget, state='disabled'):
	try:
		if state in widget.configure().keys():
			widget.configure(state=state)
	except tk.TclError as t:
		print('tcl error, is passed state valid: %s' % state)
	for child in widget.winfo_children():
		set_widget_state(child, state=state)

'''
cascades binding from root widget down through it's children. 
Useful for custom compound widgets.
Do not use for app-wide shortcuts - use the top level Tk() object
which cascades automatically.

TODO: support functions in the arguments
'''
def set_binding(widget, key, widget_function, *func_args):
	# check if arg is a method, then replace it with it's return value
	new_args = []
	for arg in func_args:
		if type(arg) == types.MethodType:
			print(arg)
			new_args += [lambda: arg()]
		else:
			print(arg)
			new_args += [arg]
	widget.bind( key, lambda e: widget_function(*new_args))
	for child in widget.winfo_children():
		set_binding_child(widget, child, key, widget_function, *new_args)

def set_binding_child(parent, widget, key, function, *func_args):
	widget.bind(key, lambda e: function(*func_args))
	for child in widget.winfo_children():
		set_binding_child(parent, child, key, function, *func_args)

'''
by default the return key is not associated with firing off a button 
widget's command so to remove the need to set this twice here is a
helper method
'''
def set_button_action(button_widget, command, *func_args):
	button_widget.bind('<Return>', lambda e: command(*func_args))
	button_widget.configure(command= lambda: command(*func_args))

'''
sorts tab order of supplied widget list in ascending/descending
'''
def set_tab_order(widget_list, descending=True):
	# buggy... Not sure if need to work through all frames lifting/lowering too...
	if descending:
		widget_list = widget_list[::-1]
	for i, widget in enumerate(widget_list):
		if i==len(widget_list)-1:
			widget_list[i].focus_force()
		else:
			widget.lift()


