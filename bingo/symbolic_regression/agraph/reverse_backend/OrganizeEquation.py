import numpy as np
from collections import defaultdict
from .findIndex import*

def organizeCommand(stack,constants):
    rowEq = {}
    for ind,row in enumerate(stack):
        node,c1,c2 = row[0],row[1],row[2]
        if node == 0:
            rowEq[ind] = {1:1}
        elif node == 1:
            rowEq[ind] = {0:constants[c1]}
        else:
            if node == 2:
                curEq = defaultdict(float)
                for key in rowEq[c1]:
                    curEq[key] += rowEq[c1][key]
                for key in rowEq[c2]:
                    curEq[key] += rowEq[c2][key]
                rowEq[ind] = curEq
            elif node == 3:
                curEq = defaultdict(float)
                for key in rowEq[c1]:
                    curEq[key] += rowEq[c1][key]
                for key in rowEq[c2]:
                    curEq[key] -= rowEq[c2][key]
                rowEq[ind] = curEq
            elif node == 4:
                curEq = defaultdict(float)
                for key1 in rowEq[c1]:
                    for key2 in rowEq[c2]:
                        curEq[key1+key2]+=rowEq[c1][key1]*rowEq[c2][key2]
                rowEq[ind] = curEq
            elif node == 5:
                curEq = defaultdict(float)
                for key1 in rowEq[c1]:
                    for key2 in rowEq[c2]:
                        curEq[key1-key2]+=rowEq[c1][key1]/rowEq[c2][key2]
                rowEq[ind] = curEq
            
            elif node == 13:
                curEq = defaultdict(float)
                cRow = stack[c2]
                Rind = cRow[1]
                POW = constants[Rind]
                
                for key in rowEq[c1]:
                    curEq[key*POW] = rowEq[c1][key]
                rowEq[ind] = curEq
       
    return rowEq[len(stack)-1]


def newCommand(Equation):
    
    #1. orders of equation
    pows = list(Equation)
    pows.sort()
    #2. If zero
    if len(pows) == 0:
        newConstants = [0]
        newCommand = [[1,0,0]]
        return np.array(newCommand), newConstants
    #3. If constant
    if max(pows) == 0:
        newConstants = [Equation[0]]
        newCommand = [[1,0,0]]
        return np.array(newCommand), newConstants
    #4. Otherwise
    maxPow = pows[-1]
    newCommand = [[0,0,0]]
    xPos = 0
    powPos = {1:0}
    for i in range(maxPow-1):
        newCommand.append([4,xPos,i])
        powPos[i+2] = len(newCommand)-1
    
    newConstants = []
    lastRow = None
    for ind,POW in enumerate(pows):
        const = Equation[POW]
        if POW == 0:
            newConstants,ind = findConstantsIndex(newConstants,const)
            newCommand.append([1,ind,ind])
            lastRow = len(newCommand)-1
        elif POW == 1:
            newConstants,ind = findConstantsIndex(newConstants,const)
            newCommand.append([1,ind,ind])
            lastInd = len(newCommand)-1
            newCommand.append([4,lastInd,xPos])
            if lastRow!=None:
                newCommand.append([2,lastRow,len(newCommand)-1])
            lastRow = len(newCommand)-1
        else:
            newConstants,ind = findConstantsIndex(newConstants,const)
            newCommand.append([1,ind,ind])
            lastInd = len(newCommand)-1
            newCommand.append([4,powPos[POW],lastInd])
            
            if lastRow!=None:
                newCommand.append([2,lastRow,len(newCommand)-1])
            lastRow = len(newCommand)-1
    
    return np.array(newCommand), newConstants
