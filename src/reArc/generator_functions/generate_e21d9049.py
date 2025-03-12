def generate_e21d9049(diff_lb: float, diff_ub: float) -> dict:
    cols = interval(0, 10, 1)    
    h = unifint(diff_lb, diff_ub, (10, 30))
    w = unifint(diff_lb, diff_ub, (10, 30))
    ph = unifint(diff_lb, diff_ub, (2, 9))
    pw = unifint(diff_lb, diff_ub, (2, 9))
    bgc = choice(cols)
    remcols = remove(bgc, cols)
    hbar = frozenset({(choice(remcols), (k, 0)) for k in range(ph)})
    wbar = frozenset({(choice(remcols), (0, k)) for k in range(pw)})
    locih = randint(0, h - ph)
    locjh = randint(0, w - 1)
    loch = (locih, locjh)
    locjw = randint(0, w - pw)
    lociw = randint(0, h - 1)
    locw = (lociw, locjw)
    canv = canvas(bgc, (h, w))
    hbar = shift(hbar, loch)
    wbar = shift(wbar, locw)
    cp = (lociw, locjh)
    col = choice(remcols)
    hbard = extract(hbar, lambda cij: abs(cij[1][0] - lociw) % ph == 0)[1]
    hbar = sfilter(hbar, lambda cij: abs(cij[1][0] - lociw) % ph != 0) | {(col, hbard)}
    wbard = extract(wbar, lambda cij: abs(cij[1][1] - locjh) % pw == 0)[1]
    wbar = sfilter(wbar, lambda cij: abs(cij[1][1] - locjh) % pw != 0) | {(col, wbard)}
    gi = paint(canv, hbar | wbar)
    go = paint(canv, hbar | wbar)
    for k in range(h//ph + 1):
        go = paint(go, shift(hbar, (k*ph, 0)))
        go = paint(go, shift(hbar, (-k*ph, 0)))
    for k in range(w//pw + 1):
        go = paint(go, shift(wbar, (0, k*pw)))
        go = paint(go, shift(wbar, (0, -k*pw)))
    return {'input': gi, 'output': go}

