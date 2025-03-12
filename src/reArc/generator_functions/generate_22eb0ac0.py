def generate_22eb0ac0(diff_lb: float, diff_ub: float) -> dict:
    colopts = interval(0, 10, 1)
    gi = canvas(0, (1, 1))
    h = unifint(diff_lb, diff_ub, (4, 30))
    w = unifint(diff_lb, diff_ub, (4, 30))
    bgc = choice(colopts)
    remcols = remove(bgc, colopts)
    gi = canvas(bgc, (h, w))
    go = canvas(bgc, (h, w))
    nlocs = unifint(diff_lb, diff_ub, (1, h))
    locs = sample(interval(0, h, 1), nlocs)
    while set(locs).issubset({0, h - 1}):
        locs = sample(interval(0, h, 1), nlocs)
    mp = nlocs // 2
    nbarsdev = unifint(diff_lb, diff_ub, (0, mp))
    nbars = choice((nbarsdev, h - nbarsdev))
    nbars = max(0, min(nbars, nlocs))
    barlocs = sample(locs, nbars)
    nonbarlocs = difference(locs, barlocs)
    barcols = [choice(remcols) for j in range(nbars)]
    acols = [choice(remcols) for j in range(len(nonbarlocs))]
    bcols = [choice(remove(acols[j], remcols)) for j in range(len(nonbarlocs))]
    for bc, bl in zip(barcols, barlocs):
        gi = fill(gi, bc, ((bl, 0), (bl, w - 1)))
        go = fill(go, bc, connect((bl, 0), (bl, w - 1)))
    for (a, b), loc in zip(zip(acols, bcols), nonbarlocs):
        gi = fill(gi, a, {(loc, 0)})
        go = fill(go, a, {(loc, 0)})
        gi = fill(gi, b, {(loc, w - 1)})
        go = fill(go, b, {(loc, w - 1)})
    if choice((True, False)):
        gi = dmirror(gi)
        go = dmirror(go)
    return {'input': gi, 'output': go}

