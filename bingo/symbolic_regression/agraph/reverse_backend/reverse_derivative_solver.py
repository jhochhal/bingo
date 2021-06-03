import numpy as np
from .DepthFirstSearch import DepthFirstSearch
from .DerivativeCommand import DerivativeCommand
from .OrganizeEquation import *
from .OrganizeEquation2 import *
from .findIndex import*

def _reverse_eval(deriv_wrt_node,stack,constants,simplify):
    #1. Simplify equation
    if simplify:
        Eq,wEq = organizeEquation(stack,constants)
        stack, constants = organizeStack(Eq,wEq)
        #Equation = organizeCommand(stack,constants)
        #stack, constants = newCommand(Equation)

        
    #2. Find paths
    row,col = stack.shape
    root = row-1
    paths, NUM, maxInd,stack,constants = DepthFirstSearch(root, stack, constants, deriv_wrt_node)
    stack = np.array(stack)
    
    #3. Return value
    if maxInd == float('-inf'):
        try:
            nInd = constants.index(NUM)
            return np.array([[1,nInd,nInd]]),constants
        except:
            constants.append(NUM)
            return np.array([[1,len(constants)-1,len(constants)-1]]),constants
    
    #4. Main Derivative algorithm
    newStack,constants = DerivativeCommand(deriv_wrt_node, stack, constants,paths,NUM,maxInd)
    newStack = np.array(newStack)
   
    return newStack,constants