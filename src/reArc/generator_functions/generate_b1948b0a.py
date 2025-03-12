def generate_b1948b0a(diff_lb: float, diff_ub: float) -> dict:
    cols = remove(6, interval(0, 10, 1))
    h = unifint(diff_lb, diff_ub, (2, 30))
    w = unifint(diff_lb, diff_ub, (2, 30))
    npd = unifint(diff_lb, diff_ub, (0, (h * w) // 2))
    np = choice((npd, h * w - npd))
    np = min(max(0, npd), h * w)
    gi = canvas(6, (h, w))
    inds = totuple(asindices(gi))
    pp = sample(inds, np)
    npp = difference(inds, pp)
    for ij in npp:
        gi = fill(gi, choice(cols), {ij})
    go = fill(gi, 2, pp)
    return {'input': gi, 'output': go}

