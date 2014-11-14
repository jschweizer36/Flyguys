'''                                                                                       
this code parses our data                            
'''
import sys  #importing the sys library                                                    

if __name__ == '__main__':
    inputtext = open(sys.argv[1])                               
    version = inputtext.read(100)  
    print version