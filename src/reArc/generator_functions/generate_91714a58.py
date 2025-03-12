def generate_91714a58(diff_lb: float, diff_ub: float) -> dict:
    cols = interval(0, 10, 1)
    h = unifint(diff_lb, diff_ub, (6, 30))
    w = unifint(diff_lb, diff_ub, (6, 30))
    bgc, targc = sample(cols, 2)
    remcols = remove(bgc, cols)
    nnoise = unifint(diff_lb, diff_ub, (1, (h * w) // 2))
    gi = canvas(bgc, (h, w))
    inds = totuple(asindices(gi))
    noise = sample(inds, nnoise)
    ih = randint(2, h // 2)
    iw = randint(2, w // 2)
    loci = randint(0, h - ih)
    locj = randint(0, w - iw)
    loc = (loci, locj)
    bd = backdrop(frozenset({(loci, locj), (loci + ih - 1, locj + iw - 1)}))
    go = fill(gi, targc, bd)
    for ij in noise:
        col = choice(remcols)
        gi = fill(gi, col, {ij})
    gi = fill(gi, targc, bd)
    return {'input': gi, 'output': go}

