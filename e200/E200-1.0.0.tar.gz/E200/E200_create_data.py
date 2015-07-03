import h5py as h5
import warnings
import numpy as _np

import logging
logger = logging.getLogger(__name__)
loggerlevel = 9

__all__ = ['E200_create_data']
def E200_create_data(group_parent,group_name):
	# ======================================
	# Check if group name already exists
	# ======================================
	if group_name in group_parent.keys():
		logger.log(level=loggerlevel,msg='Data with name "{}" already exists.'.format(group_name))
		return group_parent[group_name]

	# ======================================
	# Create different kinds of groups
	# ======================================
	group_child = group_parent.create_group(group_name)
	group_child.create_dataset('UID',shape=(0,),maxshape=(None,),dtype=_np.int64)

	ref_dtype = h5.special_dtype(ref=h5.Reference)
	group_child.create_dataset('dat',shape=(0,),maxshape=(None,),dtype=ref_dtype)

	group_child.create_group('refs')

	return group_child
