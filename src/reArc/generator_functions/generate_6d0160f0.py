def generate_6d0160f0(diff_lb: float, diff_ub: float) -> dict:
    cols = difference(interval(0, 10, 1), (4,))
    h = unifint(diff_lb, diff_ub, (2, 5))
    w = unifint(diff_lb, diff_ub, (2, 5))
    nh, nw = h, w
    bgc, linc = sample(cols, 2)
    fullh = h * nh + nh - 1
    fullw = w * nw + nw - 1
    gi = canvas(bgc, (fullh, fullw))
    for iloc in range(h, fullh, h+1):
        gi = fill(gi, linc, hfrontier((iloc, 0)))
    for jloc in range(w, fullw, w+1):
        gi = fill(gi, linc, vfrontier((0, jloc)))
    noccs = unifint(diff_lb, diff_ub, (1, h * w))
    denseinds = asindices(canvas(-1, (h, w)))
    sparseinds = {(a*(h+1), b*(w+1)) for a, b in denseinds}
    locs = sample(totuple(sparseinds), noccs)
    trgtl = choice(locs)
    remlocs = remove(trgtl, locs)
    ntrgt = unifint(diff_lb, diff_ub, (1, (h * w - 1)))
    place = choice(totuple(denseinds))
    ncols = unifint(diff_lb, diff_ub, (1, 9))
    ccols = sample(cols, ncols)
    candss = totuple(remove(place, denseinds))
    trgrem = sample(candss, ntrgt)
    trgrem = {(choice(ccols), ij) for ij in trgrem}
    trgtobj = {(4, place)} | trgrem
    go = paint(gi, shift(sfilter(trgtobj, lambda cij: cij[0] != linc), multiply(place, increment((h, w)))))
    gi = paint(gi, shift(trgtobj, trgtl))
    toleaveout = ccols
    for rl in remlocs:
        tlo = choice(totuple(ccols))
        ncells = unifint(diff_lb, diff_ub, (1, h * w - 1))
        inds = sample(totuple(denseinds), ncells)
        obj = {(choice(remove(tlo, ccols) if len(ccols) > 1 else ccols), ij) for ij in inds}
        toleaveout = remove(tlo, toleaveout)
        gi = paint(gi, shift(obj, rl))
    return {'input': gi, 'output': go}

