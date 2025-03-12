def generate_d511f180(diff_lb: float, diff_ub: float) -> dict:
    cols = difference(interval(0, 10, 1), (5, 8))
    h = unifint(diff_lb, diff_ub, (2, 30))
    w = unifint(diff_lb, diff_ub, (2, 30))
    numc = unifint(diff_lb, diff_ub, (1, 8))
    ccols = sample(cols, numc)
    c = canvas(-1, (h, w))
    inds = totuple(asindices(c))
    numbg = unifint(diff_lb, diff_ub, (0, (h * w) // 2))
    bginds = sample(inds, numbg)
    idx = randint(0, numbg)
    blues = bginds[:idx]
    greys = bginds[idx:]
    rem = difference(inds, bginds)
    gi = fill(c, 8, blues)
    gi = fill(gi, 5, greys)
    go = fill(c, 5, blues)
    go = fill(go, 8, greys)
    for ij in rem:
        col = choice(ccols)
        gi = fill(gi, col, {ij})
        go = fill(go, col, {ij})
    return {'input': gi, 'output': go}

