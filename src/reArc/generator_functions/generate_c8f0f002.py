def generate_c8f0f002(diff_lb: float, diff_ub: float) -> dict:
    cols = remove(7, interval(0, 10, 1))
    h = unifint(diff_lb, diff_ub, (2, 30))
    w = unifint(diff_lb, diff_ub, (2, 30))
    numc = unifint(diff_lb, diff_ub, (1, 9))
    ccols = sample(cols, numc)
    c = canvas(-1, (h, w))
    inds = totuple(asindices(c))
    numo = unifint(diff_lb, diff_ub, (0, (h * w) // 2))
    orng = sample(inds, numo)
    rem = difference(inds, orng)
    gi = fill(c, 7, orng)
    go = fill(c, 5, orng)
    for ij in rem:
        col = choice(ccols)
        gi = fill(gi, col, {ij})
        go = fill(go, col, {ij})
    return {'input': gi, 'output': go}

