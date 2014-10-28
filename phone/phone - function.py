#Author: Mohamed Hakim
#Edited: 10/28/2014
#Remark: started as a copy of phone.py

import xlrd
from Employee import Employee

def Phone(phone):
	#reading in the weights
	with open("PhoneWeight.csv","r") as f:
		weights = [x.split("\n")[0].split(",") for x in f.readlines()]# read2List
		weights = {ind[0]:ind[1] for ind in weights}# List2dict
	#print weights

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
	return Threats

#--test
#Reading in the data from the excel spreadsheet 
dataset = xlrd.open_workbook('Lockheed_Data_Sample.xls')

#Storing each tab of the spreadsheet into a new list
employee_info = dataset.sheet_by_index(0)
job_hx = dataset.sheet_by_index(3)
phoneLog = dataset.sheet_by_index(5)
        
#Store Phone Sheet Data
phone = []
for i in range(1,phoneLog.nrows):
        phone.append(phoneLog.row(i))

print Phone(phone)
