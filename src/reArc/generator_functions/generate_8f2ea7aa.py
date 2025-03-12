def generate_8f2ea7aa(diff_lb: float, diff_ub: float) -> dict:
    colopts = interval(0, 10, 1)
    d = unifint(diff_lb, diff_ub, (2, 5))
    bgc = choice(colopts)
    remcols = remove(bgc, colopts)
    d2 = d ** 2
    gi = canvas(bgc, (d2, d2))
    go = canvas(bgc, (d2, d2))
    minig = canvas(bgc, (d, d))
    inds = totuple(asindices(minig))
    mp = d2 // 2
    devrng = (0, mp)
    dev = unifint(diff_lb, diff_ub, devrng)
    devs = choice((+1, -1))
    num = mp + devs * dev
    num = max(min(num, d2), 0)
    locs = set(sample(inds, num))
    while shape(locs) != (d, d):
        locs.add(choice(totuple(set(inds) - locs)))
    ncols = unifint(diff_lb, diff_ub, (1, 9))
    cols = sample(remcols, ncols)
    for ij in locs:
        minig = fill(minig, choice(cols), {ij})
    itv = interval(0, d2, d)
    plcopts = totuple(product(itv, itv))
    plc = choice(plcopts)
    minigo = asobject(minig)
    gi = paint(gi, shift(minigo, plc))
    for ij in locs:
        go = paint(go, shift(minigo, multiply(ij, d)))
    return {'input': gi, 'output': go}

