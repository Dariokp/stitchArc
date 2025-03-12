def generate_ec883f72(diff_lb: float, diff_ub: float) -> dict:
    cols = interval(0, 10, 1)
    h = unifint(diff_lb, diff_ub, (6, 30))
    w = unifint(diff_lb, diff_ub, (6, 30))
    ohi = unifint(diff_lb, diff_ub, (0, h - 6))
    owi = unifint(diff_lb, diff_ub, (0, w - 6))
    oh = h - 5 - ohi
    ow = w - 5 - owi
    loci = randint(0, h - oh)
    locj = randint(0, w - ow)
    bgc, sqc, linc = sample(cols, 3)
    gi = canvas(bgc, (h, w))
    obj = backdrop(frozenset({(loci, locj), (loci + oh - 1, locj + ow - 1)}))
    gi = fill(gi, sqc, obj)
    obob = outbox(outbox(obj))
    gi = fill(gi, linc, obob)
    ln1 = shoot(lrcorner(obob), (1, 1))
    ln2 = shoot(ulcorner(obob), (-1, -1))
    ln3 = shoot(llcorner(obob), (1, -1))
    ln4 = shoot(urcorner(obob), (-1, 1))
    lns = (ln1 | ln2 | ln3 | ln4) & ofcolor(gi, bgc)
    go = fill(gi, sqc, lns)
    return {'input': gi, 'output': go}

