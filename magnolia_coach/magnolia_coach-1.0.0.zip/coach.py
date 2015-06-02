"""This is the "coach.py" module  and it provides to extract time data from txt files and print three of the
unique shortest time for each player. There are two functions: sanitize() is to clean time data and get_coach_data
is to read time data from txtfiles."""

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

def get_coach_data(filename):
    try:
        with open(filename) as f:
            data = f.readline()
            return(data.strip().split(','))
    except IOError:
        print('FIle Error: ' + str(error))
        return(None)

james = get_coach_data('james.txt')
julie = get_coach_data('julie.txt')
mikey = get_coach_data('mikey.txt')
sarah = get_coach_data('sarah.txt')

print sorted(set([sanitize(each_t) for each_t in james]))[0:3]# list comprehension
print sorted(set([sanitize(each_t) for each_t in julie]))[0:3]
print sorted(set([sanitize(each_t) for each_t in mikey]))[0:3]
print sorted(set([sanitize(each_t) for each_t in sarah]))[0:3]
        

