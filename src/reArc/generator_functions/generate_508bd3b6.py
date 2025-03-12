def generate_508bd3b6(diff_lb: float, diff_ub: float) -> dict:
    cols = remove(3, interval(0, 10, 1))
    h = unifint(diff_lb, diff_ub, (5, 30))
    w = unifint(diff_lb, diff_ub, (h, 30))
    barh = unifint(diff_lb, diff_ub, (1, h // 2))
    barloci = unifint(diff_lb, diff_ub, (2, h - barh))
    bgc = choice(cols)
    remcols = remove(bgc, cols)
    barc = choice(remcols)
    remcols = remove(barc, remcols)
    linc = choice(remcols)
    gi = canvas(bgc, (h, w))
    for j in range(barloci, barloci + barh):
        gi = fill(gi, barc, connect((j, 0), (j, w - 1)))
    dotlociinv = unifint(diff_lb, diff_ub, (0, barloci - 1))
    dotloci = min(max(0, barloci - 2 - dotlociinv), barloci - 1)
    ln1 = shoot((dotloci, 0), (1, 1))
    ofbgc = ofcolor(gi, bgc)
    ln1 = sfilter(ln1 & ofbgc, lambda ij: ij[0] < barloci)
    ln1 = order(ln1, first)
    ln2 = shoot(ln1[-1], (-1, 1))
    ln2 = sfilter(ln2 & ofbgc, lambda ij: ij[0] < barloci)
    ln2 = order(ln2, last)[1:]
    ln = ln1 + ln2
    k = len(ln1)
    lineleninv = unifint(diff_lb, diff_ub, (0, k - 2))
    linelen = k - lineleninv
    givenl = ln[:linelen]
    reml = ln[linelen:]
    gi = fill(gi, linc, givenl)
    go = fill(gi, 3, reml)
    mfs = (identity, dmirror, cmirror, vmirror, hmirror, rot90, rot180, rot270)
    nmfs = choice((1, 2))
    for fn in sample(mfs, nmfs):
        gi = fn(gi)
        go = fn(go)
    return {'input': gi, 'output': go}

