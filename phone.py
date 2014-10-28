#Author: Mohamed Hakim
#Edited: 10/26/2014
#Remark: started as a copy of Peter's TempleAnalytic_Main.py

def phone_log(name,phoneLog):
    #reading in the weights
    with open("PhoneWeight.csv","r") as f:
        weights = [x.split("\n")[0].split(",") for x in f.readlines()]# read2List
        weights = {ind[0]:ind[1] for ind in weights}# List2dict
    #print weights

    #Store Phone Sheet Data
    phone = []
    
    for i in range(1,phoneLog.nrows):
        if(phoneLog.cell(i,3).value == name):
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
    return Threats
