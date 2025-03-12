def generate_3e980e27(diff_lb: float, diff_ub: float) -> dict:
    cols = difference(interval(0, 10, 1), (2, 3))
    h = unifint(diff_lb, diff_ub, (11, 30))
    w = unifint(diff_lb, diff_ub, (11, 30))
    bgc, rcol, gcol = sample(cols, 3)
    objs = []
    for (fixc, remc) in ((2, rcol), (3, gcol)):
        oh = unifint(diff_lb, diff_ub, (2, 5))
        ow = unifint(diff_lb, diff_ub, (2, 5))
        bounds = asindices(canvas(-1, (oh, ow)))
        obj = {choice(totuple(bounds))}
        ncellsd = unifint(diff_lb, diff_ub, (0, (oh * ow) // 2))
        ncells = choice((ncellsd, oh * ow - ncellsd))
        ncells = min(max(2, ncells), oh * ow)
        for k in range(ncells - 1):
            obj.add(choice(totuple((bounds - obj) & mapply(neighbors, obj))))
        obj = normalize(obj)
        fixp = choice(totuple(obj))
        rem = remove(fixp, obj)
        obj = {(fixc, fixp)} | recolor(remc, rem)
        objs.append(obj)
    robj, gobj = objs
    obj1, obj2 = sample(objs, 2)
    loci1 = randint(0, h - height(obj1) - height(obj2) - 1)
    locj1 = randint(0, w - width(obj1))
    loci2 = randint(loci1+height(obj1)+1, h - height(obj2))
    locj2 = randint(0, w - width(obj2))
    gi = canvas(bgc, (h, w))
    obj1p = shift(obj1, (loci1, locj1))
    obj2p = shift(obj2, (loci2, locj2))
    gi = paint(gi, obj1p)
    gi = paint(gi, obj2p)
    noccs = unifint(diff_lb, diff_ub, (1, (h * w) // int(1.5 * (len(robj) + len(gobj)))))
    succ = 0
    tr = 0
    maxtr = 5 * noccs
    robj = vmirror(robj)
    inds = ofcolor(gi, bgc) - (mapply(neighbors, toindices(obj1p)) | mapply(neighbors, toindices(obj2p)))
    go = tuple(e for e in gi)
    objopts = [robj, gobj]
    while tr < maxtr and succ < noccs:
        tr += 1
        obj = choice(objopts)
        oh, ow = shape(obj)
        cands = sfilter(inds, lambda ij: ij[0] <= h - oh and ij[1] <= w - ow)
        if len(cands) == 0:
            continue
        loc = choice(totuple(cands))
        plcd = shift(obj, loc)
        plcdi = toindices(plcd)
        if plcdi.issubset(inds):
            succ += 1
            inds = (inds - plcdi) - mapply(neighbors, plcdi)
            gi = paint(gi, sfilter(plcd, lambda cij: cij[0] in (2, 3)))
            go = paint(go, plcd)
    if unifint(diff_lb, diff_ub, (1, 100)) < 30:
        c = choice((2, 3))
        giobjs = objects(gi, F, T, T)
        goobjs = objects(go, F, T, T)
        gi = fill(gi, bgc, mfilter(giobjs, lambda o: c in palette(o)))
        go = fill(go, bgc, mfilter(goobjs, lambda o: c in palette(o)))
    return {'input': gi, 'output': go}

