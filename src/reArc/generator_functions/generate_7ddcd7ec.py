def generate_7ddcd7ec(diff_lb: float, diff_ub: float) -> dict:
    cols = interval(0, 10, 1)
    crns = (((0, 0), (-1, -1)), ((0, 1), (-1, 1)), ((1, 0), (1, -1)), ((1, 1), (1, 1)))
    h = unifint(diff_lb, diff_ub, (5, 30))
    w = unifint(diff_lb, diff_ub, (5, 30))
    bgc = choice(cols)
    gi = canvas(bgc, (h, w))
    go = canvas(bgc, (h, w))
    num = unifint(diff_lb, diff_ub, (0, 4))
    chos = sample(crns, num)
    loci = randint(0, h - 2)
    locj = randint(0, w - 2)
    loc = (loci, locj)
    remcols = remove(bgc, cols)
    for sp, dr in crns:
        sp2 = add(loc, sp)
        col = choice(remcols)
        gi = fill(gi, col, {sp2})
        go = fill(go, col, {sp2})
        if (sp, dr) in chos:
            gi = fill(gi, col, {add(sp2, dr)})
            go = fill(go, col, shoot(sp2, dr))
    return {'input': gi, 'output': go}

