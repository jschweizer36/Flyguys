'''
Created on Oct 23, 2014
This file is composed of 6 functions that determine the threat level of lockheads employees 
The functions all check different fields for example (phone call history, server access logs, and more)
each function will parse the database given to us, and return a value of threat
the total threat from each fucntion will be returned as a vlaue of points, and the points from each function will be averaged together giving a final rating
the results of the threat level will be written to a csv file along with the person's name, NTID, employee ID, department, and the start they work in
this file will be saved for records, and will create a new file each time the program runs

@author Flyguys
'''
import xlrd
import sys
from matplotlib import *
from Employee import Employee
import unicodedata

'''
This function checks the threat level of each employee based on their flight history
What we looked for was inconsistencies in the travel history (double booked flights, flights to different areas)
This functions input takes the employee class we generate, and the air travel tab from the database
This checks for each occurence of the persons employee ID and sees when they have flights booked
If they only have one flight booked for a day they do not get a threat level
If they have multiple flights on the same day at the same time they are given a threat level
The threat level raises based on how many times they have flights that are double booked
'''
#Air threat level
def airThreat(e, air_travel):
    #Determining the threat of air travel
    count = 0
    threatCount = 0
    threat = 0
    for i in range(0, air_travel.nrows):
        if (air_travel.cell(i,1).value==e.name):
            count=count+1
            #print count
            if i+1 >= air_travel.nrows:                                         #Used to avoid an index error
                break
            if (air_travel.cell(i,5).value == air_travel.cell(i+1,5).value):
                threatCount=threatCount+1
                #print threatCount
                
    if count ==0:
        return 0
    else:
        threat=float(threatCount)/float(count)
        #Print threat
        return threat

'''
This function checks the threat level of an employee based on their access log history
The function input takes in the employee class, and the access log tab
It then counts the number of times a user accesses the server based on their username, and counts for each instance
The data is over a years worth of time, so we broke up the amount of times based on how many work days are in a year
The points depened on how many times a certain user accesses the server within that year
'''
#Access Log threat level
def access_log(e, access_logs): #Initializing the access log function 
    points = 0  #setting an initial value for points 
    count = 0 #setting an initial value for a counter

    for x in range (0, access_logs.nrows-1):
        if (access_logs.cell(x+1,0).value == e.ntid):
            count=count+1
            
    if (count < 300):
        points = points + 0.1
    elif (count < 320):
        points = points + 0.2
    elif (count < 340):
        points = points + 0.3
    elif (count < 360):
        points = points + 0.4
    else:
        points = points + 0.5
    
    return (float(points)/3) *.1

'''
This function checks the threat level of each employee based on their job histry (demotions, promotions, raises)
One of the things we were told to look for were personal stressors from the work place
This function's input is the employee class, and the job hx tab from the database
It checks through each occurence of the employee's ID and checks the string to see what happened
For example if the string is "Demotion for Infraction" the employee is given 0.6 points
Where as if the string was "New Hire" they would recieve no points, and their total points are averaged and returned to the main function
'''
#Job History Threat Level
def job_history_score(e,job_hx):
    # Initialization
    job_history = []
    points = 0
    count = 0
    
    # loop to create a list of the job history of the employee
    for m in range(0,job_hx.nrows-1):
        if (int(job_hx.cell(m+1,0).value) == e.id):
            count = count +1
            job_state = job_hx.cell(m+1,8).value
            job_depar = job_hx.cell(m+1,16).value
            job_history.append(job_hx.cell(m+1,3).value)
            
    # loop to score the employee based on their job history
    for reason in job_history:
        reason = unicodedata.normalize('NFC',reason)
        
        if reason == "Demotion for Infraction":
            points = points + 0.6
        elif reason == "Demotion for Performance":
            points = points + 0.6
        elif reason == "Termination for Cause":
            points = points + 0.9
        elif reason == "Termination due to Business Reduction":
            points = points + 0.9
        elif reason == "Termination due to Self Separation":
            points = points + 0.9
        elif reason == "New Hire":
            points = points + 0
        elif reason == "Pay Increase for performance":
            points = points + 0
        elif reason == "Promotion for performance":
            points = points + 0
        elif reason == "Self demotion to Change Position":
            points = points + 0.2
    if count == 0:
        count = 1
    # return the points value
    return float(points)/float(count),job_state,job_depar


'''
This function determines a threat level of each employee baseed upon their phone records
The input to the funciton is 



I HAVE NO IDEA HOW THIS WORKS CAN SOMEONE EXPLAIN
'''
#Phone log threat level
def phone_log(phone):
    #reading in the weights
    with open("PhoneWeight.csv","r") as f:
        weights = [x.split("\n")[0].split(",") for x in f.readlines()]# read2List
        weights = {ind[0]:ind[1] for ind in weights}# List2dict
        
    #now find phone number that appear once only and is duration less than 10mins
    occurance = {}
    for rows in phone:
        if rows[10].value < 10:
            try:
                temp = occurance[rows[2].value]
                occurance.pop(rows[2].value)
            except KeyError:
                occurance[rows[2].value] = [rows[3].value,rows[6].value,rows[7].value]
    #for these entries weight their threat based on location
    Threats = []
    for entry in occurance:
        littleThreat= (float(weights[str(occurance[entry][1])])+\
            float(weights[str(occurance[entry][2])]))/2
        if (littleThreat)>0:
            Threats.append([str(occurance[entry][0]),littleThreat/float(10)])
    return Threats

