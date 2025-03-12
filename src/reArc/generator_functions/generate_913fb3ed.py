def generate_913fb3ed(diff_lb: float, diff_ub: float) -> dict:
    dim_bounds = (1, 30)
    cols = difference(interval(0, 10, 1), (1, 2, 3, 4, 6, 8))
    sr = (2, 3, 8)
    tr = (1, 6, 4)
    prs = list(zip(sr, tr))
    h = unifint(diff_lb, diff_ub, (1, 30))
    w = unifint(diff_lb, diff_ub, (1, 30))
    bgc = choice(cols)
    gi = canvas(bgc, (h, w))
    go = canvas(bgc, (h, w))
    numc = unifint(diff_lb, diff_ub, (1, max(1, (h * w) // 10)))
    inds = asindices(gi)
    for k in range(numc):
        if len(inds) == 0:
            break
        loc = choice(totuple(inds))
        a, b = choice(prs)
        inds = (inds - neighbors(loc)) - outbox(neighbors(loc))
        inds = remove(loc, inds)
        gi = fill(gi, a, {loc})
        go = fill(go, a, {loc})
        go = fill(go, b, neighbors(loc))
    return {'input': gi, 'output': go}

