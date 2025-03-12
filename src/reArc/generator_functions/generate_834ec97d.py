def generate_834ec97d(diff_lb: float, diff_ub: float) -> dict:
    cols = remove(4, interval(0, 10, 1))
    h = unifint(diff_lb, diff_ub, (2, 30))
    w = unifint(diff_lb, diff_ub, (2, 30))
    loci = unifint(diff_lb, diff_ub, (0, h - 2))
    locjd = unifint(diff_lb, diff_ub, (0, w // 2))
    locj = choice((locjd, w - locjd))
    locj = min(max(0, locj), w - 1)
    loc = (loci, locj)
    bgc, fgc = sample(cols, 2)
    c = canvas(bgc, (h, w))
    gi = fill(c, fgc, {loc})
    go = fill(c, fgc, {add(loc, (1, 0))})
    for jj in range(w//2 + 1):
        go = fill(go, 4, connect((0, locj + 2 * jj), (loci, locj + 2 * jj)))
        go = fill(go, 4, connect((0, locj - 2 * jj), (loci, locj - 2 * jj)))
    return {'input': gi, 'output': go}

