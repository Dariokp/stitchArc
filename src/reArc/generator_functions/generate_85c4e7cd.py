def generate_85c4e7cd(diff_lb: float, diff_ub: float) -> dict:
    colopts = interval(0, 10, 1)
    h = unifint(diff_lb, diff_ub, (1, 15))
    w = unifint(diff_lb, diff_ub, (1, 15))
    ncols = unifint(diff_lb, diff_ub, (1, 10))
    cols = sample(colopts, ncols)
    colord = [choice(cols) for j in range(min(h, w))]
    shp = (h*2, w*2)
    gi = canvas(0, shp)
    go = canvas(0, shp)
    for idx, (ci, co) in enumerate(zip(colord, colord[::-1])):
        ulc = (idx, idx)
        lrc = (h*2 - 1 - idx, w*2 - 1 - idx)
        bx = box(frozenset({ulc, lrc}))
        gi = fill(gi, ci, bx)
        go = fill(go, co, bx)
    return {'input': gi, 'output': go}

