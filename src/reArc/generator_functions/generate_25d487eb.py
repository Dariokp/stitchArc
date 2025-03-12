def generate_25d487eb(diff_lb: float, diff_ub: float) -> dict:
    cols = interval(0, 10, 1)
    h = unifint(diff_lb, diff_ub, (10, 30))
    w = unifint(diff_lb, diff_ub, (10, 30))
    bgc = choice(cols)
    remcols = remove(bgc, cols)
    ncols = unifint(diff_lb, diff_ub, (2, 8))
    ccols = sample(remcols, ncols)
    gi = canvas(bgc, (h, w))
    go = canvas(bgc, (h, w))
    nobjs = unifint(diff_lb, diff_ub, (1, (h * w) // 30))
    succ = 0
    tr = 0
    maxtr = 10 * nobjs
    inds = asindices(go)
    while tr < maxtr and succ < nobjs:
        if len(inds) == 0:
            break
        tr += 1
        dim = randint(1, 3)
        obj = backdrop(frozenset({(0, 0), (dim, dim)}))
        obj = sfilter(obj, lambda ij: ij[0] <= ij[1])
        obj = obj | shift(vmirror(obj), (0, dim))
        mp = {(0, dim)}
        tric, linc = sample(ccols, 2)
        inobj = recolor(tric, obj - mp) | recolor(linc, mp)
        loc = choice(totuple(inds))
        iplcd = shift(inobj, loc)
        loci, locj = loc
        oplcd = iplcd | recolor(linc, connect((loci, locj + dim), (h - 1, locj + dim)) - toindices(iplcd))
        fullinds = asindices(gi)
        oplcdi = toindices(oplcd)
        if oplcdi.issubset(inds):
            succ += 1
            gi = paint(gi, iplcd)
            go = paint(go, oplcd)
        rotf = choice((identity, rot90, rot180, rot270))
        gi = rotf(gi)
        go = rotf(go)
        h, w = shape(gi)
        ofc = ofcolor(go, bgc)
        inds = ofc - mapply(dneighbors, asindices(go) - ofc)
    return {'input': gi, 'output': go}

