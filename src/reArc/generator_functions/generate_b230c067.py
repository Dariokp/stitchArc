def generate_b230c067(diff_lb: float, diff_ub: float) -> dict:
    cols = difference(interval(0, 10, 1), (1, 2))
    while True:
        h = unifint(diff_lb, diff_ub, (10, 30))
        w = unifint(diff_lb, diff_ub, (10, 30))
        oh = unifint(diff_lb, diff_ub, (2, h // 3 - 1))
        ow = unifint(diff_lb, diff_ub, (2, w // 3 - 1))
        numcd = unifint(diff_lb, diff_ub, (0, (oh * ow) // 2))
        numc = choice((numcd, oh * ow - numcd))
        numca = min(max(2, numc), oh * ow - 2)
        bounds = asindices(canvas(-1, (oh, ow)))
        sp = choice(totuple(bounds))
        shp = {sp}
        for k in range(numca):
            ij = choice(totuple((bounds - shp) & mapply(neighbors, shp)))
            shp.add(ij)
        shpa = normalize(shp)
        shpb = set(normalize(shp))
        mxnch = oh * ow - len(shpa)
        nchinv = unifint(diff_lb, diff_ub, (1, mxnch))
        nch = mxnch - nchinv
        nch = min(max(1, nch), mxnch)
        for k in range(nch):
            ij = choice(totuple((bounds - shpb) & mapply(neighbors, shpb)))
            shpb.add(ij)
        if choice((True, False)):
            shpa, shpb = shpb, shpa
        bgc, fgc = sample(cols, 2)
        c = canvas(bgc, (h, w))
        inds = asindices(c)
        acands = sfilter(inds, lambda ij: ij[0] <= h - height(shpa) and ij[1] <= w - width(shpa))
        aloc = choice(totuple(acands))
        aplcd = shift(shpa, aloc)
        gi = fill(c, fgc, aplcd)
        go = fill(c, 2, aplcd)
        maxtrials = 10
        tr = 0
        succ = 0
        inds = (inds - aplcd) - mapply(neighbors, aplcd)
        inds = sfilter(inds, lambda ij: ij[0] <= h - height(shpb) and ij[1] <= w - width(shpb))
        while succ < 2 and tr <= maxtrials:
            if len(inds) == 0:
                break
            loc = choice(totuple(inds))
            plcbd = shift(shpb, loc)
            if plcbd.issubset(inds):
                gi = fill(gi, fgc, plcbd)
                go = fill(go, 1, plcbd)
                succ += 1
                inds = (inds - plcbd) - mapply(neighbors, plcbd)
            tr += 1
        if succ == 2:
            break
    return {'input': gi, 'output': go}

