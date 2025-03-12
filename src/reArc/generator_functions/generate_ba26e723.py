def generate_ba26e723(diff_lb: float, diff_ub: float) -> dict:
    cols = difference(interval(0, 10, 1), (0, 6))
    h = unifint(diff_lb, diff_ub, (2, 30))
    w = unifint(diff_lb, diff_ub, (2, 30))
    gi = canvas(0, (h, w))
    go = canvas(0, (h, w))
    opts = interval(0, h, 1)
    ncols = unifint(diff_lb, diff_ub, (1, 8))
    ccols = sample(cols, ncols)
    for j in range(w):
        nc = unifint(diff_lb, diff_ub, (1, h - 1))
        locs = sample(opts, nc)
        obj = frozenset({(choice(ccols), (ii, j)) for ii in locs})
        gi = paint(gi, obj)
        if j % 3 == 0:
            obj = recolor(6, obj)
        go = paint(go, obj)
    return {'input': gi, 'output': go}

