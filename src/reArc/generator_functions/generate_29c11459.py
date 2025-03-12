def generate_29c11459(diff_lb: float, diff_ub: float) -> dict:
    colopts = remove(5, interval(0, 10, 1))
    gi = canvas(0, (1, 1))
    h = unifint(diff_lb, diff_ub, (5, 30))
    w = unifint(diff_lb, diff_ub, (5, 29))
    if w % 2 == 0:
        w = choice((max(5, w - 1), min(29, w + 1)))
    bgc = choice(colopts)
    remcols = remove(bgc, colopts)
    ncols = unifint(diff_lb, diff_ub, (2, len(remcols)))
    ccols = sample(remcols, ncols)
    gi = canvas(bgc, (h, w))
    go = canvas(bgc, (h, w))
    nlocs = unifint(diff_lb, diff_ub, (1, h))
    locs = sample(interval(0, h, 1), nlocs)
    while set(locs).issubset({0, h - 1}):
        locs = sample(interval(0, h, 1), nlocs)
    acols = []
    bcols = []
    aforb = -1
    bforb = -1
    for k in range(nlocs):
        ac = choice(remove(aforb, ccols))
        acols.append(ac)
        aforb = ac
        bc = choice(remove(bforb, ccols))
        bcols.append(bc)
        bforb = bc
    for (a, b), loc in zip(zip(acols, bcols), sorted(locs)):
        gi = fill(gi, a, {(loc, 0)})
        gi = fill(gi, b, {(loc, w - 1)})
        go = fill(go, a, connect((loc, 0), (loc, w // 2 - 1)))
        go = fill(go, b, connect((loc, w // 2 + 1), (loc, w - 1)))
        go = fill(go, 5, {(loc, w // 2)})
    if choice((True, False)):
        gi = dmirror(gi)
        go = dmirror(go)
    return {'input': gi, 'output': go}

