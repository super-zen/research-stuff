def sinkholes(S, factor=1):
    X = sorted(S)
    step = (X[-1] - X[0]) / len(X)
    Y = [ X[0] + step/factor*i for i in range(factor*len(X)+1) ]
    counters = [ 0 for y in Y ]
    
    for x in X:
        idx = 0

        while x > Y[idx]:
            idx += 1

            if idx >= len(Y):
                idx = len(Y) - 1
                break

        if abs(Y[idx] - x) < abs(Y[idx-1] - x):
            counters[idx] += 1

        else:
            counters[idx-1] += 1

    mode_mag = max(counters)
    modes = []

    for i, c in enumerate(counters):
        if c == mode_mag:
            modes.append(Y[i])
    
    return modes

