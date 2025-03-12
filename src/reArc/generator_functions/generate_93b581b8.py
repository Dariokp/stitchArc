def generate_93b581b8(diff_lb: float, diff_ub: float) -> dict:
    cols = interval(0, 10, 1)
    h = unifint(diff_lb, diff_ub, (10, 30))
    w = unifint(diff_lb, diff_ub, (10, 30))
    bgc = choice(cols)
    remcols = remove(bgc, cols)
    numcols = unifint(diff_lb, diff_ub, (1, 9))
    ccols = sample(remcols, numcols)
    numocc = unifint(diff_lb, diff_ub, (1, (h * w) // 50))
    succ = 0
    tr = 0
    maxtr = 10 * numocc
    gi = canvas(bgc, (h, w))
    go = canvas(bgc, (h, w))
    inds = asindices(gi)
    fullinds = asindices(gi)
    while tr < maxtr and succ < numocc:
        tr += 1
        cands = sfilter(inds, lambda ij: ij[0] <= h - 2 and ij[1] <= w - 2)
        if len(cands) == 0:
            break
        loc = choice(totuple(cands))
        c1, c2, c3, c4 = [choice(ccols) for k in range(4)]
        q = {(0, 0), (0, 1), (1, 0), (1, 1)}
        inobj = {(c1, (0, 0)), (c2, (0, 1)), (c3, (1, 0)), (c4, (1, 1))}
        outobj = inobj | recolor(c4, shift(q, (-2, -2))) | recolor(c3, shift(q, (-2, 2))) | recolor(c2, shift(q, (2, -2))) | recolor(c1, shift(q, (2, 2)))
        inobjplcd = shift(inobj, loc)
        outobjplcd = shift(outobj, loc)
        outobjplcd = sfilter(outobjplcd, lambda cij: cij[1] in fullinds)
        outobjplcdi = toindices(outobjplcd)
        if outobjplcdi.issubset(inds):
            succ += 1
            inds = (inds - outobjplcdi) - mapply(dneighbors, toindices(inobjplcd))
            gi = paint(gi, inobjplcd)
            go = paint(go, outobjplcd)
    return {'input': gi, 'output': go}

