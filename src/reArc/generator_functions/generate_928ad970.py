def generate_928ad970(diff_lb: float, diff_ub: float) -> dict:
    cols = interval(0, 10, 1)
    h = unifint(diff_lb, diff_ub, (10, 30))
    w = unifint(diff_lb, diff_ub, (10, 30))
    ih = unifint(diff_lb, diff_ub, (9, h))
    iw = unifint(diff_lb, diff_ub, (9, w))
    bgc, linc, dotc = sample(cols, 3)
    loci = randint(0, h - ih)
    locj = randint(0, w - iw)
    ulc = (loci, locj)
    lrc = (loci + ih - 1, locj + iw - 1)
    dot1 = choice(totuple(connect(ulc, (loci + ih - 1, locj)) - {ulc, (loci + ih - 1, locj)}))
    dot2 = choice(totuple(connect(ulc, (loci, locj + iw - 1)) - {ulc, (loci, locj + iw - 1)}))
    dot3 = choice(totuple(connect(lrc, (loci + ih - 1, locj)) - {lrc, (loci + ih - 1, locj)}))
    dot4 = choice(totuple(connect(lrc, (loci, locj + iw - 1)) - {lrc, (loci, locj + iw - 1)}))
    a, b = sorted(sample(interval(loci + 2, loci + ih - 2, 1), 2))
    while a + 1 == b:
        a, b = sorted(sample(interval(loci + 2, loci + ih - 2, 1), 2))
    c, d = sorted(sample(interval(locj + 2, locj + iw - 2, 1), 2))
    while c + 1 == d:
        c, d = sorted(sample(interval(locj + 2, locj + iw - 2, 1), 2))
    sp = box(frozenset({(a, c), (b, d)}))
    bx = {dot1, dot2, dot3, dot4}
    gi = canvas(bgc, (h, w))
    go = canvas(bgc, (h, w))
    gi = fill(gi, dotc, bx)
    gi = fill(gi, linc, sp)
    go = fill(gi, linc, inbox(bx))
    return {'input': gi, 'output': go}

