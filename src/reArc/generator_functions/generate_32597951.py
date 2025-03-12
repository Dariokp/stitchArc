def generate_32597951(diff_lb: float, diff_ub: float) -> dict:
    cols = remove(3, interval(0, 10, 1))
    h = unifint(diff_lb, diff_ub, (10, 30))
    w = unifint(diff_lb, diff_ub, (10, 30))
    ih = unifint(diff_lb, diff_ub, (2, h // 2))
    iw = unifint(diff_lb, diff_ub, (2, w // 2))
    bgc, noisec, fgc = sample(cols, 3)
    c = canvas(bgc, (h, w))
    inds = totuple(asindices(c))
    ndev = unifint(diff_lb, diff_ub, (1, (h * w) // 2))
    num = choice((ndev, h * w - ndev))
    num = min(max(num, 0), h * w)
    ofc = sample(inds, num)
    c = fill(c, noisec, ofc)
    loci = randint(0, h - ih)
    locj = randint(0, w - iw)
    bd = backdrop(frozenset({(loci, locj), (loci + ih - 1, locj + iw - 1)}))
    tofillfc = bd & ofcolor(c, bgc)
    gi = fill(c, fgc, tofillfc)
    if len(tofillfc) > 0:
        go = fill(gi, 3, backdrop(tofillfc) & ofcolor(gi, noisec))
    else:
        go = gi
    return {'input': gi, 'output': go}

