def generate_b2862040(diff_lb: float, diff_ub: float) -> dict:
    cols = difference(interval(0, 10, 1), (8,))
    while True:
        h = unifint(diff_lb, diff_ub, (10, 30))
        w = unifint(diff_lb, diff_ub, (10, 30))
        nobjs = unifint(diff_lb, diff_ub, (1, (h * w) // 16))
        succ = 0
        tr = 0
        maxtr = 10 * nobjs
        bgc = choice(cols)
        remcols = remove(bgc, cols)
        gi = canvas(bgc, (h, w))
        inds = asindices(gi)
        while succ < nobjs and tr < maxtr:
            tr += 1
            oh = randint(3, 6)
            ow = randint(3, 6)
            obj = box(frozenset({(0, 0), (oh - 1, ow - 1)}))
            if choice((True, False)):
                nkeep = unifint(diff_lb, diff_ub, (2, len(obj) - 1))
                nrem = len(obj) - nkeep
                obj = remove(choice(totuple(obj - corners(obj))), obj)
                for k in range(nrem - 1):
                    xx = sfilter(obj, lambda ij: len(dneighbors(ij) & obj) == 1)
                    if len(xx) == 0:
                        break
                    obj = remove(choice(totuple(xx)), obj)
            npert = unifint(diff_lb, diff_ub, (0, oh + ow))
            objcands = outbox(obj) | outbox(outbox(obj)) | outbox(outbox(outbox(obj)))
            obj = set(obj)
            for k in range(npert):
                obj.add(choice(totuple((objcands - obj) & (mapply(dneighbors, obj) & objcands))))
            obj = normalize(obj)
            oh, ow = shape(obj)
            cands = sfilter(inds, lambda ij: ij[0] <= h - oh and ij[1] <= w - ow)
            if len(cands) == 0:
                continue
            loc = choice(totuple(cands))
            plcd = shift(obj, loc)
            if plcd.issubset(inds):
                gi = fill(gi, choice(remcols), plcd)
                succ += 1
                inds = (inds - plcd) - mapply(neighbors, plcd)
        objs = objects(gi, T, F, F)
        bobjs = colorfilter(objs, bgc)
        objsm = mfilter(bobjs, compose(flip, rbind(bordering, gi)))
        if len(objsm) > 0:
            res = mfilter(objs - bobjs, rbind(adjacent, objsm))
            go = fill(gi, 8, res)
            break
    return {'input': gi, 'output': go}

