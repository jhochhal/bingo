import numpy as np
from .findIndex import *
from bingo.symbolic_regression.agraph.operator_definitions import *

# Load x column
def _loadx(_param1,_param2,_path,_answer,_stack,_constants,_same):
    pass

# Load constant
def _loadc(_param1,_param2,_path,_answer,_stack,_constants,_same):
    pass

# Addition
def _add(param1,param2,path,answer,_stack,_constants,_same):
    newpath1,newpath2 = path[:],path[:]
    newAnswer1,newAnswer2 = [answer[0],answer[1][:]],[answer[0],answer[1][:]]
    newpath1 += [param1]
    newpath2 += [param2]
    # param1
    newAnswer1[0] *= 1
    # param2
    newAnswer2[0] *= 1
    return newpath1,newAnswer1,newpath2,newAnswer2 

# Subtraction
def _subtract(param1,param2,path,answer,_stack,_constants,_same):
    newpath1,newpath2 = path[:],path[:]
    newAnswer1,newAnswer2 = [answer[0],answer[1][:]],[answer[0],answer[1][:]]
    newpath1 += [param1]
    newpath2 += [param2]
    if param1 == param2:
        # param1
        newAnswer1[0] *= 0
        # param2
        newAnswer2[0] *= 0
    else:
        # param1
        newAnswer1[0] *= 1
        # param2
        newAnswer2[0] *= -1
    return newpath1,newAnswer1,newpath2,newAnswer2 

# Multiplication
def _multiply(param1,param2,path,answer,stack,constants,same):
    newpath1,newpath2 = path[:],path[:]
    newAnswer1,newAnswer2 = [answer[0],answer[1][:]],[answer[0],answer[1][:]]
    newpath1 += [param1]
    newpath2 += [param2]

    # param1
    array1 = stack[param2]
    node1,c1,_ = array1
    if node1 == 1:
        newAnswer1[0] *= constants[c1]
    else:
        if param2 in same:
            newAnswer1[1] += [same[param2]]
        else:
            newAnswer1[1] += [param2]

    # param2
    array2 = stack[param1]
    node2,c2,_ = array2
    if node2 == 1:
        newAnswer2[0] *= constants[c2]
    else:
        if param1 in same:
            newAnswer1[1] += [same[param1]]
        else:
            newAnswer2[1] += [param1]

    return newpath1,newAnswer1,newpath2,newAnswer2

# Sine
def _sin(param1,param2,path,answer,stack,constants,same):
    newpath = path[:]
    newpath += [param1]
    newAnswer = [answer[0],answer[1][:]]
    
    array = stack[param1]
    node,c1,c2 = array
    if node == 1:
        newAnswer[0] *= np.cos(constants[c1])
    else:
        _,ind = findCommandIndex(stack,[7,param1,param2])
        if ind in same:
            newAnswer[1] += [same[ind]]
        else:
            newAnswer[1] += [ind]
    
    return newpath, newAnswer, None, None

# Cosine
def _cos(param1,param2,path,answer,stack,constants,same):
    newpath = path[:]
    newpath += [param1]
    newAnswer = [answer[0],answer[1][:]]
    
    array = stack[param1]
    node,c1,c2 = array
    if node == 1:
        newAnswer[0] *= - np.sin(constants[c1])
    else:
        newAnswer[0] *= -1
        _,ind = findCommandIndex(stack,[6,param1,param2])
        if ind in same:
            newAnswer[1] += [same[ind]]
        else:
            newAnswer[1] += [ind]
    return newpath, newAnswer, None, None

# Reverse function        
def reverse_function(node,param1,param2,path,answer,stack,constants,same):
    return MAP[node](param1,param2,path,answer,stack,constants,same)    


MAP = {VARIABLE: _loadx,
       CONSTANT: _loadc,
       ADDITION: _add,
       SUBTRACTION: _subtract,
       MULTIPLICATION: _multiply,
       SIN: _sin,
       COS: _cos}





    
    
