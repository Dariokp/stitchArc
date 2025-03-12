def generate_be94b721(diff_lb: float, diff_ub: float) -> dict:
    cols = interval(0, 10, 1)
    h = unifint(diff_lb, diff_ub, (6, 30))
    w = unifint(diff_lb, diff_ub, (6, 30))
    no = unifint(diff_lb, diff_ub, (3, max(3, (h * w) // 16)))
    bgc = choice(cols)
    remcols = remove(bgc, cols)
    c = canvas(bgc, (h, w))
    nc = unifint(diff_lb, diff_ub, (no+1, max(no+1, 2*no)))
    inds = asindices(c)
    ch = choice(totuple(inds))
    shp = {ch}
    inds = remove(ch, inds)
    for k in range(nc - 1):
        shp.add(choice(totuple((inds - shp) & mapply(dneighbors, shp))))
    inds = (inds - shp) - mapply(neighbors, shp)
    trgc = choice(remcols)
    gi = fill(c, trgc, shp)
    go = fill(canvas(bgc, shape(shp)), trgc, normalize(shp))
    for k in range(no):
        if len(inds) == 0:
            break
        ch = choice(totuple(inds))
        shp = {ch}
        nc2 = unifint(diff_lb, diff_ub, (1, nc - 1))
        for k in range(nc2 - 1):
            cands = totuple((inds - shp) & mapply(dneighbors, shp))
            if len(cands) == 0:
                break
            shp.add(choice(cands))
        col = choice(remcols)
        gi = fill(gi, col, shp)
        inds = (inds - shp) - mapply(neighbors, shp)
    return {'input': gi, 'output': go}

