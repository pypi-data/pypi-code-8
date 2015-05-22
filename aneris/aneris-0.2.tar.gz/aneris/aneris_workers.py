import datetime

workers = \
{ \

#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#
#david_o
#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#

	"david_o": \
	{ \
		"default_committed_hours_start_date": datetime.date(2014, 5, 18), \
		"default_committed_hours":
		{ \
			"monday"    : [ 3 ], \
			"wednesday" : [ 3, 0 ],       \
			"thursday"  : [ 0, 0, 3, 0 ], \
			"friday"    : [ 3, 2 ],       \
		} \
	}, \

#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#
#david_o_work
#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#

	"david_o_work": \
	{ \
		"default_committed_hours_start_date": datetime.date(2014, 5, 18), \
		"default_committed_hours":
		{ \
			"monday"    : [ 1 ], \
		} \
	}, \
}

work_days = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]
