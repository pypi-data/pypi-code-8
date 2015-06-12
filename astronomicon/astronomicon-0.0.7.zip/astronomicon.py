""" Astronomicon.py  This contains a set of astronomy and astrology calculations as an exercise in learning python.
Absolutely not ready yet"""
import time;

""" get int returns the integer component of a division"""    
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
    retu = 0;

    #if (year is not exactly divisible by 4) then (it is a common year)
    #else if (year is not exactly divisible by 100) then (it is a leap year)
    #else if (year is not exactly divisible by 400) then (it is a common year)
    #else (it is a leap year)
    
    div_by_4 = get_mod(year, 4);
    div_by_100 = get_mod(year, 100);
    div_by_400 = get_mod(year, 400);

    if (div_by_4 != 0):
        retu = 0;
    else:
        retu = 1;

    if (div_by_100 != 0):
        retu = 1;
    else:
        if (div_by_400 != 0):
            retu = 0;
        else:
            retu = 1;

    return retu;
   
""" get now returns current date time"""    
def get_now():
    localtime = time.asctime( time.localtime(time.time()) );
    return localtime;   