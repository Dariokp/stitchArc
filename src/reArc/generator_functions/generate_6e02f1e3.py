def generate_6e02f1e3(diff_lb: float, diff_ub: float) -> dict:
    cols = interval(0, 10, 1)
    d = unifint(diff_lb, diff_ub, (3, 30))
    c = canvas(0, (d, d))
    inds = list(asindices(c))
    shuffle(inds)
    num = d ** 2
    numcols = choice((1, 2, 3))
    chcols = sample(cols, numcols)
    if len(chcols) == 1:
        gi = canvas(chcols[0], (d, d))
        go = canvas(0, (d, d))
        go = fill(go, 5, connect((0, 0), (0, d - 1)))
    elif len(chcols) == 2:
        c1, c2 = chcols
        mp = (d ** 2) // 2
        nc1 = unifint(diff_lb, diff_ub, (1, mp))
        a = inds[:nc1]
        b = inds[nc1:]
        gi = fill(c, c1, a)
        gi = fill(gi, c2, b)
        go = fill(canvas(0, (d, d)), 5, connect((0, 0), (d - 1, d - 1)))
    elif len(chcols) == 3:
        c1, c2, c3 = chcols
        kk = d ** 2
        a = int(1/3 * kk)
        b = int(2/3 * kk)
        adev = unifint(diff_lb, diff_ub, (0, a - 1))
        bdev = unifint(diff_lb, diff_ub, (0, kk - b - 1))
        a -= adev
        b -= bdev
        x1, x2, x3 = inds[:a], inds[a:b], inds[b:]
        gi = fill(c, c1, x1)
        gi = fill(gi, c2, x2)
        gi = fill(gi, c3, x3)
        go = fill(canvas(0, (d, d)), 5, connect((d - 1, 0), (0, d - 1)))
    return {'input': gi, 'output': go}

