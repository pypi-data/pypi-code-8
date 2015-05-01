__author__ = 'Tom James Holub'


def unique(list_with_possible_duplicates):
	return list(set(list_with_possible_duplicates))


def subtract(first, second):
	if type(first) is list and type(second) is list:
		result = []
		for value in first:
			if value not in second:
				result.append(value)
		return result

	raise TypeError('can only subtract list-list')


def add_unique(unique_list, unique):
	if unique not in unique_list:
		unique_list.append(unique)