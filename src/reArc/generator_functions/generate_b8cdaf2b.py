def generate_b8cdaf2b(diff_lb: float, diff_ub: float) -> dict:
    cols = interval(0, 10, 1)
    h = unifint(diff_lb, diff_ub, (3, 30))
    w = unifint(diff_lb, diff_ub, (3, 30))
    bgc, linc, dotc = sample(cols, 3)
    lin = connect((0, 0), (0, w - 1))
    winv = unifint(diff_lb, diff_ub, (2, w - 1))
    w2 = w - winv
    w2 = min(max(w2, 1), w - 2)
    locj = randint(1, w - w2 - 1)
    bar2 = connect((0, locj), (0, locj + w2 - 1))
    c = canvas(bgc, (h, w))
    gi = fill(c, linc, lin)
    gi = fill(gi, dotc, bar2)
    gi = fill(gi, linc, shift(bar2, (1, 0)))
    go = fill(gi, dotc, shoot((2, locj - 1), (1, -1)))
    go = fill(go, dotc, shoot((2, locj + w2), (1, 1)))
    rotf = choice((identity, rot90, rot180, rot270))
    gi = rotf(gi)
    go = rotf(go)
    return {'input': gi, 'output': go}

