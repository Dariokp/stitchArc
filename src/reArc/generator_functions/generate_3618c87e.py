def generate_3618c87e(diff_lb: float, diff_ub: float) -> dict:
    cols = interval(0, 10, 1)
    h = unifint(diff_lb, diff_ub, (4, 30))
    w = unifint(diff_lb, diff_ub, (4, 30))
    bgc, linc, dotc = sample(cols, 3)
    c = canvas(bgc, (h, w))
    ln = connect((0, 0), (0, w - 1))
    nlocs = unifint(diff_lb, diff_ub, (1, w//2))
    locs = []
    opts = interval(0, w, 1)
    for k in range(nlocs):
        if len(opts) == 0:
            break
        ch = choice(opts)
        locs.append(ch)
        opts = remove(ch, opts)
        opts = remove(ch-1, opts)
        opts = remove(ch+1, opts)
    nlocs = len(opts)
    gi = fill(c, linc, ln)
    go = fill(c, linc, ln)
    for j in locs:
        hh = randint(1, h - 3)
        lnx = connect((0, j), (hh, j))
        gi = fill(gi, linc, lnx)
        go = fill(go, linc, lnx)
        gi = fill(gi, dotc, {(hh+1, j)})
        go = fill(go, dotc, {(0, j)})
    rotf = choice((identity, rot90, rot180, rot270))
    gi = rotf(gi)
    go = rotf(go)
    return {'input': gi, 'output': go}

