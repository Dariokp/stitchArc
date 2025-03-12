def generate_444801d8(diff_lb: float, diff_ub: float) -> dict:
    cols = interval(0, 10, 1)
    h = unifint(diff_lb, diff_ub, (10, 30))
    w = unifint(diff_lb, diff_ub, (10, 30))
    nobjs = unifint(diff_lb, diff_ub, (1, (h * w) // 25))
    bgc = choice(cols)
    remcols = remove(bgc, cols)
    numcols = unifint(diff_lb, diff_ub, (2, 9))
    ccols = sample(remcols, numcols)
    succ = 0
    tr = 0
    maxtr = 5 * nobjs
    gi = canvas(bgc, (h, w))
    go = canvas(bgc, (h, w))
    inds = asindices(gi)
    while succ < nobjs and tr < maxtr:
        tr += 1
        oh = randint(4, 6)
        ow = 5
        bx = box({(1, 0), (oh - 1, 4)}) - {(1, 2)}
        fullobj = backdrop({(0, 0), (oh - 1, 4)})
        cands = backdrop(bx) - bx
        dot = choice(totuple(cands))
        dcol, bxcol = sample(ccols, 2)
        inobj = recolor(bxcol, bx) | recolor(dcol, {dot})
        outobj = recolor(bxcol, bx) | recolor(dcol, fullobj - bx)
        if choice((True, False)):
            inobj = shift(hmirror(inobj), UP)
            outobj = hmirror(outobj)
        cands = sfilter(inds, lambda ij: ij[0] <= h - oh and ij[1] <= w - ow)
        if len(cands) == 0:
            continue
        loc = choice(totuple(cands))
        outplcd = shift(outobj, loc)
        outplcdi = toindices(outplcd)
        if outplcdi.issubset(inds):
            succ += 1
            inplcd = shift(inobj, loc)
            inds = (inds - outplcdi) - outbox(inplcd)
            gi = paint(gi, inplcd)
            go = paint(go, outplcd)
    return {'input': gi, 'output': go}

