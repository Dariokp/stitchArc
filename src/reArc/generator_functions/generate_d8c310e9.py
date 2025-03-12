def generate_d8c310e9(diff_lb: float, diff_ub: float) -> dict:
    cols = interval(0, 10, 1)
    h = unifint(diff_lb, diff_ub, (3, 30))
    w = unifint(diff_lb, diff_ub, (10, 30))
    p = unifint(diff_lb, diff_ub, (2, (w - 1) // 3))
    bgc = choice(cols)
    remcols = remove(bgc, cols)
    numc = unifint(diff_lb, diff_ub, (1, 9))
    ccols = sample(remcols, numc)
    obj = set()
    for j in range(p):
        numcells = unifint(diff_lb, diff_ub, (1, h - 1))
        for ii in range(h - 1, h - numcells - 1, -1):
            loc = (ii, j)
            col = choice(ccols)
            cell = (col, loc)
            obj.add(cell)
    gi = canvas(bgc, (h, w))
    minobj = obj | shift(obj, (0, p))
    addonw = randint(0, p)
    addon = sfilter(obj, lambda cij: cij[1][1] < addonw)
    fullobj = minobj | addon
    leftshift = randint(0, addonw)
    fullobj = shift(fullobj, (0, -leftshift))
    gi = paint(gi, fullobj)
    go = tuple(e for e in gi)
    for j in range(w//(2*p)+2):
        go = paint(go, shift(fullobj, (0, j * 2 * p)))
    mfs = (identity, rot90, rot180, rot270)
    fn = choice(mfs)
    gi = fn(gi)
    go = fn(go)
    return {'input': gi, 'output': go}

