from collections import defaultdict
from .sameLine import *

def DepthFirstSearch(root, commands, constants, deriv_wrt_node):
    #1. Change commands to list
    commands = commands.tolist()
    X = [0,deriv_wrt_node,deriv_wrt_node]
    
    paths,NUM = [],0
    cnt = defaultdict(int)
    GMax = float('-inf')
    SUM = defaultdict(float)
    
    if X not in commands:
        return SUM, NUM, GMax
    
    same = sameOrder(commands)
    #2. Iniitialize 
    stack = [([root],
              [1,[]])]
             
    while stack:
        
        path, ANS = stack.pop()
        element = path[-1]
        
        array = commands[element]

        node = commands[element][0]
        children = [commands[element][1],commands[element][2]]
        
        if array == X:
            if len(ANS[1])==0:
                NUM += ANS[0]   
            else:
                GMax = max(GMax,max(ANS[1]))
                ANS[1].sort()
                
                const,indexes = ANS
                if const!=0:
                    SUM[tuple(indexes)] += const
                    
        if node!=0 and node!=1:
            if children:
                for cInd,c in enumerate(children):
                    newpath = path[:]
                    newpath += [c]
                    newANS= [ANS[0],ANS[1][:]]
                    
                    # Multiplication 
                    if node == 4:
                        if cInd == 0:
                            tmp = commands[children[1]]
                            if tmp[0] == 1:
                                newANS[0] *= constants[tmp[1]]
                            else:
                                if children[1] in same:
                                    newANS[1] += [same[children[1]]]
                                else:
                                    newANS[1] += [children[1]]
                                
                        else:
                            tmp = commands[children[0]]
                            if tmp[0] == 1:
                                newANS[0] *= constants[tmp[1]]
                            else:
                                if children[0] in same:
                                    newANS[1] += [same[children[0]]]
                                else:
                                    newANS[1] += [children[0]]
                                
                    # Add    
                    elif node == 2:
                        newANS[0] *= 1
                        
                    # Minus
                    elif node ==3 :
                        if children[0] == children[1]:
                            newANS[0] *= 0
                        else:    
                            if cInd == 0:
                                newANS[0] *= 1
                            else:
                                newANS[0] *= -1

                    
                    stack.append((newpath,newANS))

    return SUM, NUM, GMax
