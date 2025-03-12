def generate_0d3d703e(diff_lb: float, diff_ub: float) -> dict:
    incols = (1, 2, 3, 4, 5, 6, 8, 9)
    outcols = (5, 6, 4, 3, 1, 2, 9, 8)
    k = len(incols)
    h = unifint(diff_lb, diff_ub, (4, 30))
    w = unifint(diff_lb, diff_ub, (4, 30))
    gi = canvas(-1, (h, w))
    go = canvas(-1, (h, w))
    inds = asindices(gi)
    numc = unifint(diff_lb, diff_ub, (1, k))
    idxes = sample(interval(0, k, 1), numc)
    for ij in inds:
        idx = choice(idxes)
        gi = fill(gi, incols[idx], {ij})
        go = fill(go, outcols[idx], {ij})
    return {'input': gi, 'output': go}

