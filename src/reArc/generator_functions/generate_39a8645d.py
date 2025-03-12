def generate_39a8645d(diff_lb: float, diff_ub: float) -> dict:
    cols = interval(0, 10, 1)
    h = unifint(diff_lb, diff_ub, (15, 30))
    w = unifint(diff_lb, diff_ub, (15, 30))
    oh = randint(2, 4)
    ow = randint(2, 4)
    bgc = choice(cols)
    remcols = remove(bgc, cols)
    nobjs = unifint(diff_lb, diff_ub, (1, oh + ow))
    ccols = sample(remcols, nobjs+1)
    mxcol = ccols[0]
    rcols = ccols[1:]
    maxnocc = unifint(diff_lb, diff_ub, (nobjs + 2, max(nobjs + 2, (h * w) // 16)))
    tr = 0
    maxtr = 10 * maxnocc
    succ = 0
    allobjs = []
    bounds = asindices(canvas(-1, (oh, ow)))
    for k in range(nobjs + 1):
        while True:
            ncells = randint(oh + ow - 1, oh * ow)
            cobj = {choice(totuple(bounds))}
            while shape(cobj) != (oh, ow) and len(cobj) < ncells:
                cobj.add(choice(totuple((bounds - cobj) & mapply(neighbors, cobj))))
            if cobj not in allobjs:
                break
        allobjs.append(frozenset(cobj))
    mcobj = normalize(allobjs[0])
    remobjs = apply(normalize, allobjs[1:])
    mxobjcounter = 0
    remobjcounter = {robj: 0 for robj in remobjs}
    gi = canvas(bgc, (h, w))
    inds = asindices(gi)
    while tr < maxtr and succ < maxnocc:
        tr += 1
        candobjs = [robj for robj, cnt in remobjcounter.items() if cnt + 1 < mxobjcounter]
        if len(candobjs) == 0 or randint(0, 100) / 100 > diff_lb:
            obj = mcobj
            col = mxcol
        else:
            obj = choice(candobjs)
            col = rcols[remobjs.index(obj)]
        cands = sfilter(inds, lambda ij: ij[0] <= h - oh and ij[1] <= w - ow)
        if len(cands) == 0:
            break
        loc = choice(totuple(cands))
        plcd = shift(obj, loc)
        if plcd.issubset(inds - mapply(neighbors, ofcolor(gi, col))):
            succ += 1
            inds = (inds - plcd) - mapply(dneighbors, plcd)
            gi = fill(gi, col, plcd)
            if obj in remobjcounter:
                remobjcounter[obj] += 1
            else:
                mxobjcounter += 1
    go = fill(canvas(bgc, shape(mcobj)), mxcol, mcobj)
    return {'input': gi, 'output': go}

