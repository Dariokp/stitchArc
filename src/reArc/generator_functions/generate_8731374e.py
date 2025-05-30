def generate_8731374e(diff_lb: float, diff_ub: float) -> dict:
    cols = interval(0, 10, 1)    
    h = unifint(diff_lb, diff_ub, (10, 30))
    w = unifint(diff_lb, diff_ub, (10, 30))
    inh = randint(5, h - 2)
    inw = randint(5, w - 2)
    bgc, fgc = sample(cols, 2)
    num = unifint(diff_lb, diff_ub, (1, min(inh, inw)))
    mat = canvas(bgc, (inh - 2, inw - 2))
    tol = lambda g: list(list(e) for e in g)
    tot = lambda g: tuple(tuple(e) for e in g)
    mat = fill(mat, fgc, connect((0, 0), (num - 1, num - 1)))
    mat = tol(mat)
    shuffle(mat)
    mat = tol(dmirror(tot(mat)))
    shuffle(mat)
    mat = dmirror(tot(mat))
    sgi = paint(canvas(bgc, (inh, inw)), shift(asobject(mat), (1, 1)))
    inds = ofcolor(sgi, fgc)
    lins = mapply(fork(combine, vfrontier, hfrontier), inds)
    go = fill(sgi, fgc, lins)
    numci = unifint(diff_lb, diff_ub, (3, 10))
    numc = 13 - numci
    ccols = sample(cols, numc)
    c = canvas(-1, (h, w))
    inds = asindices(c)
    obj = {(choice(ccols), ij) for ij in inds}
    gi = paint(c, obj)
    loci = randint(1, h - inh - 1)
    locj = randint(1, w - inw - 1)
    loc = (loci, locj)
    plcd = shift(asobject(sgi), loc)
    gi = paint(gi, plcd)
    a, b = ulcorner(plcd)
    c, d = lrcorner(plcd)
    p1 = choice(totuple(connect((a - 1, b), (a - 1, d))))
    p2 = choice(totuple(connect((a, b - 1), (c, b - 1))))
    p3 = choice(totuple(connect((c + 1, b), (c + 1, d))))
    p4 = choice(totuple(connect((a, d + 1), (c, d + 1))))
    remcols = remove(bgc, ccols)
    fixobj = {
        (choice(remcols), p1), (choice(remcols), p2),
        (choice(remcols), p3), (choice(remcols), p4)
    }
    gi = paint(gi, fixobj)
    return {'input': gi, 'output': go}

