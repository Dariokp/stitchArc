def generate_5521c0d9(diff_lb: float, diff_ub: float) -> dict:
    cols = interval(0, 10, 1)    
    h = unifint(diff_lb, diff_ub, (4, 30))
    w = unifint(diff_lb, diff_ub, (6, 30))
    inds = interval(0, w, 1)
    nobjs = unifint(diff_lb, diff_ub, (1, w//3))
    speps = sample(inds, nobjs*2)
    while 0 in speps or w - 1 in speps:
        nobjs = unifint(diff_lb, diff_ub, (1, w//3))
        speps = sample(inds, nobjs*2)
    speps = sorted(speps)
    starts = speps[::2]
    ends = speps[1::2]
    bgc = choice(cols)
    remcols = remove(bgc, cols)
    ncols = unifint(diff_lb, diff_ub, (2, 9))
    ccols = sample(remcols, ncols)
    forb = -1
    gi = canvas(bgc, (h, w))
    go = canvas(bgc, (h, w))
    forb = -1
    for sp, ep in zip(starts, ends):
        col = choice(remove(forb, ccols))
        forb = col
        hdev = unifint(diff_lb, diff_ub, (0, h//2))
        hei = choice((hdev, h - hdev))
        hei = min(max(1, hei), h - 1)
        ulc = (h - hei, sp)
        lrc = (h - 1, ep)
        obj = backdrop(frozenset({ulc, lrc}))
        gi = fill(gi, col, obj)
        go = fill(go, col, shift(obj, (-hei, 0)))
    rotf = choice((identity, rot90, rot180, rot270))
    gi = rotf(gi)
    go = rotf(go)
    return {'input': gi, 'output': go}

