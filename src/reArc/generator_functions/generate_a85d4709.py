def generate_a85d4709(diff_lb: float, diff_ub: float) -> dict:
    cols = difference(interval(0, 10, 1), (2, 3, 4))
    h = unifint(diff_lb, diff_ub, (2, 30))
    w3 = unifint(diff_lb, diff_ub, (1, 10))
    w = w3 * 3
    bgc, dotc = sample(cols, 2)
    gi = canvas(bgc, (h, w))
    go = canvas(bgc, (h, w))
    for ii in range(h):
        loc = randint(0, w3 - 1)
        dev = unifint(diff_lb, diff_ub, (0, w3 // 2 + 1))
        loc = w3 // 3 + choice((+dev, -dev))
        loc = min(max(0, loc), w3 - 1)
        ofs, col = choice(((0, 2), (1, 4), (2, 3)))
        loc += ofs * w3
        gi = fill(gi, dotc, {(ii, loc)})
        ln = connect((ii, 0), (ii, w - 1))
        go = fill(go, col, ln)
    return {'input': gi, 'output': go}

