print "program Start"

with open("test.csv","r") as f:#opening the .csv
    lines = f.readlines()#reading in the lines

new_lines = [x.split(",") for x in lines]#removing commas

print new_lines[2][3]#an example of accessing an element

print "program done"
