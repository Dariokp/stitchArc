def generate_d4469b4b(diff_lb: float, diff_ub: float) -> dict:
    cols = difference(interval(0, 10, 1), (1, 2, 3))
    canv = canvas(5, (3, 3))
    A = fill(canv, 0, {(1, 0), (2, 0), (1, 2), (2, 2)})
    B = fill(canv, 0, corners(asindices(canv)))
    C = fill(canv, 0, {(0, 0), (0, 1), (1, 0), (1, 1)})
    colabc = ((2, A), (1, B), (3, C))
    h = unifint(diff_lb, diff_ub, (2, 30))
    w = unifint(diff_lb, diff_ub, (2, 30))
    col, go = choice(colabc)
    gi = canvas(col, (h, w))
    inds = asindices(gi)
    numc = unifint(diff_lb, diff_ub, (1, 7))
    ccols = sample(cols, numc)
    numcells = unifint(diff_lb, diff_ub, (0, h * w - 1))
    locs = sample(totuple(inds), numcells)
    otherobj = {(choice(ccols), ij) for ij in locs}
    gi = paint(gi, otherobj)
    return {'input': gi, 'output': go}

