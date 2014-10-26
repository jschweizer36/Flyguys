'''
Created on Oct 23, 2014

@author: pete
This function will be used to gather important information about each employee
We will be gathering each employees names (first and last), NTID, and their empolyee ID
This function will also get and set the threat of each of the employees
Just a test
'''

class Employee:
    def __init__(self, id, name, ntid ):  #initializing of the employee class
        self.id = id          #defining the employee ID number
        self.name = name      #defining the name of the employee
        self.ntid = ntid      #defining the NTID of the employee
        self.threat = 0       #setting the initial threat level of the employee
        
    def setThreat(self, threat):  #initializing the set threat class
        self.threat = threat;     #defining the varialbe for threat
        
    def getThreat(self):          #initializing the get thret class
        return self.threat        #returning the value of the threat
