def generate_bd4472b8(diff_lb: float, diff_ub: float) -> dict:
    cols = interval(1, 10, 1)
    h = unifint(diff_lb, diff_ub, (1, 28))
    w = unifint(diff_lb, diff_ub, (2, 8))
    bgc = choice(cols)
    remcols = remove(bgc, cols)
    linc = choice(remcols)
    ccols = sample(remcols, w)
    cc = (tuple(ccols),)
    br = canvas(linc, (1, w))
    lp = canvas(bgc, (h, w))
    gi = vconcat(vconcat(cc, br), lp)
    go = vconcat(vconcat(cc, br), lp)
    pt = hupscale(dmirror(cc), w)
    pto = asobject(pt)
    idx = 2
    while idx < h+3:
        go = paint(go, shift(pto, (idx, 0)))
        idx += w
    rotf = choice((identity, rot90, rot180, rot270))
    gi = rotf(gi)
    go = rotf(go)
    return {'input': gi, 'output': go}

