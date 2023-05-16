from csv import reader
import numpy as np
from artemis import *
from metrics import *
import math
import matplotlib.pyplot as plt
import random
import os
import sys

def load_csv(filename):
    file = open(filename, "rt")
    lines = reader(file)
    dataset = list(lines)
    return dataset

def str_column_to_float(dataset, column):
    for row in dataset:
        row[column] = int(row[column].strip())

def save3DArray(toSave, array):
    arr_reshaped = array.reshape(array.shape[0], -1)
    np.savetxt(toSave, arr_reshaped)


def checkEffort(finalList, buggyset, cmapping, numcomp):
    perBugEffort = np.zeros(len(buggyset))
    perBugRank = np.zeros(len(buggyset))
    devsEffort = np.zeros(1)
    bugsFoundCount = 0
    numBugs = len(buggyset)
    currRank = 0
    nextRank = currRank + 1
    while currRank <= finalList.shape[0]:
        bugsFoundInThisCheck = 0
        toCheck = finalList[currRank:nextRank]
        for i in range(toCheck.shape[0]):
            devsEffort[i] = devsEffort[i] + (cmapping == int(toCheck[i])).sum()
            if toCheck[i] in buggyset:
                buggyset.remove(toCheck[i])
                bugsFoundInThisCheck += 1
        if bugsFoundInThisCheck > 0:
            for i in range(bugsFoundInThisCheck):
                perBugEffort[bugsFoundCount] = float(max(devsEffort) / numcomp)
                perBugRank[bugsFoundCount] = max(devsEffort)
                bugsFoundCount = bugsFoundCount + 1
        currRank = nextRank
        nextRank = currRank + 1
        if bugsFoundCount == numBugs:
            break
    return perBugEffort, perBugRank

def runSelectionForMetric(sbflMetric, project):
    abspath = 'allSpectrums/'
    parameterPath = 'ParameterSelection/'
    pGrid = np.arange(0.1, 0.01, 0.001, 0.0001, 0.00001)
    betaGrid = range(5, 105, 5)
    muGrid = range(1, 21)
    gridEffortMean = np.zeros((len(pGrid), len(betaGrid), len(muGrid)))
    gridEffortMedian = np.zeros((len(pGrid), len(betaGrid), len(muGrid)))
    gridZ = 0
    for p in pGrid:
        gridX = 0    
        for maxUniverse in betaGrid:            
            gridY = 0
            for numUniverse in muGrid:                
                refEffortMean = []
                refEffortMedian = []               
                foldPath = abspath
                detailsPath = foldPath + 'Details.txt'
                file1 = open(detailsPath, 'r')
                Lines = file1.readlines()
                file1.close()
                Lines.pop(0)
                k = 0
                for line in Lines:                   
                    k = k + 1
                    line = line.strip('\n')
                    splitStr = line.split(',')
                    s = splitStr[0]
                    origName = s
                    s = s[:-12]
                    fname = s
                    if project in fname:
                        continue
                    spath = foldPath + fname + 'Reduced_Spectrum.txt'
                    spec = load_csv(spath)
                    for i in range(len(spec[0])):
                        str_column_to_float(spec, i)
                    spec = np.array(spec)
                    activityMatrix = spec[:, :-1]
                    errorVector = spec[:, -1]
                    if errorVector.sum() < 1:
                        continue
                    if activityMatrix.shape[1] < numUniverse:
                        continue
                    refinementFlag = True
                    rankingList = explorer(activityMatrix, errorVector.copy(), activityMatrix.shape[1], sbflMetric, numUniverse, maxUniverse, p)
                    finalList = merge(rankingList, activityMatrix.shape[1])
                    numcomponents = 0                   
                    with open((foldPath + origName), "r") as File:
                        read = reader(File,delimiter=' ')
                        for row in read:                            
                            numcomponents = len(row) - 1
                            break
                    cmapping = np.zeros(numcomponents)
                    bpath = foldPath + fname + 'Candidates.txt'
                    mpath = foldPath + fname + 'Reduced_Spectrum_ComponentMap.txt'
                    file = open(mpath, 'r')
                    mappings = file.readlines()
                    for item in mappings:
                        item = item.strip('\n')
                        m = item.split(',')
                        for i in range(1, len(m)):
                            cmapping[int(m[i])] = int(m[0])
                    file.close()
                    file = open(bpath, 'r')
                    buggy = file.readlines()
                    buggy = buggy[0].strip('\n')
                    buggy = buggy.split(',')
                    if len(buggy) < 2:
                        continue                    
                    buggyset = set()
                    for item in buggy:
                        buggyset.add(int(cmapping[int(item) - 1]))
                    file.close()
                    toremove = set()
                    for item in buggyset:
                        x = spec[:, int(item)]
                        if sum(x) == 0:
                            toremove.add(item)
                        else:
                            e = spec[:, -1]
                            x = np.where(x == 1)
                            e = e[x]
                            if sum(e) == 0:
                                toremove.add(item)
                    buggyset = buggyset - toremove
                    bugs = buggyset.copy()
                    bugs1 = bugs.copy()
                    if len(buggyset) >= 1:
                        universeEffort, universeRank = checkEffort(finalList, buggyset.copy(), cmapping, numcomponents)
                        refEffortMean.append(np.mean(universeEffort))
                        refEffortMedian.append(np.median(universeEffort))
                gridEffortMean[gridZ, gridX, gridY] = np.mean(refEffortMean)
                gridEffortMedian[gridZ, gridX, gridY] = np.mean(refEffortMedian)
                gridY = gridY + 1
            gridX = gridX + 1
        gridZ = gridZ + 1

    toSaveMean = parameterPath + sbflMetric.__name__ + 'ParameterSelectionMeanFold' + project + '.txt'
    toSaveMedian = parameterPath + sbflMetric.__name__ + 'ParameterSelectionMedianFold' + project + '.txt'
    save3DArray(toSaveMean, gridEffortMean)
    save3DArray(toSaveMedian, gridEffortMedian)

def callParameterSelection(project):
    parameterPath = 'ParameterSelection/'
    if not os.path.exists(parameterPath):
        os.mkdir(parameterPath)
    for metric in (ochiai, tarantula, kulczynski, dstar2, op2, barinel):
        print('Running Parameter Selection For : ' + metric.__name__)
        runSelectionForMetric(metric, project)

if __name__ == '__main__':
    project = sys.argv[1]
    print('Running parameter section for fold : ' + project)
    callParameterSelection(project)


