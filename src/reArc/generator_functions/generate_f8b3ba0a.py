def generate_f8b3ba0a(diff_lb: float, diff_ub: float) -> dict:
    cols = interval(0, 10, 1)
    h = unifint(diff_lb, diff_ub, (1, 5))
    w = unifint(diff_lb, diff_ub, (1, 5))
    nh = unifint(diff_lb, diff_ub, (3, 29 // (h + 1)))
    nw = unifint(diff_lb, diff_ub, (3, 29 // (w + 1)))
    fullh = (h + 1) * nh + 1
    fullw = (w + 1) * nw + 1
    fullbgc, bgc = sample(cols, 2)
    remcols = remove(fullbgc, remove(bgc, cols))
    shp = shift(asindices(canvas(-1, (h, w))), (1, 1))
    gi = canvas(fullbgc, (fullh, fullw))
    locs = set()
    for a in range(nh):
        for b in range(nw):
            loc = (a * (h + 1), b * (w + 1))
            locs.add(loc)
            gi = fill(gi, bgc, shift(shp, loc))
    numc = unifint(diff_lb, diff_ub, (1, (nh * nw) // 2 - 1))
    stack = []
    nn = numc + 1
    ncols = 0
    while nn > 1 and numc > 0 and len(remcols) > 0:
        nn3 = int(0.5 * (8 * numc + 1) ** 0.5 - 1)
        nn = min(max(1, nn3), nn - 1)
        col = choice(remcols)
        remcols = remove(col, remcols)
        numc -= nn
        stack.append((col, nn))
    go = dmirror((tuple(c for c, nn in stack),))
    for col, nn in stack:
        slocs = sample(totuple(locs), nn)
        gi = fill(gi, col, mapply(lbind(shift, shp), slocs))
        locs = locs - set(slocs)
    return {'input': gi, 'output': go}

