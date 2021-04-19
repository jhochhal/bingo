from collections import defaultdict

def sameOrder(stack):
    rowInfo = {}
    index = {}
    for ind,row in enumerate(stack):
        if row[0] == 2 or row[0] == 4:
            row = [row[0],min(row[1],row[2]),max(row[1],row[2])]
            row = tuple(row)
            if row not in rowInfo:
                rowInfo[row] = ind
            else:
                index[ind]=rowInfo[row]
        else:
            row = tuple(row)
            if row not in rowInfo:
                rowInfo[row] = ind
            else:
                index[ind]=rowInfo[row]
            
    return index
