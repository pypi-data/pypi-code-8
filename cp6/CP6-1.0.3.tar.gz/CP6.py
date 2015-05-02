
def sanitize(time_string):
    if '-' in time_string:
        splitter = '-'
    elif ':' in time_string:
        splitter = ':'
    else:
        return(time_string)
    (mins,secs) = time_string.split(splitter)
    return(mins+'.'+secs)

def get_coach_data(file_name):
    try:
        with open(file_name) as f:
            data = f.readline()
        temp1 = data.strip().split(',')
        return({'NAME'  : temp1.pop(0),
                'DOB'   : temp1.pop(0),
                'TIME'  : str(sorted(set([sanitize(t) for t in temp1]))[0:3])})
    except IOError as err:
        print('File Error: ' + str(err))
        return(None)


