def generate_6aa20dc0(diff_lb: float, diff_ub: float) -> dict:
    cols = interval(0, 10, 1)
    h = unifint(diff_lb, diff_ub, (10, 30))
    w = unifint(diff_lb, diff_ub, (10, 30))
    od = unifint(diff_lb, diff_ub, (2, 4))
    ncellsextra = randint(1, max(1, (od ** 2 - 2) // 2))
    sinds = asindices(canvas(-1, (od, od)))
    extracells = set(sample(totuple(sinds - {(0, 0), (od - 1, od - 1)}), ncellsextra))
    extracells.add(choice(totuple(dneighbors((0, 0)) & sinds)))
    extracells.add(choice(totuple(dneighbors((od - 1, od - 1)) & sinds)))
    extracells = frozenset(extracells)
    bgc, fgc, c1, c2 = sample(cols, 4)
    obj = frozenset({(c1, (0, 0)), (c2, (od - 1, od - 1))}) | recolor(fgc, extracells)
    obj = obj | dmirror(obj)
    if choice((True, False)):
        obj = hmirror(obj)
    gi = canvas(bgc, (h, w))
    loci = randint(0, h - od)
    locj = randint(0, w - od)
    plcd = shift(obj, (loci, locj))
    gi = paint(gi, plcd)
    go = tuple(e for e in gi)
    inds = asindices(gi)
    inds = inds - backdrop(outbox(plcd))
    nocc = unifint(diff_lb, diff_ub, (1, max(1, (h * w) // (od ** 2 * 2))))
    succ = 0
    tr = 0
    maxtr = 4 * nocc
    while succ < nocc and tr < maxtr:
        tr += 1
        fac = randint(1, 4)
        mf1 = choice((identity, dmirror, vmirror, cmirror, hmirror))
        mf2 = choice((identity, dmirror, vmirror, cmirror, hmirror))
        mf = compose(mf2, mf1)
        cobj = normalize(upscale(mf(obj), fac))
        ohx, owx = shape(cobj)
        cands = sfilter(inds, lambda ij: ij[0] <= h - ohx and ij[1] <= w - owx)
        if len(cands) == 0:
            continue
        locc = choice(totuple(cands))
        cobjo = shift(cobj, locc)
        cobji = sfilter(cobjo, lambda cij: cij[0] != fgc)
        cobjoi = toindices(cobjo)
        if cobjoi.issubset(inds):
            succ += 1
            inds = inds - backdrop(outbox(cobjoi))
            gi = paint(gi, cobji)
            go = paint(go, cobjo)
    return {'input': gi, 'output': go}

