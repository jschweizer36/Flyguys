'''
This function will analyze each employees access to the server 
We will use their NTID to check to see how often they log on
The more they log on the higher the threat they will be
'''

import unicodedata #this is the library we will use to convert values to strings

def access_log(NTID, access): #Initializing the access log function 
    points = 0  #setting an initial value for points 
    count = 0 #setting an initial value for a counter

    for x in range (0, access.nrows-1):
        if (access.cell(x+1,0).value == NTID):
            count = count + 1
            
    if (count < 100):
        points = points + .1
    elif (count <200):
        points = points + .2
    else:
        points = points + .3

    return points 
        

main()
