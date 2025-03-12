def generate_8d510a79(diff_lb: float, diff_ub: float) -> dict:
    cols = difference(interval(0, 10, 1), (1, 2))
    h = unifint(diff_lb, diff_ub, (5, 30))
    w = unifint(diff_lb, diff_ub, (3, 30))
    barloci = randint(2, h - 3)
    bgc = choice(cols)
    remcols = remove(bgc, cols)
    barcol = choice(remcols)
    gi = canvas(bgc, (h, w))
    bar = connect((barloci, 0), (barloci, w - 1))
    gi = fill(gi, barcol, bar)
    go = tuple(e for e in gi)
    jinds = interval(0, w, 1)
    numtop = unifint(diff_lb, diff_ub, (1, w - 1))
    numbot = unifint(diff_lb, diff_ub, (1, w - 1))
    tops = sample(jinds, numtop)
    bots = sample(jinds, numbot)
    for t in tops:
        loci = randint(0, barloci - 2)
        col = choice((1, 2))
        loc = (loci, t)
        gi = fill(gi, col, {loc})
        if col == 1:
            go = fill(go, col, connect(loc, (0, t)))
        else:
            go = fill(go, col, connect(loc, (barloci - 1, t)))
    for t in bots:
        loci = randint(barloci + 2, h - 1)
        col = choice((1, 2))
        loc = (loci, t)
        gi = fill(gi, col, {loc})
        if col == 1:
            go = fill(go, col, connect(loc, (h - 1, t)))
        else:
            go = fill(go, col, connect(loc, (barloci + 1, t)))
    if choice((True, False)):
        gi = dmirror(gi)
        go = dmirror(go)
    return {'input': gi, 'output': go}

