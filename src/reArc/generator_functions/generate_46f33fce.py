def generate_46f33fce(diff_lb: float, diff_ub: float) -> dict:
    cols = interval(0, 10, 1)
    h = unifint(diff_lb, diff_ub, (2, 7))
    w = unifint(diff_lb, diff_ub, (2, 7))
    nc = unifint(diff_lb, diff_ub, (0, (h * w) // 2 - 1))
    bgc = choice(cols)
    remcols = remove(bgc, cols)
    go = canvas(bgc, (h, w))
    gi = canvas(bgc, (h*2, w*2))
    inds = totuple(asindices(go))
    locs = sample(inds, nc)
    objo = frozenset({(choice(remcols), ij) for ij in locs})
    f = lambda cij: (cij[0], double(cij[1]))
    obji = shift(apply(f, objo), (1, 1))
    gi = paint(gi, obji)
    go = paint(go, objo)
    go = upscale(go, 4)
    return {'input': gi, 'output': go}

