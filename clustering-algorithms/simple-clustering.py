def clustering(S):
    ''' Simple clustering algorithm for finding the mode
        of a dataset with some tolerance
    '''
    X = sorted(S)
    tol = (X[-1] - X[0]) / len(X)
    Y = [ len(interval_intersection((x-tol, x+tol), X)) for x in X ]
    mode_mag = max(Y)
    modes = []

    for i, y in enumerate(Y):
        if y == mode_mag:
            modes.append(X[i])

    return modes

def interval_intersection(S, I):
    ''' Computes the intersection of a list and an interval
        does not remove duplicates in the list
    '''
    assert len(I) == 2
   
    X = sorted(S)
    I = sorted(I)
    
    i = 0
    while X[i] < I[0]:
        i += 1
    
    j = -1
    while X[j] > T[1]:
        j -= 1

    Y = [ X[i] for i in range(i, len(X) + j + 1) ]
    return Y
