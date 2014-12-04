'''
Created on Oct 23, 2014
This file is composed of functions that determine the threat level of lockheads employees 
The functions all check different fields for example phone call history, server access logs, and more.
Each function will parse the database given to us, and return a value of threat.
The total threat from each function will be returned as a value of points, and the points from each function will be averaged together giving a final threat level.
The results of the threat level will be written to a csv file along with the person's name, NTID, employee ID, department, and the state they work in.
This file will be saved and used to present the data on our website.
Each time the function runs it updates the csv file with any new information for the employees.

@author Mohammed Hakim, Pete Mollica, Joseph Schweizer, Joseph Throne

Last edit: December 4, 2014
'''
import xlrd
import sys
from Employee import Employee
import unicodedata

'''
This function checks the threat level of each employee based on their flight history
What we looked for was inconsistencies in the travel history (double booked flights, flights to different areas)
This functions takes as inputs the employee class we generate, and the air travel information from the database
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
            if i+1 >= air_travel.nrows:   #Used to avoid an index error
                break
            if (air_travel.cell(i,5).value == air_travel.cell(i+1,5).value):
                threatCount=threatCount+1
    if count ==0:
        return 0
    else:
        threat=float(threatCount)/float(count)
        return threat

'''
This function checks the threat level of an employee based on their access log history
The function input takes in the employee class, and the access log information
It then counts the number of times a user accesses the server based on their username, and counts for each instance
The data is over a years worth of time, so we broke up the amount of times based on how many work days are in a year
The points depend on how many times a certain user accesses the server within that year
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
This function checks the threat level of each employee based on their job history (demotions, promotions, raises)
One of the things our research showed to look for were personal stressors from the work place
This function's input is the employee class, and the job hx information from the database.
It checks through each occurrence of the employee's ID and sees what happened to the employee job status.
For example if the string is "Demotion for Infraction" the employee is given 0.6 points,
where as if the string was "New Hire" they would receive no points. Then, their total points are averaged and returned to the main function
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
This function assumes that unique calls which take less than 10 minutes are possibly an insider threat
This assumption is due to the possibility that if a new customer calls in most likely they will need some clarifications
Once the unique phone calls are found, the function figure out which employee made or answered that phone call.
These employee are then given a certain threat level based on the number of unique calls they have made.
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
    #for these entries a weight is given for their threat based on location
    Threats = []
    for entry in occurance:
        littleThreat= (float(weights[str(occurance[entry][1])])+\
            float(weights[str(occurance[entry][2])]))/2
        if (littleThreat)>0:
            Threats.append([str(occurance[entry][0]),littleThreat/float(10)])
    return Threats

'''
This function determines the threat level of an employee based on their citizenship.
Our research showed that we should analyze each employee's heritage, and 
if they were born in a certain area they should be assigned a threat level.
This function's input is the empolyee class, and the citizenship information from the database.
This function looks for each employee ID and then for the information about where they were born and raised.
Based on the location the employee is assigned a certain threat level.
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

'''
The following function is our main function. This function makes a a list of employee objects for all of the employees.
The employee class assigns a name, id number, and NTID.
Once all of the employee objects are made, the function determines an overall threat level for each employee.
The function then creates a csv file containing the id, name, ntid, threat, state and department for each employee.
This csv file is used in our javascript code to present the data graphically on our webpage.
'''

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
        
    #Creating all of our employee objects
    emp=[]
    idnum = 0
    name = ''
    ntid = ''
    temp = 0
    for i in range(1,1001):
        idnum = int(employee_info.cell(i,0).value)     #Finding Employee ID Number and storing it in idnum
        name = employee_info.cell(i,7).value + ',' + employee_info.cell(i,5).value  #Finding Employee Name and storing it in name
        for j in range(1,job_hx.nrows):
            if (int(job_hx.cell(j,0).value) == idnum):
                ntid = job_hx.cell(j,19).value     #Finding NTID and storing it in ntid
                break
        Temp = Employee(idnum, name, ntid) 
        try:
            temp = phoneName[name]
            Temp.threat = temp
        except KeyError:
            pass                                   #Creating a Employee object
        emp.append(Temp)                           #Storing the object in a list of the employee objects
    
    
    print 'id,name,ntid,threat,state,department'
      
    for i in range(0,len(emp)):
        Threatphone = emp[i].threat
        Threatair = airThreat(emp[i], air_travel)
        Threataccess = access_log(emp[i], access_logs)
        Threatjobhx,state,dept = job_history_score(emp[i], job_hx)
        ThreatCitizen = citizenship_score(emp[i],citzenship)
        Threat = .2*Threatphone + .35*Threatair + .05*Threataccess + .3*Threatjobhx + .1 *ThreatCitizen   #Scaled threats
        emp[i].threat = Threat
        print '"'+str(emp[i].id)+'"'+ ',' +'"'+emp[i].name+'"'+ ',' +'"'+ emp[i].ntid+'"'+ ',' +'"'+str(emp[i].threat)+'"'+ ',' +'"'+dept+'"'+ ',' +'"'+state+'"'+ ','
    
    sys.stdout = OrigOut
