def generate_ded97339(diff_lb: float, diff_ub: float) -> dict:
    cols = interval(0, 10, 1)
    h = unifint(diff_lb, diff_ub, (5, 30))
    w = unifint(diff_lb, diff_ub, (5, 30))
    bgc, linc = sample(cols, 2)
    gi = canvas(bgc, (h, w))
    ndots = unifint(diff_lb, diff_ub, (2, (h * w) // 9))
    inds = asindices(gi)
    dots = set()
    if choice((True, False)):
        idxi = randint(0, h - 1)
        locj1 = randint(0, w - 3)
        locj2 = randint(locj1 + 2, w - 1)
        dots.add((idxi, locj1))
        dots.add((idxi, locj2))
    else:
        idxj = randint(0, w - 1)
        loci1 = randint(0, h - 3)
        loci2 = randint(loci1 + 2, h - 1)
        dots.add((loci1, idxj))
        dots.add((loci2, idxj))
    for k in range(ndots - 2):
        if len(inds) == 0:
            break
        loc = choice(totuple(inds))
        dots.add(loc)
        inds = (inds - {loc}) - neighbors(loc)
    gi = fill(gi, linc, dots)
    go = tuple(e for e in gi)
    for ii, r in enumerate(gi):
        if r.count(linc) > 1:
            a = r.index(linc)
            b = w - r[::-1].index(linc) - 1
            go = fill(go, linc, connect((ii, a), (ii, b)))
    go = dmirror(go)
    gi = dmirror(gi)
    for ii, r in enumerate(gi):
        if r.count(linc) > 1:
            a = r.index(linc)
            b = h - r[::-1].index(linc) - 1
            go = fill(go, linc, connect((ii, a), (ii, b)))
    return {'input': gi, 'output': go}

