def generate_137eaa0f(diff_lb: float, diff_ub: float) -> dict:
    cols = interval(0, 10, 1)
    h = unifint(diff_lb, diff_ub, (2, 4))
    w = unifint(diff_lb, diff_ub, (2, 4))
    bgc = choice(cols)
    remcols = remove(bgc, cols)
    dotc = choice(remcols)
    remcols = remove(dotc, remcols)
    go = canvas(dotc, (h, w))
    inds = totuple(asindices(go))
    loc = choice(inds)
    reminds = remove(loc, inds)
    nc = unifint(diff_lb, diff_ub, (1, min(h * w - 1, 8)))
    choscols = sample(remcols, nc)
    cd = {c: set() for c in choscols}
    for c in choscols:
        ij = choice(reminds)
        cd[c].add(ij)
        reminds = remove(ij, reminds)
    for ri in reminds:
        cd[choice(choscols)].add(ri)
    for c, idxes in cd.items():
        go = fill(go, c, idxes)
    gih = unifint(diff_lb, diff_ub, (min(h, w) * 2, 30))
    giw = unifint(diff_lb, diff_ub, (min(h, w) * 2, 30))
    objs = tuple(
        normalize(insert((dotc, loc), frozenset({(c, ij) for ij in cd[c]}))) \
            for c in choscols
    )
    maxtr = min(h, w) * 2
    maxtrtot = 1000
    while True:
        succ = True
        gi = canvas(bgc, (gih, giw))
        inds = asindices(gi)
        for obj in objs:
            oh, ow = shape(obj)
            succ2 = False
            tr = 0
            while tr < maxtr and not succ2:
                loci = randint(0, gih - oh)
                locj = randint(0, giw - ow)
                plcd = shift(obj, (loci, locj))
                tr += 1
                if toindices(plcd).issubset(inds):
                    succ2 = True
            if succ2:
                gi = paint(gi, plcd)
                inds = difference(inds, toindices(plcd))
                inds = difference(inds, mapply(neighbors, toindices(plcd)))
            else:
                succ = False
                break
        if succ:
            break
        maxtrtot += 1
        if maxtrtot < 1000:
            break
        maxtr = int(maxtr * 1.5)
        gih = randint(gih, 30)
        giw = randint(giw, 30)
    return {'input': gi, 'output': go}

