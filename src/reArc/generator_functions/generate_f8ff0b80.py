def generate_f8ff0b80(diff_lb: float, diff_ub: float) -> dict:
    cols = interval(0, 10, 1)
    h = unifint(diff_lb, diff_ub, (10, 30))
    w = unifint(diff_lb, diff_ub, (10, 30))
    bgc = choice(cols)
    remcols = remove(bgc, cols)
    nobjs = unifint(diff_lb, diff_ub, (1, min(30, (h * w) // 25)))
    gi = canvas(bgc, (h, w))
    numcells = unifint(diff_lb, diff_ub, (nobjs+1, 36))
    base = asindices(canvas(-1, (6, 6)))
    maxtr = 10
    inds = asindices(gi)
    go = []
    for k in range(nobjs):
        if len(inds) == 0 or numcells < 2:
            break
        numcells = unifint(diff_lb, diff_ub, (nobjs - k, numcells - 1))
        if numcells == 0:
            break
        sp = choice(totuple(base))
        shp = {sp}
        reminds = remove(sp, base)
        for kk in range(numcells - 1):
            shp.add(choice(totuple((reminds - shp) & mapply(neighbors, shp))))
        shp = normalize(shp)
        validloc = False
        rems = sfilter(inds, lambda ij: ij[0] <= h - height(shp) and ij[1] <= w - width(shp))
        if len(rems) == 0:
            break
        loc = choice(totuple(rems))
        tr = 0
        while not validloc and tr < maxtr:
            loc = choice(totuple(inds))
            validloc = shift(shp, loc).issubset(inds)
            tr += 1
        if validloc:
            plcd = shift(shp, loc)
            col = choice(remcols)
            go.append(col)
            inds = (inds - plcd) - mapply(neighbors, plcd)
            gi = fill(gi, col, plcd)
    go = dmirror((tuple(go),))
    return {'input': gi, 'output': go}

