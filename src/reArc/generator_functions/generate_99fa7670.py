def generate_99fa7670(diff_lb: float, diff_ub: float) -> dict:
    cols = interval(0, 10, 1)
    h = unifint(diff_lb, diff_ub, (3, 30))
    w = unifint(diff_lb, diff_ub, (3, 30))
    num = unifint(diff_lb, diff_ub, (1, h // 2))
    inds = interval(0, h, 1)
    starts = sorted(sample(inds, num))
    ends = [x - 1 for x in starts[1:]] + [h - 1]
    nc = unifint(diff_lb, diff_ub, (1, 9))
    bgc = choice(cols)
    remcols = remove(bgc, cols)
    ccols = sample(remcols, nc)
    gi = canvas(bgc, (h, w))
    go = canvas(bgc, (h, w))
    for s, e in zip(starts, ends):
        col = choice(ccols)
        locj = randint(0, w - 2)
        l1 = connect((s, locj), (s, w - 1))
        l2 = connect((s, w - 1), (e, w - 1))
        gi = fill(gi, col, {(s, locj)})
        go = fill(go, col, l1 | l2)
    return {'input': gi, 'output': go}

