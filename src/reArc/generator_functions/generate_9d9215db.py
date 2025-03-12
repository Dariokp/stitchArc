def generate_9d9215db(diff_lb: float, diff_ub: float) -> dict:
    cols = interval(0, 10, 1)    
    h = unifint(diff_lb, diff_ub, (5, 14))
    w = unifint(diff_lb, diff_ub, (5, 14))
    h = h * 2 + 1
    w = w * 2 + 1
    bgc = choice(cols)
    remcols = remove(bgc, cols)
    ub = min(h, w)//4
    nrings = unifint(diff_lb, diff_ub, (1, ub))
    onlinesbase = tuple([(2*k+1, 2*k+1) for k in range(ub)])
    onlines = sample(onlinesbase, nrings)
    onlines = {(choice(remcols), ij) for ij in onlines}
    gi = canvas(bgc, (h, w))
    gi = paint(gi, onlines)
    linsbase = apply(rbind(add, (0, 2)), onlinesbase[:-1])
    nlines = unifint(diff_lb, diff_ub, (1, len(linsbase)))
    linesps = sample(linsbase, nlines)
    colors = [choice(remcols) for k in range(nlines)]
    dots = {(col, ij) for col, ij in zip(colors, linesps)}
    dots2 = {(col, ij[::-1]) for col, ij in zip(colors, linesps)}
    gi = paint(gi, dots | dots2)
    ff = lambda ij: ij[1] % 2 == 1
    ff2 = lambda ij: ij[0] % 2 == 1
    linesps2 = tuple(x[::-1] for x in linesps)
    lines = tuple(sfilter(connect(ij, (ij[0], w - ij[1] - 1)), ff) for ij in linesps)
    lines2 = tuple(sfilter(connect(ij, (h - ij[0] - 1, ij[1])), ff2) for ij in linesps2)
    lines = merge({recolor(col, l1 | l2) for col, (l1, l2) in zip(colors, zip(lines, lines2))})
    gobase = paint(gi, lines)
    go = paint(gobase, merge(fgpartition(vmirror(gobase))))
    go = paint(go, merge(fgpartition(hmirror(gobase))))
    go = paint(go, merge(fgpartition(vmirror(hmirror(gobase)))))
    rotf = choice((identity, rot90, rot180, rot270))
    gi = rotf(gi)
    go = rotf(go)
    return {'input': gi, 'output': go}

