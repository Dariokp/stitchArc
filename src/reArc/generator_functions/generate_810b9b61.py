def generate_810b9b61(diff_lb: float, diff_ub: float) -> dict:
    cols = difference(interval(0, 10, 1), (3,))
    h = unifint(diff_lb, diff_ub, (10, 30))
    w = unifint(diff_lb, diff_ub, (10, 30))
    bgc = choice(cols)
    remcols = remove(bgc, cols)
    ncols = unifint(diff_lb, diff_ub, (1, 6))
    ccols = sample(remcols, ncols)
    nobjs = unifint(diff_lb, diff_ub, (3, (h * w) // 10))
    succ = 0
    tr = 0
    maxtr = 5 * nobjs
    gi = canvas(bgc, (h, w))
    go = canvas(bgc, (h, w))
    inds = asindices(gi)
    while succ < nobjs and tr < maxtr:
        tr += 1
        oh = randint(3, 5)
        ow = randint(3, 5)
        cands = sfilter(inds, lambda ij: ij[0] <= h - oh and ij[1] <= w - ow)
        if len(cands) == 0:
            continue
        loc = choice(totuple(cands))
        loci, locj = loc
        obj = box(frozenset({(loci, locj), (loci + oh - 1, locj + ow - 1  )}))
        mfs = (identity, dmirror, cmirror, vmirror, hmirror)
        nmfs = choice((1, 2))
        for fn in sample(mfs, nmfs):
            obj = fn(obj)
            obj = normalize(obj)
        oh, ow = shape(obj)
        cands = sfilter(inds, lambda ij: ij[0] <= h - oh and ij[1] <= w - ow)
        if len(cands) == 0:
            continue
        loc = choice(totuple(cands))
        plcd = shift(obj, loc)
        if choice((True, False)):
            ninobjc = unifint(diff_lb, diff_ub, (1, len(plcd) - 1))
            inobj = frozenset(sample(totuple(plcd), ninobjc))
        else:
            inobj = plcd
        if inobj.issubset(inds):
            succ += 1
            inds = (inds - inobj) - mapply(dneighbors, inobj)
            col = choice(ccols)
            gi = fill(gi, col, inobj)
            go = fill(go, 3 if box(inobj) == inobj and min(shape(inobj)) > 2 else col, inobj)
    return {'input': gi, 'output': go}

