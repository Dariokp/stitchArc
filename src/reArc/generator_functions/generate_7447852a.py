def generate_7447852a(diff_lb: float, diff_ub: float) -> dict:
    cols = remove(4, interval(0, 10, 1))
    w = unifint(diff_lb, diff_ub, (2, 8))
    h = unifint(diff_lb, diff_ub, (w+1, 30))
    bgc, linc = sample(cols, 2)
    remcols = remove(bgc, remove(linc, cols))
    c = canvas(bgc, (h, w))
    sp = (h - 1, 0)
    gi = fill(c, linc, {sp})
    direc = 1
    while True:
        sp = add(sp, (-1, direc))
        if sp[1] == w - 1 or sp[1] == 0:
            direc *= -1
        gi2 = fill(gi, linc, {sp})
        if gi2 == gi:
            break
        gi = gi2
    gi = rot90(gi)
    objs = objects(gi, T, F, F)
    inds = ofcolor(gi, bgc)
    numcols = unifint(diff_lb, diff_ub, (1, 7))
    ccols = sample(remcols, numcols)
    ncells = unifint(diff_lb, diff_ub, (0, len(inds)))
    locs = sample(totuple(inds), ncells)
    obj = {(choice(ccols), ij) for ij in locs}
    gi = paint(gi, obj)
    go = tuple(e for e in gi)
    objs = order(colorfilter(objs, bgc), leftmost)
    objs = merge(set(objs[0::3]))
    go = fill(go, 4, objs)
    return {'input': gi, 'output': go}

