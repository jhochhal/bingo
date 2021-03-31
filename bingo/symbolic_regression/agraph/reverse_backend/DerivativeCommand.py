import numpy as np
from .findIndex import*

def DerivativeCommand(deriv_wrt_node, stack, constants,paths,NUM,maxInd,zero):

    # 0. Initialization           
    newStack = stack[:maxInd+1].tolist()
    lastInd = None

    # 1. Insert zero array to stack
    newStack,zArrInd = findCommandIndex(newStack,zero)
    info = {}
    # 2. Main algorithm
    for path in paths:
        const = paths[path]
        indexes = list(path)
        n = len(indexes)
        if n == 1:
            if const == 1:
                curInd = indexes[0]
            elif const == -1:
                newStack.append([3,zArrInd, indexes[0]])
                curInd = len(newStack)-1
            else:
                constants,cInd = findConstantsIndex(constants,const)
                cLine = [1,cInd,cInd]
                newStack,cArrInd = findCommandIndex(newStack,cLine)    
                newStack.append([4,cArrInd, indexes[0]])
                curInd = len(newStack)-1
                
        else:
            if n == 2:
                cur = tuple(indexes[:2])
                if cur in info:
                    rInd = info[cur]
                else:
                    newStack.append([4,indexes[0],indexes[1]])
                    info[cur] = len(newStack)-1
                    rInd = len(newStack)-1
            else:
                mInd = None
                for i in range(1,len(indexes)):
                    cur = tuple(indexes[:i+1])
                    if cur in info:
                        mInd = len(cur)
                        irInd = info[cur]
                        
                if mInd == None:
                    newStack.append([4,indexes[0],indexes[1]])
                    
                    cur = tuple(indexes[:2])
                    info[cur] = len(newStack)-1
                    for i in range(2,len(indexes)):
                        index = indexes[i]
                        curL = len(newStack)-1
                        newStack.append([4,index,curL])
                        
                        cur = tuple(indexes[:i+1])
                        info[cur] = len(newStack)-1
                    rInd = len(newStack)-1
                    
                else:
                    if mInd > len(indexes)-1:
                        rInd = irInd
                    else:
                        newStack.append([4,irInd,indexes[mInd]])
                        cur = tuple(indexes[:mInd+1])
                        info[cur] = len(newStack)-1
                        if  mInd == len(indexes)-1:
                            rInd = len(newStack)-1
                        else:
                            for i in range(mInd+1,len(indexes)):
                                index = indexes[i]
                                curL = len(newStack)-1
                                newStack.append([4,index,curL])
                                
                                cur = tuple(indexes[:i+1])
                                info[cur] = len(newStack)-1
                            rInd = len(newStack)-1
            if const==1:
                curInd = rInd

            elif const==-1:
                newStack.append([3,zArrInd, rInd])
                curInd = len(newStack)-1
                
            elif abs(const)!=1:
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

