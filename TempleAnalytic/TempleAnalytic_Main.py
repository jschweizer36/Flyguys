'''
Created on Oct 23, 2014

@author
'''
import xlrd
from matplotlib import *
from Employee import Employee



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
        
    #Printing each employee object
    print str(emp[0].id) + ' ' + emp[0].name + ' ' + emp[0].ntid
    print str(emp[1].id) + ' ' + emp[1].name + ' ' + emp[1].ntid
    print str(emp[2].id) + ' ' + emp[2].name + ' ' + emp[2].ntid
    print str(emp[3].id) + ' ' + emp[3].name + ' ' + emp[3].ntid
    
    
    