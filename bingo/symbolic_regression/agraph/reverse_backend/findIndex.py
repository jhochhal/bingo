
def findCommandIndex(stack,array):
    try:
        ind = stack.index(array)
    except:
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

