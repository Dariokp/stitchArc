def generate_e509e548(diff_lb: float, diff_ub: float) -> dict:
    cols = difference(interval(0, 10, 1), (1, 2, 6))
    getL = lambda h, w: connect((0, 0), (h - 1, 0)) | connect((0, 0), (0, w - 1))
    getU = lambda h, w: connect((0, 0), (0, w - 1)) | connect((0, 0), (randint(1, h - 1), 0)) | connect((0, w - 1), (randint(1, h - 1), w - 1))
    getH = lambda h, w: connect((0, 0), (0, w - 1)) | shift(connect((0, 0), (h - 1, 0)) | connect((h - 1, 0), (h - 1, randint(1, w - 1))), (0, randint(1, w - 2)))
    minshp_getter_pairs = ((2, 2, getL), (2, 3, getU), (3, 3, getH))
    colmapper = {getL: 1, getU: 6, getH: 2}
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
        minh, minw, getter = choice(minshp_getter_pairs)
        oh = randint(minh, 6)
        ow = randint(minw, 6)
        obj = getter(oh, ow)
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
        if plcd.issubset(inds):
            succ += 1
            inds = (inds - plcd) - mapply(dneighbors, plcd)
            col = choice(ccols)
            gi = fill(gi, col, plcd)
            go = fill(go, colmapper[getter], plcd)
    return {'input': gi, 'output': go}

