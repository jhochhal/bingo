def OrderOfEquation(stack):
    rowRank = {}
    for ind,line in enumerate(stack):
        node,c1,c2 = line[0],line[1],line[2]
        if node == 0:
            rowRank[ind] = 1
        elif node == 1:
            rowRank[ind] = 0
        else:
            if node == 2 or node == 3:
                rowRank[ind] = max(rowRank[c1],rowRank[c2])
            elif node == 4:
                rowRank[ind] = rowRank[c1] + rowRank[c2]
                
    return rowRank[len(stack)-1]
