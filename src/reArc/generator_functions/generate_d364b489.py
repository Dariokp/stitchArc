def generate_d364b489(diff_lb: float, diff_ub: float) -> dict:
    cols = difference(interval(0, 10, 1), (2, 6, 7, 8))    
    h = unifint(diff_lb, diff_ub, (4, 30))
    w = unifint(diff_lb, diff_ub, (4, 30))
    bgc, fgc = sample(cols, 2)
    gi = canvas(bgc, (h, w))
    inds = totuple(asindices(gi))
    num = unifint(diff_lb, diff_ub, (1, (h * w) // 5))
    res = set()
    for j in range(num):
        if len(inds) == 0:
            break
        r = choice(inds)
        inds = remove(r, inds)
        inds = difference(inds, neighbors(r))
        inds = difference(inds, totuple(shift(apply(rbind(multiply, TWO), dneighbors(ORIGIN)), r)))
        res.add(r)
    gi = fill(gi, fgc, res)
    go = fill(gi, 7, shift(res, LEFT))
    go = fill(go, 6, shift(res, RIGHT))
    go = fill(go, 8, shift(res, DOWN))
    go = fill(go, 2, shift(res, UP))
    return {'input': gi, 'output': go}

