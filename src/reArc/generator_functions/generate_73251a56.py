def generate_73251a56(diff_lb: float, diff_ub: float) -> dict:
    cols = interval(0, 10, 1)
    while True:
        d = unifint(diff_lb, diff_ub, (10, 30))
        h, w = d, d
        noisec = choice(cols)
        remcols = remove(noisec, cols)
        nsl = unifint(diff_lb, diff_ub, (2, min(9, h//2)))
        slopes = [0] + sorted(sample(interval(1, h-1, 1), nsl - 1))
        ccols = sample(cols, nsl)
        gi = canvas(-1, (h, w))
        inds = asindices(gi)
        for col, hdelt in zip(ccols, slopes):
            slope = hdelt / w
            locs = sfilter(inds, lambda ij: slope * ij[1] <= ij[0])
            gi = fill(gi, col, locs)
        ln = connect((0, 0), (d - 1, d - 1))
        gi = fill(gi, ccols[-2], ln)
        obj = asobject(gi)
        obj = sfilter(obj, lambda cij: cij[1][1] >= cij[1][0])
        gi = paint(gi, dmirror(obj))
        cf1 = lambda g: ccols[-2] in palette(toobject(ln, g))
        cf2 = lambda g: len((ofcolor(g, noisec) & frozenset({ij[::-1] for ij in ofcolor(g, noisec)})) - ln) == 0
        ndist = unifint(diff_lb, diff_ub, (1, (h * w) // 15))
        tr = 0
        succ = 0
        maxtr = 10 * ndist
        go = tuple(e for e in gi)
        while tr < maxtr and succ < ndist:
            tr += 1
            oh = randint(1, 5)
            ow = randint(1, 5)
            loci = randint(1, h - oh - 1)
            locj = randint(1, w - ow - 1)
            bd = backdrop(frozenset({(loci, locj), (loci + oh - 1, locj + ow - 1)}))
            gi2 = fill(gi, noisec, bd)
            if cf1(gi2) and cf2(gi2):
                succ += 1
                gi = gi2
        if gi != go:
            break
    rotf = choice((identity, rot90, rot180, rot270))
    gi = rotf(gi)
    go = rotf(go)
    return {'input': gi, 'output': go}

