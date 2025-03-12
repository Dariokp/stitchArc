def generate_8403a5d5(diff_lb: float, diff_ub: float) -> dict:
    cols = remove(5, interval(0, 10, 1))
    h = unifint(diff_lb, diff_ub, (3, 30))
    w = unifint(diff_lb, diff_ub, (3, 30))
    loccinv = unifint(diff_lb, diff_ub, (1, w - 1))
    locc = w - loccinv
    bgc, fgc = sample(cols, 2)
    c = canvas(bgc, (h, w))
    idx = (h - 1, locc)
    gi = fill(c, fgc, {idx})
    go = canvas(bgc, (h, w))
    for j in range(locc, w, 2):
        go = fill(go, fgc, connect((0, j), (h - 1, j)))
    for j in range(locc+1, w, 4):
        go = fill(go, 5, {(0, j)})
    for j in range(locc+3, w, 4):
        go = fill(go, 5, {(h-1, j)})
    return {'input': gi, 'output': go}

