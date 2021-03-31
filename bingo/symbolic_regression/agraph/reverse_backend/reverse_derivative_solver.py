import numpy as np
from bingo.symbolic_regression.agraph.evaluation_backend import evaluation_backend
from .DepthFirstSearch import DepthFirstSearch
from .DerivativeCommand import DerivativeCommand
from .findIndex import*

def _reverse_eval(deriv_wrt_node,x,stack,constants):
    # 1. make zero array
    try:
        zInd = constants.index(0.0)
        zero = [1,zInd,zInd]
    except:
        constants.append(0.0)
        zero = [1,len(constants)-1,len(constants)-1]
    # 2. No variable Return 0
    ev = evaluation_backend.evaluate(stack, x, constants).reshape(len(x))
    con = np.all(ev == ev[0])
    zeros = np.zeros(len(x))
    if np.allclose(ev, zeros, atol=10e-5) or con == True:
        return np.array([zero]), constants
    if con == True:
        try:
            nInd = constants.index(ev[0])
            return np.array([[1,nInd,nInd]]),constants
        except:
            constants.append(ev[0])
            return np.array([[1,len(constants)-1,len(constants)-1]]),constants
        
    # 3. Call paths
    row,col = stack.shape
    root = row-1
    paths, NUM, maxInd = DepthFirstSearch(root, stack, constants, deriv_wrt_node)
    

    # 4. No equation, Return constant 
    if maxInd == float('-inf'):
        try:
            nInd = constants.index(NUM)
            return np.array([[1,nInd,nInd]]),constants
        except:
            constants.append(NUM)
            return np.array([[1,len(constants)-1,len(constants)-1]]),constants
    # 5. Find derivative command array
    newStack,constants = DerivativeCommand(deriv_wrt_node, stack, constants,paths,NUM,maxInd,zero)
    newStack = np.array(newStack)
    return newStack,constants
