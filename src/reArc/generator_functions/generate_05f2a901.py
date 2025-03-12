def generate_05f2a901(diff_lb: float, diff_ub: float) -> dict:
    cols = interval(0, 10, 1)
    h = unifint(diff_lb, diff_ub, (8, 30))
    w = unifint(diff_lb, diff_ub, (8, 30))
    objh = unifint(diff_lb, diff_ub, (2, min(w//2, h//2)))
    objw = unifint(diff_lb, diff_ub, (objh, w//2))
    bb = asindices(canvas(-1, (objh, objw)))
    sp = choice(totuple(bb))
    obj = {sp}
    bb = remove(sp, bb)
    ncells = unifint(diff_lb, diff_ub, (objh + objw, objh * objw))
    for k in range(ncells - 1):
        obj.add(choice(totuple((bb - obj) & mapply(dneighbors, obj))))
    if height(obj) * width(obj) == len(obj):
        obj = remove(choice(totuple(obj)), obj)
    obj = normalize(obj)
    objh, objw = shape(obj)
    loci = unifint(diff_lb, diff_ub, (3, h - objh))
    locj = unifint(diff_lb, diff_ub, (0, w - objw))
    loc = (loci, locj)
    bgc, fgc, destc = sample(cols, 3)
    gi = canvas(bgc, (h, w))
    go = canvas(bgc, (h, w))
    obj = shift(obj, loc)
    gi = fill(gi, fgc, obj)
    sqd = randint(1, min(w, loci - 1))
    locisq = randint(0, loci-sqd-1)
    locjsq = randint(locj-sqd+1, locj+objw-1)
    locsq = (locisq, locjsq)
    sq = backdrop({(locisq, locjsq), (locisq+sqd-1, locjsq+sqd-1)})
    gi = fill(gi, destc, sq)
    go = fill(go, destc, sq)
    while len(obj & sq) == 0:
        obj = shift(obj, (-1, 0))
    obj = shift(obj, (1, 0))
    go = fill(go, fgc, obj)
    mfs = (identity, dmirror, cmirror, vmirror, hmirror, rot90, rot180, rot270)
    nmfs = choice((1, 2))
    for fn in sample(mfs, nmfs):
        gi = fn(gi)
        go = fn(go)
    return {'input': gi, 'output': go}

