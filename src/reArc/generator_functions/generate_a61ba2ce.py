def generate_a61ba2ce(diff_lb: float, diff_ub: float) -> dict:
    cols = interval(0, 10, 1)
    h = unifint(diff_lb, diff_ub, (4, 15))
    w = unifint(diff_lb, diff_ub, (4, 15))
    lociL = randint(2, h - 2)
    lociR = randint(2, h - 2)
    locjT = randint(2, w - 2)
    locjB = randint(2, w - 2)
    bgc, c1, c2, c3, c4 = sample(cols, 5)
    ulco = connect((0, 0), (lociL - 1, 0)) | connect((0, 0), (0, locjT - 1))
    urco = connect((0, w - 1), (0, locjT)) | connect((0, w - 1), (lociR - 1, w - 1))
    llco = connect((h - 1, 0), (lociL, 0)) | connect((h - 1, 0), (h - 1, locjB - 1))
    lrco = connect((h - 1, w - 1), (h - 1, locjB)) | connect((h - 1, w - 1), (lociR, w - 1))
    go = canvas(bgc, (h, w))
    go = fill(go, c1, ulco)
    go = fill(go, c2, urco)
    go = fill(go, c3, llco)
    go = fill(go, c4, lrco)
    fullh = unifint(diff_lb, diff_ub, (2 * h, 30))
    fullw = unifint(diff_lb, diff_ub, (2 * w, 30))
    gi = canvas(bgc, (fullh, fullw))
    objs = (ulco, urco, llco, lrco)
    ocols = (c1, c2, c3, c4)
    while True:
        inds = asindices(gi)
        locs = []
        for o, c in zip(objs, ocols):
            cands = sfilter(inds, lambda ij: shift(o, ij).issubset(inds))
            if len(cands) == 0:
                break
            loc = choice(totuple(cands))
            locs.append(loc)
            inds = inds - shift(o, loc)
        if len(locs) == 4:
            break
    for o, c, l in zip(objs, ocols, locs):
        gi = fill(gi, c, shift(o, l))
    return {'input': gi, 'output': go}

