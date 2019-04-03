from pymarc import MARCReader
import re
import sys, csv ,operator

fhand = open('H:\\marcscorer python\\console', encoding="utf-8")
 
for line in fhand:
    
    normalizedTitle = line.split("|")[4]
    
    #mylist = normalizedTitle.sort()
        
    print (normalizedTitle)


