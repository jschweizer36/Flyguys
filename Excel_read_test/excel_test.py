'''
Created on Oct 21, 2014

@author: Joseph
'''
import xlrd
book = xlrd.open_workbook("Lockheed_Data.xls")
print "The number of worksheets is", book.nsheets
print "Worksheet name(s):", book.sheet_names()
sh = book.sheet_by_index(6)
#print sh.name, sh.nrows, sh.ncols
print "Cell D30 is", sh.cell_value(rowx=2, colx=2)
#for rx in range(sh.nrows):
    #print sh.row(rx)