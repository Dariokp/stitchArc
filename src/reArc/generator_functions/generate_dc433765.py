def generate_dc433765(diff_lb: float, diff_ub: float) -> dict:
    cols = remove(4, interval(0, 10, 1))
    h = unifint(diff_lb, diff_ub, (4, 30))
    w = unifint(diff_lb, diff_ub, (4, 30))
    bgc, src = sample(cols, 2)
    gi = canvas(bgc, (h, w))
    go = canvas(bgc, (h, w))
    inds = asindices(gi)
    if choice((True, False)):
        opts = {(ii, 0) for ii in range(h - 2)} | {(0, jj) for jj in range(1, w - 2, 1)}
        opts = tuple([inds & shoot(src, (1, 1)) for src in opts])
        opts = order(opts, size)
        k = len(opts)
        opt = unifint(diff_lb, diff_ub, (0, k - 1))
        ln = order(opts[opt], first)
        epi = unifint(diff_lb, diff_ub, (2, len(ln) - 1))
        ep = ln[epi]
        ln = ln[:epi-1][::-1]
        spi = unifint(diff_lb, diff_ub, (0, len(ln) - 1))
        sp = ln[spi]
        gi = fill(gi, src, {sp})
        gi = fill(gi, 4, {ep})
        go = fill(go, src, {add(sp, (1, 1))})
        go = fill(go, 4, {ep})
    else:
        loci = randint(0, h - 1)
        objw = unifint(diff_lb, diff_ub, (3, w))
        locj1 = randint(0, w - objw)
        locj2 = locj1 + objw - 1
        sp = (loci, locj1)
        ep = (loci, locj2)
        gi = fill(gi, src, {sp})
        gi = fill(gi, 4, {ep})
        go = fill(go, src, {add(sp, (0, 1))})
        go = fill(go, 4, {ep})
    mfs = (identity, dmirror, cmirror, vmirror, hmirror, rot90, rot180, rot270)
    nmfs = choice((1, 2))
    for fn in sample(mfs, nmfs):
        gi = fn(gi)
        go = fn(go)
    return {'input': gi, 'output': go}

