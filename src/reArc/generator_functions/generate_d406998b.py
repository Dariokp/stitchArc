def generate_d406998b(diff_lb: float, diff_ub: float) -> dict:
    cols = remove(3, interval(0, 10, 1))
    h = unifint(diff_lb, diff_ub, (3, 30))
    w = unifint(diff_lb, diff_ub, (2, 30))
    bgc, dotc = sample(cols, 2)
    gi = canvas(bgc, (h, w))
    go = canvas(bgc, (h, w))
    itv = interval(0, h, 1)
    for j in range(w):
        nilocs = unifint(diff_lb, diff_ub, (1, h // 2 - 1 if h % 2 == 0 else h // 2))
        ilocs = sample(itv, nilocs)
        locs = {(ii, j) for ii in ilocs}
        gi = fill(gi, dotc, locs)
        go = fill(go, dotc if (j - w) % 2 == 0 else 3, locs)
    return {'input': gi, 'output': go}

