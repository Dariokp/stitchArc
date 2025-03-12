def generate_5c2c9af4(diff_lb: float, diff_ub: float) -> dict:
    cols = interval(0, 10, 1)
    h = unifint(diff_lb, diff_ub, (5, 30))
    w = unifint(diff_lb, diff_ub, (5, 30))
    boxhd = unifint(diff_lb, diff_ub, (0, h // 2))
    boxwd = unifint(diff_lb, diff_ub, (0, w // 2))
    boxh = choice((boxhd, h - boxhd))
    boxw = choice((boxwd, w - boxwd))
    if boxh % 2 == 0:
        boxh = choice((boxh - 1, boxh + 1))
    if boxw % 2 == 0:
        boxw = choice((boxw - 1, boxw + 1))
    boxh = min(max(1, boxh), h if h % 2 == 1 else h - 1)
    boxw = min(max(1, boxw), w if w % 2 == 1 else w - 1)
    boxshap = (boxh, boxw)
    loci = randint(0, h - boxh)
    locj = randint(0, w - boxw)
    loc = (loci, locj)
    bgc = choice(cols)
    remcols = remove(bgc, cols)
    fgc = choice(remcols)
    c = canvas(bgc, (h, w))
    cpi = loci + boxh // 2
    cpj = locj + boxw // 2
    cp = (cpi, cpj)
    A = (loci, locj)
    B = (loci + boxh - 1, locj + boxw - 1)
    gi = fill(c, fgc, {A, B, cp})
    go = fill(c, fgc, {A, B, cp})
    cond = True
    ooo = {A, B, cp}
    if hline(ooo) and len(ooo) == 3:
        go = fill(go, fgc, hfrontier(cp))
        cond = False
    if vline(ooo) and len(ooo) == 3:
        go = fill(go, fgc, vfrontier(cp))
        cond = False
    k = 1
    while cond:
        f1 = k * (boxh // 2)
        f2 = k * (boxw // 2)
        ulci = cpi - f1
        ulcj = cpj - f2
        lrci = cpi + f1
        lrcj = cpj + f2
        ulc = (ulci, ulcj)
        lrc = (lrci, lrcj)
        bx = box(frozenset({ulc, lrc}))
        go2 = fill(go, fgc, bx)
        cond = go != go2
        go = go2
        k += 1
    if choice((True, False)):
        gi = dmirror(gi)
        go = dmirror(go)
    return {'input': gi, 'output': go}

