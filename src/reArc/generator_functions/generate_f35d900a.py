def generate_f35d900a(diff_lb: float, diff_ub: float) -> dict:
    cols = remove(5, interval(0, 10, 1))
    h = unifint(diff_lb, diff_ub, (4, 30))
    w = unifint(diff_lb, diff_ub, (4, 30))
    bgc, c1, c2 = sample(cols, 3)
    oh = unifint(diff_lb, diff_ub, (4, h))
    ow = unifint(diff_lb, diff_ub, (4, w))
    loci = randint(0, h - oh)
    locj = randint(0, w - ow)
    bx = box(frozenset({(loci, locj), (loci + oh - 1, locj + ow - 1)}))
    gi = canvas(bgc, (h, w))
    go = canvas(bgc, (h, w))
    gi = fill(gi, c1, {ulcorner(bx), lrcorner(bx)})
    gi = fill(gi, c2, {urcorner(bx), llcorner(bx)})
    go = fill(go, c1, {ulcorner(bx), lrcorner(bx)})
    go = fill(go, c2, {urcorner(bx), llcorner(bx)})
    go = fill(go, c1, neighbors(urcorner(bx)) | neighbors(llcorner(bx)))
    go = fill(go, c2, neighbors(ulcorner(bx)) | neighbors(lrcorner(bx)))
    crns = corners(bx)
    for c in crns:
        cobj = {c}
        remcorns = remove(c, crns)
        belongto = sfilter(bx, lambda ij: manhattan(cobj, {ij}) <= valmin(remcorns, lambda cc: manhattan({ij}, {cc})))
        valids = sfilter(belongto, lambda ij: manhattan(cobj, {ij}) > 1 and manhattan(cobj, {ij}) % 2 == 0)
        go = fill(go, 5, valids)
    return {'input': gi, 'output': go}

