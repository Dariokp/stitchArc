def generate_67a423a3(diff_lb: float, diff_ub: float) -> dict:
    cols = remove(4, interval(0, 10, 1))
    h = unifint(diff_lb, diff_ub, (3, 30))
    w = unifint(diff_lb, diff_ub, (3, 30))
    bgc = choice(cols)
    remcols = remove(bgc, cols)
    gi = canvas(bgc, (h, w))
    lineh = unifint(diff_lb, diff_ub, (1, h // 3))
    linew = unifint(diff_lb, diff_ub, (1, w // 3))
    loci = randint(1, h - lineh - 1)
    locj = randint(1, w - linew - 1)
    acol = choice(remcols)
    bcol = choice(remove(acol, remcols))
    for a in range(lineh):
        gi = fill(gi, acol, connect((loci+a, 0), (loci+a, w-1)))
    for b in range(linew):
        gi = fill(gi, bcol, connect((0, locj+b), (h-1, locj+b)))
    bx = outbox(frozenset({(loci, locj), (loci + lineh - 1, locj + linew - 1)}))
    go = fill(gi, 4, bx)
    if choice((True, False)):
        gi = dmirror(gi)
        go = dmirror(go)
    return {'input': gi, 'output': go}

