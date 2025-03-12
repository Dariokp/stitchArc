def generate_ae3edfdc(diff_lb: float, diff_ub: float) -> dict:
    cols = difference(interval(0, 10, 1), (1, 2, 3, 7))
    h = unifint(diff_lb, diff_ub, (8, 30))
    w = unifint(diff_lb, diff_ub, (8, 30))
    bgc = choice(cols)
    go = canvas(bgc, (h, w))
    inds = asindices(go)
    rdi = randint(1, h - 2)
    rdj = randint(1, w - 2)
    rd = (rdi, rdj)
    reminds = inds - ({rd} | neighbors(rd))
    reminds = sfilter(reminds, lambda ij: 1 <= ij[0] <= h - 2 and 1 <= ij[1] <= w - 2)
    bd = choice(totuple(reminds))
    bdi, bdj = bd
    go = fill(go, 2, {rd})
    go = fill(go, 1, {bd})
    ngd = unifint(diff_lb, diff_ub, (1, 8))
    gd = sample(totuple(neighbors(rd)), ngd)
    nod = unifint(diff_lb, diff_ub, (1, 8))
    od = sample(totuple(neighbors(bd)), nod)
    go = fill(go, 3, gd)
    go = fill(go, 7, od)
    gdmapper = {d: (3, position({rd}, {d})) for d in gd}
    odmapper = {d: (7, position({bd}, {d})) for d in od}
    mpr = {**gdmapper, **odmapper}
    ub = (len(gd) + len(od)) * ((h + w) // 5)
    ndist = unifint(diff_lb, diff_ub, (1, ub))
    gi = tuple(e for e in go)
    fullinds = asindices(gi)
    for k in range(ndist):
        options = []
        for loc, (col, direc) in mpr.items():
            ii, jj = add(loc, direc)
            if (ii, jj) in fullinds and gi[ii][jj] == bgc:
                options.append((loc, col, direc))
        if len(options) == 0:
            break
        loc, col, direc = choice(options)
        del mpr[loc]
        newloc = add(loc, direc)
        mpr[newloc] = (col, direc)
        gi = fill(gi, bgc, {loc})
        gi = fill(gi, col, {newloc})
    return {'input': gi, 'output': go}

