import numpy as np
import csv

def PreProcessSpectrum(filename,path):
    IN=[]
    OUT=[]
    with open(filename,"r") as File:
        reader=csv.reader(File,delimiter=' ')
        for row in reader:
            if len(row)<=1:
                print("Error.....!!!")
                return False
                
            else:
                t=[]
                for i in range(len(row)-1):
                    t.append(int(row[i]))
                IN.append(t)
                if row[-1] =='+':
                    OUT.append(0)
                elif row[-1] == '-':
                    OUT.append(1)
    #Do Preprocessing and create a Map;
    ActivityMerge={}
    row=len(IN)
    col=len(IN[0])
    IN=np.array(IN)
    for c in range(col):
        Act=tuple(IN[:,c])
        if Act not in ActivityMerge:
            ActivityMerge[Act]=set()

    for c in range(col):
        ActC=tuple(IN[:,c])
        temp=ActivityMerge[ActC]
        #---------Converting to Actual Component number
        temp.add(c)
        ActivityMerge[ActC]=temp
        
    
    ActivityMap={}
    NewData=[]
    index=0
    for act in ActivityMerge:
        NewData.append(list(act))
        ActivityMap[index]=ActivityMerge[act]
        index+=1
    NewData=np.array(NewData)
    NewData=NewData.T

    rOutName = path + '_Reduced_Spectrum.txt'
    rMapName = path + '_Reduced_Spectrum_ComponentMap.txt'
    
    with open(rOutName,"w") as File:
        writer=csv.writer(File)
        for i,o in zip(NewData,OUT):
            #print("Yes")
            temp=list(i)
            temp.append(o)
            #print(temp)
            writer.writerow(temp)
    with open(rMapName,"w") as File:
        writer=csv.writer(File)
        for i in ActivityMap:
            #print([i]+list(ActivityMap[i]))
            writer.writerow([i]+list(ActivityMap[i]))
    return True
    #return NewData,OUT,ActivityMerge,ActivityMap

#------------------------------------------------------------------------------
"""
Testing Funtions
"""
#Activity=ReadFromFile("Temp/sample.txt")
#INPUT,OUTPUT,oldMap,NewMap=ReadFromFile("benchmarks/chart14d2Spectrum.txt")
#INPUT,OUTPUT,oldMap,NewMap=PreProcessSpectrum("benchmarks/chart14d1Spectrum.txt","New_Spectrum")