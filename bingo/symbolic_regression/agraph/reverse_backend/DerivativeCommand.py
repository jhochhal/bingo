import numpy as np
from .findIndex import*

def DerivativeCommand(deriv_wrt_node, stack, constants,paths,NUM,maxInd):

    # 0. Initialization           
    newStack = stack[:maxInd+1].tolist()
    
    lastInd = None
   
    # 1. Main algorithm
    for path in paths:
        const = paths[path]
        indexes = list(path)
        n = len(indexes)
        if n == 1:
            if const == 1:
                curInd = indexes[0]
            else:
                constants,cInd = findConstantsIndex(constants,const)
                cLine = [1,cInd,cInd]
                newStack,cArrInd = findCommandIndex(newStack,cLine)    
                newStack.append([4,cArrInd, indexes[0]])
                curInd = len(newStack)-1
                
        else:
            if n == 2:
                newStack.append([4,indexes[0],indexes[1]])
                rInd = len(newStack)-1
            else:
                newStack.append([4,indexes[0],indexes[1]])
                for i in range(2,len(indexes)):
                    index = indexes[i]
                    curL = len(newStack)-1
                    newStack.append([4,index,curL])
                    
                rInd = len(newStack)-1
                
            if const==1:
                curInd = rInd
                
            else:
                constants,cInd = findConstantsIndex(constants,const)
                cLine = [1,cInd,cInd]
                newStack,cArrInd = findCommandIndex(newStack,cLine)    
                newStack.append([4,cArrInd, rInd])
                curInd = len(newStack)-1
            
        if lastInd != None:
            newStack.append([2,lastInd,curInd])
            curInd = len(newStack)-1
            
        # Switch lastInd     
        lastInd = curInd
    
    if NUM!=0:
        constants,nInd = findConstantsIndex(constants,NUM)
        newStack.append([1,nInd,nInd])
        ind1,ind2 = len(newStack)-1,len(newStack)-2
        newStack.append([2,ind1,ind2])
    
    return newStack,constants
