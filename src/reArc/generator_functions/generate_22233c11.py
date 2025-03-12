def generate_22233c11(diff_lb: float, diff_ub: float) -> dict:
    cols = remove(8, interval(0, 10, 1))
    h = unifint(diff_lb, diff_ub, (5, 30))
    w = unifint(diff_lb, diff_ub, (5, 30))
    nobjs = unifint(diff_lb, diff_ub, (1, (h * w) // 10))
    succ = 0
    tr = 0
    maxtr = 10 * nobjs
    bgc = choice(cols)
    remcols = remove(bgc, cols)
    gi = canvas(bgc, (h, w))
    go = canvas(bgc, (h, w))
    inds = asindices(gi)
    fullinds = asindices(gi)
    ncols = unifint(diff_lb, diff_ub, (1, 8))
    ccols = sample(remcols, ncols)
    while succ < nobjs and tr < maxtr:
        if len(inds) == 0:
            break
        tr += 1
        od = randint(1, 3)
        fulld = 4 * od
        g = canvas(bgc, (4, 4))
        g = fill(g, 8, {(0, 3), (3, 0)})
        col = choice(ccols)
        g = fill(g, col, {(1, 1), (2, 2)})
        if choice((True, False)):
            g = hmirror(g)
        g = upscale(g, od)
        inobj = recolor(col, ofcolor(g, col))
        outobj = inobj | recolor(8, ofcolor(g, 8))
        loc = choice(totuple(inds))
        outobj = shift(outobj, loc)
        inobj = shift(inobj, loc)
        outobji = toindices(outobj)
        if toindices(inobj).issubset(inds) and (outobji & fullinds).issubset(inds):
            succ += 1
            inds = (inds - outobji) - mapply(neighbors, outobji)
            gi = paint(gi, inobj)
            go = paint(go, outobj)
    return {'input': gi, 'output': go}

