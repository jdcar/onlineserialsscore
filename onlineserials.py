from pymarc import MARCReader
import re

with open('C:\\Users\\jdc6\\Desktop\\Export.dat', 'rb') as fh:

    reader = MARCReader(fh)
    print ("Result|OCLC Number|Score|Title|Normalized Title|First Date|Second Date|ISSN")
    for record in reader:
      
        recordScore = 0
        
        oclcNumber = re.sub(r"=001  ", "", str(record["001"]))   
        oclcNumber1 = re.sub(r"(o\w+?)(\d+)", r"\2", oclcNumber)
        oclcNumber2 = re.sub(r"\\", r"", oclcNumber1)
          
        subjects = str(record.subjects())
        firstDate = re.sub(r"(.{13})(....)(.+)", r"\2", str(record["008"]))
        secondDate = re.sub(r"(.{17})(....)(.+)", r"\2", str(record["008"]))
        title = str(record.title())
        catalogingLanguage = str(record["040"]["b"])
                       
        if record.leader[7] is "s":
                        
            if re.match(r"=008  .{23}o" , str(record["008"])):
                            
                if re.match(r".+DELETION.+", str(record["936"])):
                    
                    deletion = 0
                  
                    #print ("Reported for deletion |", oclcNumber)
                     
                elif re.match(r".{13}0", str(record["008"])):
                     
                    zeros = 0
                    
                    #print ("Zeros in the date field |", oclcNumber)
                     
#                 elif record.leader[17] is "3":
#                     
#                     level3envl = 0
#                      
#                     print ("Encoding level three |", oclcNumber)         
                     
                elif re.match(r"^(?!.*(eng|None)).*$", catalogingLanguage):
                
                    foreign = 0
                    #print ("Foreign language cataloging |", oclcNumber)
                 
                else:
                                
## start scoring the record here
                    if re.match(r"=008  .{7}uuuu", str(record["008"])):
                                 
                        recordScore = recordScore - 3
                         
                    if re.match(r"=008  .{15}xx", str(record["008"])):
                         
                        recordScore = recordScore - 1
                         
                    if re.match(r"=008  .{35}und", str(record["008"])):
                         
                        recordScore = recordScore - 1
                         
                    if record["042"] is not None:
                         
                        recordScore = recordScore + 7
                         
                    if record.leader[17] is "I" or record.leader[17] is " ":
                               
                        recordScore = recordScore + 5
                         
                    if record.leader[17] is "M" or record.leader[17] is "L" or record.leader[17] is "K" or record.leader[17] is "7":
                                                   
                        recordScore = recordScore + 1
                         
                    if record["006"] is not None:
                         
                        recordScore = recordScore + 1
                         
                    if record["260"] is not None:
                         
                        recordScore = recordScore + 1
     
                    if record["264"] is not None:
                         
                        recordScore = recordScore + 1    
                         
                    if record["310"] is not None:
                         
                        recordScore = recordScore + 1
                         
                    if record["336"] is not None:
                         
                        recordScore = recordScore + 1
                         
                    if record["362"] is not None:
                         
                        recordScore = recordScore + 1
                         
                    if re.match(r"=588.+", str(record["588"])):
                         
                        recordScore = recordScore + 1    

                    if re.match(r"=6..  .0", subjects):
                           
                        recordScore = recordScore + 2
                          
                    if subjects is None:
                          
                        recordScore = recordScore - 5
                         
                    if re.match(r".+pcc.+", str(record["042"])):
                          
                        recordScore = recordScore + 100
                        
                    #TItle normalization
                    
                    removeDefiniteArticles = re.sub("(^)(The |El |La |Los |Las |Der |Die |Das |Les |Le |L' |Il |I |Le )", "", title)

                    titlenospace = re.sub("\s", "", removeDefiniteArticles)
        
                    titlenoperiod = re.sub("\.", "", titlenospace)
        
                    titlelowercase = titlenoperiod.lower()
        
                    ampersand = re.sub(r"&", r"and", titlelowercase)
                                            
                    removeDash = re.sub("-", "", ampersand)
                    
                    print("online serial|", oclcNumber2, "|", recordScore, "|", title, "|", removeDash, "|", firstDate, "|", secondDate, "|", record["022"], sep="")
            else: 
                
                notOnline = 0  
                #print("not online |", oclcNumber, "|", recordScore, "|", title, "|", title, "|", firstDate, "|", secondDate, "|", record["022"], sep="")
                                     
        else:
              
            notaSerial = 0  
            #print("not a serial |", oclcNumber, "|", recordScore, "|", title, "|", title, "|", firstDate, "|", secondDate, "|", record["022"], sep="")         
