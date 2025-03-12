def generate_eb5a1d5d(diff_lb: float, diff_ub: float) -> dict:
    cols = interval(0, 10, 1)
    d = unifint(diff_lb, diff_ub, (2, 10))
    go = canvas(-1, (d*2-1, d*2-1))
    colss = sample(cols, d)
    for j, cc in enumerate(colss):
        go = fill(go, cc, box(frozenset({(j, j), (2*d - 2 - j, 2*d - 2 - j)})))
    nvenl = unifint(diff_lb, diff_ub, (0, 30 - d))
    nhenl = unifint(diff_lb, diff_ub, (0, 30 - d))
    enl = [nvenl, nhenl]
    gi = tuple(e for e in go)
    while (enl[0] > 0 or enl[1] > 0) and max(shape(gi)) < 30:
        opts = []
        if enl[0] > 0:
            opts.append((identity, 0))
        if enl[1] > 0:
            opts.append((dmirror, 1))
        mirrf, ch = choice(opts)
        gi = mirrf(gi)
        idx = randint(0, len(gi) - 1)
        gi = gi[:idx+1] + gi[idx:]
        gi = mirrf(gi)
        enl[ch] -= 1
    return {'input': gi, 'output': go}

