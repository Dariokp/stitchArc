def generate_54d82841(diff_lb: float, diff_ub: float) -> dict:
    cols = remove(4, interval(0, 10, 1))
    h = unifint(diff_lb, diff_ub, (5, 30))
    w = unifint(diff_lb, diff_ub, (5, 30))
    bgc = choice(cols)
    remcols = remove(bgc, cols)
    nshps = unifint(diff_lb, diff_ub, (1, w // 3))
    gi = canvas(bgc, (h, w))
    go = canvas(bgc, (h, w))
    locs = interval(1, w - 1, 1)
    for k in range(nshps):
        if len(locs) == 0:
            break
        loc = choice(locs)
        locs = remove(loc, locs)
        locs = remove(loc + 1, locs)
        locs = remove(loc - 1, locs)
        locs = remove(loc + 2, locs)
        locs = remove(loc - 2, locs)
        loci = randint(1, h - 1)
        col = choice(remcols)
        ij = (loci, loc)
        shp = neighbors(ij) - connect((loci + 1, loc - 1), (loci + 1, loc + 1))
        gi = fill(gi, col, shp)
        go = fill(go, col, shp)
        go = fill(go, 4, {(h - 1, loc)})
    rotf = choice((identity, rot90, rot180, rot270))
    gi = rotf(gi)
    go = rotf(go)
    return {'input': gi, 'output': go}

