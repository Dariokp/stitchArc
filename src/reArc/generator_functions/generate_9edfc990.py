def generate_9edfc990(diff_lb: float, diff_ub: float) -> dict:
    cols = interval(2, 10, 1)
    h = unifint(diff_lb, diff_ub, (5, 30))
    w = unifint(diff_lb, diff_ub, (5, 30))
    namt = unifint(diff_lb, diff_ub, (int(0.4 * h * w), int(0.7 * h * w)))
    gi = canvas(0, (h, w))
    inds = asindices(gi)
    locs = sample(totuple(inds), namt)
    noise = {(choice(cols), ij) for ij in locs}
    gi = paint(gi, noise)
    remlocs = inds - set(locs)
    numc = unifint(diff_lb, diff_ub, (1, max(1, len(remlocs) // 10)))
    blocs = sample(totuple(remlocs), numc)
    gi = fill(gi, 1, blocs)
    objs = objects(gi, T, F, F)
    objs = colorfilter(objs, 0)
    res = mfilter(objs, rbind(adjacent, blocs))
    go = fill(gi, 1, res)
    return {'input': gi, 'output': go}

