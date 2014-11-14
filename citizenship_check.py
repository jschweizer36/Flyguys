'''
The function will be used to determine the threat level of an employee based on their origin of birth                                  
The threat level is based on the danger of the country                         
'''

# library used to change unicode to string                                     

import unicodedata

# citizenship checking function                                                

def citizenship_score(idnumber,citizenship):
    # Initialization                                   
    birth_country = []
    points = 0

    # loop to create a list of the country of birth of the employee          

    for x in range(0,citizenship.nrows-1):
        if (int(citizenship.cell(x+1,0).value) == idnumber):
            birth_country.append(citizenship.cell(m+1,2).value)

    # loop over all of the employees to find their birth country               

    for country in birth_country:
        country = unicodedata.normalize('NFC',country)

        if country == "US":   #If the country is The United States
            points = points + .1
        elif country == "SE":   #If the country is Sweden
            points = points + .2
        elif country == "NP":   #If the country is Nepal
            points = points + .3
        elif country == "CR":   #If the country is Costa Rica
            points = points + .4
        elif country == "PE":   #If the country is Peru
            points = points + .5
        elif country == "ER":   #If the country is Eritrea
            points = points + .6

    return points
