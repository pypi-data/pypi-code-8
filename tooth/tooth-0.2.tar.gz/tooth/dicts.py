__author__ = 'Tom James Holub'


def get_key(dictionary, for_value):
	if type(dictionary) is dict:
		for key, value in dictionary.items():
			if value == for_value:
				return key
	else:
		raise TypeError('can only subtract list-list')


def join(first, second):
	added = first.copy()
	for key in second:
		if key not in added:
			added[key] = second[key]
	return added


class Dict(dict):
	def __init__(self, *args, **kwargs):
		super(Dict, self).__init__(*args, **kwargs)
		self.__dict__ = self
