def generate_780d0b14(diff_lb: float, diff_ub: float) -> dict:
    cols = interval(0, 10, 1)
    nh = unifint(diff_lb, diff_ub, (2, 6))
    nw = unifint(diff_lb, diff_ub, (2, 6))
    bgc = choice(cols)
    remcols = remove(bgc, cols)
    ncols = unifint(diff_lb, diff_ub, (3, 9))
    ccols = sample(remcols, ncols)
    go = canvas(-1, (nh, nw))
    obj = {(choice(ccols), ij) for ij in asindices(go)}
    go = paint(go, obj)
    while len(dedupe(go)) < nh or len(dedupe(dmirror(go))) < nw:
        obj = {(choice(ccols), ij) for ij in asindices(go)}
        go = paint(go, obj)
    h = unifint(diff_lb, diff_ub, (2*nh+nh-1, 30))
    w = unifint(diff_lb, diff_ub, (2*nw+nw-1, 30))
    hdist = [2 for k in range(nh)]
    for k in range(h - 2 * nh - nh + 1):
        idx = randint(0, nh - 1)
        hdist[idx] += 1
    wdist = [2 for k in range(nw)]
    for k in range(w - 2 * nw - nw + 1):
        idx = randint(0, nw - 1)
        wdist[idx] += 1
    gi = merge(tuple(repeat(r, c) + (repeat(bgc, nw),) for r, c in zip(go, hdist)))[:-1]
    gi = dmirror(merge(tuple(repeat(r, c) + (repeat(bgc, h),) for r, c in zip(dmirror(gi), wdist)))[:-1])
    objs = objects(gi, T, F, F)
    bgobjs = colorfilter(objs, bgc)
    objs = objs - bgobjs
    for obj in objs:
        gi = fill(gi, bgc, sample(totuple(toindices(obj)), unifint(diff_lb, diff_ub, (1, len(obj) // 2))))
    return {'input': gi, 'output': go}

