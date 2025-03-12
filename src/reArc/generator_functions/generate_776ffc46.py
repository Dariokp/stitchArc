def generate_776ffc46(diff_lb: float, diff_ub: float) -> dict:
    cols = interval(0, 10, 1)
    h = unifint(diff_lb, diff_ub, (10, 30))
    w = unifint(diff_lb, diff_ub, (10, 30))
    bgc, sqc, inc, outc = sample(cols, 4)
    gi = canvas(bgc, (h, w))
    sqh = randint(3, h//3+1)
    sqw = randint(3, w//3+1)
    loci = randint(0, 3)
    locj = randint(0, w - sqw)
    bx = box(frozenset({(loci, locj), (loci + sqh - 1, locj + sqw - 1)}))
    bounds = asindices(canvas(-1, (sqh - 2, sqw - 2)))
    obj = {choice(totuple(bounds))}
    ncells = randint(1, (sqh - 2) * (sqw - 2))
    for k in range(ncells - 1):
        obj.add(choice(totuple((bounds - obj) & mapply(dneighbors, obj))))
    obj = normalize(obj)
    oh, ow = shape(obj)
    objp = shift(obj, (loci+1+randint(0, sqh-oh-2), locj+1+randint(0, sqw-ow-2)))
    gi = fill(gi, sqc, bx)
    gi = fill(gi, inc, objp)
    inds = (ofcolor(gi, bgc) - backdrop(bx)) - mapply(neighbors, backdrop(bx))
    cands = sfilter(inds, lambda ij: shift(obj, ij).issubset(inds))
    loc = choice(totuple(cands))
    plcd = shift(obj, loc)
    gi = fill(gi, outc, plcd)
    inds = (inds - plcd) - mapply(neighbors, plcd)
    noccs = unifint(diff_lb, diff_ub, (0, (h * w) // 20))
    succ = 0
    tr = 0
    maxtr = 5 * noccs
    fullinds = asindices(gi)
    while tr < maxtr and succ < noccs:
        tr += 1
        if choice((True, False)):
            sqh = randint(3, h//3+1)
            sqw = randint(3, w//3+1)
            bx = box(frozenset({(0, 0), (sqh - 1, sqw - 1)}))
            bounds = asindices(canvas(-1, (sqh - 2, sqw - 2)))
            obj2 = {choice(totuple(bounds))}
            ncells = randint(1, (sqh - 2) * (sqw - 2))
            for k in range(ncells - 1):
                obj2.add(choice(totuple((bounds - obj2) & mapply(dneighbors, obj2))))
            if normalize(obj2) == obj:
                if len(obj2) < (sqh - 2) * (sqw - 2):
                    obj2.add(choice(totuple((bounds - obj2) & mapply(dneighbors, obj2))))
                else:
                    continue
            obj2 = normalize(obj2)
            ooh, oow = shape(obj2)
            cands1 = connect((-1, -1), (-1, w - sqw + 1))
            cands2 = connect((h-sqh+1, -1), (h-sqh+1, w - sqw + 1))
            cands3 = connect((-1, -1), (h - sqh + 1, -1))
            cands4 = connect((-1, w-sqw+1), (h - sqh + 1, w-sqw+1))
            cands = cands1 | cands2 | cands3 | cands4
            if len(cands) == 0:
                continue
            loc = choice(totuple(cands))
            sloci, slocj = loc
            plcdbx = shift(bx, loc)
            if (backdrop(plcdbx) & fullinds).issubset(inds):
                succ += 1
                oloci = randint(sloci+1, sloci+1+randint(0, sqh-ooh-2))
                olocj = randint(slocj+1, slocj+1+randint(0, sqw-oow-2))
                gi = fill(gi, sqc, plcdbx)
                gi = fill(gi, inc, shift(obj2, (oloci, olocj)))
                inds = inds - backdrop(outbox(plcdbx))
        else:
            ooh = randint(1, h//3-1)
            oow = randint(1, w//3-1)
            bounds = asindices(canvas(-1, (ooh, oow)))
            obj2 = {choice(totuple(bounds))}
            ncells = randint(1, oow * ooh)
            for k in range(ncells - 1):
                obj2.add(choice(totuple((bounds - obj2) & mapply(dneighbors, obj2))))
            if normalize(obj2) == obj:
                if len(obj2) < ooh * oow:
                    obj2.add(choice(totuple((bounds - obj2) & mapply(dneighbors, obj2))))
                else:
                    continue
        if choice((True, False, False)):
            obj2 = obj
        obj2 = normalize(obj2)
        ooh, oow = shape(obj2)
        for kk in range(randint(1, 3)):
            cands = sfilter(inds, lambda ij: ij[0] <= h - ooh and ij[1] <= w - oow)
            if len(cands) == 0:
                continue
            loc = choice(totuple(cands))
            plcd = shift(obj2, loc)
            if plcd.issubset(inds):
                succ += 1
                inds = (inds - plcd) - mapply(neighbors, plcd)
                gi = fill(gi, outc, plcd)
    objs = objects(gi, T, F, F)
    objs = colorfilter(objs, outc)
    objs = mfilter(objs, lambda o: equality(normalize(toindices(o)), obj))
    go = fill(gi, inc, objs)
    return {'input': gi, 'output': go}

