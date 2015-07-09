"""
MPA DATA PROPERTY MODIFIER
AUTHOR: YUHANG WANG
DATE: 07-06-2015
"""
#-------------------------------------------------
import matplotlib.pyplot
#-------------------------------------------------


def set_matrix_extent(object_matrix_plot, new_x_min, new_x_max, new_y_min, new_y_max):
	"""
	Set the plot extent when plotting a matrix 
	:param object object_matrix_plot: matplotlib "AxesImage" object
	:param float new_x_min: new x min 
	:param float new_x_max: new x max
	:param float new_y_min: new y min 
	:param float new_y_min: new y max 
	"""
	matplotlib.pyplot.setp(object_matrix_plot, extent=[new_x_min, new_x_max, new_y_min, new_y_max])