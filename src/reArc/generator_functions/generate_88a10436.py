def generate_88a10436(diff_lb: float, diff_ub: float) -> dict:
    cols = interval(0, 10, 1)
    h = unifint(diff_lb, diff_ub, (8, 30))
    w = unifint(diff_lb, diff_ub, (8, 30))
    objh = unifint(diff_lb, diff_ub, (0, 2))
    objw = unifint(diff_lb, diff_ub, (0 if objh > 0 else 1, 2))
    objh = objh * 2 + 1
    objw = objw * 2 + 1
    bb = asindices(canvas(-1, (objh, objw)))
    sp = (objh // 2, objw // 2)
    obj = {sp}
    bb = remove(sp, bb)
    ncells = unifint(diff_lb, diff_ub, (max(objh, objw), objh * objw))
    for k in range(ncells - 1):
        obj.add(choice(totuple((bb - obj) & mapply(dneighbors, obj))))
    while height(obj) != objh or width(obj) != objw:
        obj.add(choice(totuple((bb - obj) & mapply(dneighbors, obj))))
    bgc, fgc = sample(cols, 2)
    remcols = remove(bgc, remove(fgc, cols))
    ncols = unifint(diff_lb, diff_ub, (1, 8))
    ccols = sample(remcols, ncols)
    obj = {(choice(ccols), ij) for ij in obj}
    obj = normalize(obj)
    gi = canvas(bgc, (h, w))
    go = canvas(bgc, (h, w))
    loci = randint(0, h - objh)
    locj = randint(0, w - objw)
    loc = (loci, locj)
    plcd = shift(obj, loc)
    gi = paint(gi, plcd)
    go = paint(go, plcd)
    inds = (asindices(gi) - toindices(plcd)) - mapply(neighbors, toindices(plcd))
    nobjs = unifint(diff_lb, diff_ub, (1, (h * w) // (2 * ncells)))
    maxtrials = 4 * nobjs
    tr = 0
    succ = 0
    while succ < nobjs and tr <= maxtrials:
        if len(inds) == 0:
            break
        loc = choice(totuple(inds))
        plcd = shift(obj, loc)
        plcdi = toindices(plcd)
        if plcdi.issubset(inds):
            go = paint(go, plcd)
            gi = fill(gi, fgc, {center(plcdi)})
            succ += 1
            inds = (inds - plcdi) - mapply(dneighbors, plcdi)
        tr += 1
    return {'input': gi, 'output': go}

