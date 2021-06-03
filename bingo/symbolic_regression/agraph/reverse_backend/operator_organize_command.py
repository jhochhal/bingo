import numpy as np
from .findIndex import *
from collections import defaultdict
from bingo.symbolic_regression.agraph.operator_definitions import *

# Load x column (0)
def _loadx(param1,param2,index,stack,constants,Equations):
    # (X, param1, power): coefficient
    Equations[index] = {((0, param1, 1),):1}
    
# Load constant (1)
def _loadc(param1,param2,index,stack,constants,Equations):
    Equations[index] = {1:constants[param1]}

# Addition (2)
def _add(param1,param2,index,stack,constants,Equations):
    curEq = defaultdict(float)
    for p in [param1,param2]:
        for node in Equations[p]:
            curEq[node] += Equations[p][node]
            
    Equations[index] = curEq

# Subtraction (3)
def _subtract(param1,param2,index,stack,constants,Equations):
    curEq = defaultdict(float)
    for ind,p in enumerate([param1,param2]):
        for node in Equations[p]:
            if ind == 0:
                curEq[node] += Equations[p][node]
            else:
                curEq[node] -= Equations[p][node]
                    
    Equations[index] = curEq

# Multiplication (4)
def _multiply(param1,param2,index,stack,constants,Equations):
    curEq = defaultdict(float)
    for node1 in Equations[param1]:
        for node2 in Equations[param2]:
            if (isinstance(node1,int)) and (isinstance(node2,int)):
                curEq[node1] += Equations[param1][node1]*Equations[param2][node2]
            elif (isinstance(node1,int)) and not (isinstance(node2,int)):
                curEq[node2] += Equations[param1][node1]*Equations[param2][node2]
            elif not (isinstance(node1,int)) and (isinstance(node2,int)):
                curEq[node1] += Equations[param1][node1]*Equations[param2][node2]
            else:
                tmp = {}
                list1,list2 = list(node1),list(node2)
                for ele in list1:
                    tmp[(ele[0],ele[1])] = ele[2]

                for ele in list2:
                    if (ele[0],ele[1]) in tmp:
                        tmp[(ele[0],ele[1])] += ele[2]
                    else:
                        tmp[(ele[0],ele[1])] = ele[2]

                nd = []
                for key in tmp:
                    POW = tmp[key]
                    nd.append((key[0],key[1],POW))
            
                nd = tuple(nd)
                
                curEq[nd] += Equations[param1][node1]*Equations[param2][node2]
                        
        
    Equations[index] = curEq
    
# Division (5)
def _divide(param1,param2,index,stack,constants,Equations):
    curEq = defaultdict(float)
    for node1 in Equations[param1]:
        for node2 in Equations[param2]:
            if (isinstance(node1,int)) and (isinstance(node2,int)):
                curEq[node1] += Equations[param1][node1]/Equations[param2][node2]
            elif (isinstance(node1,int)) and not (isinstance(node2,int)):
                new_node2 = (node2[0],-node2[1])
                curEq[new_node2] += Equations[param1][node1]/Equations[param2][node2]
            elif not (isinstance(node1,int)) and (isinstance(node2,int)):
                curEq[node1] += Equations[param1][node1]/Equations[param2][node2]
            else:
                tmp = {}
                list1,list2 = list(node1),list(node2)
                for ele in list1:
                    tmp[(ele[0],ele[1])] = ele[2]

                for ele in list2:
                    if (ele[0],ele[1]) in tmp:
                        tmp[(ele[0],ele[1])] -= ele[2]
                    else:
                        tmp[(ele[0],ele[1])] = -ele[2]

                nd = []
                for key in tmp:
                    POW = tmp[key]
                    nd.append((key[0],key[1],POW))
            
                nd = tuple(nd)
                curEq[nd] += Equations[param1][node1]/Equations[param2][node2]
                
    Equations[index] = curEq

# Sine (6)
def _sin(param1,param2,index,stack,constants,Equations):
    curEq = defaultdict(float)
    if len(Equations[param1]) == 1:
        node = list(Equations[param1])
        if node == 1:
            curEq[1] = np.sin(Equations[param1][1])
    
    curEq[((6,param1,1),)] = 1
            
    Equations[index] = curEq
    
def sin_eval(num):
    return np.sin(num)

# Sine (7)
def _cos(param1,param2,index,stack,constants,Equations):
    curEq = defaultdict(float)
    if len(Equations[param1]) == 1:
        node = list(Equations[param1])
        if node == 1:
            curEq[1] = np.cos(Equations[param1][1])
    
    curEq[((7,param1,1),)] = 1
            
    Equations[index] = curEq

def cos_eval(num):
    return np.cos(num)  


# organize function        
def organize_function(node,param1,param2,index,stack,constants,Equations):
    return MAP[node](param1,param2,index,stack,constants,Equations)    

# eval function 
def eval_function(node,num):
    return MAP_eval[node](num)

MAP = {VARIABLE: _loadx,
       CONSTANT: _loadc,
       ADDITION: _add,
       SUBTRACTION: _subtract,
       MULTIPLICATION: _multiply,
       DIVISION: _divide,
       SIN: _sin,
       COS: _cos}

MAP_eval = {SIN: sin_eval,
            COS: cos_eval}


