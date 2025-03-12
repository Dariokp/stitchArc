def generate_855e0971(diff_lb: float, diff_ub: float) -> dict:
    cols = interval(0, 10, 1)
    nbarsd = unifint(diff_lb, diff_ub, (1, 4))
    nbars = choice((nbarsd, 11 - nbarsd))
    nbars = max(3, nbars)
    h = unifint(diff_lb, diff_ub, (nbars, 30))
    w = unifint(diff_lb, diff_ub, (3, 30))
    barsizes = [2] * nbars
    while sum(barsizes) < h:
        j = randint(0, nbars - 1)
        barsizes[j] += 1
    gi = tuple()
    go = tuple()
    locs = interval(0, w, 1)
    dotc = choice(cols)
    remcols = remove(dotc, cols)
    lastcol = -1
    nloclbs = [choice((0, 1)) for k in range(len(barsizes))]
    if sum(nloclbs) < 2:
        loc1, loc2 = sample(interval(0, len(nloclbs), 1), 2)
        nloclbs[loc1] = 1
        nloclbs[loc2] = 1
    for bs, nloclb in zip(barsizes, nloclbs):
        col = choice(remove(lastcol, remcols))
        gim = canvas(col, (bs, w))
        gom = canvas(col, (bs, w))
        nl = unifint(diff_lb, diff_ub, (nloclb, w // 2))
        chlocs = sample(locs, nl)
        for jj in chlocs:
            idx = (randint(0, bs - 1), jj)
            gim = fill(gim, dotc, {idx})
            gom = fill(gom, dotc, vfrontier(idx))
        lastcol = col
        gi = gi + gim
        go = go + gom
    if choice((True, False)):
        gi = dmirror(gi)
        go = dmirror(go)
    return {'input': gi, 'output': go}

