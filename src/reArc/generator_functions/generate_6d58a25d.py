def generate_6d58a25d(diff_lb: float, diff_ub: float) -> dict:
    cols = interval(0, 10, 1)
    shp = normalize(frozenset({
    (0, 0), (1, 0), (1, 1), (1, -1), (2, -1), (2, -2), (2, 1), (2, 2), (3, 3), (3, -3)
    }))
    h = unifint(diff_lb, diff_ub, (5, 30))
    w = unifint(diff_lb, diff_ub, (8, 30))
    bgc = choice(cols)
    remcols = remove(bgc, cols)
    c = canvas(bgc, (h, w))
    inds = totuple(asindices(c))
    c1 = choice(remcols)
    c2 = choice(remove(c1, remcols))
    loci = randint(0, h - 4)
    locj = randint(0, w - 7)
    plcd = shift(shp, (loci, locj))
    rem = difference(inds, plcd)
    nnoise = unifint(diff_lb, diff_ub, (1, max(1, len(rem) // 2 - 1)))
    nois = sample(rem, nnoise)
    gi = fill(c, c2, nois)
    gi = fill(gi, c1, plcd)
    ff = lambda ij: len(intersection(shoot(ij, (-1, 0)), plcd)) > 0
    trg = sfilter(nois, ff)
    gg = lambda ij: valmax(sfilter(plcd, lambda kl: kl[1] == ij[1]), first) + 1
    kk = lambda ij: connect((gg(ij), ij[1]), (h - 1, ij[1]))
    fullres = mapply(kk, trg)
    go = fill(gi, c2, fullres)
    rotf = choice((identity, rot90, rot180, rot270))
    gi = rotf(gi)
    go = rotf(go)
    return {'input': gi, 'output': go}

