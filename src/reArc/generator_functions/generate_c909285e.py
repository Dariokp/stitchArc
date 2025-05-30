def generate_c909285e(diff_lb: float, diff_ub: float) -> dict:
    cols = interval(0, 10, 1)
    h = unifint(diff_lb, diff_ub, (5, 30))
    w = unifint(diff_lb, diff_ub, (5, 30))
    nfronts = unifint(diff_lb, diff_ub, (1, (h + w) // 2))
    bgc = choice(cols)
    remcols = remove(bgc, cols)
    boxcol = choice(remcols)
    remcols = remove(boxcol, remcols)
    gi = canvas(bgc, (h, w))
    inds = totuple(asindices(gi))
    for k in range(nfronts):
        ff = choice((hfrontier, vfrontier))
        loc = choice(inds)
        inds = remove(loc, inds)
        col = choice(remcols)
        gi = fill(gi, col, ff(loc))
    oh = unifint(diff_lb, diff_ub, (3, max(3, (h - 2) // 2)))
    ow = unifint(diff_lb, diff_ub, (3, max(3, (w - 2) // 2)))
    loci = randint(1, h - oh - 1)
    locj = randint(1, w - ow - 1)
    bx = box(frozenset({(loci, locj), (loci + oh - 1, locj + ow - 1)}))
    gi = fill(gi, boxcol, bx)
    go = subgrid(bx, gi)
    return {'input': gi, 'output': go}

