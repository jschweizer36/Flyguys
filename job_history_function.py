'''
Created on Oct 26, 2014

function to get the job history of an employee and score them based on their history

@author: Joseph
'''
# library used to change unicode to string
import unicodedata

# function 
def job_history_score(idnumber,job_hx):
    # Initialization
    job_history = []
    points = 0
    
    # loop to create a list of the job history of the employee
    for m in range(0,job_hx.nrows-1):
        if (int(job_hx.cell(m+1,0).value) == idnumber):
            job_history.append(job_hx.cell(m+1,3).value)
            
    # loop to score the employee based on their job history
    for reason in job_history:
        reason = unicodedata.normalize('NFC',reason)
        
        if reason == "Demotion for Infraction":
            points = points + 1
        elif reason == "Demotion for Performance":
            points = points + 2
        elif reason == "Termination for Cause":
            points = points + 3
        elif reason == "Termination due to Business Reduction":
            points = points + 4
        elif reason == "Termination due to Self Separation":
            points = points + 5
        elif reason == "New Hire":
            points = points + 6
        elif reason == "Pay Increase for performance":
            points = points + 7
        elif reason == "Promotion for performance":
            points = points + 8
        elif reason == "Self demotion to Change Position":
            points = points + 9
            
    # return the points value
    return points