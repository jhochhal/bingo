import numpy as np
from .findIndex import *
from bingo.symbolic_regression.agraph.operator_definitions import *

# Load x column (0)
def _loadx(_param1,_param2,_path,_answer,_commands,_constants,_same,_stack):
    pass

# Load constant (1)
def _loadc(_param1,_param2,_path,_answer,_commands,_constants,_same,_stack):
    pass

# Addition (2)
def _add(param1,param2,path,answer,_commands,_constants,_same,stack):
    newpath1,newpath2 = path[:],path[:]
    newAnswer1,newAnswer2 = [answer[0],answer[1][:]],[answer[0],answer[1][:]]
    newpath1 += [param1]
    newpath2 += [param2]
    # param1
    newAnswer1[0] *= 1
    # param2
    newAnswer2[0] *= 1
    stack.append((newpath1,newAnswer1))
    stack.append((newpath2,newAnswer2)) 

# Subtraction (3)
def _subtract(param1,param2,path,answer,_commands,_constants,_same,stack):
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
        
    stack.append((newpath1,newAnswer1))
    stack.append((newpath2,newAnswer2)) 

# Multiplication (4)
def _multiply(param1,param2,path,answer,commands,constants,same,stack):
    newpath1,newpath2 = path[:],path[:]
    newAnswer1,newAnswer2 = [answer[0],answer[1][:]],[answer[0],answer[1][:]]
    newpath1 += [param1]
    newpath2 += [param2]

    # param1
    array1 = commands[param2]
    node1,c1,_ = array1
    if node1 == 1:
        newAnswer1[0] *= constants[c1]
    else:
        if param2 in same:
            newAnswer1[1] += [same[param2]]
        else:
            newAnswer1[1] += [param2]

    # param2
    array2 = commands[param1]
    node2,c2,_ = array2
    if node2 == 1:
        newAnswer2[0] *= constants[c2]
    else:
        if param1 in same:
            newAnswer2[1] += [same[param1]]
        else:
            newAnswer2[1] += [param1]

    stack.append((newpath1,newAnswer1))
    stack.append((newpath2,newAnswer2))

# Division (5)
def _divide(param1,param2,path,answer,commands,constants,same,stack):
    newpath1,newpath2 = path[:],path[:]
    newAnswer1,newAnswer2 = [answer[0],answer[1][:]],[answer[0],answer[1][:]]
    newpath1 += [param1]
    newpath2 += [param2]

    _, one_ele = findConstantsIndex(constants,1)
    _, one_ind = findCommandIndex(commands,[1,one_ele,one_ele])
    
    # param1
    array1 = commands[param2]
    node1,c1,_ = array1
    if node1 == 1:
        newAnswer1[0] *= 1/constants[c1]
    else:
        if param2 in same:
            _, denom_ind = findCommandIndex(commands,[5,one_ind,same[param2]])
            newAnswer1[1] += [denom_ind]
        else:
            _, denom_ind = findCommandIndex(commands,[5,one_ind,param2])
            newAnswer1[1] += [denom_ind]

    # param2
    array2 = commands[param1]
    node2,c2,_ = array2
    if node2 == 1 and node1==1:
        newAnswer2[0] *= - constants[c2]/(constants[c1]**2)
    else:
        if node2 == 1 and node1 != 1:
            newAnswer2[0] *= - constants[c2]
            _, denom2_ind = findCommandIndex(commands,[4,denom_ind,denom_ind])
            newAnswer2[1] += [denom2_ind]
            
        elif node2 != 1 and node1 == 1:
            newAnswer2[0] *= - 1/(constants[c1]**2)
            if param1 in same:
                newAnswer2[1] += [same[param1]]
            else:
                newAnswer2[1] += [param1]
        else:
            _, denom2_ind = findCommandIndex(commands,[4,denom_ind,denom_ind])
            if param1 in same:
                _, line_ind = findCommandIndex(commands,[4,denom2_ind,same[param1]])
                newAnswer2[0] *= -1
                newAnswer2[1] += [line_ind]
            else:
                _, line_ind = findCommandIndex(commands,[4,denom2_ind,param1])
                newAnswer2[0] *= -1
                newAnswer2[1] += [line_ind]
            
    stack.append((newpath1,newAnswer1))
    stack.append((newpath2,newAnswer2))

# Sine (6)
def _sin(param1,param2,path,answer,commands,constants,same,stack):
    newpath = path[:]
    newpath += [param1]
    newAnswer = [answer[0],answer[1][:]]
    
    array = commands[param1]
    node,c1,c2 = array
    if node == 1:
        newAnswer[0] *= np.cos(constants[c1])
    else:
        _,ind = findCommandIndex(commands,[7,param1,param2])
        if ind in same:
            newAnswer[1] += [same[ind]]
        else:
            newAnswer[1] += [ind]
    
    stack.append((newpath,newAnswer))

# Cosine (7)
def _cos(param1,param2,path,answer,commands,constants,same,stack):
    newpath = path[:]
    newpath += [param1]
    newAnswer = [answer[0],answer[1][:]]
    
    array = commands[param1]
    node,c1,c2 = array
    if node == 1:
        newAnswer[0] *= - np.sin(constants[c1])
    else:
        newAnswer[0] *= -1
        _,ind = findCommandIndex(commands,[6,param1,param2])
        if ind in same:
            newAnswer[1] += [same[ind]]
        else:
            newAnswer[1] += [ind]
            
    stack.append((newpath,newAnswer))

# Reverse function        
def reverse_function(node,param1,param2,path,answer,commands,constants,same,stack):
    return MAP[node](param1,param2,path,answer,commands,constants,same,stack)    


MAP = {VARIABLE: _loadx,
       CONSTANT: _loadc,
       ADDITION: _add,
       SUBTRACTION: _subtract,
       MULTIPLICATION: _multiply,
       DIVISION: _divide,
       SIN: _sin,
       COS: _cos}





    
    
