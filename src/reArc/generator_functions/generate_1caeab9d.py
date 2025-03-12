def generate_1caeab9d(diff_lb: float, diff_ub: float) -> dict:
    cols = difference(interval(0, 10, 1), (1,))
    h = unifint(diff_lb, diff_ub, (3, 30))
    w = unifint(diff_lb, diff_ub, (6, 30))
    oh = unifint(diff_lb, diff_ub, (1, h//2))
    ow = unifint(diff_lb, diff_ub, (1, w//3))
    bb = asindices(canvas(-1, (oh, ow)))
    sp = choice(totuple(bb))
    obj = {sp}
    bb = remove(sp, bb)
    ncellsd = unifint(diff_lb, diff_ub, (0, (oh * ow) // 2))
    ncells = choice((ncellsd, oh * ow - ncellsd))
    ncells = min(max(0, ncells), oh * ow - 1)
    for k in range(ncells):
        obj.add(choice(totuple((bb - obj) & mapply(neighbors, obj))))
    obj = normalize(obj)
    oh, ow = shape(obj)
    loci = randint(0, h - oh)
    numo = unifint(diff_lb, diff_ub, (2, min(8, w // ow))) - 1
    itv = interval(0, w, 1)
    locj = randint(0, w - ow)
    objp = shift(obj, (loci, locj))
    bgc = choice(cols)
    remcols = remove(bgc, cols)
    c = canvas(bgc, (h, w))
    gi = fill(c, 1, objp)
    go = fill(c, 1, objp)
    itv = difference(itv, interval(locj, locj + ow, 1))
    for k in range(numo):
        cands = sfilter(itv, lambda j: set(interval(j, j + ow, 1)).issubset(set(itv)))
        if len(cands) == 0:
            break
        locj = choice(cands)
        col = choice(remcols)
        remcols = remove(col, remcols)
        gi = fill(gi, col, shift(obj, (randint(0, h - oh), locj)))
        go = fill(go, col, shift(obj, (loci, locj)))
        itv = difference(itv, interval(locj, locj + ow, 1))
    return {'input': gi, 'output': go}

