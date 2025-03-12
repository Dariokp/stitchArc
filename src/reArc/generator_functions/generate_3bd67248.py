def generate_3bd67248(diff_lb: float, diff_ub: float) -> dict:
    cols = difference(interval(0, 10, 1), (2, 4))
    h = unifint(diff_lb, diff_ub, (3, 15))
    w = unifint(diff_lb, diff_ub, (3, 15))
    bgc, linc = sample(cols, 2)
    fac = unifint(diff_lb, diff_ub, (1, 30 // max(h, w)))
    gi = canvas(bgc, (h, w))
    gi = fill(gi, linc, connect((0, 0), (h - 1, 0)))
    go = fill(gi, 4, connect((h - 1, 1), (h - 1, w - 1)))
    go = fill(go, 2, shoot((h - 2, 1), (-1, 1)))
    rotf = choice((identity, rot90, rot180, rot270))
    gi = rotf(gi)
    go = rotf(go)
    gi = upscale(gi, fac)
    go = upscale(go, fac)
    return {'input': gi, 'output': go}

