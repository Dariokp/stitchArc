def generate_3eda0437(diff_lb: float, diff_ub: float) -> dict:
    cols = difference(interval(1, 10, 1), (6,))
    h = unifint(diff_lb, diff_ub, (3, 8))
    w = unifint(diff_lb, diff_ub, (3, 30))
    if choice((True, False)):
        h, w = w, h
    ncols = unifint(diff_lb, diff_ub, (1, 8))
    fgcs = sample(cols, ncols)
    gi = canvas(-1, (h, w))
    gi = paint(gi, {(choice(fgcs), ij) for ij in asindices(gi)})
    spac = unifint(diff_lb, diff_ub, (1, (h * w) // 3 * 2))
    inds = asindices(gi)
    obj = sample(totuple(inds), spac)
    gi = fill(gi, 0, obj)
    locx = (randint(0, h-1), randint(0, w-1))
    gi = fill(gi, 0, {locx, add(locx, RIGHT), add(locx, DOWN), add(locx, UNITY)})
    maxsiz = -1
    mapper = dict()
    maxpossw = max([r.count(0) for r in gi])
    maxpossh = max([c.count(0) for c in dmirror(gi)])
    for a in range(2, maxpossh+1):
        for b in range(2, maxpossw+1):
            siz = a * b
            if siz < maxsiz:
                continue
            objx = recolor(0, asindices(canvas(-1, (a, b))))
            occs = occurrences(gi, objx)
            if len(occs) > 0:
                if siz == maxsiz:
                    mapper[objx] = occs
                elif siz > maxsiz:
                    mapper = {objx: occs}
                    maxsiz = siz
    go = tuple(e for e in gi)
    for obj, locs in mapper.items():
        go = fill(go, 6, mapply(lbind(shift, obj), locs))
    return {'input': gi, 'output': go}

