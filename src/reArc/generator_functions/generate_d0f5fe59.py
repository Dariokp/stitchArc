def generate_d0f5fe59(diff_lb: float, diff_ub: float) -> dict:
    cols = interval(0, 10, 1)
    h = unifint(diff_lb, diff_ub, (10, 30))
    w = unifint(diff_lb, diff_ub, (10, 30))
    nobjs = unifint(diff_lb, diff_ub, (1, min(30, (h * w) // 9)))
    bgc = choice(cols)
    remcols = remove(bgc, cols)
    fgc = choice(remcols)
    nfound = 0
    trials = 0
    maxtrials = nobjs * 5
    gi = canvas(bgc, (h, w))
    inds = asindices(gi)
    while trials < maxtrials and nfound < nobjs:
        oh = unifint(diff_lb, diff_ub, (1, 5))
        ow = unifint(diff_lb, diff_ub, (1, 5))
        bx = asindices(canvas(-1, (oh, ow)))
        sp = choice(totuple(bx))
        shp = {sp}
        dev = unifint(diff_lb, diff_ub, (0, (oh * ow) // 2))
        ncells = choice((dev, oh * ow - dev))
        ncells = min(max(1, ncells), oh * ow - 1)
        for k in range(ncells):
            ij = choice(totuple((bx - shp) & mapply(dneighbors, shp)))
            shp.add(ij)
        shp = normalize(shp)
        if len(inds) == 0:
            break
        loc = choice(totuple(inds))
        plcd = shift(shp, loc)
        if plcd.issubset(inds):
            gi = fill(gi, fgc, plcd)
            inds = (inds - plcd) - mapply(neighbors, plcd)
            nfound += 1
        trials += 1
    go = canvas(bgc, (nfound, nfound))
    go = fill(go, fgc, connect((0, 0), (nfound - 1, nfound - 1)))
    return {'input': gi, 'output': go}

