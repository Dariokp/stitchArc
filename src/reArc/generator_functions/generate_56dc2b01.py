def generate_56dc2b01(diff_lb: float, diff_ub: float) -> dict:
    cols = difference(interval(0, 10, 1), (2, 8))
    h = unifint(diff_lb, diff_ub, (4, 30))
    w = unifint(diff_lb, diff_ub, (6, 30))
    oh = unifint(diff_lb, diff_ub, (1, h))
    ow = unifint(diff_lb, diff_ub, (1, (w - 1) // 2 - 1))
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
    locj = unifint(diff_lb, diff_ub, (1, w - ow))
    bgc, objc = sample(cols, 2)
    gi = canvas(bgc, (h, w))
    barlocji = unifint(diff_lb, diff_ub, (0, locj))
    barlocj = locj - barlocji
    barlocj = min(max(0, barlocj), locj - 1)
    gi = fill(gi, 2, connect((0, barlocj), (h - 1, barlocj)))
    go = fill(gi, objc, shift(obj, (loci, barlocj + 1)))
    go = fill(go, 8, connect((0, barlocj + ow + 1), (h - 1, barlocj + ow + 1)))
    gi = fill(gi, objc, shift(obj, (loci, locj)))
    mfs = (identity, dmirror, cmirror, vmirror, hmirror, rot90, rot180, rot270)
    nmfs = choice((1, 2))
    for fn in sample(mfs, nmfs):
        gi = fn(gi)
        go = fn(go)
    return {'input': gi, 'output': go}

