def generate_af902bf9(diff_lb: float, diff_ub: float) -> dict:
    cols = remove(2, interval(0, 10, 1))
    h = unifint(diff_lb, diff_ub, (10, 30))
    w = unifint(diff_lb, diff_ub, (10, 30))
    bgc = choice(cols)
    remcols = remove(bgc, cols)
    numcols = unifint(diff_lb, diff_ub, (1, 8))
    ccols = sample(remcols, numcols)
    numsq = unifint(diff_lb, diff_ub, (1, (h * w) // 20))
    succ = 0
    maxtr = 5 * numsq
    tr = 0
    gi = canvas(bgc, (h, w))
    go = canvas(bgc, (h, w))
    inds = asindices(gi)
    while tr < maxtr and succ < numsq:
        tr += 1
        oh = randint(3, 5)
        ow = randint(3, 5)
        cands = sfilter(inds, lambda ij: ij[0] <= h - oh and ij[1] <= w - ow)
        if len(cands) == 0:
            continue
        loc = choice(totuple(cands))
        loci, locj = loc
        sq = backdrop(frozenset({(loci, locj), (loci + oh - 1, locj + ow - 1)}))
        if sq.issubset(inds):
            inds = inds - sq
            succ += 1
            col = choice(ccols)
            crns = corners(sq)
            gi = fill(gi, col, crns)
            go = fill(go, col, crns)
            ins = backdrop(inbox(crns))
            go = fill(go, 2, ins)
    return {'input': gi, 'output': go}

