def generate_d89b689b(diff_lb: float, diff_ub: float) -> dict:
    cols = remove(5, interval(0, 10, 1))
    h = unifint(diff_lb, diff_ub, (4, 30))
    w = unifint(diff_lb, diff_ub, (4, 30))
    bgc, sqc, a, b, c, d = sample(cols, 6)
    loci = randint(1, h - 3)
    locj = randint(1, w - 3)
    canv = canvas(bgc, (h, w))
    go = fill(canv, a, {(loci, locj)})
    go = fill(go, b, {(loci, locj+1)})
    go = fill(go, c, {(loci+1, locj)})
    go = fill(go, d, {(loci+1, locj+1)})
    inds = totuple(asindices(canv))
    aopts = sfilter(inds, lambda ij: ij[0] < loci and ij[1] < locj)
    bopts = sfilter(inds, lambda ij: ij[0] < loci and ij[1] > locj + 1)
    copts = sfilter(inds, lambda ij: ij[0] > loci + 1 and ij[1] < locj)
    dopts = sfilter(inds, lambda ij: ij[0] > loci + 1 and ij[1] > locj + 1)
    aopts = order(aopts, lambda ij: manhattan({ij}, {(loci, locj)}))
    bopts = order(bopts, lambda ij: manhattan({ij}, {(loci, locj + 1)}))
    copts = order(copts, lambda ij: manhattan({ij}, {(loci + 1, locj)}))
    dopts = order(dopts, lambda ij: manhattan({ij}, {(loci + 1, locj + 1)}))
    aidx = unifint(diff_lb, diff_ub, (0, len(aopts) - 1))
    bidx = unifint(diff_lb, diff_ub, (0, len(bopts) - 1))
    cidx = unifint(diff_lb, diff_ub, (0, len(copts) - 1))
    didx = unifint(diff_lb, diff_ub, (0, len(dopts) - 1))
    loca = aopts[aidx]
    locb = bopts[bidx]
    locc = copts[cidx]
    locd = dopts[didx]
    gi = fill(canv, sqc, backdrop({(loci, locj), (loci + 1, locj + 1)}))
    gi = fill(gi, a, {loca})
    gi = fill(gi, b, {locb})
    gi = fill(gi, c, {locc})
    gi = fill(gi, d, {locd})
    return {'input': gi, 'output': go}

