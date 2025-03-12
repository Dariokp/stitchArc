def generate_a61f2674(diff_lb: float, diff_ub: float) -> dict:
    cols = remove(2, remove(1, interval(0, 10, 1)))
    w = unifint(diff_lb, diff_ub, (5, 28))
    h = unifint(diff_lb, diff_ub, (w // 2 + 1, 30))
    bgc, fgc = sample(cols, 2)
    gi = canvas(bgc, (h, w))
    go = canvas(bgc, (h, w))
    nbars = unifint(diff_lb, diff_ub, (2, w // 2))
    barlocs = []
    options = interval(0, w, 1)
    while len(options) > 0 and len(barlocs) < nbars:
        loc = choice(options)
        barlocs.append(loc)
        options = remove(loc, options)
        options = remove(loc + 1, options)
        options = remove(loc - 1, options)
    barheights = sample(interval(0, h, 1), nbars)
    for j, bh in zip(barlocs, barheights):
        gi = fill(gi, fgc, connect((0, j), (bh, j)))
        if bh == max(barheights):
            go = fill(go, 1, connect((0, j), (bh, j)))
        if bh == min(barheights):
            go = fill(go, 2, connect((0, j), (bh, j)))
    rotf = choice((identity, rot90, rot180, rot270))
    gi = rotf(gi)
    go = rotf(go)
    return {'input': gi, 'output': go}

