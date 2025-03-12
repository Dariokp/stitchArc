def generate_36d67576(diff_lb: float, diff_ub: float) -> dict:
    cols = interval(0, 10, 1)
    while True:
        h = unifint(diff_lb, diff_ub, (10, 30))
        w = unifint(diff_lb, diff_ub, (10, 30))
        bgc, mainc, markerc = sample(cols, 3)
        remcols = difference(cols, (bgc, mainc, markerc))
        ncols = unifint(diff_lb, diff_ub, (1, len(remcols)))
        ccols = sample(remcols, ncols)
        gi = canvas(bgc, (h, w))
        oh = unifint(diff_lb, diff_ub, (2, 5))
        ow = unifint(diff_lb, diff_ub, (3 if oh == 2 else 2, 5))
        if choice((True, False)):
            oh, ow = ow, oh
        bounds = asindices(canvas(-1, (oh, ow)))
        ncells = unifint(diff_lb, diff_ub, (4, len(bounds)))
        obj = {choice(totuple(bounds))}
        for k in range(ncells - 1):
            obj.add(choice(totuple((bounds - obj) & mapply(neighbors, obj))))
        obj = normalize(obj)
        oh, ow = shape(obj)
        ntocompc = unifint(diff_lb, diff_ub, (1, ncells - 3))
        markercell = choice(totuple(obj))
        remobj = remove(markercell, obj)
        markercellobj = {(markerc, markercell)}
        tocompc = set(sample(totuple(remobj), ntocompc))
        mainpart = (obj - {markercell}) - tocompc
        mainpartobj = recolor(mainc, mainpart)
        tocompcobj = {(choice(remcols), ij) for ij in tocompc}
        obj = tocompcobj | mainpartobj | markercellobj
        smobj = mainpartobj | markercellobj
        smobjn = normalize(smobj)
        isfakesymm = False
        for symmf in [dmirror, cmirror, hmirror, vmirror]:
            if symmf(smobjn) == smobjn and symmf(obj) != obj:
                isfakesymm = True
                break
        if isfakesymm:
            continue
        loci = randint(0, h - oh)
        locj = randint(0, w - ow)
        plcd = shift(obj, (loci, locj))
        gi = paint(gi, plcd)
        plcdi = toindices(plcd)
        inds = (asindices(gi) - plcdi) - mapply(neighbors, plcdi)
        noccs = unifint(diff_lb, diff_ub, (1, max(1, (h * w) // (2 * len(obj)))))
        succ = 0
        tr = 0
        maxtr = noccs * 5
        go = tuple(e for e in gi)
        while tr < maxtr and succ < noccs:
            tr += 1
            mf1 = choice((identity, dmirror, cmirror, hmirror, vmirror))
            mf2 = choice((identity, dmirror, cmirror, hmirror, vmirror))
            mf = compose(mf1, mf2)
            outobj = normalize(mf(obj))
            inobj = sfilter(outobj, lambda cij: cij[0] in [mainc, markerc])
            oh, ow = shape(outobj)
            cands = sfilter(inds, lambda ij: ij[0] <= h - oh and ij[1] <= w - ow)
            if len(cands) == 0:
                continue
            loc = choice(totuple(cands))
            outobjp = shift(outobj, loc)
            inobjp = shift(inobj, loc)
            outobjpi = toindices(outobjp)
            if outobjpi.issubset(inds):
                succ += 1
                inds = (inds - outobjpi) - mapply(neighbors, outobjpi)
                gi = paint(gi, inobjp)
                go = paint(go, outobjp)
        break
    return {'input': gi, 'output': go}

