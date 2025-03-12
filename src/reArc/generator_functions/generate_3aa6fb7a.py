def generate_3aa6fb7a(diff_lb: float, diff_ub: float) -> dict:
    base = (ORIGIN, RIGHT, DOWN, UNITY)
    cols = remove(1, interval(0, 10, 1))
    h = unifint(diff_lb, diff_ub, (3, 30))
    w = unifint(diff_lb, diff_ub, (3, 30))
    bgc = choice(cols)
    remcols = remove(bgc, cols)
    fgc = choice(remcols)
    gi = canvas(bgc, (h, w))
    inds = totuple(asindices(gi))
    maxnum = ((h * w) // 2) // 3
    num = unifint(diff_lb, diff_ub, (1, maxnum))
    kk, tr = 0, 0
    maxtrials = num * 2
    binds = set()
    while kk < num and tr < maxtrials:
        loc = choice(inds)
        ooo = choice(base)
        oo = remove(ooo, base)
        oop = shift(oo, loc)
        if set(oop).issubset(inds):
            inds = difference(inds, totuple(combine(oop, totuple(mapply(dneighbors, oop)))))
            gi = fill(gi, fgc, oop)
            binds.add(add(ooo, loc))
            kk += 1
        tr += 1
    go = fill(gi, 1, binds)
    return {'input': gi, 'output': go}

