def generate_e9614598(diff_lb: float, diff_ub: float) -> dict:
    cols = remove(3, interval(0, 10, 1))    
    h = unifint(diff_lb, diff_ub, (5, 30))
    w = unifint(diff_lb, diff_ub, (5, 30))
    r = randint(0, h - 1)
    sizh = unifint(diff_lb, diff_ub, (2, w//2))
    siz = 2 * sizh + 1
    siz = min(max(5, siz), w)
    locj = randint(0, w - siz)
    bgc, dotc = sample(cols, 2)
    c = canvas(bgc, (h, w))
    A = (r, locj)
    B = (r, locj+siz-1)
    gi = fill(c, dotc, {A, B})
    locc = (r, locj + siz // 2)
    go = fill(gi, 3, {locc})
    go = fill(go, 3, dneighbors(locc))
    if choice((True, False)):
        gi = dmirror(gi)
        go = dmirror(go)
    return {'input': gi, 'output': go}

