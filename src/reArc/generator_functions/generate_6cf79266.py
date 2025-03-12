def generate_6cf79266(diff_lb: float, diff_ub: float) -> dict:
    cols = difference(interval(0, 10, 1), (0, 1))
    h = unifint(diff_lb, diff_ub, (6, 30))
    w = unifint(diff_lb, diff_ub, (6, 30))
    nfgcs = unifint(diff_lb, diff_ub, (1, 8))
    ccols = sample(cols, nfgcs)
    gi = canvas(-1, (h, w))
    fgcobj = {(choice(ccols), ij) for ij in asindices(gi)}
    gi = paint(gi, fgcobj)
    num = unifint(diff_lb, diff_ub, (int(0.25 * h * w), int(0.6 * h * w)))
    inds = asindices(gi)
    locs = sample(totuple(inds), num)
    gi = fill(gi, 0, locs)
    noccs = unifint(diff_lb, diff_ub, (1, (h * w) // 16))
    cands = asindices(canvas(-1, (h - 2, w - 2)))
    locs = sample(totuple(cands), noccs)
    mini = asindices(canvas(-1, (3, 3)))
    for ij in locs:
        gi = fill(gi, 0, shift(mini, ij))
    trg = recolor(0, mini)
    occs = occurrences(gi, trg)
    go = tuple(e for e in gi)
    for occ in occs:
        go = fill(go, 1, shift(mini, occ))
    return {'input': gi, 'output': go}

