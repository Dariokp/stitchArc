def generate_447fd412(diff_lb: float, diff_ub: float) -> dict:
    cols = interval(0, 10, 1)
    h = unifint(diff_lb, diff_ub, (12, 30))
    w = unifint(diff_lb, diff_ub, (12, 30))
    bgc, indic, mainc = sample(cols, 3)
    oh = unifint(diff_lb, diff_ub, (1, 4))
    ow = unifint(diff_lb, diff_ub, (1, 4))
    if oh * ow < 3:
        if choice((True, False)):
            oh = unifint(diff_lb, diff_ub, (3, 4))
        else:
            ow = unifint(diff_lb, diff_ub, (3, 4))
    bounds = asindices(canvas(-1, (oh, ow)))
    ncells = unifint(diff_lb, diff_ub, (3, oh * ow))
    obj = {choice(totuple(bounds))}
    for k in range(ncells - 1):
        obj.add(choice(totuple((bounds - obj) & mapply(neighbors, obj))))
    obj = normalize(obj)
    oh, ow = shape(obj)
    objt = totuple(obj)
    kk = len(obj)
    nindic = randint(1, kk // 2 if kk % 2 == 1 else kk // 2 - 1)
    indicobj = set(sample(objt, nindic))
    mainobj = obj - indicobj
    obj = recolor(indic, indicobj) | recolor(mainc, mainobj)
    loci = randint(0, h - oh)
    locj = randint(0, w - ow)
    gi = canvas(bgc, (h, w))
    go = canvas(bgc, (h, w))
    plcd = shift(obj, (loci, locj))
    gi = paint(gi, plcd)
    go = paint(go, plcd)
    inds = ofcolor(gi, bgc) - mapply(neighbors, toindices(plcd))
    fullinds = asindices(gi)
    noccs = unifint(diff_lb, diff_ub, (1, max(1, (h * w) // (4 * len(plcd)))))
    tr = 0
    maxtr = 5 * noccs
    succ = 0
    while succ < noccs and tr < maxtr:
        tr += 1
        fac = randint(1, min(5, min(h, w) // max(oh, ow) - 1))
        outobj = upscale(obj, fac)
        inobj = sfilter(outobj, lambda cij: cij[0] == indic)
        hh, ww = shape(outobj)
        cands = sfilter(inds, lambda ij: ij[0] <= h - hh and ij[1] <= w - ww)
        if len(cands) == 0:
            continue
        loc = choice(totuple(cands))
        inobjp = shift(inobj, loc)
        outobjp = shift(outobj, loc)
        outobjp = sfilter(outobjp, lambda cij: cij[1] in fullinds)
        outobjpi = toindices(outobjp)
        if outobjpi.issubset(inds):
            succ += 1
            inds = (inds - outobjpi) - mapply(neighbors, toindices(inobjp))
            gi = paint(gi, inobjp)
            go = paint(go, outobjp)
    return {'input': gi, 'output': go}

