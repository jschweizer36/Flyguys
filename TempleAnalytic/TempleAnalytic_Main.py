'''
Created on Oct 23, 2014

@author
'''
import xlrd
from matplotlib import *
from Employee import Employee
import unicodedata

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


#Access Log threat level
def access_log(e, access_logs): #Initializing the access log function 
    points = 0  #setting an initial value for points 
    count = 0 #setting an initial value for a counter

    for x in range (0, access_logs.nrows-1):
        if (access_logs.cell(x+1,0).value == e.ntid):
            count=count+1
            
    if (count < 100):
        points = points + 1
    elif (count <200):
        points = points +2
    else:
        points = points + 3
    
    return (float(points)/3) * .1


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
            
    # return the points value
    return float(points)/float(count)

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
    #Reading in the data from the excel spreadsheet 
    dataset = xlrd.open_workbook('Lockheed_Data_Sample.xls')
    
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
    print phoneName   
    print
        
    #Creating all of our employee objects
    emp=[]
    idnum = 0
    name = ''
    ntid = ''
    temp = 0
    for i in range(1,employee_info.nrows):
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
    
    
    #Printing each employee object
    print str(emp[0].id) + ' ' + emp[0].name + ' ' + emp[0].ntid + ' ' + str(emp[0].threat)
    print str(emp[1].id) + ' ' + emp[1].name + ' ' + emp[1].ntid + ' ' + str(emp[1].threat)
    print str(emp[2].id) + ' ' + emp[2].name + ' ' + emp[2].ntid + ' ' + str(emp[2].threat)
    print str(emp[3].id) + ' ' + emp[3].name + ' ' + emp[3].ntid + ' ' + str(emp[3].threat)
    print 
    

    
    for i in range(0,len(emp)):
        Threatphone = emp[i].threat
        Threatair = airThreat(emp[i], air_travel)
        Threataccess = access_log(emp[i], access_logs)
        Threatjobhx = job_history_score(emp[i], job_hx)
        ThreatCitizen = citizenship_score(emp[i],citzenship)
        print "Travel threat = " + str(Threatair)
        print "Access log threat level = " + str(Threataccess)
        print "Job History threat level = " + str(Threatjobhx)
        print "Citizenship threat level = " + str(ThreatCitizen)
        Threat = .2*Threatphone + .35*Threatair + .05*Threataccess + .3*Threatjobhx + .1 *ThreatCitizen   #Scaled threats
        print Threat
        print
