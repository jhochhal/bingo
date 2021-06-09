import numpy as np
from collections import defaultdict
from .findIndex import*
from .operator_organize_command import organize_function
from .operator_organize_command import eval_function

def organizeEquation(stack,constants):
    Equations = {}
    for index,row in enumerate(stack):
        node,param1,param2 = row
        organize_function(node,param1,param2,index,stack,constants,Equations)
    keys = list(Equations)
    return Equations[keys[-1]], Equations

def organizeStack(Equation,WEquation):
    #1. orders of equation
    pows = pow_oder(Equation)
    #2. constant answer
    if len(Equation) == 1:
        keys = list(Equation)
        if isinstance(keys[0],int):
            newConstants = [Equation[1]]
            newCommand = [[1,0,0]]
            return np.array(newCommand), newConstants
    
    #3. generate x^0....x^k
    newCommand,newConstants = [],[]
    newCommand,newConstants,xPos,powPos = basicCommand(newCommand,newConstants,pows)
    #4. Design command
    NUM = 0
    lastRow = None

    for chain in Equation:
        # constant
        if (isinstance(chain,int)):
            NUM += Equation[chain]   
        else:
            const = Equation[chain]
            if const!=1:
                newConstants,const_ind = findConstantsIndex(newConstants,const)
                newCommand,const_line_ind = findCommandIndex(newCommand,[1,const_ind,const_ind])
                
            chain = list(chain)
            for index,ele in enumerate(chain):
                operator,node,POW = ele
                xind = powPos[node][POW]
                if index == 0:
                    lastInd = xind
                else:
                    newCommand,lastInd = findCommandIndex(newCommand,[4,lastInd,xind])
                        
            if const!=1:    
                newCommand,_ = findCommandIndex(newCommand,[4,const_line_ind,lastInd])
            if lastRow!=None:
                newCommand.append([2,lastRow,len(newCommand)-1])
            lastRow = len(newCommand)-1
            
    if NUM!=0:
        newConstants,ind = findConstantsIndex(newConstants,NUM)
        newCommand,line_ind = findCommandIndex(newCommand,[1,ind,ind])
        if lastRow!=None:
            newCommand.append([2,lastRow,len(newCommand)-1])
        lastRow = line_ind
    
    return np.array(newCommand), newConstants

def pow_oder(Equation):
    keys = list(Equation)
    pows = defaultdict(list)
    for key in keys:
        if (isinstance(key,int)):
            continue
        else:
            for ele in key:
                if ele[0] == 0:
                    pows[ele[1]].append(ele)

    for ele in pows:
        cur = pows[ele]
        cur.sort(key = lambda cur: cur[2])
        pows[ele] = cur

    return pows

def basicCommand(newCommand,newConstants,pows):
    xPos,powPos = {},{}
    for key in pows:
        cur_pows = pows[key]
        _, node, max_pow = cur_pows[-1]
        _, _, min_pow = cur_pows[0]
        # Generate X^0
        newCommand,xind = findCommandIndex(newCommand,[0,node,node])
        # In the case of 1/X
        if min_pow < 0:
            newConstants,oneCon = findConstantsIndex(newConstants,1)
            newCommand,oneind = findCommandIndex(newCommand,[1,oneCon,oneCon])
            newCommand,xinvind = findCommandIndex(newCommand,[5,oneind,xind])
            powPos[node] =  {-1: xinvind}
            pw = -1
            for i in range(powPos[node][-1], powPos[node][-1]+abs(min_pow)-1):
                newCommand.append([4,powPos[node][-1],i])
                pw-=1
                powPos[node][pw] = len(newCommand)-1
                
        xPos[node] = xind
        if node not in powPos:
            powPos[node] = {1: xPos[node]}
        else:
            powPos[node][1] = xPos[node]
        pw = 1
        for i in range(xPos[node],xPos[node]+max_pow-1):
            newCommand.append([4,xPos[node],i])
            pw+=1
            powPos[node][pw] = len(newCommand)-1
    return newCommand,newConstants,xPos,powPos
