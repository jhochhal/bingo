def OrderOfEquation(stack, deriv_with_node):
    rowRank = {}
    for ind,line in enumerate(stack):
        node,c1,c2 = line
        # X_0, X_1, or X_n
        if node == 0:
            if c1 == deriv_with_node:
                rowRank[ind] = 1
            else:
                rowRank[ind] = 0
        
        # Constant
        elif node == 1:
            rowRank[ind] = 0
        # Other operators
        else:
            # Add or Subtraction
            if node == 2 or node == 3:
                rowRank[ind] = max(rowRank[c1],rowRank[c2])
            # Multiplication
            elif node == 4:
                rowRank[ind] = rowRank[c1] + rowRank[c2]
            # Sine or Cosine
            elif node == 6 or node == 7:
                if rowRank[c1]!=0 or rowRank[c2]!=0:
                    rowRank[ind] = float('inf')
                else:
                    rowRank[ind] = 0
                    
    return rowRank[len(stack)-1]
