def generate_98cf29f8(diff_lb: float, diff_ub: float) -> dict:
    cols = interval(0, 10, 1)
    h = unifint(diff_lb, diff_ub, (10, 30))
    w = unifint(diff_lb, diff_ub, (10, 30))
    objh = unifint(diff_lb, diff_ub, (2, h - 5))
    objw = unifint(diff_lb, diff_ub, (2, w - 5))
    loci = randint(0, h - objh)
    locj = randint(0, w - objw)
    loc = (loci, locj)
    obj = backdrop(frozenset({(loci, locj), (loci + objh - 1, locj + objw - 1)}))
    bgc, objc, otherc = sample(cols, 3)
    gi = canvas(bgc, (h, w))
    gi = fill(gi, objc, obj)
    bmarg = h - (loci + objh)
    rmarg = w - (locj + objw)
    tmarg = loci
    lmarg = locj
    margs = (bmarg, rmarg, tmarg, lmarg)
    options = [idx for idx, marg in enumerate(margs) if marg > 2]
    pos = choice(options)
    for k in range(pos):
        gi = rot90(gi)
    h, w = shape(gi)
    ofc = ofcolor(gi, objc)
    locis = randint(lowermost(ofc)+2, h-2)
    locie = randint(locis+1, h-1)
    locjs = randint(0, min(w - 2, rightmost(ofc)))
    locje = randint(max(locjs+1, leftmost(ofc)), w - 1)
    otherobj = backdrop(frozenset({(locis, locjs), (locie, locje)}))
    ub = min(rightmost(ofc), rightmost(otherobj))
    lb = max(leftmost(ofc), leftmost(otherobj))
    jloc = randint(lb, ub)
    ln = connect((lowermost(ofc)+1, jloc), (uppermost(otherobj)-1, jloc))
    gib = tuple(e for e in gi)
    gi = fill(gi, otherc, otherobj)
    gi = fill(gi, otherc, ln)
    go = fill(gib, otherc, shift(otherobj, (-len(ln), 0)))
    mfs = (identity, dmirror, cmirror, vmirror, hmirror, rot90, rot180, rot270)
    nmfs = choice((1, 2))
    for fn in sample(mfs, nmfs):
        gi = fn(gi)
        go = fn(go)
    return {'input': gi, 'output': go}

