""" Astronomicon.py  This contains a set of astronomy and astrology calculations as an exercise in learning python.
Absolutely not ready yet"""
""" get int returns the integer component of a division""" 
import time;
  
def get_int(one, two):
    return int(one / two);

""" get modulus returns the modulus component of a division"""
def get_mod(one, two):
    return (one % two);

def get_easter(year, debug=0):
    a = get_mod(year, 19);
    b = get_int(year, 100);
    c = get_mod(year, 100);
    d = get_int(b, 4);
    e = get_mod(b, 4);
    f = get_int((b+8), 25);
    g = get_int((b-f+1), 3);
    h = get_mod(((19 * a) + b - d - g + 15), 30);
    i = get_int(c, 4);
    k = get_mod(c, 4);
    l = get_mod((32+(2*e)+(2*i)-h -k), 7);
    m = get_int((32+(2 * e)+(2*i)-h -k),451);
    n = get_int((h+l-(7*m)+114), 31);
    p = get_mod((h+l-(7*m)+114), 31);
    month = n;
    date = p+1;
    
    if debug == 1:
        print ("Debug calculation results");
        print ("\n my year = ", year);
        print ("Divide the year by 19             a(",a,")");
        print ("Divide the year by 100            b(",b,")\tc(",c,")");
        print ("Divide b by 4                     d(",d,")\te(",e,")");
        print ("Divide (b+8) by 25                f(",f,")");
        print ("Divide (b - f + 1)/3              g(",g,")");
        print ("Divide(19a+b-d-f+15) by 30        h(",h,")");
        print ("Divide c by 4                     i(",i,")\tk(",k,")");
        print ("Divide <lots> by 7>               l(",l,")");
        print ("Divide <lots> by 451>             m(",m,")");
        print ("Divide lots by 31                 n(",n,")\tp(",p,")");
        
    return str(date) + "-" + str(month) + "-" + str(year);

def is_leap_year(year):
    ret = 0;

    #if (year is not exactly divisible by 4) then (it is a common year)
    #else if (year is not exactly divisible by 100) then (it is a leap year)
    #else if (year is not exactly divisible by 400) then (it is a common year)
    #else (it is a leap year)
    
    div_by_4 = get_mod(year, 4);
    div_by_100 = get_mod(year, 100);
    div_by_400 = get_mod(year, 400);
    
    if (div_by_4 != 0):
        ret = 0;
    else:
        ret = 1;
        if (div_by_100 != 0):
            ret = 1;
        else:
            if (div_by_400 != 0):
                ret = 0;
            else:
                ret = 1;

    return ret;
   
""" get now returns current date time"""    
def get_time():
    localtime = time.asctime( time.localtime(time.time()) );
    return localtime;

""" takes a list containing day, month, year"""
def get_day_number(date):
    day = date[0];
    month = date[1];
    year = date[2];
    days = 0;

    # error checks
    error = check_date(date);
    
    #do we have a leap year
    leap = is_leap_year(year);
    months = [0, 0, 31, 59, 90, 120, 151, 181, 212, 243, 273, 304, 334];

    days = months[month];
    if (month > 2):
        if (is_leap_year(year)):
            days = days + 1;   # increment 1 for leap year if a leap year and date is past February
    days = days + day;   # Increment the date

    return days;
	    
""" checks that date is valid and off the form dd-mm-yyyy"""
""" returns 1 if valid and 0 if invalid """
def check_date(date):
    day = date[0];
    month = date[1];
    year = date[2];

    if month > 12 or month < 1:
        return 0;
    
    leap = is_leap_year(year);
    
    data = {"1":"31", "2":"28", "3":"31", "4":"30", "5":"31", "6":"30", "7":"31", "8":"31", "9":"30", "10":"31", "11":"30", "12":"31",}
    
    # modify if a leap year
    if leap:
        data["2"] = 29;
        
    days_in_month = data[str(month)];
    
    if  int(day) > int(days_in_month):
        return 0;

        
    print ("data from check_date (leap year):", data["2"]);
    print ("data from check_date (days_in_month):", days_in_month);
    
    return 1;

    
        
        