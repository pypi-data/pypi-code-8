"""The module is "Athlete.py" which provides a class called AthleteList to handle the data of athletes. AthleteList
is the subclass of list and contains 2 attributes (name  and dob refers to the name and birthday of the athlete
respectively)."""

def sanitize(time_string):
    """The function is used to transform time_string (e.g. '2-3','2:3') to the standard form (e.g. '2.3').
        It has one arguement "time_string" which is the time string to be transformed.
        It returns to the standard time form mins.secs (e.g. "2.3")."""    
    if '-' in time_string:
        splitter = '-'
    elif ':' in time_string:
        splitter = ':'
    else:
        return (time_string)
    (mins,secs) = time_string.split(splitter)
    return (mins+'.'+secs)

class AthleteList(list):
    def __init__(self, a_name, a_dob = None, a_times =[]):
        """The function is automatically invoked while constructing class AthleteList.
            a_name is the name of athlete.
            a_dob is the birthday of athlete.
            a_times is the list of athlete times."""
        list.__init__([])
        self.name = a_name
        self.dob = a_dob
        self.extend(a_times)

    def top3(self):
        """The function is used to return the top 3 fastest times of the athlete"""
        return sorted(set([sanitize(t) for t in self]))[0:3]

    def add_time(self, time):
        """The function is used to add a time value"""
        self.append(time)

    def add_times(self, time):
        """The function is used to add a list of times"""
        self.extend(time)
