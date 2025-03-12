def generate_7b6016b9(diff_lb: float, diff_ub: float) -> dict:
    cols = remove(3, remove(2, interval(0, 10, 1)))
    while True:
        h = unifint(diff_lb, diff_ub, (5, 30))
        w = unifint(diff_lb, diff_ub, (5, 30))
        bgc, fgc = sample(cols, 2)
        numl = unifint(diff_lb, diff_ub, (4, min(h, w)))
        gi = canvas(bgc, (h, w))
        jint = interval(0, w, 1)
        iint = interval(0, h, 1)
        iopts = interval(1, h-1, 1)
        jopts = interval(1, w-1, 1)
        numlh = randint(numl//3, numl//3*2)
        numlw = numl - numlh
        for k in range(numlh):
            if len(iopts) == 0:
                continue
            loci = choice(iopts)
            iopts = remove(loci, iopts)
            iopts = remove(loci+1, iopts)
            iopts = remove(loci-1, iopts)
            a, b = sample(jint, 2)
            a = randint(0, a)
            b = randint(b, w - 1)
            gi = fill(gi, fgc, connect((loci, a), (loci, b)))
        for k in range(numlw):
            if len(jopts) == 0:
                continue
            locj = choice(jopts)
            jopts = remove(locj, jopts)
            jopts = remove(locj+1, jopts)
            jopts = remove(locj-1, jopts)
            a, b = sample(iint, 2)
            a = randint(0, a)
            b = randint(b, h - 1)
            gi = fill(gi, fgc, connect((a, locj), (b, locj)))
        objs = objects(gi, T, F, F)
        bgobjs = colorfilter(objs, bgc)
        tofill = toindices(mfilter(bgobjs, compose(flip, rbind(bordering, gi))))
        if len(tofill) > 0:
            break
    tofix = mapply(neighbors, tofill) - tofill
    gi = fill(gi, fgc, tofix)
    go = fill(gi, 2, tofill)
    go = replace(go, bgc, 3)
    return {'input': gi, 'output': go}

