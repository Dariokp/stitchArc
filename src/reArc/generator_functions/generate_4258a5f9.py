def generate_4258a5f9(diff_lb: float, diff_ub: float) -> dict:
    colopts = remove(1, interval(0, 10, 1))
    h = unifint(diff_lb, diff_ub, (2, 30))
    w = unifint(diff_lb, diff_ub, (2, 30))
    bgc = choice(colopts)
    remcols = remove(bgc, colopts)
    fgc = choice(remcols)
    gi = canvas(bgc, (h, w))
    mp = ((h * w) // 2) if (h * w) % 2 == 1 else ((h * w) // 2 - 1)
    ndots = unifint(diff_lb, diff_ub, (1, mp))
    inds = totuple(asindices(gi))
    dots = sample(inds, ndots)
    go = fill(gi, 1, mapply(neighbors, frozenset(dots)))
    go = fill(go, fgc, dots)
    gi = fill(gi, fgc, dots)
    return {'input': gi, 'output': go}

