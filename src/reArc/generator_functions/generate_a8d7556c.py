def generate_a8d7556c(diff_lb: float, diff_ub: float) -> dict:
    cols = difference(interval(0, 10, 1), (0, 2))
    h = unifint(diff_lb, diff_ub, (6, 30))
    w = unifint(diff_lb, diff_ub, (6, 30))
    fgc = choice(cols)
    c = canvas(fgc, (h, w))
    numblacks = unifint(diff_lb, diff_ub, (1, (h * w) // 3 * 2))
    inds = totuple(asindices(c))
    blacks = sample(inds, numblacks)
    gi = fill(c, 0, blacks)
    numsq = unifint(diff_lb, diff_ub, (1, (h * w) // 10))
    sqlocs = sample(inds, numsq)
    gi = fill(gi, 0, shift(sqlocs, (0, 0)))
    gi = fill(gi, 0, shift(sqlocs, (0, 1)))
    gi = fill(gi, 0, shift(sqlocs, (1, 0)))
    gi = fill(gi, 0, shift(sqlocs, (1, 1)))
    go = tuple(e for e in gi)
    for a in range(h - 1):
        for b in range(w - 1):
            if gi[a][b] == 0 and gi[a+1][b] == 0 and gi[a][b+1] == 0 and gi[a+1][b+1] == 0:
                go = fill(go, 2, {(a, b), (a+1, b), (a, b+1), (a+1, b+1)})
    return {'input': gi, 'output': go}

