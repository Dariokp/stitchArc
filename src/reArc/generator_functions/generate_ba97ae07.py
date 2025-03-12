def generate_ba97ae07(diff_lb: float, diff_ub: float) -> dict:
    cols = interval(0, 10, 1)
    h = unifint(diff_lb, diff_ub, (3, 30))
    w = unifint(diff_lb, diff_ub, (3, 30))
    bgc = choice(cols)
    remcols = remove(bgc, cols)
    gi = canvas(bgc, (h, w))
    go = canvas(bgc, (h, w))
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
    for b in range(linew):
        go = fill(go, bcol, connect((0, locj+b), (h-1, locj+b)))
    for a in range(lineh):
        go = fill(go, acol, connect((loci+a, 0), (loci+a, w-1)))
    if choice((True, False)):
        gi = dmirror(gi)
        go = dmirror(go)
    return {'input': gi, 'output': go}

