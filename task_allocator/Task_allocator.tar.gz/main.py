import datetime
from datetime import datetime
import fileinput


def status_check():
        query=raw_input("Enter Your Query:")            #Enter the Query format tasktype Usermane Country Start time(Local) End time(Local)
        b=query.split()                                 #Spliting the query into words
        dates = []
        dates.append(b[3])                                     
        dates.append(b[4])
        current_date_time=datetime.now().strftime('%b/%d/%Y-%H:%M')     #Picking current time from OS
        print "Current Date & Time=>", current_date_time
        for d in dates:
            date = datetime.strptime(d, '%b/%d/%Y-%H:%M')               #Changing into datetime format
            #print type(date)
            date = date.strftime('%b/%d/%Y-%H:%M')
            #print date
        if current_date_time>= b[3] and current_date_time<=b[4]:        #Compairing with Current Time
            print "True!"
            return
        else:
            print "False!"
          


def enhanced_search():
        query=raw_input("Enter Your enhanced_search:")       #Enter the Query format tasktype Usermane Country Start time(Local) End time(Local)
        b=query.split()                                      #Spliting the query into words
        current_date_time=datetime.now().strftime('%b/%d/%Y-%H:%M') #Picking current time from OS
        print "Current Date & Time=>", current_date_time
        dates= []
        dates.append(b[3])
        dates.append(b[4])
        for d in dates:
            date = datetime.strptime(d, '%b/%d/%Y-%H:%M')                #Changing into datetime format
            #print type(date)
            date = date.strftime('%b/%d/%Y-%H:%M')
            #print date
        if current_date_time>= b[3] and current_date_time<=b[4]:         #Compairing with Current Time
            print "True!\n"
            return
        for i in range(count):                                           #Accessing the data taken from the file
            temp=content[i]
            temp=temp.split()
            if(b[0]==temp[0] and b[1]==temp[1]):                         #Compairing with the task type and username
                if current_date_time<temp[3]:                            #Compairing for the probable time in future
                    print "\nTask will be picked up between:", temp[3] + " to "+ temp[4]+"\n"
                    return
   






content = []
count=0
for line in fileinput.input():                                            #Commandline Agrument for the filename
    content.append(line.strip())
    count+=1
fileinput.close()                                                         #Closing the file
inp=0
while(inp!=3):
    inp=input("Press 1.status_check 2.enhanced_search 3.Exit=>\n");        #List view to choose the type of query
    if inp==1:
        status_check()
    elif inp==2:
        enhanced_search()
    elif inp==3:
        break
    else:
        continue

