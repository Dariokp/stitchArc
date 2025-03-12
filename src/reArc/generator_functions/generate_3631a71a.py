def generate_3631a71a(diff_lb: float, diff_ub: float) -> dict:
    cols = interval(0, 10, 1)
    h = unifint(diff_lb, diff_ub, (6, 15))
    w = h
    bgc, patchcol = sample(cols, 2)
    patchcol = choice(cols)
    bgc = choice(remove(patchcol, cols))
    remcols = difference(cols, (bgc, patchcol))
    c = canvas(bgc, (h, w))
    inds = sfilter(asindices(c), lambda ij: ij[0] >= ij[1])
    ncols = unifint(diff_lb, diff_ub, (1, 8))
    ccols = sample(remcols, ncols)
    ncells = unifint(diff_lb, diff_ub, (1, len(inds)))
    cells = set(sample(totuple(inds), ncells))
    obj = {(choice(ccols), ij) for ij in cells}
    c = paint(dmirror(paint(c, obj)), obj)
    c = hconcat(c, vmirror(c))
    c = vconcat(c, hmirror(c))
    cutoff = 2
    go = dmirror(dmirror(c[:-cutoff])[:-cutoff])
    gi = tuple(e for e in go)
    forbidden = asindices(canvas(-1, (cutoff, cutoff)))
    dmirrareaL = shift(asindices(canvas(-1, (h*2-2*cutoff, cutoff))), (cutoff, 0))
    dmirrareaT = shift(asindices(canvas(-1, (cutoff, 2*w-2*cutoff))), (0, cutoff))
    inds1 = sfilter(asindices(gi), lambda ij: cutoff <= ij[0] < h and cutoff <= ij[1] < w and ij[0] >= ij[1])
    inds2 = dmirror(inds1)
    inds3 = shift(hmirror(inds1), (h-cutoff, 0))
    inds4 = shift(hmirror(inds2), (h-cutoff, 0))
    inds5 = shift(vmirror(inds1), (0, w-cutoff))
    inds6 = shift(vmirror(inds2), (0, w-cutoff))
    inds7 = shift(hmirror(vmirror(inds1)), (h-cutoff, w-cutoff))
    inds8 = shift(hmirror(vmirror(inds2)), (h-cutoff, w-cutoff))
    f1 = identity
    f2 = dmirror
    f3 = lambda x: hmirror(shift(x, invert((h-cutoff, 0))))
    f4 = lambda x: dmirror(hmirror(shift(x, invert((h-cutoff, 0)))))
    f5 = lambda x: vmirror(shift(x, invert((0, w-cutoff))))
    f6 = lambda x: dmirror(vmirror(shift(x, invert((0, w-cutoff)))))
    f7 = lambda x: vmirror(hmirror(shift(x, invert((h-cutoff, w-cutoff)))))
    f8 = lambda x: dmirror(vmirror(hmirror(shift(x, invert((h-cutoff, w-cutoff))))))
    indsarr = [inds1, inds2, inds3, inds4, inds5, inds6, inds7, inds8]
    farr = [f1, f2, f3, f4, f5, f6, f7, f8]
    ndist = unifint(diff_lb, diff_ub, (1, int((2*h*2*w) ** 0.5)))
    succ = 0
    tr = 0
    maxtr = 10 * ndist
    fullh, fullw = shape(gi)
    while succ < ndist and tr < maxtr:
        tr += 1
        oh = randint(2, h//2+1)
        ow = randint(2, w//2+1)
        loci = randint(0, fullh - oh)
        locj = randint(0, fullw - ow)
        bd = backdrop(frozenset({(loci, locj), (loci + oh - 1, locj + ow - 1)}))
        isleft = set()
        gi2 = fill(gi, patchcol, bd)
        if patchcol in palette(toobject(forbidden, gi2)):
            continue
        oo1 = toindices(sfilter(toobject(dmirrareaL, gi2), lambda cij: cij[0] != patchcol))
        oo2 = toindices(sfilter(toobject(dmirrareaT, gi2), lambda cij: cij[0] != patchcol))
        oo2 = frozenset({(ij[1], ij[0]) for ij in oo2})
        if oo1 | oo2 != dmirrareaL:
            continue
        for ii, ff in zip(indsarr, farr):
            oo = toobject(ii, gi2)
            rem = toindices(sfilter(oo, lambda cij: cij[0] != patchcol))
            if len(rem) > 0:
                isleft = isleft | ff(rem)
        if isleft != inds1:
            continue
        succ += 1
        gi = gi2
    return {'input': gi, 'output': go}

