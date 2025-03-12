def generate_91413438(diff_lb: float, diff_ub: float) -> dict:
    cols = interval(1, 10, 1)
    h = unifint(diff_lb, diff_ub, (2, 5))
    w = unifint(diff_lb, diff_ub, (2, 5))
    maxnb = min(h * w - 1, min(30//h, 30//w))
    minnb = int(0.5 * ((4 * h * w + 1) ** 0.5 - 1)) + 1
    nbi = unifint(diff_lb, diff_ub, (0, maxnb - minnb))
    nb = min(max(minnb, maxnb - nbi), maxnb)
    fgc = choice(cols)
    c = canvas(0, (h, w))
    obj = sample(totuple(asindices(c)), h * w - nb)
    gi = fill(c, fgc, obj)
    go = canvas(0, (h * nb, w * nb))
    for j in range(h * w - nb):
        loc = (j // nb, j % nb)
        go = fill(go, fgc, shift(obj, multiply((h, w), loc)))
    return {'input': gi, 'output': go}

