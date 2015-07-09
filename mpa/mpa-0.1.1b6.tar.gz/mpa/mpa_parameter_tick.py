"""
MPA AXIS TICK PARAMETERS
AUTHOR: YUHANG WANG
DATE: 06-24-2015
"""

class TickParameters:
	"""
	Tick and its label parameters
	"""
	_convention_ = {
		"X TICK MAJOR MINOR OR BOTH":"x_tick_major_minor_or_both",
		"Y TICK MAJOR MINOR OR BOTH":"y_tick_major_minor_or_both",
		"X TICK IN OUT OR INOUT":"x_tick_in_out_or_inout",
		"Y TICK IN OUT OR INOUT":"y_tick_in_out_or_inout",
		"X TICK LENGTH":"x_tick_length",
		"Y TICK LENGTH":"y_tick_length",
		"X TICK WIDTH":"x_tick_width",
		"Y TICK WIDTH":"y_tick_width",
		"X TICK LABEL FONT SIZE":"x_tick_label_font_size",
		"Y TICK LABEL FONT SIZE":"y_tick_label_font_size",
		"X TICK LABEL FONT WEIGHT":"x_tick_label_font_weight",
		"Y TICK LABEL FONT WEIGHT":"y_tick_label_font_weight",
		"X TICK COLOR":"x_tick_color",
		"Y TICK COLOR":"y_tick_color",
		"X TICK LABEL COLOR":"x_tick_label_color",
		"Y TICK LABEL COLOR":"y_tick_label_color",
		"X TICK LABEL PADDING":"x_tick_label_padding",
		"Y TICK LABEL PADDING":"y_tick_label_padding",
		"X TICK AND LABEL Z ORDER":"x_tick_and_label_z_order",
		"Y TICK AND LABEL Z ORDER":"y_tick_and_label_z_order",
		"X TICK SHOW TOP":"x_tick_show_top",
		"X TICK SHOW BOTTOM":"x_tick_show_bottom",
		"Y TICK SHOW LEFT":"y_tick_show_left",
		"Y TICK SHOW RIGHT":"y_tick_show_right",		
		"X TICK LABEL SHOW TOP":"x_tick_label_show_top",
		"X TICK LABEL SHOW BOTTOM":"x_tick_label_show_bottom",
		"Y TICK LABEL SHOW LEFT":"y_tick_label_show_left",
		"Y TICK LABEL SHOW RIGHT":"y_tick_label_show_right",
		"X TICK LABEL NUMBER OF DECIMAL PLACES":"x_tick_label_number_of_decimal_places",
		"Y TICK LABEL NUMBER OF DECIMAL PLACES":"y_tick_label_number_of_decimal_places",
		"X TICK RESET OLD PARAMETER":"x_tick_reset_old_parameter",
		"Y TICK RESET OLD PARAMETER":"y_tick_reset_old_parameter",
		"X TICK LABEL HIDE OVERLAP":"x_tick_label_hide_overlap",
		"Y TICK LABEL HIDE OVERLAP":"y_tick_label_hide_overlap",
		"X TICK LABEL HIDE FIRST":"x_tick_label_hide_first",
		"Y TICK LABEL HIDE FIRST":"y_tick_label_hide_first",		
		"X TICK LABEL HIDE LAST":"x_tick_label_hide_last",
		"Y TICK LABEL HIDE LAST":"y_tick_label_hide_last",
		"X TICK USER DEFINED ON":"x_tick_user_defined_on",
		"Y TICK USER DEFINED ON":"y_tick_user_defined_on",
		"X NEW TICK ARRAY":"x_new_tick_array",
		"Y NEW TICK ARRAY":"y_new_tick_array",
		"X TICK LABEL USER DEFINED ON":"x_tick_label_user_defined_on",
		"Y TICK LABEL USER DEFINED ON":"y_tick_label_user_defined_on",
		"X NEW TICK LABEL ARRAY":"x_new_tick_label_array",
		"Y NEW TICK LABEL ARRAY":"y_new_tick_label_array",
		"X TICK LABEL ROTATION DEGREE":"x_tick_label_rotation_degree",
		"Y TICK LABEL ROTATION DEGREE":"y_tick_label_rotation_degree",
		}

	# Default parameters corresponding to entries in _convention_
	_user_default_ = {
		"x_tick_major_minor_or_both":"major",
		"y_tick_major_minor_or_both":"major",
		"x_tick_in_out_or_inout":"inout",
		"y_tick_in_out_or_inout":"inout",
		"x_tick_length":5,
		"y_tick_length":5,
		"x_tick_width":2,
		"y_tick_width":2,
		"x_tick_label_font_size":30,
		"y_tick_label_font_size":30,
		"x_tick_label_font_weight":0,
		"y_tick_label_font_weight":0,
		"x_tick_color":'k',
		"y_tick_color":'k',
		"x_tick_label_color":'k',
		"y_tick_label_color":'k',
		"x_tick_label_padding":10,
		"y_tick_label_padding":10,
		"x_tick_and_label_z_order":0,
		"y_tick_and_label_z_order":0,
		"x_tick_show_top":True,
		"x_tick_show_bottom":True,
		"y_tick_show_left":True,
		"y_tick_show_right":True,
		"x_tick_label_show_top":False,
		"x_tick_label_show_bottom":True,
		"y_tick_label_show_left":True,
		"y_tick_label_show_right":False,
		"x_tick_label_number_of_decimal_places":None,
		"y_tick_label_number_of_decimal_places":None,
		"x_tick_reset_old_parameter":False,
		"y_tick_reset_old_parameter":False,
		"x_tick_label_hide_overlap":False,
		"y_tick_label_hide_overlap":False,
		"x_tick_label_hide_first":0,
		"y_tick_label_hide_first":0,		
		"x_tick_label_hide_last":0,
		"y_tick_label_hide_last":0,
		"x_tick_label_user_defined_on":False,
		"y_tick_label_user_defined_on":False,
		"x_new_tick_label_array":None,
		"y_new_tick_label_array":None,
		"x_tick_user_defined_on":False,
		"y_tick_user_defined_on":False,
		"x_new_tick_array":None,
		"y_new_tick_array":None,
		"x_tick_label_rotation_degree":None,
		"y_tick_label_rotation_degree":None,
		}

	# The following additional defaults are only used internally
	# for the sake of symmetry between x and y parameters.
	# However they are not exposed to users, because
	# these parameters are meaningless.
	# For example, 'y' axis doesn't have ticks on the top.
	# This is useful since we can now use a for loop
	# to iterate all options for x and y axis uniformly.
	_internal_default_ = {
		"y_tick_show_top":False,
		"y_tick_show_bottom":False,
		"x_tick_show_left":False,
		"x_tick_show_right":False,
		"y_tick_label_show_top":False,
		"y_tick_label_show_bottom":False,
		"x_tick_label_show_left":False,
		"x_tick_label_show_right":False,
		}

	## Now merge the two default dictionaries
	_defaults_ = _user_default_.copy()
	_defaults_.update(_internal_default_)

	@staticmethod
	def get_convention():
		"""
		Get the convention dictionary
		"""
		return TickParameters._convention_

	@staticmethod
	def get_default():
		"""
		Get the default value dictionary
		"""
		return TickParameters._defaults_.copy()	

	@staticmethod
	def get_description():
		"""
		Description of this class 
		"""
		return "TICK PARAMETERS"
