from collections import defaultdict
from .sameLine import *
from .findIndex import *
from .operator import reverse_function

def DepthFirstSearch(root, commands, constants, deriv_wrt_node):
    #1. Change numpy array to array list
    commands = commands.tolist()
    X = [0,deriv_wrt_node,deriv_wrt_node]
    
    paths,NUM = [],0
    MAX = float('-inf')
    SUM = defaultdict(float)
    
    if X not in commands:
        return SUM, NUM, MAX, commands, constants
    
    same = sameOrder(commands)
    #2. Iniitialize 
    stack = [([root],
              [1,[]])]
    
    #3. Main DFS algorithm 
    while stack:
        path, Answer = stack.pop()
        element = path[-1]
        array = commands[element]
        node,param1,param2 = array
        # Find answer
        if array == X:
            if len(Answer[1])==0:
                NUM += Answer[0]   
            else:
                Answer[1].sort()
                const,indexes = Answer
                if const!=0:
                    MAX = max(MAX,max(Answer[1]))
                    SUM[tuple(indexes)] += const
                    
        # Find path if node is not leaf
        if node!=0 and node!=1:
           
            reverse_function(node,param1,param2,path,Answer,commands,constants,same,stack)
           

    return SUM, NUM, MAX, commands,constants
