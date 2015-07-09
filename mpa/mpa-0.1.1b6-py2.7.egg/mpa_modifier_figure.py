"""
MPA FIGURE MODIFIER
AUTHOR: YUHANG WANG
DATE: 06-24-2015
"""


def add_title(object_axis, figure_title, title_font_size):
	"""
	Add figure title 
	:param object_axis: matplotlib Axis object
	:param figure_title: title 
	:param title_font_size: font size 
	"""
	object_axis.set_title(figure_title, fontsize=title_font_size)
