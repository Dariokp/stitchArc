def generate_ce9e57f2(diff_lb: float, diff_ub: float) -> dict:
    cols = remove(8, interval(0, 10, 1))    
    h = unifint(diff_lb, diff_ub, (6, 30))
    w = unifint(diff_lb, diff_ub, (6, 30))
    nbars = unifint(diff_lb, diff_ub, (2, (w - 2) // 2))
    locopts = interval(1, w - 1, 1)
    barlocs = []
    for k in range(nbars):
        if len(locopts) == 0:
            break
        loc = choice(locopts)
        barlocs.append(loc)
        locopts = remove(loc, locopts)
        locopts = remove(loc + 1, locopts)
        locopts = remove(loc - 1, locopts)
    bgc = choice(cols)
    remcols = remove(bgc, cols)
    numc = unifint(diff_lb, diff_ub, (1, 8))
    colss = sample(remcols, numc)
    gi = canvas(bgc, (h, w))
    go = canvas(bgc, (h, w))
    for j in barlocs:
        barloci = unifint(diff_lb, diff_ub, (1, h - 2))
        fullbar = connect((0, j), (barloci, j))
        halfbar = connect((0, j), (barloci // 2 if barloci % 2 == 1 else (barloci - 1) // 2, j))
        barcol = choice(colss)
        gi = fill(gi, barcol, fullbar)
        go = fill(go, barcol, fullbar)
        go = fill(go, 8, halfbar)
    rotf = choice((identity, rot90, rot180, rot270))
    gi = rotf(gi)
    go = rotf(go)
    return {'input': gi, 'output': go}

