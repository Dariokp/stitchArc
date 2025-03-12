def generate_63613498(diff_lb: float, diff_ub: float) -> dict:
    cols = interval(0, 10, 1)
    h = unifint(diff_lb, diff_ub, (10, 30))
    w = unifint(diff_lb, diff_ub, (10, 30))
    bgc, sepc = sample(cols, 2)
    remcols = remove(bgc, remove(sepc, cols))
    ncols = unifint(diff_lb, diff_ub, (1, 8))
    ccols = sample(remcols, ncols)
    objh = unifint(diff_lb, diff_ub, (1, h//3))
    objw = unifint(diff_lb, diff_ub, (1, w//3))
    bounds = asindices(canvas(-1, (objh, objw)))
    sp = choice(totuple(bounds))
    obj = {sp}
    ncells = unifint(diff_lb, diff_ub, (1, (objh * objw)))
    for k in range(ncells - 1):
        obj.add(choice(totuple((bounds - obj) & mapply(dneighbors, obj))))
    gi = canvas(bgc, (h, w))
    objc = choice(ccols)
    gi = fill(gi, objc, obj)
    sep = connect((objh+1, 0), (objh+1, objw+1)) | connect((0, objw+1), (objh+1, objw+1))
    gi = fill(gi, sepc, sep)
    inds = asindices(gi)
    inds -= backdrop(sep)
    nobjs = unifint(diff_lb, diff_ub, (1, (h * w) // 20))
    succ = 0
    tr = 0
    maxtr = 5 * nobjs
    baseobj = normalize(obj)
    obj = normalize(obj)
    go = tuple(e for e in gi)
    while (succ < nobjs and tr < maxtr) or succ == 0:
        tr += 1
        oh, ow = shape(obj)
        cands = sfilter(inds, lambda ij: ij[0] <= h - oh and ij[1] <= w - ow)
        if len(cands) == 0:
            break
        loc = choice(totuple(cands))
        plcd = shift(obj, loc)
        if plcd.issubset(inds):
            col = choice(ccols)
            gi = fill(gi, col, plcd)
            go = fill(go, sepc if succ == 0 else col, plcd)
            succ += 1
            inds = (inds - plcd) - mapply(dneighbors, plcd)
        objh = randint(1, h // 3)
        objw = randint(2 if objh == 1 else 1, w // 3)
        if choice((True, False)):
            objh, objw = objw, objh
        bounds = asindices(canvas(-1, (objh, objw)))
        sp = choice(totuple(bounds))
        obj = {sp}
        ncells = unifint(diff_lb, diff_ub, (1, (objh * objw)))
        for k in range(ncells - 1):
            obj.add(choice(totuple((bounds - obj) & mapply(dneighbors, obj))))
        obj = normalize(obj)
        obj = set(obj)
        if obj == baseobj:
            if len(obj) < objh * objw:
                obj.add(choice(totuple((bounds - obj) & mapply(dneighbors, obj))))
            else:
                obj = remove(choice(totuple(corners(obj))), obj)
        obj = normalize(obj)
    rotf = choice((identity, rot90, rot180, rot270))
    gi = rotf(gi)
    go = rotf(go)
    return {'input': gi, 'output': go}