'''
This function determines the threat level of an employee based on their citizenship
We were told to analyze each employee's heritage, and if they were born in a dangeroues area they should be a threat
This functions input is the empolyee class, and the citizenship tab from the database
This function looks for each employee using their ID and then grabs the column that says where they were born
Then it checks what the string says, and returns a points values based on where they employee was born
'''
def citizenship_score(e,citizenship):
    # Initialization                                   
    birth_country = []
    points = 0

    # loop to create a list of the country of birth of the employee          

    for x in range(0,citizenship.nrows-1):
        if (int(citizenship.cell(x+1,0).value) == e.id):
            birth_country.append(citizenship.cell(x+1,2).value)

    # loop over all of the employees to find their birth country               

    for country in birth_country:
        country = unicodedata.normalize('NFC',country)

        if country == "US":   #If the country is The United States
            points = 0.0
        elif country == "SE":   #If the country is Sweden
            points = 0.1
        elif country == "NP":   #If the country is Nepal
            points = 0.2
        elif country == "CR":   #If the country is Costa Rica
            points = 0.3
        elif country == "PE":   #If the country is Peru
            points = 0.4
        elif country == "ER":   #If the country is Eritrea
            points = 0.5

    return float(points)

if __name__ == '__main__':
    OrigOut = sys.stdout
    sys.stdout = open("Output.csv","w")

    #Reading in the data from the excel spreadsheet 
    dataset = xlrd.open_workbook('Lockheed_Data.xls')
    
    #Storing each tab of the spreadsheet into a new list
    employee_info = dataset.sheet_by_index(0)
    citzenship = dataset.sheet_by_index(1)
    employee_contract = dataset.sheet_by_index(2)
    job_hx = dataset.sheet_by_index(3)
    air_travel = dataset.sheet_by_index(4)
    phonecall_logs = dataset.sheet_by_index(5)
    access_logs = dataset.sheet_by_index(6)

    #Phone list
    phone = []
    for i in range(1,phonecall_logs.nrows):
        phone.append(phonecall_logs.row(i))
    Threatphone = phone_log(phone)
    phoneName = {x[0]:x[1] for x in Threatphone}
    #Debugging prints
    #print phoneName   
    #print
        
    #Creating all of our employee objects
    emp=[]
    idnum = 0
    name = ''
    ntid = ''
    temp = 0
    for i in range(1,1001):
        idnum = int(employee_info.cell(i,0).value)                                              #Finding Employee ID Number and storing it in idnum
        name = employee_info.cell(i,7).value + ',' + employee_info.cell(i,5).value              #Finding Employee Name and storing it in name
        for j in range(1,job_hx.nrows):
            if (int(job_hx.cell(j,0).value) == idnum):
                ntid = job_hx.cell(j,19).value                                                  #Finding NTID and storing it in ntid
                break
        Temp = Employee(idnum, name, ntid) 
        try:
            temp = phoneName[name]
            Temp.threat = temp
        except KeyError:
            pass                                                     #Creating a Employee object
        emp.append(Temp)                                                                        #Storing the object in a list of the employee objects
    
    
    #Printing each employee object for debugging 
    ''' 
    print str(emp[0].id) + ' ' + emp[0].name + ' ' + emp[0].ntid + ' ' + str(emp[0].threat)
    print str(emp[1].id) + ' ' + emp[1].name + ' ' + emp[1].ntid + ' ' + str(emp[1].threat)
    print str(emp[2].id) + ' ' + emp[2].name + ' ' + emp[2].ntid + ' ' + str(emp[2].threat)
    print str(emp[3].id) + ' ' + emp[3].name + ' ' + emp[3].ntid + ' ' + str(emp[3].threat)
    print 
    print job_hx.cell(1,16).value
    print job_hx.cell(1,8).value
    '''
    print 'id,name,ntid,threat,state,department'
      
    for i in range(0,len(emp)):
        #emp[i].state = job_hx.cell(i+1,16).value
        #emp[i].department = job_hx.cell(i+1,8).value
        Threatphone = emp[i].threat
        Threatair = airThreat(emp[i], air_travel)
        Threataccess = access_log(emp[i], access_logs)
        Threatjobhx,state,dept = job_history_score(emp[i], job_hx)
        ThreatCitizen = citizenship_score(emp[i],citzenship)
        ''' debugging prints
        print "Travel threat = " + str(Threatair)
        print "Access log threat level = " + str(Threataccess)
        print "Job History threat level = " + str(Threatjobhx)
        print "Citizenship threat level = " + str(ThreatCitizen)
        print "Department is: "   + emp[i].department
        print "State is: " + emp[i].state
        '''
        Threat = .2*Threatphone + .35*Threatair + .05*Threataccess + .3*Threatjobhx + .1 *ThreatCitizen   #Scaled threats
        emp[i].threat = Threat
        #print Threat
        print '"'+str(emp[i].id)+'"'+ ',' +'"'+emp[i].name+'"'+ ',' +'"'+ emp[i].ntid+'"'+ ',' +'"'+str(emp[i].threat)+'"'+ ',' +'"'+dept+'"'+ ',' +'"'+state+'"'+ ','
    
    sys.stdout = OrigOut
