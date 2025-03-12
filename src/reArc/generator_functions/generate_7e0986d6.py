def generate_7e0986d6(diff_lb: float, diff_ub: float) -> dict:
    cols = interval(0, 10, 1)
    h = unifint(diff_lb, diff_ub, (10, 30))
    w = unifint(diff_lb, diff_ub, (10, 30))
    bgc = choice(cols)
    remcols = remove(bgc, cols)
    nsqcols = unifint(diff_lb, diff_ub, (1, 5))
    sqcols = sample(remcols, nsqcols)
    remcols = difference(remcols, sqcols)
    nnoisecols = unifint(diff_lb, diff_ub, (1, len(remcols)))
    noisecols = sample(remcols, nnoisecols)
    numsq = unifint(diff_lb, diff_ub, (1, (h * w) // 25))
    succ = 0
    tr = 0
    maxtr = 5 * numsq
    go = canvas(bgc, (h, w))
    inds = asindices(go)
    while tr < maxtr and succ < numsq:
        tr += 1
        oh = randint(2, 7)
        ow = randint(2, 7)
        cands = sfilter(inds, lambda ij: ij[0] <= h - oh and ij[1] <= w - ow)
        if len(cands) == 0:
            continue
        loc = choice(totuple(cands))
        loci, locj = loc
        sq = backdrop(frozenset({(loci, locj), (loci + oh - 1, locj + ow - 1)}))
        if sq.issubset(inds):
            succ += 1
            inds = (inds - sq) - outbox(sq)
            col = choice(sqcols)
            go = fill(go, col, sq)
    gi = tuple(e for e in go)
    namt = unifint(diff_lb, diff_ub, (1, (h * w) // 9))
    cands = asindices(gi)
    for k in range(namt):
        if len(cands) == 0:
            break
        loc = choice(totuple(cands))
        col = gi[loc[0]][loc[1]]
        torem = neighbors(loc) & ofcolor(gi, col)
        cands = cands - torem
        noisec = choice(noisecols)
        gi = fill(gi, noisec, {loc})
    return {'input': gi, 'output': go}

