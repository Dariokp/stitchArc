def generate_ff28f65a(diff_lb: float, diff_ub: float) -> dict:
    cols = difference(interval(0, 10, 1), (1, 2))
    mpr = {1: (0, 0), 2: (0, 2), 3: (1, 1), 4: (2, 0), 5: (2, 2)}
    h = unifint(diff_lb, diff_ub, (3, 30))
    w = unifint(diff_lb, diff_ub, (3, 30))
    bgc = choice(cols)
    nred = randint(1, 5)
    gi = canvas(bgc, (h, w))
    succ = 0
    tr = 0
    maxtr = 5 * nred
    inds = asindices(gi)
    while tr < maxtr and succ < nred:
        tr += 1
        oh = randint(1, h//2+1)
        ow = randint(1, w//2+1)
        cands = sfilter(inds, lambda ij: ij[0] <= h - oh and ij[1] <= w - ow)
        if len(cands) == 0:
            continue
        loc = choice(totuple(cands))
        loci, locj = loc
        bd = backdrop(frozenset({(loci, locj), (loci+oh-1, locj+ow-1)}))
        if bd.issubset(inds):
            succ += 1
            inds = (inds - bd) - mapply(dneighbors, bd)
            gi = fill(gi, 2, bd)
    nblue = succ
    namt = unifint(diff_lb, diff_ub, (0, nred * 2))
    succ = 0
    tr = 0
    maxtr = 5 * namt
    remcols = remove(bgc, cols)
    tr += 1
    while tr < maxtr and succ < namt:
        tr += 1
        oh = randint(1, h//2+1)
        ow = randint(1, w//2+1)
        cands = sfilter(inds, lambda ij: ij[0] <= h - oh and ij[1] <= w - ow)
        if len(cands) == 0:
            continue
        loc = choice(totuple(cands))
        loci, locj = loc
        bd = backdrop(frozenset({(loci, locj), (loci+oh-1, locj+ow-1)}))
        if bd.issubset(inds):
            succ += 1
            inds = (inds - bd) - mapply(dneighbors, bd)
            gi = fill(gi, choice(remcols), bd)
    go = canvas(bgc, (3, 3))
    for k in range(nblue):
        go = fill(go, 1, {mpr[k+1]})
    return {'input': gi, 'output': go}

