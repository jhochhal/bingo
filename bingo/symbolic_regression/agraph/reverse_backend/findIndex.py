
def findCommandIndex(stack,array):
    try:
        ind = stack.index(array)
    except:
        if array[0]==2 or array[0]==4:
            try:
                ind = stack.index([array[0],array[2],array[1]])
            except:
                stack.append(array)
                ind = len(stack)-1
        else:
            stack.append(array)
            ind = len(stack)-1
    return stack, ind

def findConstantsIndex(constants,element):
    try:
        ind = constants.index(element)
    except:
        constants.append(element)
        ind = len(constants)-1
    return constants, ind

