def generate_22168020(diff_lb: float, diff_ub: float) -> dict:
    cols = interval(0, 10, 1)
    h = unifint(diff_lb, diff_ub, (6, 30))
    w = unifint(diff_lb, diff_ub, (6, 30))
    num = unifint(diff_lb, diff_ub, (1, min(9, (h * w) // 10)))
    bgc = choice(cols)
    remcols = remove(bgc, cols)
    gi = canvas(bgc, (h, w))
    go = canvas(bgc, (h, w))
    succ = 0
    tr = 0
    maxtr = 6 * num
    inds = asindices(gi)
    while tr < maxtr and succ < num:
        d = unifint(diff_lb, diff_ub, (2, 5))
        oh = d + 1
        ow = 2 * d
        if len(inds) == 0:
            tr += 1
            continue
        loc = choice(totuple(inds))
        loci, locj = loc
        io1 = connect(loc, (loci + d - 1, locj + d - 1))
        io2 = connect((loci, locj + ow - 1), (loci + d - 1, locj + d))
        io = io1 | io2 | {(loci + d, locj + d - 1), (loci + d, locj + d)}
        oo = merge(sfilter(prapply(connect, io, io), hline))
        mf = choice((identity, dmirror, cmirror, hmirror, vmirror))
        io = mf(io)
        oo = mf(oo)
        col = choice(remcols)
        if oo.issubset(inds):
            gi = fill(gi, col, io)
            go = fill(go, col, oo)
            succ += 1
            inds = inds - oo
            remcols = remove(col, remcols)
        tr += 1
    return {'input': gi, 'output': go}

