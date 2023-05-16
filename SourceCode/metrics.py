import numpy as np
import math

def ochiai(c, e):
    numFailingTests = (e > 0).sum()
    numExecutions = (c > 0).sum()
    numExecutionsFailed = (e[(c > 0)] > 0).sum()
    if numExecutionsFailed == 0:
        score = 0
    else:
        score = (numExecutionsFailed / math.sqrt(numExecutions * numFailingTests))
    return score

def tarantula(c, e):
    numFailingTests = (e > 0).sum()
    numPassingTests = (e == 0).sum()
    numExecutionsFailed = (e[(c > 0)] > 0).sum()
    numExecutionssPassed = (e[(c > 0)] == 0).sum()
    term1 = numExecutionsFailed / numFailingTests
    if numPassingTests == 0:
        term2 = 0
    else:
        term2 = numExecutionssPassed / numPassingTests
    if term1 == 0:
        return 0
    else:
        return (term1 / (term1 + term2))

def kulczynski(c, e):
    power = 1   #dstar is Kulczynski if power = 1
    numExecutionsFailed = (e[(c > 0)] > 0).sum()
    numExecutionssPassed = (e[(c > 0)] == 0).sum()
    numUncoveredFailed = (e[(c == 0)] > 0).sum()
    denominator = numExecutionssPassed + numUncoveredFailed
    if denominator == 0:
        return 1
    else:
        return (numExecutionsFailed ** power) / denominator

def dstar2(c, e):
    power = 2   #dstar is Kulczynski if power = 1
    numExecutionsFailed = (e[(c > 0)] > 0).sum()
    numExecutionssPassed = (e[(c > 0)] == 0).sum()
    numUncoveredFailed = (e[(c == 0)] > 0).sum()
    denominator = numExecutionssPassed + numUncoveredFailed
    if denominator == 0:
        return 1
    else:
        return (numExecutionsFailed ** power) / denominator

def dstar3(c, e):
    power = 3   #dstar is Kulczynski if power = 1
    numExecutionsFailed = (e[(c > 0)] > 0).sum()
    numExecutionssPassed = (e[(c > 0)] == 0).sum()
    numUncoveredFailed = (e[(c == 0)] > 0).sum()
    denominator = numExecutionssPassed + numUncoveredFailed
    if denominator == 0:
        return 1
    else:
        return (numExecutionsFailed ** power) / denominator

def op2(c, e):
    numExecutionsFailed = (e[(c > 0)] > 0).sum()
    numExecutionssPassed = (e[(c > 0)] == 0).sum()
    numTotalPassed = (e == 0).sum()
    score = numExecutionsFailed - (numExecutionssPassed / (numTotalPassed + 1))
    return score

def barinel(c, e):
    numExecutionsFailed = (e[(c > 0)] > 0).sum()
    numTotalExecuted = (c > 0).sum()
    if numTotalExecuted == 0:
        return 0
    else:
        return (numExecutionsFailed / numTotalExecuted)