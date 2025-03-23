def solution(n, control):
    key = dict(zip(['w','a','s','d'], [1,-1,10,-10]))
    for c in control:
        n += key[c]

    return n
