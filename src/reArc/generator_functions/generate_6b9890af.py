def generate_6b9890af(diff_lb: float, diff_ub: float) -> dict:
    cols = interval(0, 10, 1)
    oh = unifint(diff_lb, diff_ub, (2, 5))
    ow = unifint(diff_lb, diff_ub, (2, 5))
    h = unifint(diff_lb, diff_ub, (2*oh+2, 30))
    w = unifint(diff_lb, diff_ub, (2*ow+2, 30))
    bounds = asindices(canvas(-1, (oh, ow)))
    obj = {choice(totuple(bounds))}
    while shape(obj) != (oh, ow):
        obj.add(choice(totuple((bounds - obj) & mapply(neighbors, obj))))
    maxfac = 1
    while oh * maxfac + 2 <= h - oh and ow * maxfac + 2 <= w - ow:
        maxfac += 1
    maxfac -= 1
    fac = unifint(diff_lb, diff_ub, (1, maxfac))
    bgc, sqc = sample(cols, 2)
    remcols = remove(bgc, remove(sqc, cols))
    numc = unifint(diff_lb, diff_ub, (1, 8))
    ccols = sample(remcols, numc)
    obj = {(choice(ccols), ij) for ij in obj}
    gi = canvas(bgc, (h, w))
    sq = box(frozenset({(0, 0), (oh * fac + 1, ow * fac + 1)}))
    loci = randint(0, h - (oh * fac + 2) - oh)
    locj = randint(0, w - (ow * fac + 2))
    gi = fill(gi, sqc, shift(sq, (loci, locj)))
    loci = randint(loci+oh*fac+2, h - oh)
    locj = randint(0, w - ow)
    objp = shift(obj, (loci, locj))
    gi = paint(gi, objp)
    go = canvas(bgc, (oh * fac + 2, ow * fac + 2))
    go = fill(go, sqc, sq)
    go2 = paint(canvas(bgc, (oh, ow)), obj)
    upscobj = asobject(upscale(go2, fac))
    go = paint(go, shift(upscobj, (1, 1)))
    rotf = choice((identity, rot90, rot180, rot270))
    gi = rotf(gi)
    go = rotf(go)
    return {'input': gi, 'output': go}

