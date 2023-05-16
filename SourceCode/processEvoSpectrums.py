from csv import reader
from operator import contains
from posixpath import abspath
import numpy as np
import shutil
from scipy.stats import wilcoxon
import os
from preProcess import *

def load_csv(filename):
    file = open(filename, "rt")
    lines = reader(file)
    dataset = list(lines)
    return dataset

def str_column_to_float(dataset, column):
    for row in dataset:
        row[column] = int(row[column].strip())

def PreProcessBugs(bugPath, project, bugNum, run, spectraPath, sOutName):
    BLdata=[]
    bName = bugPath + '/' + project + '-' + str(bugNum) + '.buggy.lines'
    cName = bugPath + '/' + project + '-' + str(bugNum) + '.candidates'
    bOutName = sOutName + '_Candidates.txt'

    try:
        with open(bName,"r")as F:
            reader=csv.reader(F,delimiter='#')
            for row in reader:
                BLdata.append(row)
    except:
        return False
    
    index=0
    spectra={}
    codeLine={}
    
    with open(spectraPath,"r") as F:
        reader=csv.reader(F,delimiter=':')
        for row in reader:
            if index !=0:
                spectra[index]=row
                if row[-1] not in codeLine:
                    temp=list()
                    temp.append([row[0],index])
                    codeLine[row[-1]]=temp
                else:
                    #print("Check This Case")
                    temp=codeLine[row[-1]]
                    temp.append([row[0],index])
                    codeLine[row[-1]]=temp
            index+=1
    """
    BLdata=[]
    with open(buggy_lines+"/"+str(d)+".buggy.lines","r")as F:
        reader=csv.reader(F,delimiter='#');
        for row in reader:
            BLdata.append(row)
    """
    GT=[]
    for row in BLdata:
        if row[-1]=="FAULT_OF_OMISSION":
            #print("Fault emission")
            Candidate_data=[]
            with open(cName,"r") as F:
                reader=csv.reader(F,delimiter=',')
                for Canrow in reader:
                    #-------------------------------------------
                    #print("Root : ",Canrow[0].split("#")[-1])
                    if Canrow[0].split("#")[-1]== row[1]:
                        #print(row[1],Canrow)
                        Candidate_data.append(Canrow[1])
            for C in Candidate_data:
                bl_name=C.split(".")[0].split("/")[-1]
                cl=C.split("#")[-1]
                if cl not in codeLine:
                    #print("Entry:",C,"Not present in Spectra File in ",Bfolder)
                    continue
                entries=codeLine[cl]
                for entry in entries:
                    if entry[0].split("#")[0].split("$")[-1]==bl_name:
                        #print(row[0:2],entry)
                        if entry[-1] not in GT:
                            GT.append(entry[-1])                
                #print(bl_name)           
                
        else:
            if row[1] not in codeLine:
                #print("Entry:",row[0:2],"Not present in Spectra File in ",Bfolder)
                continue
            for entry in codeLine[row[1]]:
                #print(row[0:2],entry)
                entry_name=entry[0].split("#")[0].split("$")[-1]
                col_no=entry[-1]
                bl_name=row[0].split(".")[0].split("/")[-1]
                if entry_name==bl_name:
                    if col_no not in GT:
                        GT.append(col_no)
                """
                spectra_colname=[0]
                spectra_colname=spectra_colname.split("#")[0].split("$")[-1]
                bl_name=row[0]
                bl_name=bl_name.split(".")[0].split("/")[-1];
                if spectra_colname==bl_name:
                    GT.append(codeLine[row[1]][1])
                print("Easily Handled",spectra_colname ,bl_name)
                """
    #Write GT values to a File
    with open(bOutName,"w") as F:
        writer=csv.writer(F)
        writer.writerow(GT)
    
    return True
    


projects = ('Chart', 'Closure', 'Lang', 'Math', 'Mockito', 'Time')
projectContains = [26, 133, 65, 106, 38, 27]
abspath = '/home/alex/d4jcoverage/d4j_Spectrums_Coverage/'
outPath = '/home/alex/processData/'
bugPath = '/home/alex/d4jbuggyLines/buggy-lines/'
method = 'coverage'
methodCap = 'VRDDU'
specName = 'matrix.txt'
mapName = 'spectra.csv'
f = open("Details.txt", "a")

for projectNum in range(len(projects)):
    project = projects[projectNum]
    for run in range(1, 6):
        for bugNum in range(1, projectContains[projectNum] + 1):
            spath = abspath + 'evo_' + project + '_' + method + str(run) + '/bug' + str(bugNum) + '/' + str(run) + '/fl/fault_localization_log/' + project + '/evosuite-' + methodCap + '/' + str(bugNum) + 'b.' + str(bugNum) + '.sfl/txt/'
            print(project + ' ' + str(run) + ' ' + str(bugNum))
            # input()
            if os.path.exists(spath):
                sName = spath + specName
                mName = spath + mapName
                if os.path.isfile(sName) and os.path.isfile(mName) and os.path.getsize(sName) > 0:
                    sOutName = project + '_bug' + str(bugNum) + '_' + method + str(run)
                    retStatus = PreProcessBugs(bugPath, project, bugNum, run, mName, sOutName)
                    if retStatus:                        
                        origName = sOutName + '_Spectrum.txt'
                        shutil.copyfile(sName, origName)
                        PreProcessSpectrum(sName, sOutName)                        
                        toWrite = origName + ',0,0,0,0,0,0\n'
                        f.write(toWrite)
                    #input()
                    
f.close()
