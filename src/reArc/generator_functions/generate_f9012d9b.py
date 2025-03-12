def generate_f9012d9b(diff_lb: float, diff_ub: float) -> dict:
    cols = interval(1, 10, 1)    
    hp = unifint(diff_lb, diff_ub, (2, 10))
    wp = unifint(diff_lb, diff_ub, (2, 10))
    srco = canvas(0, (hp, wp))
    inds = asindices(srco)
    nc = unifint(diff_lb, diff_ub, (1, 9))
    ccols = sample(cols, nc)
    obj = {(choice(ccols), ij) for ij in inds}
    srco = paint(srco, obj)
    gi = paint(srco, obj)
    numhp = unifint(diff_lb, diff_ub, (3, 30 // hp))
    numwp = unifint(diff_lb, diff_ub, (3, 30 // wp))
    for k in range(numhp - 1):
        gi = vconcat(gi, srco)
    srco = tuple(e for e in gi)
    for k in range(numwp - 1):
        gi = hconcat(gi, srco)
    hcropfac = randint(0, hp)
    for k in range(hcropfac):
        gi = gi[:-1]
    gi = dmirror(gi)
    wcropfac = randint(0, wp)
    for k in range(wcropfac):
        gi = gi[:-1]
    gi = dmirror(gi)
    h, w = shape(gi)
    sgh = unifint(diff_lb, diff_ub, (1, h - hp - 1))
    sgw = unifint(diff_lb, diff_ub, (1, w - wp - 1))
    loci = randint(0, h - sgh)
    locj = randint(0, w - sgw)
    loc = (loci, locj)
    shp = (sgh, sgw)
    obj = {loc, decrement(add(loc, shp))}
    obj = backdrop(obj)
    go = subgrid(obj, gi)
    gi = fill(gi, 0, obj)
    mf = choice((
        identity, rot90, rot180, rot270,
        dmirror, vmirror, hmirror, cmirror
    ))
    gi = mf(gi)
    go = mf(go)
    return {'input': gi, 'output': go}

