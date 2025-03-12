def generate_8e1813be(diff_lb: float, diff_ub: float) -> dict:
    cols = interval(0, 10, 1)
    bgc, sqc = sample(cols, 2)
    remcols = remove(bgc, remove(sqc, cols))
    nbars = unifint(diff_lb, diff_ub, (3, 8))
    ccols = sample(remcols, nbars)
    w = unifint(diff_lb, diff_ub, (nbars+3, 30))
    hmarg = unifint(diff_lb, diff_ub, (2 * nbars, 30 - nbars))
    ccols = list(ccols)
    go = tuple(repeat(col, nbars) for col in ccols)
    gi = tuple(repeat(col, w) for col in ccols)
    r = repeat(bgc, w)
    for k in range(hmarg):
        idx = randint(0, len(go) - 1)
        gi = gi[:idx] + (r,) + gi[idx:]
    h2 = nbars + hmarg
    oh, ow = nbars, nbars
    loci = randint(1, h2 - oh - 2)
    locj = randint(1, w - ow - 2)
    sq = backdrop(frozenset({(loci, locj), (loci + oh - 1, locj + ow - 1)}))
    gi = fill(gi, sqc, sq)
    gi = fill(gi, bgc, outbox(sq))
    if choice((True, False)):
        gi = dmirror(gi)
        go = dmirror(go)
    return {'input': gi, 'output': go}

