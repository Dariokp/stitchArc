def generate_ea32f347(diff_lb: float, diff_ub: float) -> dict:
    cols = difference(interval(0, 10, 1), (1, 2, 4))
    h = unifint(diff_lb, diff_ub, (5, 30))
    w = unifint(diff_lb, diff_ub, (5, 30))
    a = unifint(diff_lb, diff_ub, (3, 30))
    b = unifint(diff_lb, diff_ub, (2, a))
    c = unifint(diff_lb, diff_ub, (1, b))
    if c - a == 2:
        if a > 1:
            a -= 1
        elif c < min(h, w):
            c += 1
    bgc = choice(cols)
    remcols = remove(bgc, cols)
    gi = canvas(bgc, (h, w))
    go = canvas(bgc, (h, w))
    inds = asindices(gi)
    for col, l in zip((1, 4, 2), (a, b, c)):
        ln1 = connect((0, 0), (0, l - 1))
        ln2 = connect((0, 0), (l - 1, 0))
        tmpg = fill(gi, -1, asindices(gi) - inds)
        occs1 = occurrences(tmpg, recolor(bgc, ln1))
        occs2 = occurrences(tmpg, recolor(bgc, ln2))
        pool = []
        if len(occs1) > 0:
            pool.append((ln1, occs1))
        if len(occs2) > 0:
            pool.append((ln2, occs2))
        ln, occs = choice(pool)
        loc = choice(totuple(occs))
        plcd = shift(ln, loc)
        gi = fill(gi, choice(remcols), plcd)
        go = fill(go, col, plcd)
        inds = (inds - plcd) - mapply(dneighbors, plcd)
    return {'input': gi, 'output': go}

