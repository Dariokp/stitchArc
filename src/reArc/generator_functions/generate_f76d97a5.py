def generate_f76d97a5(diff_lb: float, diff_ub: float) -> dict:
    cols = remove(0, remove(5, interval(0, 10, 1)))
    h = unifint(diff_lb, diff_ub, (4, 30))
    w = unifint(diff_lb, diff_ub, (4, 30))
    col = choice(cols)
    gi = canvas(5, (h, w))
    go = canvas(col, (h, w))
    numdev = unifint(diff_lb, diff_ub, (0, (h * w) // 2))
    num = choice((numdev, h * w - numdev))
    num = min(max(1, num), h * w)
    inds = totuple(asindices(gi))
    locs = sample(inds, num)
    gi = fill(gi, col, locs)
    go = fill(go, 0, locs)
    return {'input': gi, 'output': go}

