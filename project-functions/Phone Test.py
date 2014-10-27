#Autho: Mohamed Hakim
#Edited: 10/26/2014
#Remark: started as a copy of Peter's TempleAnalytic_Main.py

import xlrd
from Employee import Employee

def phone_log(name,phoneLog):
#reading in the weights
with open("PhoneWeight.csv","r") as f:
    weights = [x.split("\n")[0].split(",") for x in f.readlines()]# read2List
    weights = {ind[0]:ind[1] for ind in weights}# List2dict
#print weights


#Reading in the data from the excel spreadsheet 
dataset = xlrd.open_workbook('Lockheed_Data_Sample.xls')

#Storing each tab of the spreadsheet into a new list
employee_info = dataset.sheet_by_index(0)
job_hx = dataset.sheet_by_index(3)
phoneLog = dataset.sheet_by_index(5)


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
    Temp = Employee(idnum, name, ntid)                                                      #Creating a Employee object
    emp.append(Temp)                                                                        #Storing the object in a list of the employee objects
    
#Store Phone Sheet Data
phone = []
for i in range(1,phoneLog.nrows):
    phone.append(phoneLog.row(i))
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
    if ((float(weights[str(occurance[entry][1])])+\
        float(weights[str(occurance[entry][2])]))/2)>0:
        Threats.append(occurance[entry][0])
print Threats
