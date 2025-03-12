def generate_d90796e8(diff_lb: float, diff_ub: float) -> dict:
    cols = difference(interval(0, 10, 1), (8, 2, 3))
    h = unifint(diff_lb, diff_ub, (3, 30))
    w = unifint(diff_lb, diff_ub, (3, 30))
    bgc, noisec = sample(cols, 2)
    gi = canvas(bgc, (h, w))
    nocc = unifint(diff_lb, diff_ub, (1, (h * w) // 3))
    inds = asindices(gi)
    locs = sample(totuple(inds), nocc)
    obj = frozenset({(choice((noisec, 2, 3)), ij) for ij in locs})
    gi = paint(gi, obj)
    fixloc = choice(totuple(inds))
    fixloc2 = choice(totuple(dneighbors(fixloc) & inds))
    gi = fill(gi, 2, {fixloc})
    gi = fill(gi, 3, {fixloc2})
    go = tuple(e for e in gi)
    reds = ofcolor(gi, 2)
    greens = ofcolor(gi, 3)
    tocover = set()
    tolblue = set()
    for r in reds:
        inters = dneighbors(r) & greens
        if len(inters) > 0:
            tocover.add(r)
            tolblue = tolblue | inters
    go = fill(go, bgc, tocover)
    go = fill(go, 8, tolblue)
    return {'input': gi, 'output': go}

