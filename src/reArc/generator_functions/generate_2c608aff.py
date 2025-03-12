def generate_2c608aff(diff_lb: float, diff_ub: float) -> dict:
    cols = interval(0, 10, 1)    
    h = unifint(diff_lb, diff_ub, (10, 30))
    w = unifint(diff_lb, diff_ub, (10, 30))
    boxh = unifint(diff_lb, diff_ub, (2, h // 2))
    boxw = unifint(diff_lb, diff_ub, (2, w // 2))
    loci = randint(0, h - boxh)
    locj = randint(0, w - boxw)
    bgc = choice(cols)
    remcols = remove(bgc, cols)
    ccol = choice(remcols)
    remcols = remove(ccol, remcols)
    dcol = choice(remcols)
    bd = backdrop(frozenset({(loci, locj), (loci + boxh - 1, locj + boxw - 1)}))
    gi = canvas(bgc, (h, w))
    gi = fill(gi, ccol, bd)
    reminds = totuple(asindices(gi) - backdrop(outbox(bd)))
    noiseb = max(1, len(reminds) // 4)
    nnoise = unifint(diff_lb, diff_ub, (0, noiseb))
    noise = sample(reminds, nnoise)
    gi = fill(gi, dcol, noise)
    go = tuple(e for e in gi)
    hs = interval(loci, loci + boxh, 1)
    ws = interval(locj, locj + boxw, 1)
    for ij in noise:
        a, b = ij
        if a in hs:
            go = fill(go, dcol, connect(ij, (a, locj)))
        elif b in ws:
            go = fill(go, dcol, connect(ij, (loci, b)))
    go = fill(go, ccol, bd)
    return {'input': gi, 'output': go}

