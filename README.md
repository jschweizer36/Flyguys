Flyguys
=======

Data Analytics Challenge

link: http://104.131.39.157/

  This submission is towards Lockheed Martin challenge: Reducing employee insider threat. We translated the information in the given database into threat levels per employee using python then presented the data using d3js. The presented pie chart shows the distribution of employees in different departments, upon hovering over a part of the pie chart the bar graph accompanying it shows the distribution of the employees in that department into threat levels where 0 means no threat and 6 means action is required immediately. The project will be available on a server reachable by following the above link.
  
  Lockheed Martin's challlenge told us a few things to look into to determine if one of their employees was a threat or not. For starters one of the things they wanted us to check was where the employee was born. How we did this using python was by using the xlrd command, which opens the database given to us. After doing that we could then have our program search through each tab for anything we wanted. What we did was tel our code to pull all the employee's first, and last names, employee ID's, and their NTID's. By doing this we could identify each employee on every single tab. Consider the birth place example again, Lockheed gave us a tab called employee info. This tab contained both the employee ID number, and their country of birth. We had our program read through all of the ID's untill it found the person we were looking for, and after we found it our went to the column, in that row, where the country of birth was displayed and saved that into a varibale that we created. We then rated all of the conutries that their employee's came from on a scale from 0-1 based on how dangerous they were. We return that value, and that is the employee's threat level based on just country of birth. We had other functions that returned other threat levels, and we averaged all of them out. The final value was the employee's total threat level. Our other functions looked at things suchs as air travel, phone call history, personal stress, demotions or promotions, and how often they accessed the server.


Team Memeber Names:
Mohamed Hakim<br> 
Peter Mollica<br>
Joseph Schweizer<br>
Joseph Throne<br>

Accessnet ID's:<br>
tud16274<br>
tue60527<br>
tud14556<br>
tud24646v
<br>
<br>































