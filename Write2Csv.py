import sys							#Use the system

OrigOut = sys.stdout				#remember default stdandard output
sys.stdout = open("output.csv","w") #route output to .csv file

print "name"+","+"threat"+","+"age"+"," #example of printing in .csv
print "cow"+","+"1"+","+"23"+","		#example of printing in .csv

sys.stdout = OrigOut				#restore standard output to default
