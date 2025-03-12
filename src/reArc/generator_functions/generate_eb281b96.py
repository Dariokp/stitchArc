def generate_eb281b96(diff_lb: float, diff_ub: float) -> dict:
    cols = interval(0, 10, 1)
    h = unifint(diff_lb, diff_ub, (3, 8))
    w = unifint(diff_lb, diff_ub, (3, 30))
    bgc = choice(cols)
    remcols = remove(bgc, cols)
    numc = unifint(diff_lb, diff_ub, (1, 9))
    ccols = sample(remcols, numc)
    c = canvas(bgc, (h, w))
    inds = asindices(c)
    ncells = unifint(diff_lb, diff_ub, (1, h * w))
    locs = sample(totuple(inds), ncells)
    obj = {(choice(ccols), ij) for ij in locs}
    gi = paint(c, obj)
    go = vconcat(gi, hmirror(gi[:-1]))
    go = vconcat(go, hmirror(go[:-1]))
    return {'input': gi, 'output': go}

